#!/usr/bin/env node
/* global process, AbortController, setTimeout, clearTimeout, console, fetch */
/**
 * LIVEIT local Ollama diagnostics. Does not fake an NPC response.
 *
 * Run with: npm run ai:check
 * Or: OLLAMA_BASE_URL=http://192.168.1.42:11434 OLLAMA_MODEL=qwen3:4b npm run ai:check
 * Node checks the daemon/model. Browsers additionally need OLLAMA_ORIGINS.
 */
const base = (process.env.OLLAMA_BASE_URL ?? 'http://localhost:11434').replace(
  /\/+$/,
  '',
);
const model = process.env.OLLAMA_MODEL ?? 'qwen3:4b';
const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), 45_000);
try {
  console.log('Checking ' + base + ' for installed model ' + model);
  const resp = await fetch(base + '/api/tags', { signal: controller.signal });
  if (!resp.ok) throw new Error('Ollama HTTP ' + resp.status);
  const body = await resp.json();
  const names = (body.models ?? []).map((m) => m.name);
  if (!names.includes(model)) {
    throw new Error(
      'Model ' +
        model +
        ' missing. Installed models: ' +
        names.join(', ') +
        '. Run: ollama pull ' +
        model,
    );
  }
  console.log('Model available. Testing a REAL inference response...');
  const chat = await fetch(base + '/api/chat', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    signal: controller.signal,
    body: JSON.stringify({
      model,
      stream: false,
      think: false,
      options: { num_predict: 80 },
      messages: [
        {
          role: 'system',
          content:
            'You are Amelia, a fictional adult NPC in Bellweather. Say hello naturally.',
        },
        { role: 'user', content: 'Hello Amelia. What have you been up to?' },
      ],
    }),
  });
  if (!chat.ok)
    throw new Error(
      'Inference HTTP ' +
        chat.status +
        ': ' +
        (await chat.text()).slice(0, 300),
    );
  const result = await chat.json();
  const reply = result?.message?.content;
  if (typeof reply !== 'string' || !reply.trim())
    throw new Error('Empty model output.');
  console.log('\nREAL MODEL RESPONSE:\n' + reply.trim());
  console.log(
    '\nPASS. If mobile web fails while CLI passes, check OLLAMA_ORIGINS and iPhone LAN host.',
  );
} catch (err) {
  console.error('\nFAIL: ' + String(err));
  console.error('1. Run ollama list; if necessary ollama pull ' + model);
  console.error(
    '2. Start the Ollama daemon. On browser web, allow http://localhost:8081 in OLLAMA_ORIGINS.',
  );
  console.error(
    '3. On iPhone use Mac LAN IP and bind Ollama securely to that LAN; never expose port 11434 publicly.',
  );
  process.exitCode = 1;
} finally {
  clearTimeout(timer);
}
