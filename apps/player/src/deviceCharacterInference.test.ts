import { describe, expect, it, vi } from 'vitest';
import {
  DeviceCharacterInference,
  localGGUFPath,
  type NativeGGUFContext,
  type NativeGGUFEngine,
} from './deviceCharacterInference';

function fixture() {
  const context: NativeGGUFContext = {
    completion: vi.fn(async (_params, onToken) => {
      onToken?.({ token: 'Hello' });
      return { text: 'Hello from Bellweather.' };
    }),
    release: vi.fn(async () => {}),
  };
  const engine: NativeGGUFEngine = { initLlama: vi.fn(async () => context) };
  return { context, engine, runtime: new DeviceCharacterInference(engine) };
}

describe('device-only GGUF character AI', () => {
  it('rejects remote model URLs and directory escapes', () => {
    expect(() => localGGUFPath('https://example.com/ai.gguf')).toThrow();
    expect(() => localGGUFPath('file:///models/../secrets.gguf')).toThrow();
    expect(localGGUFPath('file:///documents/models/character.Q4_K_M.gguf')).toBe(
      'file:///documents/models/character.Q4_K_M.gguf',
    );
  });

  it('does not generate or contact a server before a native model is loaded', async () => {
    const { runtime, engine } = fixture();
    const response = await runtime.reply({
      characterId: 'amelia',
      characterName: 'Amelia',
      playerMessage: 'Hi',
      worldContext: 'café',
      memories: [],
    });
    expect(response.kind).toBe('unavailable');
    expect(engine.initLlama).not.toHaveBeenCalled();
  });

  it('uses a local model, streams tokens and keeps state outside generated dialogue', async () => {
    const { runtime, context, engine } = fixture();
    await runtime.load('file:///documents/ai/local.gguf');
    const tokens: string[] = [];
    const response = await runtime.reply({
      characterId: 'amelia',
      characterName: 'Amelia',
      playerMessage: 'Hello',
      worldContext: 'Trust is 35, café at 4pm',
      memories: ['Shared coffee yesterday'],
    }, (token) => tokens.push(token));
    expect(engine.initLlama).toHaveBeenCalledWith(expect.objectContaining({
      model: 'file:///documents/ai/local.gguf',
    }));
    expect(context.completion).toHaveBeenCalledWith(
      expect.objectContaining({
        messages: expect.arrayContaining([
          expect.objectContaining({ role: 'system', content: expect.stringContaining('Trust is 35') }),
        ]),
      }),
      expect.any(Function),
    );
    expect(tokens).toEqual(['Hello']);
    expect(response).toEqual({ kind: 'generated', text: 'Hello from Bellweather.' });
    await runtime.unload();
    expect(context.release).toHaveBeenCalledOnce();
  });

  it('degrades safely when native inference errors', async () => {
    const { runtime, context } = fixture();
    context.completion = vi.fn(async () => { throw new Error('out of memory'); });
    await runtime.load('file:///documents/ai/local.gguf');
    const response = await runtime.reply({
      characterId: 'amelia',
      characterName: 'Amelia',
      playerMessage: 'Hello',
      worldContext: '',
      memories: [],
    });
    expect(response).toMatchObject({ kind: 'unavailable', reason: 'out of memory' });
  });
});
