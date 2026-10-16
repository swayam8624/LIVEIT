'use client';
import { useState } from 'react';
import { reunion } from '@living/content';
import { parseStory } from '@living/story-schema';
export default function Studio() {
  const [title, setTitle] = useState(reunion.title);
  const [opening, setOpening] = useState(reunion.scenes[0]!.text);
  const [source, setSource] = useState(JSON.stringify(reunion, null, 2));
  const [message, setMessage] = useState('');
  function compile() {
    try {
      const story = parseStory({
        ...JSON.parse(source),
        title,
        scenes: JSON.parse(source).scenes.map((s: { id: string }) =>
          s.id === reunion.entry ? { ...s, text: opening } : s,
        ),
      });
      setSource(JSON.stringify(story, null, 2));
      setMessage(
        `Validated: ${story.scenes.length} scenes, ${story.scenes.filter((s) => s.ending).length} endings. Ready to export for local testing.`,
      );
      return story;
    } catch (e) {
      setMessage(e instanceof Error ? e.message : 'Validation failed');
      return null;
    }
  }
  function download() {
    const story = compile();
    if (!story) return;
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(story, null, 2)], { type: 'application/json' }),
    );
    const a = document.createElement('a');
    a.href = url;
    a.download = `${story.id}.v${story.version}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }
  return (
    <main>
      <header>
        <span>✳ living universe</span>
        <small>CREATOR STUDIO · LOCAL DRAFT</small>
      </header>
      <p className="eyebrow">GIVE YOUR WORLD A VOICE</p>
      <h1>
        Every encounter
        <br />
        starts with a story.
      </h1>
      <p className="intro">
        Write a moment that stays with someone. Your encounter uses the same
        safe story format as the player.
      </p>
      <div className="workspace">
        <section>
          <h2>The opening</h2>
          <label>
            Story title
            <input
              value={title}
              maxLength={100}
              onChange={(e) => setTitle(e.target.value)}
            />
          </label>
          <label>
            Amelia’s first words
            <textarea
              value={opening}
              onChange={(e) => setOpening(e.target.value)}
              rows={6}
            />
          </label>
          <p className="note">
            These fields override the title and arrival dialogue when
            validating. For advanced edits, change the graph on the right.
          </p>
          <div className="actions">
            <button onClick={compile}>Validate encounter ↗</button>
            <button className="secondary" onClick={download}>
              Export story JSON
            </button>
          </div>
          <p role="status" className="status">
            {message}
          </p>
          <aside>
            <h3>A draft, with guardrails.</h3>
            <p>
              Validation checks destinations, reachability, endings,
              unconditional fallback choices, and effect permissions. Export is
              for local testing; public publishing and moderation are future
              milestones.
            </p>
          </aside>
        </section>
        <section>
          <h2>Story graph · version 1</h2>
          <textarea
            aria-label="Story JSON"
            className="code"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            spellCheck={false}
          />
        </section>
      </div>
    </main>
  );
}
