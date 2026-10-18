// LIVEIT Vulkan city preview: true GPU compute raycasting to a portable RGB file.
// Renderer-neutral 3D block contract mirrors city-scene.ts. No GLFW/window needed,
// allowing CI to use Mesa Lavapipe and macOS to use MoltenVK when configured.
// A native React Native surface bridge is a separate, not-yet-completed phase.
#include <vulkan/vulkan.h>

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#ifndef LIVEIT_CITY_SHADER_PATH
#error "CMake must define LIVEIT_CITY_SHADER_PATH"
#endif

namespace {
void require(VkResult result, const char* operation) {
  if (result != VK_SUCCESS)
    throw std::runtime_error(std::string(operation) + " failed: VkResult " +
                             std::to_string(static_cast<int>(result)));
}

struct alignas(16) CityBlock {
  std::array<float, 4> position;    // x, z, height, material
  std::array<float, 4> dimensions;  // width, depth, unused, unused
};
static_assert(sizeof(CityBlock) == 32);

struct Configuration {
  uint32_t width;
  uint32_t height;
  uint32_t blockCount;
  uint32_t night;
  float cameraYaw;
  float cameraAltitude;
  float cameraDistance;
  float exposure;
};
static_assert(sizeof(Configuration) == 32);

uint32_t nextRandom(uint32_t state) {
  state ^= state << 13;
  state ^= state >> 17;
  state ^= state << 5;
  return state;
}

std::vector<CityBlock> generateCity(uint32_t seed) {
  std::vector<CityBlock> blocks;
  uint32_t state = seed ? seed : 1;
  for (int row = 0; row < 9; ++row) {
    for (int col = 0; col < 9; ++col) {
      if (row == 4 || col == 4) continue;
      state = nextRandom(state);
      bool garden = row >= 6 && col >= 6;
      if (garden && (state & 3u) == 0) continue;
      float height = static_cast<float>(
          garden ? 3 + (state % 6u) : 5 + (state % 19u));
      float x = static_cast<float>((col - 4) * 9);
      float z = static_cast<float>((row - 4) * 9);
      blocks.push_back({
          {{x, z, height, static_cast<float>((state >> 16) % 5u)}},
          {{static_cast<float>(5 + ((state >> 8) % 3u)),
            static_cast<float>(5 + ((state >> 12) % 3u)), 0, 0}},
      });
    }
  }
  return blocks;
}

std::vector<uint32_t> readShader(const std::string& path) {
  std::ifstream file(path, std::ios::binary | std::ios::ate);
  if (!file) throw std::runtime_error("Shader not found: " + path);
  const auto size = static_cast<std::streamsize>(file.tellg());
  if (size <= 0 || size % 4 != 0)
    throw std::runtime_error("SPIR-V file size must be divisible by four");
  file.seekg(0);
  std::vector<uint32_t> code(static_cast<size_t>(size / 4));
  if (!file.read(reinterpret_cast<char*>(code.data()), size))
    throw std::runtime_error("Unable to read shader bytecode");
  return code;
}

bool hasExtension(const std::vector<VkExtensionProperties>& list,
                  const char* name) {
  return std::any_of(list.begin(), list.end(), [name](const auto& e) {
    return std::strcmp(e.extensionName, name) == 0;
  });
}

std::vector<VkExtensionProperties> instanceExtensions() {
  uint32_t count = 0;
  require(vkEnumerateInstanceExtensionProperties(nullptr, &count, nullptr),
          "vkEnumerateInstanceExtensionProperties(count)");
  std::vector<VkExtensionProperties> result(count);
  require(vkEnumerateInstanceExtensionProperties(nullptr, &count, result.data()),
          "vkEnumerateInstanceExtensionProperties");
  return result;
}

std::vector<VkExtensionProperties> deviceExtensions(VkPhysicalDevice p) {
  uint32_t count = 0;
  require(vkEnumerateDeviceExtensionProperties(p, nullptr, &count, nullptr),
          "vkEnumerateDeviceExtensionProperties(count)");
  std::vector<VkExtensionProperties> result(count);
  require(vkEnumerateDeviceExtensionProperties(p, nullptr, &count, result.data()),
          "vkEnumerateDeviceExtensionProperties");
  return result;
}

uint32_t findHostMemory(VkPhysicalDevice physical, uint32_t supported) {
  VkPhysicalDeviceMemoryProperties memory{};
  vkGetPhysicalDeviceMemoryProperties(physical, &memory);
  for (uint32_t index = 0; index < memory.memoryTypeCount; ++index) {
    if ((supported & (1u << index)) &&
        (memory.memoryTypes[index].propertyFlags &
         (VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)) ==
            (VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT))
      return index;
  }
  throw std::runtime_error("No host-visible coherent Vulkan memory type available");
}

struct GpuBuffer {
  VkBuffer buffer{VK_NULL_HANDLE};
  VkDeviceMemory memory{VK_NULL_HANDLE};
  VkDeviceSize byteCount{};
};

GpuBuffer makeBuffer(VkDevice device, VkPhysicalDevice physical,
                     VkDeviceSize bytes, const void* initial = nullptr) {
  GpuBuffer out{};
  out.byteCount = bytes;
  VkBufferCreateInfo info{};
  info.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
  info.size = bytes;
  info.usage = VK_BUFFER_USAGE_STORAGE_BUFFER_BIT;
  info.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
  require(vkCreateBuffer(device, &info, nullptr, &out.buffer), "vkCreateBuffer");

  VkMemoryRequirements requirements{};
  vkGetBufferMemoryRequirements(device, out.buffer, &requirements);
  VkMemoryAllocateInfo alloc{};
  alloc.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
  alloc.allocationSize = requirements.size;
  alloc.memoryTypeIndex = findHostMemory(physical, requirements.memoryTypeBits);
  require(vkAllocateMemory(device, &alloc, nullptr, &out.memory), "vkAllocateMemory");
  require(vkBindBufferMemory(device, out.buffer, out.memory, 0), "vkBindBufferMemory");
  if (initial) {
    void* data = nullptr;
    require(vkMapMemory(device, out.memory, 0, bytes, 0, &data), "vkMapMemory(initial)");
    std::memcpy(data, initial, static_cast<size_t>(bytes));
    vkUnmapMemory(device, out.memory);
  }
  return out;
}

void destroyBuffer(VkDevice device, GpuBuffer& buffer) {
  if (buffer.buffer) vkDestroyBuffer(device, buffer.buffer, nullptr);
  if (buffer.memory) vkFreeMemory(device, buffer.memory, nullptr);
  buffer = {};
}

void writePpm(const std::string& path,
              const std::vector<uint32_t>& pixels,
              uint32_t width, uint32_t height) {
  std::ofstream file(path, std::ios::binary);
  if (!file) throw std::runtime_error("Cannot write " + path);
  file << "P6\n" << width << " " << height << "\n255\n";
  for (uint32_t packed : pixels) {
    const char rgb[3] = {
        static_cast<char>(packed & 255u),
        static_cast<char>((packed >> 8) & 255u),
        static_cast<char>((packed >> 16) & 255u),
    };
    file.write(rgb, sizeof(rgb));
  }
  if (!file.good()) throw std::runtime_error("Failed to write complete PPM");
}
}  // namespace

