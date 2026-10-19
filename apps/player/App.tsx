import React, { useEffect, useRef, useState } from 'react';
import {
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
  advanceCalendarMonth,
  createBirthWorld,
  performChildhoodActivity,
  skipToAge,
  type ChildhoodActivity,
  performWorldActivity,
  type WorldActivity,
  setCharacterAppearance,
  type Activity,
} from '@living/simulation-core';
import { choose, currentScene, startStory } from '@living/narrative-core';
import { loadSave, writeSave, type Save } from '@living/save-system';
import {
  DEFAULT_APPEARANCE,
  type Appearance,
  type World,
} from '@living/world-schema';
import { reunion, bookshop, firstMorning, OFFICIAL_STORIES, findOfficialStory } from '@living/content';
import { parseStory, type Story } from '@living/story-schema';
import { LOCAL_STORIES_KEY } from './src/LocalStoryLibrary';
import { LocalStoryLibrary } from './src/LocalStoryLibrary';
import { GameStage } from './src/GameStage';
import { pixelArt } from './src/pixelArt';
import { CityWorld } from './src/CityWorld';
import { ArcadePixelLife } from './src/ArcadePixelLife';
import { AvatarEditor } from './src/AvatarEditor';
import { PixelPortrait as AvatarPortrait } from './src/PixelPortrait';
import { LifeDashboard } from './src/LifeDashboard';
import { StoryPlayer } from './src/StoryPlayer';
import { gameTheme as t } from './src/gameTheme';
const c = {
  paper: t.background,
  ink: t.ink,
  muted: t.muted,
  line: t.border,
  green: t.neon,
  sage: t.panelRaised,
  orange: t.coral,
  white: t.panel,
};
const serif = t.font.display;
const gold = t.amber;
// Console-like headers and navigation, readable modern body copy.
const mono = t.font.hud;
// Same CC0 directional pixel character asset as the overworld, never a photo.
const ameliaPortrait = pixelArt.n2_down;
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
  const { width, height } = useWindowDimensions();
  const wide = width >= 1000;
  const [save, setSave] = useState<Save | null>(null);
  const latestSave = useRef<Save | null>(null);
  const scrollRef = useRef<React.ComponentRef<typeof ScrollView>>(null);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');
  const [tab, setTab] = useState<'life' | 'stories' | 'people' | 'journal'>(
    'life',
  );
  const [name, setName] = useState('Alex Morgan');
  const [pronouns, setPronouns] = useState<'they/them' | 'she/her' | 'he/him'>(
    'they/them',
  );
  const [sceneOpen, setSceneOpen] = useState(false);
  const [plannerOpen, setPlannerOpen] = useState(false);
  const [authored, setAuthored] = useState<Story>(reunion);
  const [days, setDays] = useState(1);
  const [reset, setReset] = useState(false);
  const [appearance, setAppearance] = useState<Appearance>(DEFAULT_APPEARANCE);
  const [lookDraft, setLookDraft] = useState<Appearance>(DEFAULT_APPEARANCE);
  const [editingLook, setEditingLook] = useState(false);
  const queue = useRef(Promise.resolve());
  const revision = useRef(0);
  useEffect(() => {
    let mounted = true;
    // Restore the narrative identity as well as world state. Imported story
    // content lives in the local library, not inside the authoritative save.
    // Missing/corrupted content must never overwrite or destroy a saved life.
    void loadSave(AsyncStorage)
      .then(async (value) => {
        if (!mounted) return;
        if (value) {
          latestSave.current = value;
          setSave(value);
          if (value.activeStoryId) {
            try {
              // Official stories are bundled, not user imports. Never require
              // players to re-import them merely because the app restarted.
              let active: Story | undefined = findOfficialStory(
                value.activeStoryId,
              );
              if (!active) {
                const serialized =
                  await AsyncStorage.getItem(LOCAL_STORIES_KEY);
                const untrusted: unknown = JSON.parse(serialized ?? '[]');
                if (!Array.isArray(untrusted))
                  throw new Error('Local story shelf is damaged');
                const candidate = untrusted.find(
                  (item: unknown) =>
                    typeof item === 'object' &&
                    item !== null &&
                    'id' in item &&
                    item.id === value.activeStoryId,
                );
                if (!candidate)
                  throw new Error('Imported story is no longer installed');
                active = parseStory(candidate);
              }
              if (!mounted) return;
              const timeline =
                value.active === 'life' ? value.life : value.story!;
              const progress = timeline.progress.find(
                (p) => p.storyId === active.id,
              );
              if (!progress)
                throw new Error('Saved narrative progress is missing');
              // Verify referenced scenes and story versions before displaying.
              currentScene(timeline, active);
              setAuthored(active);
              setSceneOpen(!progress.completed && !value.sceneDismissed);
              setTab('stories');
            } catch {
              if (!mounted) return;
              setSceneOpen(false);
              setTab('stories');
              setError(
                'Your saved life is safe, but its last narrative could not be restored. Re-import its original package if it was a creator story.',
              );
            }
          } else {
            const timeline =
              value.active === 'life' ? value.life : value.story!;
            const progress = timeline.progress.find(
              (p) => p.storyId === reunion.id,
            );
            setAuthored(reunion);
            setSceneOpen(
              value.active === 'story' &&
                Boolean(progress && !progress.completed),
            );
            setTab(value.active === 'story' ? 'stories' : 'life');
          }
        }
        if (mounted) setReady(true);
      })
      .catch(() => {
        if (!mounted) return;
        setError(
          'Your saved life could not be read. It has not been overwritten. Start a new life only if you want to replace it.',
        );
        setReady(true);
      });
    return () => {
      mounted = false;
    };
  }, []);
  useEffect(() => {
    // Navigation and new-character creation must not preserve an old scroll
    // offset that hides the top of the new game screen on small devices.
    scrollRef.current?.scrollTo({ y: 0, animated: false });
  }, [tab, sceneOpen, Boolean(save)]);

  function persist(next: Save) {
    latestSave.current = next;
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
    const current = latestSave.current;
    if (!current) return;
    persist(
      current.active === 'life'
        ? { ...current, life: w }
        : { ...current, story: w },
    );
  }
  // IMPORTANT: apply the operation against the newest *synchronous* world.
  // React state/JS callback closures can lag behind rapid successive taps.
  function applyWorldAction(action: (previous: World) => World) {
    run(() => {
      const current = latestSave.current;
      if (!current) return;
      const previous =
        current.active === 'life' ? current.life : current.story!;
      update(action(previous));
    });
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
    run(() => {
      const nextWorld = startStory(world!, reunion);
      setAuthored(reunion);
      persist(
        save.active === 'life'
          ? {
              ...save,
              activeStoryId: reunion.id,
              sceneDismissed: false,
              life: nextWorld,
            }
          : {
              ...save,
              activeStoryId: reunion.id,
              sceneDismissed: false,
              story: nextWorld,
            },
      );
      setSceneOpen(true);
    });
  }
  function openBookshop() {
    if (!save) return;
    run(() => {
      const reunited = save.life.progress.some(
        (p) => p.storyId === reunion.id && p.completed,
      );
      if (!reunited || save.life.day < 7)
        throw new Error(
          'Finish the reunion and spend at least a week in Bellweather first.',
        );
      const next = startStory(save.life, bookshop);
      setAuthored(bookshop);
      persist({
        ...save,
        active: 'life',
        life: next,
        activeStoryId: bookshop.id,
        sceneDismissed: false,
      });
      setTab('life');
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
            save.life.player.appearance ?? DEFAULT_APPEARANCE,
          ),
          reunion,
        );
      persist({
        ...save,
        story,
        active: 'story',
        activeStoryId: reunion.id,
        sceneDismissed: false,
      });
      setSceneOpen(true);
    });
  }
  function openOfficialStory(id: string) {
    run(() => {
      const chosen = OFFICIAL_STORIES.find(story => story.id === id);
      const current = latestSave.current;
      if (!chosen || !current) throw new Error('Story is unavailable.');
      const prior = current.life.progress.find(p => p.storyId === id);
      if (prior?.completed) throw new Error('This story is already completed in your life.');
      const next = startStory(current.life, chosen);
      setAuthored(chosen);
      persist({
        ...current, active: 'life', life: next,
        activeStoryId: chosen.id, sceneDismissed: false,
      });
      setTab('life');
      setSceneOpen(true);
    });
  }
  function newLife() {
    setAuthored(reunion);
    run(() => {
      const born = createBirthWorld(name, 'main-' + Date.now().toString(36), pronouns, appearance);
      const opening = startStory(born, firstMorning);
      setAuthored(firstMorning);
      persist({
        version: 1,
        active: 'life',
        life: opening,
        story: null,
        activeStoryId: firstMorning.id,
        sceneDismissed: false,
      });
      setReset(false);
      setTab('life');
      setSceneOpen(true);
    });
  }
  function playImported(story: Story) {
    if (!save) return;
    run(() => {
      const started = startStory(save.life, story);
      setAuthored(story);
      persist({
        ...save,
        active: 'life',
        life: started,
        activeStoryId: story.id,
        sceneDismissed: false,
      });
      setTab('life');
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
  // Keep authored story scenes inside the SAME Free Life gameplay session.
  // The world stays mounted behind the conversation; clock and movement pause.
  if (save && !reset && save.active === 'life' && tab === 'life') {
    return (
      <View style={{ width, height, backgroundColor: '#151c26' }}>
        <ArcadePixelLife
          world={save.life}
          paused={sceneOpen}
          onTalk={openEncounter}
          onStoryStart={openOfficialStory}
          onAdvanceMonth={() => applyWorldAction(advanceCalendarMonth)}
          onChildAction={(activity: ChildhoodActivity, offset: number) =>
            applyWorldAction((w) => performChildhoodActivity(w, activity, offset))}
          onSkipChildhood={(years: 2 | 5 | 13 | 18) =>
            applyWorldAction((w) => skipToAge(w, years))}
          onActivity={(activity: WorldActivity, dayOffset: number) =>
            applyWorldAction((w) => performWorldActivity(w, activity, dayOffset))}
          onNavigate={(destination) => setTab(destination)}
        />
        {sceneOpen ? (
          <View style={{ position: 'absolute', left: 0, right: 0, top: 0, bottom: 0,
            backgroundColor: '#131421f2' }}>
            <ScrollView contentContainerStyle={{ padding: 8, paddingBottom: 32 }}>
              <StoryPlayer
                world={save.life}
                story={authored}
                integrated
                onChoose={(choiceId) =>
                  applyWorldAction((w) => choose(w, authored, choiceId))
                }
                onClose={() => {
                  const current = latestSave.current;
                  if (current) persist({ ...current, sceneDismissed: true });
                  setSceneOpen(false);
                }}
                onFinish={() => {
                  setSceneOpen(false);
                  setTab('life');
                }}
              />
            </ScrollView>
          </View>
        ) : null}
      </View>
    );
  }
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
              { id: 'people', symbol: '♡', title: 'PEOPLE' },
              { id: 'journal', symbol: '◷', title: 'MEMORIES' },
            ] as const
          ).map((entry) => (
            <Pressable
              key={entry.id}
              accessibilityRole="tab"
              accessibilityState={{ selected: tab === entry.id }}
              accessibilityLabel={entry.title}
              onPress={() => {
                if (sceneOpen && save)
                  persist({ ...save, sceneDismissed: true });
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
          ref={scrollRef}
          contentContainerStyle={[s.main, { padding: wide ? 40 : 22 }]}
        >
          {error !== '' && (
            <View accessibilityRole="alert" style={s.alert}>
              <Text>{error}</Text>
            </View>
          )}
          {!save || reset ? (
            <View style={s.onboard}>
              <GameStage mode="story" compact>
                <Text style={s.stageHeadline}>
                  The life you live is the story you make.
                </Text>
                <Text style={s.stageHint}>
                  A new city. A familiar face. A million things that haven't
                  happened yet.
                </Text>
              </GameStage>
              <Tag>CHAPTER ZERO</Tag>
              <Text style={s.title}>
                A life worth{wide ? '\n' : ' '}remembering.
              </Text>
              <Text style={s.subtitle}>
                You will be born in Bellweather. Grow from infancy into childhood,
                choose your own path through school and adulthood, and build
                a life whose relationships and memories actually matter.
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
              <AvatarEditor
                appearance={appearance}
                onChange={setAppearance}
                heading="Choose how you look."
              />
              <View style={s.row}>
                <Button
                  label={
                    reset
                      ? 'Create new life & replace save →'
                      : 'Begin at birth →'
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
                      : tab === 'people'
                        ? 'PEOPLE & CONSEQUENCES'
                        : 'THE THINGS THAT STAY'}
                </Text>
                <Text accessibilityLiveRegion="polite" style={s.saveStatus}>
                  {status || 'Saved on this device'}
                </Text>
              </View>
              {sceneOpen ? (
                <StoryPlayer
                  world={world!}
                  story={authored}
                  integrated={save.active === 'life'}
                  onChoose={(choiceId) =>
                    applyWorldAction((w) => choose(w, authored, choiceId))
                  }
                  onClose={() => {
                    const current = latestSave.current;
                    if (current) persist({ ...current, sceneDismissed: true });
                    setSceneOpen(false);
                  }}
                  onFinish={() => {
                    setSceneOpen(false);
                    setTab('life');
                  }}
                />
              ) : tab === 'life' ? (
                <>
                  <View style={s.topLine}>
                    <View>
                      <Text style={s.title}>
                        {world!.day === 0
                          ? 'A new beginning.'
                          : 'A little more life.'}
                      </Text>
                      <View style={s.lifeIdentity}>
                        <AvatarPortrait
                          appearance={world!.player.appearance}
                          size={87}
                        />
                        <View style={{ flex: 1, gap: 4 }}>
                          <Text style={s.subtitle}>
                            {world!.player.name} · Age{' '}
                            {Math.floor(world!.player.ageDays / 365)} ·
                            Bellweather
                          </Text>
                          <Text style={s.small}>
                            YOUR STORY. YOUR LOOK. YOUR CHOICES.
                          </Text>
                        </View>
                      </View>
                    </View>
                    <Tag>
                      {save.active === 'story'
                        ? 'STORY CONTINUITY'
                        : 'MAIN TIMELINE'}
                    </Tag>
                  </View>
                  <LifeDashboard world={world!} onAction={applyWorldAction} />
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
                              : applyWorldAction((w) =>
                                  advanceLife(w, dest.action as Activity, days),
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
                  <CityWorld world={world!} onAction={applyWorldAction} onTalk={openEncounter} />
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
                  <View style={s.timeRow}>
                    <Text style={s.small}>SIMULATE</Text>
                    {[1, 7, 30].map((n) => (
                      <Pressable
                        key={n}
                        accessibilityRole="button"
                        accessibilityLabel={`Advance ${n} days per activity`}
                        accessibilityState={{ selected: days === n }}
                        onPress={() => setDays(n)}
                        style={[s.pace, days === n && s.paceActive]}
                      >
                        <Text
                          style={[
                            s.paceText,
                            days === n && { color: '#fff4df' },
                          ]}
                        >
                          {n === 1 ? 'One day' : `${n} days`}
                        </Text>
                      </Pressable>
                    ))}
                    <Text style={s.small}>
                      No energy timers. You set the pace.
                    </Text>
                  </View>
                  <Pressable
                    accessibilityRole="button"
                    accessibilityState={{ expanded: plannerOpen }}
                    onPress={() => setPlannerOpen((p) => !p)}
                    style={s.plannerToggle}
                  >
                    <Text style={s.plannerToggleText}>
                      {plannerOpen
                        ? '− CLOSE LIFE PLANNER'
                        : '+ OPEN LIFE PLANNER & RELATIONSHIPS'}
                    </Text>
                    <Text style={s.plannerToggleText}>
                      {plannerOpen ? '⌃' : '⌄'}
                    </Text>
                  </Pressable>
                  {plannerOpen && (
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
                                  (p) =>
                                    p.storyId === reunion.id && p.completed,
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
                          <Text style={s.eyebrow}>
                            THE PEOPLE IN YOUR ORBIT
                          </Text>
                          {world!.relationships.map((p, i) => (
                            <View style={s.personRow} key={p.characterId}>
                              <View
                                style={[
                                  s.avatar,
                                  {
                                    backgroundColor: i ? '#dfe7d7' : '#ead7cb',
                                  },
                                ]}
                              >
                                {i ? (
                                  <Text style={s.avatarText}>N</Text>
                                ) : (
                                  <Image
                                    source={ameliaPortrait}
                                    resizeMode="contain"
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
                  )}
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
                  <View style={s.bookshopFeature}>
                    <View style={{ flex: 1, gap: 7 }}>
                      <Tag>ORIGINAL STORY · CHAPTER TWO</Tag>
                      <Text style={s.cardTitle}>{bookshop.title}</Text>
                      <Text style={s.cardDescription}>
                        {bookshop.description}
                      </Text>
                      <Text style={s.small}>
                        11 illustrated narrative scenes · 3 endings · choices
                        free
                      </Text>
                      <Text style={s.small}>
                        Compatible with the main Free Life timeline; it
                        remembers your earlier reunion.
                      </Text>
                    </View>
                    <View style={{ justifyContent: 'center', gap: 8 }}>
                      <Button
                        label={
                          save.life.progress.some(
                            (p) => p.storyId === bookshop.id,
                          )
                            ? 'Continue the bookshop →'
                            : 'Enter the bookshop →'
                        }
                        disabled={
                          !save.life.progress.some(
                            (p) => p.storyId === reunion.id && p.completed,
                          ) || save.life.day < 7
                        }
                        onPress={openBookshop}
                      />
                      {(!save.life.progress.some(
                        (p) => p.storyId === reunion.id && p.completed,
                      ) ||
                        save.life.day < 7) && (
                        <Text style={s.small}>
                          Unlock naturally: complete the reunion and spend 7
                          days in Bellweather.
                        </Text>
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
                  <LocalStoryLibrary
                    onPlay={playImported}
                    protectedIds={[
                      ...save.life.progress.map((p) => p.storyId),
                      ...(save.story?.progress.map((p) => p.storyId) ?? []),
                    ]}
                  />
                </>
              ) : tab === 'people' ? (
                <>
                  <Text style={s.title}>Your people. Your history.</Text>
                  <View style={s.playerProfile}>
                    <AvatarPortrait
                      appearance={world!.player.appearance}
                      size={117}
                    />
                    <View style={{ flex: 1, gap: 8 }}>
                      <Text style={s.cardTitle}>{world!.player.name}</Text>
                      <Text style={s.small}>
                        This is your character. Appearance is not tied to stats
                        or gender.
                      </Text>
                      <Button
                        label={
                          editingLook
                            ? 'Close appearance editor'
                            : '✦ Customize my look'
                        }
                        onPress={() => {
                          if (!editingLook)
                            setLookDraft(
                              world!.player.appearance ?? DEFAULT_APPEARANCE,
                            );
                          setEditingLook(!editingLook);
                        }}
                      />
                    </View>
                  </View>
                  {editingLook && (
                    <View style={s.lookPanel}>
                      <AvatarEditor
                        appearance={lookDraft}
                        onChange={setLookDraft}
                        heading="Your look, your rules."
                        compact
                      />
                      <View style={s.row}>
                        <Button
                          label="Save appearance ✓"
                          onPress={() => {
                            run(() => {
                              update(setCharacterAppearance(world!, lookDraft));
                              setEditingLook(false);
                            });
                          }}
                        />
                        <Button
                          label="Cancel"
                          secondary
                          onPress={() => setEditingLook(false)}
                        />
                      </View>
                    </View>
                  )}
                  <Text style={s.subtitle}>
                    Relationships change as life goes on. People remember what
                    you said, and whether you made time for them.
                  </Text>
                  <View style={s.peopleGallery}>
                    {world!.relationships.map((friend) => {
                      const amelia = friend.characterId === 'amelia';
                      const name = amelia ? 'Amelia Chen' : 'Noah Bennett';
                      const memories = world!.memories.filter(
                        (memory) => memory.subject === friend.characterId,
                      );
                      const npc = world!.npcLives?.find(
                        (person) => person.characterId === friend.characterId,
                      );
                      return (
                        <View key={friend.characterId} style={s.profileCard}>
                          <View style={s.profileTop}>
                            {amelia ? (
                              <Image
                                source={ameliaPortrait}
                                resizeMode="contain"
                                style={s.profilePortrait}
                                accessibilityLabel="Amelia Chen's illustrated portrait"
                              />
                            ) : (
                              <View style={s.profileUnknown}>
                                <Text style={s.profileUnknownText}>N</Text>
                              </View>
                            )}
                            <View style={{ flex: 1, gap: 5 }}>
                              <Text style={s.cardTitle}>{name}</Text>
                              <Text style={s.small}>
                                {amelia
                                  ? 'An old friend with unfinished history'
                                  : 'Your first friend in Bellweather'}
                              </Text>
                              {npc && (
                                <>
                                  <Text style={s.eyebrow}>
                                    {npc.occupation.toUpperCase()} ·{' '}
                                    {npc.mood.toUpperCase()}
                                  </Text>
                                  <Text style={s.small}>
                                    Currently: {npc.currentGoal}
                                  </Text>
                                </>
                              )}
                              <Text style={s.eyebrow}>
                                LAST SPOKEN · DAY {friend.lastContactDay + 1}
                              </Text>
                            </View>
                          </View>
                          <View style={s.trustHeading}>
                            <Text style={s.eyebrow}>TRUST</Text>
                            <Text style={s.trust}>{friend.trust}/100</Text>
                          </View>
                          <View
                            style={s.trustTrack}
                            accessibilityLabel={`${name} trust ${friend.trust} out of 100`}
                          >
                            <View
                              style={[
                                s.trustFill,
                                { width: `${friend.trust}%` },
                              ]}
                            />
                          </View>
                          <Text style={s.small}>
                            {memories.length === 0
                              ? 'No shared story memories yet.'
                              : `${memories.length} remembered moment${memories.length === 1 ? '' : 's'}`}
                          </Text>
                          {npc && npc.milestones.length > 0 && (
                            <View style={s.npcMilestones}>
                              <Text style={s.eyebrow}>
                                LIFE OUTSIDE YOUR OWN
                              </Text>
                              {npc.milestones.slice(-3).map((item) => (
                                <Text key={item} style={s.small}>
                                  ✦ {item.replaceAll('_', ' ')}
                                </Text>
                              ))}
                            </View>
                          )}
                          <Button
                            label={
                              amelia
                                ? 'Meet at the café →'
                                : 'Spend time together →'
                            }
                            onPress={() =>
                              amelia
                                ? openEncounter()
                                : run(() =>
                                    update(
                                      advanceLife(world!, 'socialize', days),
                                    ),
                                  )
                            }
                          />
                        </View>
                      );
                    })}
                  </View>
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
  lifeIdentity: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: 12,
  },
  playerProfile: {
    flexDirection: 'row',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: 14,
    borderWidth: 1,
    borderColor: t.border,
    backgroundColor: t.panel,
    borderRadius: 13,
    padding: 12,
  },
  lookPanel: {
    borderRadius: 14,
    borderWidth: 1,
    borderColor: t.border,
    backgroundColor: t.background,
    padding: 14,
    gap: 16,
  },
  storyActors: {
    alignSelf: 'center',
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'space-between',
    width: '100%',
    maxWidth: 510,
    minHeight: 150,
    marginBottom: 10,
  },
  npcActor: {
    width: 130,
    height: 142,
    backgroundColor: '#1a2a3dcc',
    borderWidth: 2,
    borderColor: '#d5a97d',
    borderRadius: 60,
    overflow: 'hidden',
    justifyContent: 'center',
    alignItems: 'center',
  },
  npcActorImage: { width: 128, height: 140, resizeMode: 'cover' },

  npcMilestones: {
    padding: 12,
    borderRadius: 9,
    backgroundColor: t.panelRaised,
    gap: 5,
  },

  bookshopFeature: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 18,
    padding: 23,
    borderRadius: 13,
    borderWidth: 1,
    backgroundColor: t.panel,
    borderColor: t.border,
  },

  peopleGallery: { flexDirection: 'row', flexWrap: 'wrap', gap: 17 },
  profileCard: {
    flexGrow: 1,
    flexBasis: 280,
    maxWidth: 620,
    backgroundColor: '#1c293d',
    borderRadius: 13,
    borderWidth: 1,
    borderColor: t.border,
    padding: 18,
    gap: 14,
  },
  profileTop: { flexDirection: 'row', alignItems: 'center', gap: 16 },
  profilePortrait: {
    width: 95,
    height: 112,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#c38c68',
  },
  profileUnknown: {
    width: 95,
    height: 112,
    backgroundColor: '#3e4659',
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  profileUnknownText: { fontFamily: serif, color: t.amber, fontSize: 50 },
  trustHeading: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  trustTrack: {
    height: 8,
    backgroundColor: '#0c1729',
    borderRadius: 9,
    overflow: 'hidden',
  },
  trustFill: { height: '100%', backgroundColor: t.neon, borderRadius: 9 },

  paceActive: {
    backgroundColor: t.neonDeep,
    borderColor: t.neon,
    borderWidth: 1,
  },
  paceText: { color: '#cfdae5', fontSize: 12, fontWeight: '700' },
  plannerToggle: {
    minHeight: 50,
    paddingHorizontal: 17,
    paddingVertical: 12,
    borderRadius: 11,
    borderWidth: 1,
    borderColor: t.border,
    backgroundColor: t.panel,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 12,
  },
  plannerToggleText: {
    color: t.amber,
    fontSize: 12,
    fontWeight: '800',
    letterSpacing: 1,
  },

  gameNav: {
    flexDirection: 'row',
    gap: 5,
    maxWidth: 900,
    alignSelf: 'center',
    backgroundColor: '#121c2b',
    borderBottomColor: t.border,
    borderBottomWidth: 1,
    paddingVertical: 11,
    paddingHorizontal: 6,
    justifyContent: 'space-between',
    width: '100%',
  },
  gameNavItem: {
    minHeight: 44,
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: t.border,
    borderRadius: 5,
    paddingHorizontal: 3,
    backgroundColor: t.panel,
  },
  gameNavSelected: {
    backgroundColor: t.neonDeep,
    borderColor: t.neon,
  },
  gameNavText: {
    fontFamily: mono,
    fontSize: 10,
    color: '#d9d7d8',
    fontWeight: '800',
    letterSpacing: 0,
    textAlign: 'center',
  },

  speakerRow: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  speakerFallback: {
    width: 66,
    height: 78,
    borderRadius: 10,
    borderColor: t.amber,
    borderWidth: 2,
    backgroundColor: '#3b3450',
    justifyContent: 'center',
    alignItems: 'center',
  },
  speakerFallbackText: { fontSize: 30, color: t.amber, fontWeight: '700' },
  speakerPortrait: {
    width: 66,
    height: 78,
    borderRadius: 10,
    borderColor: t.amber,
    borderWidth: 2,
  },
  avatarImage: { width: 42, height: 42, borderRadius: 22 },

  stageHeadline: {
    fontFamily: serif,
    fontSize: 33,
    color: t.ink,
    fontWeight: '700',
    textShadowColor: 'rgba(0,0,0,0.75)',
    textShadowRadius: 12,
    maxWidth: 560,
  },
  stageHint: {
    fontSize: 13,
    lineHeight: 20,
    color: t.ink,
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
    borderColor: t.border,
    backgroundColor: 'rgba(9,15,25,0.88)',
  },
  destinationText: {
    color: t.ink,
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
    backgroundColor: t.background,
    borderBottomWidth: 1,
    borderBottomColor: c.line,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  logo: { fontFamily: serif, fontSize: 32, color: t.neon, letterSpacing: 1 },
  logoSub: {
    fontFamily: mono,
    fontSize: 8,
    letterSpacing: 1.6,
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
    backgroundColor: t.panelRaised,
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
    fontFamily: mono,
    fontSize: 10,
    letterSpacing: 1.7,
    color: c.muted,
    fontWeight: '600',
  },
  small: { fontSize: 12, lineHeight: 19, color: c.muted },
  tag: {
    fontFamily: mono,
    fontSize: 9,
    letterSpacing: 1.2,
    color: c.orange,
    fontWeight: '700',
    marginVertical: 6,
  },
  title: {
    fontSize: 43,
    fontFamily: serif,
    letterSpacing: 0.2,
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
    borderColor: t.border,
    borderRadius: 12,
    backgroundColor: t.background,
    marginVertical: 8,
  },
  stat: { flex: 1, minWidth: 140, padding: 16, gap: 4 },
  statValue: { fontFamily: serif, fontSize: 25, color: gold },
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
    backgroundColor: t.panel,
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
    borderColor: t.neon,
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
  alert: { padding: 16, backgroundColor: t.panelRaised, borderRadius: 5 },
  sceneLayout: { gap: 0, alignItems: 'center', width: '100%' },
  dialogue: {
    flex: 1,
    padding: 25,
    width: '100%',
    maxWidth: 980,
    marginTop: -35,
    zIndex: 2,
    borderWidth: 1,
    borderColor: c.line,
    backgroundColor: t.panel,
    borderRadius: 12,
    gap: 18,
  },
  dialogueText: {
    fontFamily: t.font.body,
    color: c.ink,
    fontSize: 23,
    lineHeight: 34,
    marginVertical: 10,
  },
  choice: {
    padding: 17,
    borderWidth: 1,
    borderColor: c.line,
    borderRadius: 10,
    backgroundColor: t.panelRaised,
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
