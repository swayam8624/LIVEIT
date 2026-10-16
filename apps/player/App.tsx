import React, { useEffect, useRef, useState } from 'react';
import {
  Platform,
  Image,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
  useWindowDimensions,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  createWorld,
  advanceLife,
  type Activity,
} from '@living/simulation-core';
import {
  choose,
  currentScene,
  startStory,
  conditionMet,
} from '@living/narrative-core';
import { loadSave, writeSave, type Save } from '@living/save-system';
import type { World } from '@living/world-schema';
import { reunion } from '@living/content';
import type { Story } from '@living/story-schema';
import { LocalStoryLibrary } from './src/LocalStoryLibrary';
import { GameStage } from './src/GameStage';
const c = {
  paper: '#0c1421',
  ink: '#f7eee1',
  muted: '#b0b7c4',
  line: '#3a4457',
  green: '#a35a37',
  sage: '#253247',
  orange: '#f8b97e',
  white: '#192536',
};
const serif = Platform.OS === 'ios' ? 'Georgia' : 'serif';
const gold = '#ecc391';
// Metro bundles this original, locally stored character portrait offline.
// eslint-disable-next-line @typescript-eslint/no-require-imports
const ameliaPortrait = require('./assets/amelia-portrait.jpg');
const money = (n: number) =>
  new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
    maximumFractionDigits: 0,
  }).format(n / 100);
