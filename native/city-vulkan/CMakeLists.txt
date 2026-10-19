cmake_minimum_required(VERSION 3.20)
project(LIVEITCityVulkan LANGUAGES CXX)

find_package(Vulkan REQUIRED)
find_program(GLSLC_EXECUTABLE NAMES glslc REQUIRED)

set(CITY_SHADER_SOURCE ${CMAKE_CURRENT_SOURCE_DIR}/shaders/city.comp)
set(CITY_SHADER_BINARY ${CMAKE_CURRENT_BINARY_DIR}/city.comp.spv)

add_custom_command(
  OUTPUT ${CITY_SHADER_BINARY}
  COMMAND ${GLSLC_EXECUTABLE} ${CITY_SHADER_SOURCE} -o ${CITY_SHADER_BINARY}
  DEPENDS ${CITY_SHADER_SOURCE}
  COMMENT "Compile LIVEIT city raycast compute shader to SPIR-V"
  VERBATIM
)

set(ACTORS_SHADER_SOURCE ${CMAKE_CURRENT_SOURCE_DIR}/shaders/actors.comp)
set(ACTORS_SHADER_BINARY ${CMAKE_CURRENT_BINARY_DIR}/actors.comp.spv)
add_custom_command(
  OUTPUT ${ACTORS_SHADER_BINARY}
  COMMAND ${GLSLC_EXECUTABLE} ${ACTORS_SHADER_SOURCE} -o ${ACTORS_SHADER_BINARY}
  DEPENDS ${ACTORS_SHADER_SOURCE}
  COMMENT "Compile all-character Vulkan 2.5D stage to SPIR-V"
  VERBATIM
)
add_custom_target(city_shader DEPENDS ${CITY_SHADER_BINARY} ${ACTORS_SHADER_BINARY})
add_executable(city_vulkan src/main.cpp)
add_dependencies(city_vulkan city_shader)
target_compile_features(city_vulkan PRIVATE cxx_std_17)
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/src/config.hpp.in
  ${CMAKE_CURRENT_BINARY_DIR}/generated/config.hpp
  @ONLY
)
target_include_directories(city_vulkan PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/generated)
target_link_libraries(city_vulkan PRIVATE Vulkan::Vulkan)

enable_testing()
add_test(NAME city_vulkan_day
  COMMAND city_vulkan ${CMAKE_CURRENT_BINARY_DIR}/city-day.ppm 256 160 day)
add_test(NAME city_vulkan_night
  COMMAND city_vulkan ${CMAKE_CURRENT_BINARY_DIR}/city-night.ppm 256 160 night)
add_test(NAME actors_vulkan_portrait
  COMMAND city_vulkan ${CMAKE_CURRENT_BINARY_DIR}/actor-portrait.ppm 320 400 day portrait 1)
add_test(NAME actors_vulkan_emotion
  COMMAND city_vulkan ${CMAKE_CURRENT_BINARY_DIR}/actor-emotion.ppm 320 400 day portrait 8)
add_test(NAME actors_vulkan_conversation
  COMMAND city_vulkan ${CMAKE_CURRENT_BINARY_DIR}/actor-conversation.ppm 512 320 night conversation 2)
add_test(NAME actors_vulkan_cast
  COMMAND city_vulkan ${CMAKE_CURRENT_BINARY_DIR}/actor-cast.ppm 512 320 day cast 1)
add_test(NAME actors_vulkan_animation
  COMMAND city_vulkan ${CMAKE_CURRENT_BINARY_DIR}/actor-animation.ppm 320 400 day portrait 1 16.0)