int main(int argc, char** argv) {
  try {
    const std::string outPath = argc > 1 ? argv[1] : "bellweather-vulkan.ppm";
    const uint32_t width = argc > 2 ? static_cast<uint32_t>(std::stoul(argv[2])) : 512u;
    const uint32_t height = argc > 3 ? static_cast<uint32_t>(std::stoul(argv[3])) : 320u;
    const bool night = argc > 4 ? std::string(argv[4]) != "day" : true;
    if (width < 64 || height < 64 || width > 2048 || height > 2048)
      throw std::runtime_error("Width and height must be 64–2048 pixels");

    // Enable MoltenVK portability enumeration only when the loader advertises it.
    // On Apple, a properly linked MoltenVK XCFramework / Vulkan loader is still
    // required. Neither framework nor native app integration is auto-installed.
    std::vector<const char*> instanceExtensionNames;
    VkInstanceCreateFlags instanceFlags = 0;
#ifdef VK_KHR_portability_enumeration
    if (hasExtension(instanceExtensions(), VK_KHR_PORTABILITY_ENUMERATION_EXTENSION_NAME)) {
      instanceExtensionNames.push_back(VK_KHR_PORTABILITY_ENUMERATION_EXTENSION_NAME);
      instanceFlags |= VK_INSTANCE_CREATE_ENUMERATE_PORTABILITY_BIT_KHR;
    }
#endif
    VkApplicationInfo app{};
    app.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    app.pApplicationName = "LIVEIT Vulkan City";
    app.apiVersion = VK_API_VERSION_1_1;
    VkInstanceCreateInfo instanceInfo{};
    instanceInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    instanceInfo.pApplicationInfo = &app;
    instanceInfo.flags = instanceFlags;
    instanceInfo.enabledExtensionCount = static_cast<uint32_t>(instanceExtensionNames.size());
    instanceInfo.ppEnabledExtensionNames = instanceExtensionNames.data();
    VkInstance instance = VK_NULL_HANDLE;
    require(vkCreateInstance(&instanceInfo, nullptr, &instance), "vkCreateInstance");

    uint32_t deviceCount = 0;
    require(vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr),
            "vkEnumeratePhysicalDevices(count)");
    if (!deviceCount) throw std::runtime_error("No Vulkan physical device, including software ICD");
    std::vector<VkPhysicalDevice> candidates(deviceCount);
    require(vkEnumeratePhysicalDevices(instance, &deviceCount, candidates.data()),
            "vkEnumeratePhysicalDevices");
    VkPhysicalDevice physical = VK_NULL_HANDLE;
    uint32_t computeFamily = 0;
    for (VkPhysicalDevice candidate : candidates) {
      uint32_t queueCount = 0;
      vkGetPhysicalDeviceQueueFamilyProperties(candidate, &queueCount, nullptr);
      std::vector<VkQueueFamilyProperties> families(queueCount);
      vkGetPhysicalDeviceQueueFamilyProperties(candidate, &queueCount, families.data());
      for (uint32_t i = 0; i < families.size(); ++i) {
        if (families[i].queueCount && (families[i].queueFlags & VK_QUEUE_COMPUTE_BIT)) {
          physical = candidate;
          computeFamily = i;
          break;
        }
      }
      if (physical) break;
    }
    if (!physical) throw std::runtime_error("No Vulkan compute queue available");
    VkPhysicalDeviceProperties properties{};
    vkGetPhysicalDeviceProperties(physical, &properties);
    std::cout << "Vulkan compute device: " << properties.deviceName << "\n";

    float queuePriority = 1.0f;
    VkDeviceQueueCreateInfo queueInfo{};
    queueInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
    queueInfo.queueFamilyIndex = computeFamily;
    queueInfo.queueCount = 1;
    queueInfo.pQueuePriorities = &queuePriority;
    std::vector<const char*> requiredDeviceExtensions;
#ifdef VK_KHR_portability_subset
    if (hasExtension(deviceExtensions(physical), VK_KHR_PORTABILITY_SUBSET_EXTENSION_NAME))
      requiredDeviceExtensions.push_back(VK_KHR_PORTABILITY_SUBSET_EXTENSION_NAME);
#endif
    VkDeviceCreateInfo deviceInfo{};
    deviceInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
    deviceInfo.queueCreateInfoCount = 1;
    deviceInfo.pQueueCreateInfos = &queueInfo;
    deviceInfo.enabledExtensionCount = static_cast<uint32_t>(requiredDeviceExtensions.size());
    deviceInfo.ppEnabledExtensionNames = requiredDeviceExtensions.data();
    VkDevice device = VK_NULL_HANDLE;
    require(vkCreateDevice(physical, &deviceInfo, nullptr, &device), "vkCreateDevice");
    VkQueue queue = VK_NULL_HANDLE;
    vkGetDeviceQueue(device, computeFamily, 0, &queue);

    const auto blocks = generateCity(0xb311);
    const VkDeviceSize pixelBytes = static_cast<VkDeviceSize>(width) * height * sizeof(uint32_t);
    GpuBuffer pixelBuffer = makeBuffer(device, physical, pixelBytes);
    GpuBuffer blockBuffer = makeBuffer(device, physical, blocks.size() * sizeof(CityBlock),
                                       blocks.data());

    std::array<VkDescriptorSetLayoutBinding, 2> bindings{};
    for (uint32_t i = 0; i < bindings.size(); ++i) {
      bindings[i].binding = i;
      bindings[i].descriptorType = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER;
      bindings[i].descriptorCount = 1;
      bindings[i].stageFlags = VK_SHADER_STAGE_COMPUTE_BIT;
    }
    VkDescriptorSetLayoutCreateInfo layoutInfo{};
    layoutInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
    layoutInfo.bindingCount = static_cast<uint32_t>(bindings.size());
    layoutInfo.pBindings = bindings.data();
    VkDescriptorSetLayout setLayout = VK_NULL_HANDLE;
    require(vkCreateDescriptorSetLayout(device, &layoutInfo, nullptr, &setLayout),
            "vkCreateDescriptorSetLayout");

    VkPushConstantRange pushRange{};
    pushRange.stageFlags = VK_SHADER_STAGE_COMPUTE_BIT;
    pushRange.offset = 0;
    pushRange.size = sizeof(Configuration);
    VkPipelineLayoutCreateInfo pipelineLayoutInfo{};
    pipelineLayoutInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
    pipelineLayoutInfo.setLayoutCount = 1;
    pipelineLayoutInfo.pSetLayouts = &setLayout;
    pipelineLayoutInfo.pushConstantRangeCount = 1;
    pipelineLayoutInfo.pPushConstantRanges = &pushRange;
    VkPipelineLayout pipelineLayout = VK_NULL_HANDLE;
    require(vkCreatePipelineLayout(device, &pipelineLayoutInfo, nullptr, &pipelineLayout),
            "vkCreatePipelineLayout");

    auto shaderBytes = readShader(LIVEIT_CITY_SHADER_PATH);
    VkShaderModuleCreateInfo shaderInfo{};
    shaderInfo.sType = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO;
    shaderInfo.codeSize = shaderBytes.size() * sizeof(uint32_t);
    shaderInfo.pCode = shaderBytes.data();
    VkShaderModule shader = VK_NULL_HANDLE;
    require(vkCreateShaderModule(device, &shaderInfo, nullptr, &shader),
            "vkCreateShaderModule");

    VkComputePipelineCreateInfo pipelineInfo{};
    pipelineInfo.sType = VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO;
    pipelineInfo.stage.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    pipelineInfo.stage.stage = VK_SHADER_STAGE_COMPUTE_BIT;
    pipelineInfo.stage.module = shader;
    pipelineInfo.stage.pName = "main";
    pipelineInfo.layout = pipelineLayout;
    VkPipeline pipeline = VK_NULL_HANDLE;
    require(vkCreateComputePipelines(device, VK_NULL_HANDLE, 1, &pipelineInfo,
                                     nullptr, &pipeline),
            "vkCreateComputePipelines");

    VkDescriptorPoolSize poolSize{};
    poolSize.type = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER;
    poolSize.descriptorCount = 2;
    VkDescriptorPoolCreateInfo poolInfo{};
    poolInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
    poolInfo.maxSets = 1;
    poolInfo.poolSizeCount = 1;
    poolInfo.pPoolSizes = &poolSize;
    VkDescriptorPool descriptorPool = VK_NULL_HANDLE;
    require(vkCreateDescriptorPool(device, &poolInfo, nullptr, &descriptorPool),
            "vkCreateDescriptorPool");
    VkDescriptorSetAllocateInfo setInfo{};
    setInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;
    setInfo.descriptorPool = descriptorPool;
    setInfo.descriptorSetCount = 1;
    setInfo.pSetLayouts = &setLayout;
    VkDescriptorSet set = VK_NULL_HANDLE;
    require(vkAllocateDescriptorSets(device, &setInfo, &set), "vkAllocateDescriptorSets");

    std::array<VkDescriptorBufferInfo, 2> descriptions{};
    descriptions[0].buffer = pixelBuffer.buffer;
    descriptions[0].range = pixelBuffer.byteCount;
    descriptions[1].buffer = blockBuffer.buffer;
    descriptions[1].range = blockBuffer.byteCount;
    std::array<VkWriteDescriptorSet, 2> writes{};
    for (uint32_t i = 0; i < writes.size(); ++i) {
      writes[i].sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
      writes[i].dstSet = set;
      writes[i].dstBinding = i;
      writes[i].descriptorCount = 1;
      writes[i].descriptorType = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER;
      writes[i].pBufferInfo = &descriptions[i];
    }
    vkUpdateDescriptorSets(device, static_cast<uint32_t>(writes.size()), writes.data(), 0, nullptr);

    VkCommandPoolCreateInfo cmdPoolInfo{};
    cmdPoolInfo.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
    cmdPoolInfo.queueFamilyIndex = computeFamily;
    VkCommandPool commandPool = VK_NULL_HANDLE;
    require(vkCreateCommandPool(device, &cmdPoolInfo, nullptr, &commandPool),
            "vkCreateCommandPool");

    VkCommandBufferAllocateInfo commandInfo{};
    commandInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
    commandInfo.commandPool = commandPool;
    commandInfo.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
    commandInfo.commandBufferCount = 1;
    VkCommandBuffer command = VK_NULL_HANDLE;
    require(vkAllocateCommandBuffers(device, &commandInfo, &command),
            "vkAllocateCommandBuffers");
    VkCommandBufferBeginInfo begin{};
    begin.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
    require(vkBeginCommandBuffer(command, &begin), "vkBeginCommandBuffer");
    vkCmdBindPipeline(command, VK_PIPELINE_BIND_POINT_COMPUTE, pipeline);
    vkCmdBindDescriptorSets(command, VK_PIPELINE_BIND_POINT_COMPUTE,
                            pipelineLayout, 0, 1, &set, 0, nullptr);
    Configuration cfg{width, height, static_cast<uint32_t>(blocks.size()),
                      night ? 1u : 0u, 0.73f, 79.0f, 117.0f, 0.9f};
    vkCmdPushConstants(command, pipelineLayout, VK_SHADER_STAGE_COMPUTE_BIT,
                       0, sizeof(cfg), &cfg);
    vkCmdDispatch(command, (width + 7u) / 8u, (height + 7u) / 8u, 1u);
    require(vkEndCommandBuffer(command), "vkEndCommandBuffer");

    VkSubmitInfo submit{};
    submit.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
    submit.commandBufferCount = 1;
    submit.pCommandBuffers = &command;
    require(vkQueueSubmit(queue, 1, &submit, VK_NULL_HANDLE), "vkQueueSubmit");
    require(vkQueueWaitIdle(queue), "vkQueueWaitIdle");

    std::vector<uint32_t> pixels(static_cast<size_t>(width) * height);
    void* mapped = nullptr;
    require(vkMapMemory(device, pixelBuffer.memory, 0, pixelBytes, 0, &mapped),
            "vkMapMemory(pixels)");
    std::memcpy(pixels.data(), mapped, static_cast<size_t>(pixelBytes));
    vkUnmapMemory(device, pixelBuffer.memory);
    writePpm(outPath, pixels, width, height);

    vkDestroyCommandPool(device, commandPool, nullptr);
    vkDestroyDescriptorPool(device, descriptorPool, nullptr);
    vkDestroyPipeline(device, pipeline, nullptr);
    vkDestroyShaderModule(device, shader, nullptr);
    vkDestroyPipelineLayout(device, pipelineLayout, nullptr);
    vkDestroyDescriptorSetLayout(device, setLayout, nullptr);
    destroyBuffer(device, pixelBuffer);
    destroyBuffer(device, blockBuffer);
    vkDestroyDevice(device, nullptr);
    vkDestroyInstance(instance, nullptr);
    std::cout << "Rendered " << width << "x" << height << " city via Vulkan -> "
              << outPath << "\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "LIVEIT Vulkan render failed: " << error.what() << '\n';
    return 1;
  }
}