function Button({
  label,
  onPress,
  secondary = false,
  disabled = false,
}: {
  label: string;
  onPress: () => void;
  secondary?: boolean;
  disabled?: boolean;
}) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={label}
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        s.button,
        secondary && s.secondary,
        disabled && { opacity: 0.45 },
        pressed && { opacity: 0.75 },
      ]}
    >
      <Text style={[s.buttonText, secondary && { color: c.ink }]}>{label}</Text>
    </Pressable>
  );
}
function Tag({ children }: { children: React.ReactNode }) {
  return <Text style={s.tag}>{children}</Text>;
}
function Stat({
  label,
  value,
  detail,
}: {
  label: string;
  value: string;
  detail: string;
}) {
  return (
    <View style={s.stat}>
      <Text style={s.eyebrow}>{label}</Text>
      <Text style={s.statValue}>{value}</Text>
      <Text style={s.small}>{detail}</Text>
    </View>
  );
}
export default function App() {
  const { width } = useWindowDimensions();
  const wide = width >= 1000;
  const [save, setSave] = useState<Save | null>(null);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');
  const [tab, setTab] = useState<'life' | 'stories' | 'journal'>('life');
  const [name, setName] = useState('Alex Morgan');
  const [pronouns, setPronouns] = useState<'they/them' | 'she/her' | 'he/him'>(
    'they/them',
  );
  const [sceneOpen, setSceneOpen] = useState(false);
  const [authored, setAuthored] = useState<Story>(reunion);
  const [days, setDays] = useState(1);
  const [reset, setReset] = useState(false);
  const queue = useRef(Promise.resolve());
  const revision = useRef(0);
  useEffect(() => {
    loadSave(AsyncStorage)
      .then((value) => {
        if (value) {
          setSave(value);
          setSceneOpen(value.active === 'story');
          setTab(value.active === 'story' ? 'stories' : 'life');
        }
        setReady(true);
      })
      .catch(() => {
        setError(
          'Your saved life could not be read. It has not been overwritten. Start a new life only if you want to replace it.',
        );
        setReady(true);
      });
  }, []);
  function persist(next: Save) {
    setSave(next);
    setError('');
    setStatus('Saving…');
    const rev = ++revision.current;
    queue.current = queue.current
      .catch(() => {})
      .then(() => writeSave(AsyncStorage, next));
    void queue.current
      .then(() => {
        if (revision.current === rev) setStatus('Saved on this device');
      })
      .catch(() => {
        if (revision.current === rev) {
          setStatus('Not saved');
          setError(
            'Storage is unavailable. Your changes are in memory; use Save again to retry before closing.',
          );
        }
      });
  }
  const world = save
    ? save.active === 'story'
      ? save.story!
      : save.life
    : null;
  function update(w: World) {
    if (!save) return;
    persist(
      save.active === 'life' ? { ...save, life: w } : { ...save, story: w },
    );
  }
  function run(action: () => void) {
    try {
      action();
    } catch (e) {
      setError(
        e instanceof Error ? e.message : 'This action could not be completed.',
      );
    }
  }
  function openEncounter() {
    if (!save) return;
    setAuthored(reunion);
    run(() => {
      update(startStory(world!, reunion));
      setSceneOpen(true);
    });
  }
  function standalone() {
    if (!save) return;
    setAuthored(reunion);
    run(() => {
      const story =
        save.story ??
        startStory(
          createWorld(
            save.life.player.name,
            'story.reunion',
            save.life.player.pronouns,
          ),
          reunion,
        );
      persist({ ...save, story, active: 'story' });
      setSceneOpen(true);
    });
  }
  function newLife() {
    setAuthored(reunion);
    run(() => {
      persist({
        version: 1,
        active: 'life',
        life: createWorld(name, 'main', pronouns),
        story: null,
      });
      setReset(false);
      setTab('life');
      setSceneOpen(false);
    });
  }
  function playImported(story: Story) {
    if (!save) return;
    run(() => {
      const started = startStory(save.life, story);
      setAuthored(story);
      persist({ ...save, active: 'life', life: started });
      setTab('stories');
      setSceneOpen(true);
    });
  }
  if (!ready)
    return (
      <View style={s.loading}>
        <Text style={s.logo}>living universe</Text>
        <Text style={s.small}>Opening your world…</Text>
      </View>
    );
  return (
    <View style={s.app}>
      <View style={[s.header, { paddingHorizontal: wide ? 48 : 22 }]}>
        <View>
          <Text style={s.logo}>✦ LIVEIT</Text>
          <Text style={s.logoSub}>EVERY CHOICE BECOMES A LIFE</Text>
        </View>
        {wide && (
          <View style={s.headerRight}>
            <View style={s.dot} />
            <Text style={s.small}>CHAPTER ONE · BELLWEATHER</Text>
          </View>
        )}
      </View>
      <View style={s.shell}>
        <View style={s.gameNav}>
          {(
            [
              { id: 'life', symbol: '⌂', title: 'FREE LIFE' },
              { id: 'stories', symbol: '✧', title: 'STORIES' },
              { id: 'journal', symbol: '◷', title: 'MEMORIES' },
            ] as const
          ).map((entry) => (
            <Pressable
              key={entry.id}
              accessibilityRole="tab"
              accessibilityState={{ selected: tab === entry.id }}
              accessibilityLabel={entry.title}
              onPress={() => {
                setTab(entry.id);
                setSceneOpen(false);
              }}
              style={({ pressed }) => [
                s.gameNavItem,
                tab === entry.id && s.gameNavSelected,
                pressed && { opacity: 0.75 },
              ]}
            >
              <Text
                style={[
                  s.gameNavText,
                  tab === entry.id && { color: '#f7d6a1' },
                ]}
              >
                {entry.symbol} {entry.title}
              </Text>
            </Pressable>
          ))}
        </View>
        <ScrollView
          contentContainerStyle={[s.main, { padding: wide ? 40 : 22 }]}
        >
          {error !== '' && (
            <View accessibilityRole="alert" style={s.alert}>
              <Text>{error}</Text>
            </View>
          )}
          {!save || reset ? (
            <View style={s.onboard}>
              <Tag>CHAPTER ZERO</Tag>
              <Text style={s.title}>
                A life worth{wide ? '\n' : ' '}remembering.
              </Text>
              <Text style={s.subtitle}>
                You’re 23, newly arrived in Bellweather. There’s £1,800 in your
                account, a city to discover, and someone from your past just
                around the corner.
              </Text>
              <Text style={s.fieldLabel}>WHAT SHOULD WE CALL YOU?</Text>
              <TextInput
                accessibilityLabel="Character name"
                value={name}
                onChangeText={setName}
                maxLength={40}
                style={s.input}
              />
              <Text style={s.fieldLabel}>YOUR PRONOUNS</Text>
              <View style={s.row}>
                {(['they/them', 'she/her', 'he/him'] as const).map((p) => (
                  <Button
                    key={p}
                    label={p}
                    secondary={pronouns !== p}
                    onPress={() => setPronouns(p)}
                  />
                ))}
              </View>
              <View style={s.row}>
                <Button
                  label={
                    reset
                      ? 'Create new life & replace save →'
                      : 'Begin your life →'
                  }
                  disabled={!name.trim()}
                  onPress={newLife}
                />
                {reset && (
                  <Button
                    label="Keep my current life"
                    secondary
                    onPress={() => setReset(false)}
                  />
                )}
              </View>
              <Text style={s.small}>
                Saved locally on this device. No account needed.
              </Text>
            </View>
          ) : (
            <>
              <View style={s.topLine}>
                <Text style={s.eyebrow}>
                  {tab === 'life'
                    ? 'YOUR LIFE, UNFOLDING'
                    : tab === 'stories'
                      ? 'A DIFFERENT WAY TO LIVE'
                      : 'THE THINGS THAT STAY'}
                </Text>
                <Text accessibilityLiveRegion="polite" style={s.saveStatus}>
                  {status || 'Saved on this device'}
                </Text>
              </View>
              {sceneOpen ? (
                <>
                  <View style={s.topLine}>
                    <View>
                      <Tag>
                        {save.active === 'life'
                          ? 'AN ENCOUNTER IN YOUR LIFE'
                          : 'STANDALONE STORY TIMELINE'}
                      </Tag>
                      <Text style={s.title}>{authored.title}</Text>
                    </View>
                    <Button
                      label="Save & leave scene"
                      secondary
                      onPress={() => {
                        persist(save);
                        setSceneOpen(false);
                      }}
                    />
                  </View>
                  <View style={s.sceneLayout}>
                    <View style={{ flex: 1.15 }}>
                      <GameStage
                        mode="story"
                        mood={currentScene(world!, authored).mood}
                      >
                        <Text style={s.stageHeadline}>
                          {authored.id === reunion.id
                            ? "A conversation you can't undo."
                            : authored.title}
                        </Text>
                        <Text style={s.stageHint}>
                          What you say here becomes part of your history.
                        </Text>
                      </GameStage>
                      <View style={s.sceneMeta}>
                        <Text style={s.small}>LIVEIT · PLAYABLE ENCOUNTER</Text>
                        <Text style={s.small}>
                          Consequences are saved to this timeline
                        </Text>
                      </View>
                    </View>
                    <View
                      style={s.dialogue}
                      key={currentScene(world!, authored).id}
                    >
                      <View style={s.speakerRow}>
                        {currentScene(
                          world!,
                          authored,
                        ).speaker.toLowerCase() === 'amelia' ? (
                          <Image
                            source={ameliaPortrait}
                            style={s.speakerPortrait}
                            accessibilityLabel="Illustrated portrait of Amelia"
                          />
                        ) : (
                          <View style={s.speakerFallback}>
                            <Text style={s.speakerFallbackText}>
                              {currentScene(world!, authored)
                                .speaker.slice(0, 1)
                                .toUpperCase() || '✧'}
                            </Text>
                          </View>
                        )}
                        <View style={{ flex: 1, gap: 3 }}>
                          <Text style={s.eyebrow}>
                            {currentScene(
                              world!,
                              reunion,
                            ).speaker.toUpperCase()}
                          </Text>
                          <Text style={s.small}>
                            THE SPACE BETWEEN · BELLWEATHER
                          </Text>
                        </View>
                      </View>
                      <Text style={s.dialogueText}>
                        {currentScene(world!, authored).text}
                      </Text>
                      {currentScene(world!, authored).choices.map((choice) => {
                        const available = choice.conditions.every((cond) =>
                          conditionMet(world!, cond),
                        );
                        return (
                          <Pressable
                            key={choice.id}
                            accessibilityRole="button"
                            disabled={!available}
                            onPress={() =>
                              run(() =>
                                update(choose(world!, authored, choice.id)),
                              )
                            }
                            style={({ pressed }) => [
                              s.choice,
                              !available && { opacity: 0.4 },
                              pressed && { backgroundColor: c.sage },
                            ]}
                          >
                            <Text style={s.choiceText}>
                              {choice.label}
                              {!available ? ' · More trust needed' : ''}
                            </Text>
                            <Text style={{ color: c.orange }}>↗</Text>
                          </Pressable>
                        );
                      })}
                      {currentScene(world!, authored).ending && (
                        <>
                          <Tag>CHAPTER COMPLETE · YOUR WORLD REMEMBERS</Tag>
                          <Text style={s.small}>
                            Your decisions are recorded in this timeline’s
                            journal.
                          </Text>
                          <Button
                            label={
                              save.active === 'life'
                                ? 'Return to your life →'
                                : 'Continue living in this timeline →'
                            }
                            onPress={() => {
                              setSceneOpen(false);
                              setTab('life');
                            }}
                          />
                        </>
                      )}
                    </View>
                  </View>
                </>
              ) : tab === 'life' ? (
                <>
                  <View style={s.topLine}>
                    <View>
                      <Text style={s.title}>
                        {world!.day === 0
                          ? 'A new beginning.'
                          : 'A little more life.'}
                      </Text>
                      <Text style={s.subtitle}>
                        {world!.player.name} · Age{' '}
                        {Math.floor(world!.player.ageDays / 365)} · Bellweather
                      </Text>
                    </View>
                    <Tag>
                      {save.active === 'story'
                        ? 'STORY CONTINUITY'
                        : 'MAIN TIMELINE'}
                    </Tag>
                  </View>
                  <GameStage mode="life">
                    <Text style={s.stageHeadline}>Your life is happening.</Text>
                    <Text style={s.stageHint}>
                      Choose where to spend your time. The city will remember
                      what you do.
                    </Text>
                    <View style={s.destinationRow}>
                      {(
                        [
                          { icon: '✦', label: 'THE CAFÉ', action: 'cafe' },
                          { icon: '↗', label: 'WORK', action: 'work' },
                          { icon: '✧', label: 'STUDY', action: 'study' },
                          { icon: '♡', label: 'FRIENDS', action: 'socialize' },
                          { icon: '☾', label: 'REST', action: 'rest' },
                        ] as const
                      ).map((dest) => (
                        <Pressable
                          key={dest.action}
                          accessibilityRole="button"
                          accessibilityLabel={dest.label}
                          style={({ pressed }) => [
                            s.destination,
                            pressed && { backgroundColor: '#865037' },
                          ]}
                          onPress={() =>
                            dest.action === 'cafe'
                              ? openEncounter()
                              : run(() =>
                                  update(
                                    advanceLife(
                                      world!,
                                      dest.action as Activity,
                                      days,
                                    ),
                                  ),
                                )
                          }
                        >
                          <Text style={s.destinationText}>
                            {dest.icon} {dest.label}
                          </Text>
                        </Pressable>
                      ))}
                    </View>
                  </GameStage>
                  <View style={s.stats}>
                    <Stat
                      label="YOUR SAVINGS"
                      value={money(world!.player.money)}
                      detail="After everyday living costs"
                    />
                    <Stat
                      label="WELLBEING"
                      value={`${world!.player.wellbeing}%`}
                      detail="Make a little room for yourself"
                    />
                    <Stat
                      label="EXPERIENCE"
                      value={`${world!.player.skill}/100`}
                      detail={
                        world!.player.career === 'employed'
                          ? 'Employed · city design studio'
                          : 'Finding your feet · freelance'
                      }
                    />
                    <Stat
                      label="YOUR CALENDAR"
                      value={`Day ${world!.day + 1}`}
                      detail="Time moves when you choose"
                    />
                  </View>
                  <View style={[s.columns, wide && { flexDirection: 'row' }]}>
                    <View style={{ flex: 1.15, gap: 22 }}>
                      <View style={s.sectionHeading}>
                        <Text style={s.sectionTitle}>
                          What will you make of today?
                        </Text>
                        <Text style={s.small}>THE EVERYDAY MATTERS</Text>
                      </View>
                      <View style={s.activities}>
                        {(
                          [
                            {
                              id: 'work',
                              icon: '↗',
                              title: 'Put yourself out there',
                              detail:
                                'Work a freelance shift. Build experience.',
                              result: '+ income · − wellbeing',
                            },
                            {
                              id: 'study',
                              icon: '✧',
                              title: 'Learn something new',
                              detail: 'A little practice opens new doors.',
                              result: '+ 4 experience per day',
                            },
                            {
                              id: 'socialize',
                              icon: '☏',
                              title: 'Make time for a friend',
                              detail: 'Catch up with Noah. Be present.',
                              result: '+ connection · + wellbeing',
                            },
                            {
                              id: 'rest',
                              icon: '☼',
                              title: 'Take a slower day',
                              detail: 'A book, an open window, no plans.',
                              result: '+ 9 wellbeing per day',
                            },
                          ] as const
                        ).map((a) => (
                          <Pressable
                            accessibilityRole="button"
                            accessibilityLabel={a.title}
                            key={a.id}
                            style={({ pressed }) => [
                              s.activity,
                              pressed && { backgroundColor: c.sage },
                            ]}
                            onPress={() =>
                              run(() =>
                                update(
                                  advanceLife(world!, a.id as Activity, days),
                                ),
                              )
                            }
                          >
                            <View style={s.activityIcon}>
                              <Text style={{ fontSize: 25, color: c.green }}>
                                {a.icon}
                              </Text>
                            </View>
                            <View style={{ flex: 1 }}>
                              <Text style={s.activityTitle}>{a.title}</Text>
                              <Text style={s.small}>{a.detail}</Text>
                              <Text style={s.result}>{a.result}</Text>
                            </View>
                            <Text style={{ fontSize: 22, color: c.muted }}>
                              ↗
                            </Text>
                          </Pressable>
                        ))}
                      </View>
                      <View style={s.timeRow}>
                        <Text style={s.small}>Each activity advances</Text>
                        {[1, 7, 30].map((n) => (
                          <Pressable
                            key={n}
                            accessibilityRole="button"
                            accessibilityLabel={`Advance ${n} days per activity`}
                            accessibilityState={{ selected: days === n }}
                            onPress={() => setDays(n)}
                            style={[
                              s.pace,
                              days === n && { backgroundColor: c.green },
                            ]}
                          >
                            <Text
                              style={{
                                fontSize: 12,
                                color: days === n ? c.white : c.ink,
                              }}
                            >
                              {n === 1 ? '1 day' : `${n} days`}
                            </Text>
                          </Pressable>
                        ))}
                      </View>
                      <Text style={s.small}>
                        £28 daily living costs are automatic. Study to 25
                        experience to find steady work.
                      </Text>
                    </View>
                    <View style={{ flex: 0.85, gap: 18 }}>
                      <View style={s.encounter}>
                        <GameStage mode="life" compact />
                        <View style={s.encounterBody}>
                          <Tag>A FAMILIAR FACE</Tag>
                          <Text style={s.cardTitle}>
                            Some stories find you.
                          </Text>
                          <Text style={s.cardDescription}>
                            Amelia is in town. There’s a table by the window,
                            and a conversation you’ve both been avoiding.
                          </Text>
                          <Button
                            label={
                              world!.progress.some(
                                (p) => p.storyId === reunion.id && p.completed,
                              )
                                ? 'Revisit your ending →'
                                : world!.progress.some(
                                      (p) => p.storyId === reunion.id,
                                    )
                                  ? 'Continue the conversation →'
                                  : 'Meet Amelia →'
                            }
                            onPress={openEncounter}
                          />
                        </View>
                      </View>
                      <View style={s.people}>
                        <Text style={s.eyebrow}>THE PEOPLE IN YOUR ORBIT</Text>
                        {world!.relationships.map((p, i) => (
                          <View style={s.personRow} key={p.characterId}>
                            <View
                              style={[
                                s.avatar,
                                { backgroundColor: i ? '#dfe7d7' : '#ead7cb' },
                              ]}
                            >
                              {i ? (
                                <Text style={s.avatarText}>N</Text>
                              ) : (
                                <Image
                                  source={ameliaPortrait}
                                  style={s.avatarImage}
                                  accessibilityLabel="Amelia Chen's portrait"
                                />
                              )}
                            </View>
                            <View style={{ flex: 1 }}>
                              <Text style={s.activityTitle}>
                                {i ? 'Noah Bennett' : 'Amelia Chen'}
                              </Text>
                              <Text style={s.small}>
                                {i
                                  ? 'Your first friend in the city'
                                  : 'An old friend. An unfinished chapter.'}
                              </Text>
                            </View>
                            <Text style={s.trust}>
                              {p.trust}
                              <Text style={s.small}>/100</Text>
                            </Text>
                          </View>
                        ))}
                      </View>
                    </View>
                  </View>
                </>
              ) : tab === 'stories' ? (
                <>
                  <Text style={s.title}>Enter another life.</Text>
                  <Text style={s.subtitle}>
                    Another perspective. A different possibility. Still your
                    choices.
                  </Text>
                  <View
                    style={[s.storyFeature, wide && { flexDirection: 'row' }]}
                  >
                    <View style={{ flex: 1 }}>
                      <GameStage mode="life" compact />
                    </View>
                    <View style={s.storyFeatureText}>
                      <Tag>ORIGINAL STORY · FAMILY & FRIENDSHIP</Tag>
                      <Text style={s.featureTitle}>{reunion.title}</Text>
                      <Text style={s.cardDescription}>
                        {reunion.description}
                      </Text>
                      <Text style={s.small}>
                        1 chapter · 3 endings · All choices free
                      </Text>
                      <View style={s.divider} />
                      <Text style={s.small}>
                        A separate continuity with its own memories and
                        relationships. Your main life keeps its history.
                      </Text>
                      <Button
                        label={
                          save.story
                            ? 'Resume your story →'
                            : 'Begin the story →'
                        }
                        onPress={standalone}
                      />
                      {save.story?.progress.some((p) => p.completed) && (
                        <Button
                          label="Replay in a fresh story timeline"
                          secondary
                          onPress={() => {
                            persist({
                              ...save,
                              active: 'story',
                              story: startStory(
                                createWorld(
                                  save.life.player.name,
                                  'story.reunion',
                                  save.life.player.pronouns,
                                ),
                                reunion,
                              ),
                            });
                            setSceneOpen(true);
                          }}
                        />
                      )}
                    </View>
                  </View>
                  <View style={s.infoBox}>
                    <Text style={s.sectionTitle}>
                      One universe. Many ways to live.
                    </Text>
                    <Text style={s.cardDescription}>
                      Meet Amelia through Free Life to carry the encounter into
                      your everyday world, or play independently here. Either
                      way, the world remembers.
                    </Text>
                  </View>
                  <LocalStoryLibrary onPlay={playImported} />
                </>
              ) : (
                <>
                  <Text style={s.title}>Your life, remembered.</Text>
                  <Text style={s.subtitle}>
                    Little moments. Difficult choices. The things that made a
                    difference.
                  </Text>
                  <Tag>
                    {save.active === 'life'
                      ? 'MAIN TIMELINE'
                      : 'STORY TIMELINE'}{' '}
                    · DAY {world!.day + 1}
                  </Tag>
                  <Text style={s.sectionTitle}>Shared memories</Text>
                  {world!.memories.length === 0 ? (
                    <View style={s.infoBox}>
                      <Text style={s.cardDescription}>
                        A fresh page. Meet Amelia at the café to write your
                        first shared memory.
                      </Text>
                    </View>
                  ) : (
                    world!.memories.map((m) => (
                      <View key={m.id} style={s.journalEntry}>
                        <Text style={s.eyebrow}>DAY {m.day + 1} · AMELIA</Text>
                        <Text style={s.memory}>{m.text}</Text>
                      </View>
                    ))
                  )}
                  <Text style={s.sectionTitle}>Life as it happened</Text>
                  {[...world!.history].reverse().map((e) => (
                    <View key={e.id} style={s.history}>
                      <Text style={s.eyebrow}>DAY {e.day + 1}</Text>
                      <Text style={s.cardDescription}>{e.text}</Text>
                    </View>
                  ))}
                </>
              )}
              <View style={s.footer}>
                <Text style={s.small}>YOUR PACE. YOUR POSSIBILITIES.</Text>
                <View style={s.row}>
                  <Button
                    label="Save again"
                    secondary
                    onPress={() => persist(save)}
                  />
                  {save.active === 'story' && (
                    <Button
                      label="Switch to main life"
                      secondary
                      onPress={() => {
                        persist({ ...save, active: 'life' });
                        setSceneOpen(false);
                        setTab('life');
                      }}
                    />
                  )}
                  <Button
                    label="Start a new life"
                    secondary
                    onPress={() => setReset(true)}
                  />
                </View>
              </View>
            </>
          )}
        </ScrollView>
      </View>
    </View>
  );
}
const s = StyleSheet.create({
  gameNav: {
    flexDirection: 'row',
    gap: 9,
    backgroundColor: '#121c2b',
    borderBottomColor: '#414457',
    borderBottomWidth: 1,
    paddingVertical: 11,
    paddingHorizontal: 12,
    justifyContent: 'center',
  },
  gameNavItem: {
    minHeight: 42,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#3e4557',
    borderRadius: 9,
    paddingHorizontal: 13,
    backgroundColor: '#1d293a',
  },
  gameNavSelected: {
    backgroundColor: '#4a3334',
    borderColor: '#dba46f',
  },
  gameNavText: {
    fontSize: 11,
    color: '#d9d7d8',
    fontWeight: '800',
    letterSpacing: 0.5,
  },

  speakerRow: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  speakerFallback: {
    width: 66,
    height: 78,
    borderRadius: 10,
    borderColor: '#e3a66d',
    borderWidth: 2,
    backgroundColor: '#3b3450',
    justifyContent: 'center',
    alignItems: 'center',
  },
  speakerFallbackText: { fontSize: 30, color: '#f4c892', fontWeight: '700' },
  speakerPortrait: {
    width: 66,
    height: 78,
    borderRadius: 10,
    borderColor: '#e3a66d',
    borderWidth: 2,
  },
  avatarImage: { width: 42, height: 42, borderRadius: 22 },

  stageHeadline: {
    fontFamily: serif,
    fontSize: 33,
    color: '#fff0d3',
    fontWeight: '700',
    textShadowColor: 'rgba(0,0,0,0.75)',
    textShadowRadius: 12,
    maxWidth: 560,
  },
  stageHint: {
    fontSize: 13,
    lineHeight: 20,
    color: '#f6e8df',
    maxWidth: 580,
    textShadowColor: '#000000',
    textShadowRadius: 8,
  },
  destinationRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginTop: 13,
  },
  destination: {
    minHeight: 46,
    justifyContent: 'center',
    paddingHorizontal: 14,
    borderRadius: 9,
    borderWidth: 1,
    borderColor: '#c99064',
    backgroundColor: 'rgba(9,15,25,0.88)',
  },
  destinationText: {
    color: '#fff1dc',
    letterSpacing: 0.8,
    fontSize: 11,
    fontWeight: '800',
  },

  app: { flex: 1, backgroundColor: c.paper },
  loading: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 20,
    backgroundColor: c.paper,
  },
  header: {
    height: 84,
    backgroundColor: '#101b2c',
    borderBottomWidth: 1,
    borderBottomColor: c.line,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  logo: { fontFamily: serif, fontSize: 29, color: gold, letterSpacing: -1 },
  logoSub: {
    fontSize: 8,
    letterSpacing: 2.7,
    color: c.muted,
    marginTop: 7,
    marginLeft: 26,
  },
  headerRight: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  dot: { width: 6, height: 6, borderRadius: 3, backgroundColor: c.orange },
  shell: { flex: 1 },
  sidebar: {
    padding: 24,
    paddingTop: 34,
    borderRightWidth: 1,
    borderRightColor: c.line,
  },
  nav: {
    paddingVertical: 14,
    paddingHorizontal: 14,
    borderRadius: 5,
    marginBottom: 7,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  navActive: {
    backgroundColor: '#303147',
    borderLeftWidth: 3,
    borderLeftColor: gold,
  },
  navText: { fontSize: 14, color: c.muted },
  sideNote: { marginTop: 100, padding: 7, opacity: 0.55 },
  sideQuote: {
    fontFamily: serif,
    fontSize: 22,
    lineHeight: 32,
    color: c.green,
    fontStyle: 'italic',
  },
  divider: { height: 1, backgroundColor: c.line, marginVertical: 22 },
  main: {
    flexGrow: 1,
    width: '100%',
    maxWidth: 1500,
    alignSelf: 'center',
    gap: 20,
  },
  eyebrow: {
    fontSize: 9,
    letterSpacing: 1.7,
    color: c.muted,
    fontWeight: '600',
  },
  small: { fontSize: 12, lineHeight: 19, color: c.muted },
  tag: {
    fontSize: 9,
    letterSpacing: 1.2,
    color: c.orange,
    fontWeight: '700',
    marginVertical: 6,
  },
  title: {
    fontSize: 48,
    fontFamily: serif,
    letterSpacing: -1.8,
    color: c.ink,
    marginVertical: 8,
  },
  subtitle: { fontSize: 14, lineHeight: 23, color: c.muted, maxWidth: 650 },
  topLine: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 14,
    flexWrap: 'wrap',
  },
  saveStatus: { fontSize: 11, color: c.green },
  stats: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    borderWidth: 1,
    borderColor: c.line,
    borderRadius: 6,
    backgroundColor: c.white,
    marginVertical: 8,
  },
  stat: { flex: 1, minWidth: 140, padding: 16, gap: 4 },
  statValue: { fontFamily: serif, fontSize: 34, color: gold },
  columns: { gap: 30, alignItems: 'stretch' },
  sectionHeading: { gap: 8 },
  sectionTitle: { fontFamily: serif, fontSize: 26, color: gold, marginTop: 8 },
  activities: { gap: 10 },
  activity: {
    padding: 18,
    borderWidth: 1,
    borderColor: c.line,
    borderRadius: 6,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 15,
    backgroundColor: c.white,
  },
  activityIcon: {
    width: 44,
    height: 48,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 5,
    backgroundColor: c.sage,
  },
  activityTitle: {
    fontSize: 14,
    color: c.ink,
    fontWeight: '600',
    marginBottom: 4,
  },
  result: { fontSize: 10, color: c.green, marginTop: 8 },
  timeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 9,
    flexWrap: 'wrap',
  },
  pace: {
    paddingHorizontal: 12,
    paddingVertical: 9,
    backgroundColor: c.sage,
    borderRadius: 4,
  },
  encounter: {
    backgroundColor: '#192536',
    borderWidth: 1,
    borderColor: c.line,
    borderRadius: 8,
    overflow: 'hidden',
  },
  encounterBody: { padding: 22, gap: 10 },
  cardTitle: { fontFamily: serif, fontSize: 28, color: gold },
  cardDescription: { fontSize: 13, lineHeight: 22, color: c.muted },
  button: {
    backgroundColor: c.green,
    paddingVertical: 13,
    paddingHorizontal: 17,
    borderRadius: 8,
    alignSelf: 'flex-start',
    borderWidth: 1,
    borderColor: '#dba36f',
  },
  buttonText: { fontSize: 12, color: c.white, fontWeight: '600' },
  secondary: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: c.line,
  },
  people: {
    padding: 19,
    borderWidth: 1,
    borderColor: c.line,
    borderRadius: 6,
    gap: 16,
  },
  personRow: { flexDirection: 'row', alignItems: 'center', gap: 11 },
  avatar: {
    width: 42,
    height: 42,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: { fontFamily: serif, color: c.green, fontSize: 20 },
  trust: { fontFamily: serif, color: c.ink, fontSize: 21 },
  footer: {
    marginTop: 25,
    paddingTop: 22,
    borderTopWidth: 1,
    borderTopColor: c.line,
    gap: 15,
  },
  row: { flexDirection: 'row', gap: 10, flexWrap: 'wrap' },
  onboard: {
    maxWidth: 680,
    alignSelf: 'center',
    width: '100%',
    paddingVertical: 40,
    gap: 20,
  },
  fieldLabel: { fontSize: 10, letterSpacing: 1.6, color: c.ink, marginTop: 12 },
  input: {
    borderWidth: 1,
    borderColor: c.line,
    padding: 17,
    fontSize: 18,
    color: c.ink,
    borderRadius: 5,
    backgroundColor: c.white,
  },
  alert: { padding: 16, backgroundColor: '#fae7d7', borderRadius: 5 },
  sceneLayout: { gap: 0, alignItems: 'center' },
  dialogue: {
    flex: 1,
    padding: 25,
    width: '100%',
    maxWidth: 980,
    marginTop: -35,
    zIndex: 2,
    borderWidth: 1,
    borderColor: c.line,
    backgroundColor: '#18243a',
    borderRadius: 12,
    gap: 18,
  },
  dialogueText: {
    fontFamily: serif,
    color: c.ink,
    fontSize: 25,
    lineHeight: 37,
    marginVertical: 10,
  },
  choice: {
    padding: 17,
    borderWidth: 1,
    borderColor: c.line,
    borderRadius: 10,
    backgroundColor: '#29374c',
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 10,
  },
  choiceText: { fontSize: 13, lineHeight: 21, color: c.ink, flex: 1 },
  sceneMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 10,
    flexWrap: 'wrap',
    paddingVertical: 15,
  },
  storyFeature: {
    borderWidth: 1,
    borderColor: c.line,
    backgroundColor: c.white,
    borderRadius: 8,
    overflow: 'hidden',
    marginVertical: 12,
  },
  storyFeatureText: { flex: 1, padding: 30, gap: 14 },
  featureTitle: { fontFamily: serif, fontSize: 38, color: c.ink },
  infoBox: { backgroundColor: c.sage, borderRadius: 6, padding: 24, gap: 12 },
  journalEntry: {
    padding: 24,
    backgroundColor: c.white,
    borderWidth: 1,
    borderColor: c.line,
    borderRadius: 6,
    gap: 12,
  },
  memory: { fontFamily: serif, fontSize: 22, lineHeight: 30, color: c.ink },
  history: {
    borderLeftWidth: 2,
    borderLeftColor: c.line,
    paddingLeft: 20,
    paddingVertical: 12,
    gap: 8,
  },
  cafe: {
    height: 380,
    minWidth: 250,
    backgroundColor: '#26344a',
    overflow: 'hidden',
    position: 'relative',
  },
  window: {
    position: 'absolute',
    left: '9%',
    top: 20,
    width: '58%',
    height: 177,
    backgroundColor: '#4b6179',
    borderWidth: 7,
    borderColor: '#4b3540',
    overflow: 'hidden',
  },
  sun: {
    position: 'absolute',
    top: 11,
    right: 15,
    width: 65,
    height: 65,
    borderRadius: 40,
    backgroundColor: '#f5ad73',
  },
  building: { position: 'absolute', bottom: 0 },
  windowCross: {
    position: 'absolute',
    left: '48%',
    top: 0,
    bottom: 0,
    width: 5,
    backgroundColor: '#8b8c73',
  },
  windowCrossH: {
    position: 'absolute',
    top: '50%',
    left: 0,
    right: 0,
    height: 4,
    backgroundColor: '#8b8c73',
  },
  picture: {
    position: 'absolute',
    right: 19,
    top: 70,
    width: 50,
    height: 65,
    borderWidth: 5,
    borderColor: '#817762',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#e9ddc1',
  },
  lampCord: {
    position: 'absolute',
    top: 0,
    right: '19%',
    height: 28,
    width: 2,
    backgroundColor: '#766c54',
  },
  lamp: {
    position: 'absolute',
    top: 27,
    right: '14%',
    width: 48,
    height: 22,
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
    backgroundColor: '#9b6b3f',
  },
  floor: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 75,
    backgroundColor: '#5d4b55',
  },
  plantPot: {
    position: 'absolute',
    left: 40,
    bottom: 62,
    width: 38,
    height: 44,
    backgroundColor: '#b77858',
    borderBottomLeftRadius: 11,
    borderBottomRightRadius: 11,
  },
  leaf: {
    position: 'absolute',
    width: 19,
    height: 65,
    borderRadius: 30,
    backgroundColor: '#697e5d',
  },
  person: {
    position: 'absolute',
    width: 140,
    height: 220,
    bottom: 22,
    left: '44%',
  },
  hair: {
    position: 'absolute',
    top: 3,
    left: 26,
    width: 89,
    height: 139,
    borderTopLeftRadius: 50,
    borderTopRightRadius: 45,
    borderBottomRightRadius: 15,
    backgroundColor: '#493d33',
  },
  body: {
    position: 'absolute',
    bottom: 0,
    left: 5,
    width: 132,
    height: 104,
    borderTopLeftRadius: 48,
    borderTopRightRadius: 48,
    backgroundColor: '#70806b',
  },
  neck: {
    position: 'absolute',
    top: 88,
    left: 58,
    width: 27,
    height: 37,
    backgroundColor: '#c69375',
  },
  face: {
    position: 'absolute',
    top: 22,
    left: 37,
    width: 66,
    height: 81,
    borderRadius: 29,
    backgroundColor: '#d6a381',
  },
  eye: {
    position: 'absolute',
    top: 35,
    width: 4,
    height: 3,
    borderRadius: 2,
    backgroundColor: '#4f3d33',
  },
  mouth: {
    position: 'absolute',
    top: 60,
    left: 28,
    width: 11,
    borderBottomWidth: 1,
    borderBottomColor: '#8d5b4d',
  },
  fringe: {
    position: 'absolute',
    top: 9,
    left: 30,
    width: 74,
    height: 35,
    borderTopLeftRadius: 40,
    borderTopRightRadius: 35,
    borderBottomRightRadius: 35,
    backgroundColor: '#493d33',
    transform: [{ rotate: '-13deg' }],
  },
  table: {
    position: 'absolute',
    bottom: 37,
    left: '28%',
    width: '73%',
    height: 16,
    backgroundColor: '#68424a',
    borderRadius: 30,
  },
  cup: {
    position: 'absolute',
    bottom: 53,
    left: '40%',
    width: 26,
    height: 26,
    backgroundColor: '#ecd2b1',
    borderBottomLeftRadius: 8,
    borderBottomRightRadius: 8,
  },
  cupHandle: {
    position: 'absolute',
    bottom: 60,
    left: '46%',
    width: 14,
    height: 14,
    borderWidth: 3,
    borderColor: '#ecd2b1',
    borderRadius: 9,
  },
  sceneLabel: {
    position: 'absolute',
    bottom: 13,
    left: 16,
    fontSize: 8,
    letterSpacing: 2,
    color: '#f8cd90',
  },
});
