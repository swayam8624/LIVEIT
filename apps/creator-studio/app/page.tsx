'use client';

import { useEffect, useMemo, useState } from 'react';
import { reunion } from '@living/content';
import { createWorld } from '@living/simulation-core';
import { choose, currentScene, conditionMet } from '@living/narrative-core';
import type { World } from '@living/world-schema';
import { parseStory, type Story } from '@living/story-schema';

type Scene = Story['scenes'][number];
const STORAGE_KEY = 'liveit:creator-draft:v1';

export default function Studio() {
  const [raw, setRaw] = useState(() => JSON.stringify(reunion, null, 2));
  const [selected, setSelected] = useState(reunion.entry);
  const [previewWorld, setPreviewWorld] = useState<World>(() =>
    createWorld('Preview Player', 'creator.preview'),
  );
  const [message, setMessage] = useState(
    'Your work is stored locally in this browser.',
  );
  const [advanced, setAdvanced] = useState(false);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = parseStory(JSON.parse(saved));
        setRaw(JSON.stringify(parsed, null, 2));
        setSelected(parsed.entry);
        setPreviewWorld(createWorld('Preview Player', 'creator.preview'));
      }
    } catch {
      setMessage(
        'An old draft could not be restored. The original sample was loaded.',
      );
    } finally {
      setLoaded(true);
    }
  }, []);
  useEffect(() => {
    if (!loaded) return;
    try {
      window.localStorage.setItem(STORAGE_KEY, raw);
    } catch {
      setMessage(
        'Local draft saving is unavailable. Export your work regularly.',
      );
    }
  }, [raw, loaded]);

  const draft = useMemo(() => {
    try {
      return { value: parseStory(JSON.parse(raw)), error: '' };
    } catch (e) {
      return {
        value: null,
        error: e instanceof Error ? e.message : 'Invalid JSON',
      };
    }
  }, [raw]);
  const story = draft.value;
  const scene = story?.scenes.find((node) => node.id === selected);
  const previewScene = useMemo(() => {
    if (!story) return null;
    try {
      return currentScene(previewWorld, story);
    } catch {
      // The editor may have just renamed/deleted a scene. Keep the previous
      // runtime untouched and invite a fresh test session instead.
      return null;
    }
  }, [previewWorld, story]);
  const previewTrust =
    previewWorld.relationships.find((p) => p.characterId === 'amelia')?.trust ??
    0;
  const previewMemoryCount = previewWorld.memories.length;

  function createStory() {
    // Safely retain the last draft before opening a new story. This avoids
    // unexpected native confirmation dialogs and makes the action undoable.
    try {
      window.localStorage.setItem(STORAGE_KEY + ':previous', raw);
    } catch {
      // Export remains available even if browser storage is disabled.
    }
    const id = 'creator.story-' + Date.now().toString(36);
    const fresh = parseStory({
      schemaVersion: 1,
      id,
      version: 1,
      title: 'Untitled story',
      description: 'An interactive chapter',
      compatibleWorlds: ['modern_life_v1'],
      minAge: 18,
      permissions: {
        relationshipTargets: ['amelia'],
        memoryTargets: ['amelia'],
      },
      entry: 'opening',
      scenes: [
        {
          id: 'opening',
          speaker: 'Narrator',
          text: 'The city is quiet. You have a decision to make.',
          mood: 'reflective',
          ending: false,
          choices: [
            {
              id: 'continue',
              label: 'See what happens',
              next: 'ending',
              conditions: [],
              effects: [],
            },
          ],
        },
        {
          id: 'ending',
          speaker: 'Narrator',
          text: 'A new chapter begins.',
          mood: 'warm',
          ending: true,
          choices: [],
        },
      ],
    });
    setRaw(JSON.stringify(fresh, null, 2));
    setSelected(fresh.entry);
    setPreviewWorld(createWorld('Preview Player', 'creator.preview'));
    setMessage(
      'New story created. Rename it, write your scenes, then validate and export.',
    );
  }

  function restorePreviousDraft() {
    try {
      const previous = window.localStorage.getItem(STORAGE_KEY + ':previous');
      if (!previous) {
        setMessage('There is no previous story draft to restore.');
        return;
      }
      const restored = parseStory(JSON.parse(previous));
      window.localStorage.setItem(STORAGE_KEY + ':previous', raw);
      setRaw(JSON.stringify(restored, null, 2));
      setSelected(restored.entry);
      setPreviewWorld(createWorld('Preview Player', 'creator.preview'));
      setMessage(
        'Previous story draft restored. Your current draft is available through Restore previous.',
      );
    } catch {
      setMessage(
        'Previous draft is invalid or unavailable. The active story was not changed.',
      );
    }
  }

  function addConnectedScene() {
    if (!story || !scene) return;
    if (story.scenes.length >= 100) {
      setMessage('The story already contains the maximum of 100 scenes.');
      return;
    }
    if (!scene.ending && scene.choices.length >= 8) {
      setMessage('This scene already has the maximum of 8 choices.');
      return;
    }
    let nextNumber = story.scenes.length + 1;
    while (story.scenes.some((item) => item.id === 'scene_' + nextNumber))
      nextNumber++;
    const id = 'scene_' + nextNumber;
    const branch: Scene['choices'][number] = {
      id: 'to_' + id,
      label: 'Take another path',
      next: id,
      conditions: [],
      effects: [],
    };
    const additional: Scene = {
      id,
      speaker: 'Narrator',
      text: 'Write the next moment here.',
      mood: 'reflective',
      ending: true,
      choices: [],
    };
    try {
      const combined = parseStory({
        ...story,
        scenes: [
          ...story.scenes.map((item) =>
            item.id === scene.id
              ? { ...item, ending: false, choices: [...item.choices, branch] }
              : item,
          ),
          additional,
        ],
      });
      write(combined);
      setSelected(id);
      setPreviewWorld(createWorld('Preview Player', 'creator.preview'));
      setMessage(
        'Connected scene created. Edit its dialogue and the choice leading here.',
      );
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : 'Could not create this branch',
      );
    }
  }

  async function copyStory() {
    const valid = validate();
    if (!valid) return;
    try {
      await navigator.clipboard.writeText(JSON.stringify(valid, null, 2));
      setMessage(
        'Copied validated story JSON. Paste it into the LIVEIT player story shelf.',
      );
    } catch {
      setMessage(
        'Clipboard permission unavailable. Use Export story to download the JSON.',
      );
    }
  }

  function write(next: Story) {
    setRaw(JSON.stringify(next, null, 2));
    setMessage('Draft updated · export to share your story');
  }
  function patchStory(patch: Partial<Story>) {
    if (!story) return;
    write({ ...story, ...patch });
  }
  function patchScene(patch: Partial<Scene>) {
    if (!story || !scene) return;
    write({
      ...story,
      scenes: story.scenes.map((node) =>
        node.id === selected ? { ...node, ...patch } : node,
      ),
    });
  }
  function updateChoice(
    index: number,
    patch: Partial<Scene['choices'][number]>,
  ) {
    if (!scene) return;
    patchScene({
      choices: scene.choices.map((choice, i) =>
        i === index ? { ...choice, ...patch } : choice,
      ),
    });
  }
  function addChoiceEffect(
    index: number,
    kind: 'build-trust' | 'damage-trust' | 'memory' | 'clear',
  ) {
    if (!story || !scene) return;
    const current = scene.choices[index];
    if (!current) return;
    if (kind === 'clear') {
      updateChoice(index, { effects: [] });
      return;
    }
    if (current.effects.length >= 20) {
      setMessage('A choice can have at most 20 validated effects.');
      return;
    }
    if (kind === 'memory') {
      const target = story.permissions.memoryTargets[0];
      if (!target) {
        setMessage(
          'Add an authorized memory target in the advanced story permissions.',
        );
        return;
      }
      const fact = (
        'creator_' +
        scene.id +
        '_' +
        current.id +
        '_' +
        current.effects.length
      )
        .replace(/[^a-zA-Z0-9_]/g, '_')
        .slice(0, 80);
      updateChoice(index, {
        effects: [
          ...current.effects,
          {
            operation: 'add_memory',
            target,
            fact,
            text: 'You chose: ' + current.label.slice(0, 200),
          },
        ],
      });
      return;
    }
    const target = story.permissions.relationshipTargets[0];
    if (!target) {
      setMessage(
        'Add an authorized relationship target in the advanced story permissions.',
      );
      return;
    }
    updateChoice(index, {
      effects: [
        ...current.effects,
        {
          operation: 'adjust_relationship',
          target,
          value: kind === 'build-trust' ? 5 : -5,
        },
      ],
    });
  }

  function validate(): Story | null {
    try {
      const compiled = parseStory(JSON.parse(raw));
      setMessage(
        '✓ Verified ' +
          compiled.scenes.length +
          ' scenes · ' +
          compiled.scenes.filter((n) => n.ending).length +
          ' endings · effects permitted',
      );
      return compiled;
    } catch (e) {
      setMessage(e instanceof Error ? e.message : 'Validation failed');
      return null;
    }
  }
  function exportStory() {
    const compiled = validate();
    if (!compiled) return;
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(compiled, null, 2)], {
        type: 'application/json',
      }),
    );
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = compiled.id + '.v' + compiled.version + '.json';
    anchor.click();
    URL.revokeObjectURL(url);
  }
  async function importStory(file?: File) {
    if (!file) return;
    try {
      const incoming = parseStory(JSON.parse(await file.text()));
      setRaw(JSON.stringify(incoming, null, 2));
      setSelected(incoming.entry);
      setPreviewWorld(createWorld('Preview Player', 'creator.preview'));
      setMessage(
        'Imported ' +
          incoming.title +
          ' · this is a local draft, not a public publication.',
      );
    } catch (e) {
      setMessage(
        e instanceof Error ? e.message : 'The story could not be imported',
      );
    }
  }
  function resetPreview() {
    setPreviewWorld(createWorld('Preview Player', 'creator.preview'));
    setMessage(
      'Preview reset. Try a different path and compare its consequences.',
    );
  }
  function playPreviewChoice(choiceId: string) {
    if (!story) return;
    try {
      // Exactly the same guards and atomic consequence engine as the player.
      const next = choose(previewWorld, story, choiceId);
      setPreviewWorld(next);
      setMessage(
        'Choice executed using the actual simulation and story runtime.',
      );
    } catch (error) {
      setMessage(
        error instanceof Error
          ? 'Preview: ' + error.message
          : 'Preview could not advance.',
      );
    }
  }

  return (
    <main className="studio-shell">
      <header className="studio-topbar">
        <span>
          ✦ LIVEIT <small> / CREATOR STUDIO</small>
        </span>
        <div className="studio-actions">
          <button type="button" className="secondary" onClick={createStory}>
            + New story
          </button>
          <button
            type="button"
            className="secondary"
            onClick={restorePreviousDraft}
          >
            ↶ Previous draft
          </button>
          <button
            type="button"
            className="secondary"
            onClick={() => void copyStory()}
          >
            Copy to player
          </button>
          <label className="upload-control">
            Import JSON
            <input
              aria-label="Import story JSON"
              type="file"
              accept=".json,application/json"
              onChange={(e) => void importStory(e.target.files?.[0])}
            />
          </label>
          <button type="button" className="secondary" onClick={validate}>
            ✓ Validate
          </button>
          <button type="button" onClick={exportStory}>
            Export story ↗
          </button>
        </div>
      </header>
      <div className="editor-heading">
        <div>
          <p className="eyebrow">STORY WORKSHOP / PRIVATE DRAFT</p>
          <h1>{story?.title || 'Untitled story'}</h1>
          <p className="intro">
            Write the moment. Direct the scene. Give the player a choice that
            matters.
          </p>
        </div>
        <p role="status" className="editor-status">
          {message}
        </p>
      </div>
      <div className="studio-grid">
        <aside className="scene-panel">
          <p className="eyebrow">
            SCENES <span>{story?.scenes.length ?? 0}</span>
          </p>
          <div className="scene-list">
            {story?.scenes.map((node, index) => (
              <button
                type="button"
                className={
                  'scene-item ' + (selected === node.id ? 'scene-selected' : '')
                }
                key={node.id}
                onClick={() => {
                  setSelected(node.id);
                  // Selecting a scene to edit does not falsify the live test timeline.
                }}
              >
                <small>{String(index + 1).padStart(2, '0')}</small>
                <span>
                  <strong>{node.id.replaceAll('_', ' ')}</strong>
                  <em>
                    {node.ending ? 'Ending' : node.choices.length + ' choices'}
                  </em>
                </span>
                <span aria-hidden>{node.ending ? '◈' : '›'}</span>
              </button>
            ))}
          </div>
          <button
            type="button"
            className="secondary add-branch"
            onClick={addConnectedScene}
            disabled={!scene}
          >
            + Add connected scene
          </button>
          <div className="scene-help">
            Story graph links are defined by each choice's destination.
            Validation checks reachability, invalid effects and endings.
          </div>
        </aside>
        <section className="editor-main">
          <div className="editor-title">
            <h2>Scene direction</h2>
            <small>{scene?.id ?? 'Choose a scene'}</small>
          </div>
          {story && (
            <label>
              Story title
              <input
                value={story.title}
                maxLength={100}
                onChange={(e) => patchStory({ title: e.target.value })}
              />
            </label>
          )}
          {scene ? (
            <>
              <div className="field-pair">
                <label>
                  Speaker{' '}
                  <input
                    value={scene.speaker}
                    maxLength={60}
                    onChange={(e) => patchScene({ speaker: e.target.value })}
                  />
                </label>
                <label>
                  Emotional tone
                  <select
                    value={scene.mood}
                    onChange={(e) =>
                      patchScene({ mood: e.target.value as Scene['mood'] })
                    }
                  >
                    <option value="reflective">Reflective</option>
                    <option value="warm">Warm</option>
                    <option value="tense">Tense</option>
                  </select>
                </label>
              </div>
              <label>
                Dialogue
                <textarea
                  rows={5}
                  value={scene.text}
                  maxLength={2000}
                  onChange={(e) => patchScene({ text: e.target.value })}
                />
              </label>
              <div className="editor-title">
                <h2>Player choices</h2>
                <small>{scene.choices.length} branches</small>
              </div>
              {scene.ending ? (
                <p className="scene-help">
                  This scene is an ending. Players return to their life after
                  it.
                </p>
              ) : (
                scene.choices.map((choice, index) => (
                  <div className="choice-editor" key={choice.id}>
                    <strong>Choice {index + 1}</strong>
                    <label>
                      Choice text
                      <input
                        value={choice.label}
                        maxLength={200}
                        onChange={(e) =>
                          updateChoice(index, { label: e.target.value })
                        }
                      />
                    </label>
                    <label>
                      Destination
                      <select
                        value={choice.next}
                        onChange={(e) =>
                          updateChoice(index, { next: e.target.value })
                        }
                      >
                        {story?.scenes.map((n) => (
                          <option value={n.id} key={n.id}>
                            {n.id}
                          </option>
                        ))}
                      </select>
                    </label>
                    <small>
                      Consequences:{' '}
                      {choice.effects
                        .map((e) =>
                          e.operation === 'adjust_relationship'
                            ? `${e.target} trust ${e.value > 0 ? '+' : ''}${e.value}`
                            : `remember: ${e.fact}`,
                        )
                        .join(' · ') || 'No state changes'}
                    </small>
                    <div
                      className="effect-controls"
                      aria-label="Add game consequences"
                    >
                      <button
                        type="button"
                        className="secondary"
                        onClick={() => addChoiceEffect(index, 'build-trust')}
                      >
                        +5 trust
                      </button>
                      <button
                        type="button"
                        className="secondary"
                        onClick={() => addChoiceEffect(index, 'damage-trust')}
                      >
                        −5 trust
                      </button>
                      <button
                        type="button"
                        className="secondary"
                        onClick={() => addChoiceEffect(index, 'memory')}
                      >
                        + Memory
                      </button>
                      <button
                        type="button"
                        className="secondary"
                        disabled={choice.effects.length === 0}
                        onClick={() => addChoiceEffect(index, 'clear')}
                      >
                        Clear effects
                      </button>
                    </div>
                  </div>
                ))
              )}
            </>
          ) : (
            <p>Select a scene on the left.</p>
          )}
          <button
            type="button"
            className="secondary"
            onClick={() => setAdvanced(!advanced)}
          >
            {advanced
              ? 'Hide advanced graph JSON'
              : 'Advanced: edit complete story JSON'}
          </button>
          {advanced && (
            <textarea
              className="code"
              aria-label="Story JSON"
              spellCheck={false}
              value={raw}
              onChange={(e) => setRaw(e.target.value)}
            />
          )}
        </section>
        <section className="preview-panel">
          <div className="editor-title">
            <h2>Playable preview</h2>
            <button type="button" className="secondary" onClick={resetPreview}>
              ↺ Restart
            </button>
          </div>
          <div
            className={
              'preview-stage mood-' + (previewScene?.mood || 'reflective')
            }
          >
            <p className="preview-location">BELLWEATHER · THE CORNER CAFÉ</p>
            <div className="preview-dialogue">
              <small>{previewScene?.speaker || 'CHARACTER'}</small>
              <p>{previewScene?.text ?? 'Select a playable scene.'}</p>
            </div>
          </div>
          <div className="preview-stats" aria-label="Preview simulation state">
            <span>
              AMELIA TRUST{' '}
              <strong data-testid="preview-trust">{previewTrust}/100</strong>
            </span>
            <span>
              MEMORIES{' '}
              <strong data-testid="preview-memory-count">
                {previewMemoryCount}
              </strong>
            </span>
            <span>
              DAY <strong>{previewWorld.day + 1}</strong>
            </span>
          </div>
          <div className="preview-choices">
            {!previewScene ? (
              <p>
                The edited story no longer matches the active preview. Restart
                the preview to run its latest graph.
              </p>
            ) : previewScene.ending ? (
              <p>
                ✦ Ending reached. The player’s story remains saved in its
                timeline.
              </p>
            ) : (
              previewScene?.choices.map((choice) => (
                <button
                  key={choice.id}
                  type="button"
                  disabled={
                    !choice.conditions.every((c) =>
                      conditionMet(previewWorld, c),
                    )
                  }
                  title={
                    choice.conditions.length
                      ? 'Requires conditions: ' +
                        JSON.stringify(choice.conditions)
                      : undefined
                  }
                  onClick={() => playPreviewChoice(choice.id)}
                >
                  {choice.label} <span>›</span>
                </button>
              ))
            )}
          </div>
          <p className="scene-help">
            This preview uses the same validated choice, condition and
            consequence engine as the player. Trust and memories change
            immediately; restart to compare another path. Export JSON to verify
            persistence in the player itself.
          </p>
        </section>
      </div>
    </main>
  );
}
