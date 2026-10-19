import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Animated, Image, Platform, Pressable, ScrollView, StyleSheet, Text,
  TextInput, View, useWindowDimensions,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { World } from '@living/world-schema';
import { pixelArt, actorArt, type PixelArtKey } from './pixelArt';
import {
  INITIAL_POSITION, STREET_WIDTH, STREET_HEIGHT, CAFE_WIDTH, CAFE_HEIGHT,
  npcAt, pixelCell, validPixelPosition,
  type Facing, type PixelPlace, type PixelPosition,
} from './pixelTownLogic';

/**
 * LIVEIT's mobile-first playable screen.
 *
 * The background is a static batch of pixel tiles. Only two Animated transforms
 * change every animation frame: the camera and the player's sprite. React state,
 * disk writes, NPC inference and timeline transitions NEVER run at frame rate.
 * This keeps touch and keyboard input independent of the visible world refresh.
 */
const TILE = 48;
const SPEED = 3.5;             // tiles per second, independent of monitor Hz
const MONTH_MS = 60 * 60 * 1000; // one real gameplay hour = 30 simulated days
const COLORS = {
  ink: '#fff4d6', dim: '#c4d8c9', brown: '#261a23',
  panel: '#211e30ee', border: '#d7a66b', gold: '#ffc678',
  coral: '#f99073', grass: '#648b73', green: '#b3e3ba',
};
type Point = { x: number; y: number };
type Message = { speaker: 'player' | 'npc'; text: string };
type Mission = { id: string; title: string; description: string; createdAge: number; completed: boolean };

function safeText(text: string): string {
  return text.trim().slice(0, 500);
}
function npcFallback(text: string, player: string): string {
  const query = text.toLowerCase();
  if (/work|job|money|rent|career/.test(query))
    return 'Bellweather has opportunity, but not every job is worth your time. What kind of work would make you proud, ' + player + '?';
  if (/friend|lonely|love|relationship|date/.test(query))
    return 'I have seen friendships begin with a tiny conversation like this. Tell me what you actually need from someone.';
  if (/story|mission|quest|adventure/.test(query))
    return 'A story does not have to happen somewhere else. We can make a promise, visit a place, or change a life right here. What would you want to do?';
  if (/hello|hi|hey|morning|evening/.test(query))
    return 'Hey, ' + player + '. The market feels different today. What is on your mind?';
  return 'I am listening. Tell me more about that, or ask me something about our lives here.';
}
function validMission(x: unknown): x is Mission {
  if (!x || typeof x !== 'object') return false;
  const m = x as Partial<Mission>;
  return typeof m.id === 'string' && typeof m.title === 'string' &&
    typeof m.description === 'string' && typeof m.createdAge === 'number' &&
    typeof m.completed === 'boolean';
}

/**
 * Web Ollama talks to the computer running this browser. On actual phones use
 * your Mac's LAN address instead of "localhost". No cloud model is involved.
 * Generated text is intentionally NEVER allowed to mutate authoritative saves.
 */
async function npcFromLocalModel(
  endpoint: string, history: Message[], player: string, month: number,
): Promise<string> {
  const url = endpoint.trim().replace(/\/+$/, '') + '/api/chat';
  if (!/^https?:\/\//i.test(url)) throw Error('Invalid local Ollama URL');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 14000);
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
      body: JSON.stringify({
        model: 'qwen3:0.6b',
        stream: false,
        think: false,
        options: { temperature: 0.75, num_predict: 180 },
        messages: [
          {
            role: 'system',
            content: 'You are Amelia, a believable 24-year-old inhabitant of Bellweather, a contemporary town. You have your own plans, feelings and memory. You are talking directly to ' + player +
              ', who is age ' + month + ' months. Speak naturally in 1–4 sentences. Carry the conversation forward, ask useful follow-up questions and remember recent context. Never claim to have completed a quest, paid money, changed health or edited the game. No stage directions, no /think, no system messages.',
          },
          ...history.slice(-16).map(item => ({
            role: item.speaker === 'player' ? 'user' : 'assistant',
            content: item.text,
          })),
        ],
      }),
    });
    if (!response.ok) throw Error('Model HTTP ' + response.status);
    const data: unknown = await response.json();
    const content = (data as { message?: { content?: unknown } }).message?.content;
    if (typeof content !== 'string' || !content.trim()) throw Error('No model reply');
    return content.replace(/<think>[\s\S]*?<\/think>/g, '').trim().slice(0, 900);
  } finally {
    clearTimeout(timer);
  }
}

export function ArcadePixelLife({
  world, onTalk, onAdvanceMonth, onNavigate,
}: {
  world: World;
  onTalk: () => void;
  onAdvanceMonth: () => void;
  onNavigate: (where: 'stories' | 'people' | 'journal' | 'life') => void;
}) {
  const { width, height } = useWindowDimensions();
  const [size, setSize] = useState({ width, height });
  const [place, setPlace] = useState<PixelPlace>('street');
  const [facing, setFacing] = useState<Facing>('down');
  const [clock, setClock] = useState(0);
  const [notice, setNotice] = useState('Walk up to Amelia and press TALK. Explore the market and café.');
  const [panel, setPanel] = useState<'none' | 'talk' | 'missions' | 'settings'>('none');
  const [messages, setMessages] = useState<Message[]>([]);
  const [draft, setDraft] = useState('');
  const [missionTitle, setMissionTitle] = useState('');
  const [missionDescription, setMissionDescription] = useState('');
  const [missions, setMissions] = useState<Mission[]>([]);
  const [endpoint, setEndpoint] = useState('http://localhost:11434');
  const [modelMode, setModelMode] = useState<'authored' | 'local'>('authored');
  const [waiting, setWaiting] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [movement, setMovement] = useState<Point>({ x: 0, y: 0 });
  const walkVector = useRef<Point>({ x: 0, y: 0 });
  const keys = useRef(new Set<string>());
  const hero = useRef({ x: INITIAL_POSITION.x, y: INITIAL_POSITION.y, place: INITIAL_POSITION.place });
  const pose = useRef(new Animated.ValueXY()).current;
  const camera = useRef(new Animated.ValueXY()).current;
  const bob = useRef(new Animated.Value(0)).current;
  const glow = useRef(new Animated.Value(0.1)).current;
  const clockRef = useRef(0);
  const monthRef = useRef(onAdvanceMonth);
  monthRef.current = onAdvanceMonth;
  const chatRef = useRef(messages);
  chatRef.current = messages;
  const busyRef = useRef(false);
  const gameKey = 'liveit.arcade.v1.' + world.timelineId;

  // Per-life progression and conversations are separate from the strict
  // world schema. Existing saves therefore remain loadable without migration.
  useEffect(() => {
    let active = true;
    setLoaded(false);
    Promise.all([
      AsyncStorage.getItem(gameKey + '.location'),
      AsyncStorage.getItem(gameKey + '.elapsed'),
      AsyncStorage.getItem(gameKey + '.chat'),
      AsyncStorage.getItem(gameKey + '.missions'),
      AsyncStorage.getItem('liveit.localOllamaEndpoint'),
    ]).then(([location, elapsed, transcript, quests, customEndpoint]) => {
      if (!active) return;
      try {
        const p: unknown = location ? JSON.parse(location) : INITIAL_POSITION;
        if (validPixelPosition(p)) {
          hero.current = { x: p.x, y: p.y, place: p.place };
          setPlace(p.place);
          setFacing(p.facing);
        }
      } catch { /* Keep valid fallback and never damage world save. */ }
      const progress = Number(elapsed);
      clockRef.current = Number.isFinite(progress) && progress >= 0
        ? Math.min(progress, MONTH_MS - 1) : 0;
      setClock(clockRef.current);
      try {
        const saved: unknown = transcript ? JSON.parse(transcript) : [];
        if (Array.isArray(saved)) {
          setMessages(saved.filter((m): m is Message =>
            m !== null && typeof m === 'object' &&
            (m.speaker === 'npc' || m.speaker === 'player') &&
            typeof m.text === 'string').slice(-80));
        }
      } catch { /* No conversation history yet. */ }
      try {
        const saved: unknown = quests ? JSON.parse(quests) : [];
        if (Array.isArray(saved)) setMissions(saved.filter(validMission).slice(-60));
      } catch { /* No created missions yet. */ }
      if (customEndpoint) setEndpoint(customEndpoint);
      setLoaded(true);
    }).catch(() => setLoaded(true));
    return () => { active = false; };
  }, [gameKey]);

  useEffect(() => {
    if (!loaded) return;
    void AsyncStorage.setItem(gameKey + '.chat', JSON.stringify(messages.slice(-80))).catch(() => {});
  }, [gameKey, loaded, messages]);
  useEffect(() => {
    if (!loaded) return;
    void AsyncStorage.setItem(gameKey + '.missions', JSON.stringify(missions.slice(-60))).catch(() => {});
  }, [gameKey, loaded, missions]);

  const isNearNpc = useCallback(() => {
    const npc = npcAt(hero.current.place);
    return Math.hypot(hero.current.x - npc.x, hero.current.y - npc.y) <= 1.8;
  }, []);
  const startChat = useCallback(() => {
    if (!isNearNpc()) {
      setNotice('Move near Amelia to begin a conversation.');
      return;
    }
    setPanel('talk');
    if (chatRef.current.length === 0) setMessages([{
      speaker: 'npc',
      text: 'Oh, hey! I thought I recognized you. How have you been?',
    }]);
  }, [isNearNpc]);

  const submit = useCallback(async (suggested?: string) => {
    const sentence = safeText(suggested ?? draft);
    if (!sentence || busyRef.current) return;
    const updated = [...chatRef.current, { speaker: 'player' as const, text: sentence }];
    chatRef.current = updated;
    setMessages(updated);
    setDraft('');
    busyRef.current = true;
    setWaiting(true);
    let reply = '';
    let connected = false;
    try {
      reply = await npcFromLocalModel(endpoint, updated, world.player.name,
        Math.floor(world.player.ageDays / 30));
      connected = true;
    } catch {
      reply = npcFallback(sentence, world.player.name);
    }
    setModelMode(connected ? 'local' : 'authored');
    setMessages(existing => [...existing, { speaker: 'npc' as const, text: reply }].slice(-80));
    busyRef.current = false;
    setWaiting(false);
  }, [draft, endpoint, world.player.ageDays, world.player.name]);

  // No setState inside the 60/120 Hz world loop. The movement animation and
  // following camera remain smooth even if no React component re-renders.
  useEffect(() => {
    if (!loaded || panel !== 'none') return;
    let active = true;
    let frame = 0;
    let last = 0;
    let lastUi = 0;
    let lastSave = 0;
    let lastClockSave = 0;
    const blocks = (x: number, y: number) => {
      const p = hero.current.place;
      const cx = Math.floor(x + 0.5);
      const cy = Math.floor(y + 0.5);
      const n = npcAt(p);
      return pixelCell(p, cx, cy).solid || (n.x === cx && n.y === cy);
    };
    const render = (timestamp: number) => {
      if (!active) return;
      const dt = last ? Math.min((timestamp - last) / 1000, 0.05) : 0;
      last = timestamp;
      const p = hero.current;
      const pad = walkVector.current;
      const vx = Number(keys.current.has('ArrowRight') || keys.current.has('KeyD')) -
        Number(keys.current.has('ArrowLeft') || keys.current.has('KeyA')) + pad.x;
      const vy = Number(keys.current.has('ArrowDown') || keys.current.has('KeyS')) -
        Number(keys.current.has('ArrowUp') || keys.current.has('KeyW')) + pad.y;
      const magnitude = Math.hypot(vx, vy);
      if (magnitude > 0) {
        const dx = (vx / magnitude) * dt * SPEED;
        const dy = (vy / magnitude) * dt * SPEED;
        if (!blocks(p.x + dx, p.y)) p.x += dx;
        if (!blocks(p.x, p.y + dy)) p.y += dy;
        const nextFacing: Facing = Math.abs(vx) > Math.abs(vy)
          ? vx > 0 ? 'right' : 'left' : vy > 0 ? 'down' : 'up';
        setFacing(previous => previous === nextFacing ? previous : nextFacing);
        bob.setValue(Math.sin(timestamp / 70) * 2);
      } else {
        bob.setValue(Math.sin(timestamp / 440) * 0.7);
      }
      // Portal transitions need to be detected by entering a tile, not by
      // colliding with the café's solid façade.
      const terrain = pixelCell(p.place, Math.floor(p.x + 0.5), Math.floor(p.y + 0.5));
      if (terrain.portal === 'cafe') {
        p.place = 'cafe'; p.x = 5; p.y = 8;
        setPlace('cafe'); setNotice('The café smells of coffee and rain.');
      } else if (terrain.portal === 'street') {
        p.place = 'street'; p.x = 5; p.y = 7;
        setPlace('street'); setNotice('Back in Bellweather market.');
      }
      pose.setValue({ x: p.x * TILE, y: p.y * TILE });
      const worldWidth = (p.place === 'street' ? STREET_WIDTH : CAFE_WIDTH) * TILE;
      const worldHeight = (p.place === 'street' ? STREET_HEIGHT : CAFE_HEIGHT) * TILE;
      const cameraX = Math.min(0, Math.max(size.width - worldWidth,
        size.width / 2 - (p.x + 0.5) * TILE));
      const cameraY = Math.min(0, Math.max(size.height - worldHeight,
        size.height / 2 - (p.y + 0.5) * TILE));
      camera.setValue({ x: cameraX, y: cameraY });
      if (dt > 0) {
        clockRef.current += dt * 1000;
        if (clockRef.current >= MONTH_MS) {
          clockRef.current -= MONTH_MS;
          monthRef.current();
        }
      }
      if (timestamp - lastUi > 1000) {
        setClock(clockRef.current);
        glow.setValue(0.04 + 0.19 * Math.pow(Math.sin(Math.PI * clockRef.current / MONTH_MS), 2));
        lastUi = timestamp;
      }
      if (timestamp - lastSave > 2200) {
        const facingNow: Facing = magnitude > 0
          ? Math.abs(vx) > Math.abs(vy) ? vx > 0 ? 'right' : 'left' : vy > 0 ? 'down' : 'up'
          : 'down';
        const coord: PixelPosition = {
          place: p.place, x: Math.round(p.x), y: Math.round(p.y),
          facing: facingNow,
        };
        if (validPixelPosition(coord))
          void AsyncStorage.setItem(gameKey + '.location', JSON.stringify(coord)).catch(() => {});
        lastSave = timestamp;
      }
      if (timestamp - lastClockSave > 5500) {
        void AsyncStorage.setItem(gameKey + '.elapsed', String(clockRef.current)).catch(() => {});
        lastClockSave = timestamp;
      }
      frame = requestAnimationFrame(render);
    };
    frame = requestAnimationFrame(render);
    return () => {
      active = false;
      cancelAnimationFrame(frame);
      void AsyncStorage.setItem(gameKey + '.elapsed', String(clockRef.current)).catch(() => {});
    };
  }, [bob, camera, gameKey, glow, loaded, panel, pose, size.height, size.width]);

  // Browser-only physical keyboard support. Text inputs must never move
  // the avatar; mobile touch pads write the same movement vector.
  useEffect(() => {
    if (Platform.OS !== 'web' || typeof window === 'undefined') return;
    const down = (e: KeyboardEvent) => {
      const target = e.target;
      if (target instanceof HTMLElement &&
        (target.isContentEditable || ['INPUT', 'TEXTAREA'].includes(target.tagName))) return;
      if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyW','KeyA','KeyS','KeyD'].includes(e.code)) {
        e.preventDefault(); keys.current.add(e.code);
      }
      if (e.code === 'KeyE' && panel === 'none') startChat();
    };
    const up = (e: KeyboardEvent) => keys.current.delete(e.code);
    const blur = () => keys.current.clear();
    window.addEventListener('keydown', down);
    window.addEventListener('keyup', up);
    window.addEventListener('blur', blur);
    return () => {
      window.removeEventListener('keydown', down);
      window.removeEventListener('keyup', up);
      window.removeEventListener('blur', blur);
    };
  }, [panel, startChat]);

  // Spatial map tiles are created only when changing between the two maps.
  const tiles = useMemo(() => {
    const columns = place === 'street' ? STREET_WIDTH : CAFE_WIDTH;
    const rows = place === 'street' ? STREET_HEIGHT : CAFE_HEIGHT;
    const elements: React.ReactElement[] = [];
    for (let y = 0; y < rows; y++) for (let x = 0; x < columns; x++) {
      const tile = pixelCell(place, x, y);
      const source: PixelArtKey = tile.prop && tile.prop in pixelArt
        ? tile.prop as PixelArtKey : tile.terrain === 'grass2' ? 'grass' : tile.terrain;
      elements.push(
        <Image key={x + ':' + y} source={pixelArt[source]} resizeMode="stretch"
          style={{ position: 'absolute', left: x * TILE, top: y * TILE,
            width: TILE, height: TILE }} />
      );
    }
    return elements;
  }, [place]);

  const npc = npcAt(place);
  const worldWidth = (place === 'street' ? STREET_WIDTH : CAFE_WIDTH) * TILE;
  const worldHeight = (place === 'street' ? STREET_HEIGHT : CAFE_HEIGHT) * TILE;
  const ageMonths = Math.floor(world.player.ageDays / 30);
  const dayWithinMonth = Math.min(30, Math.floor(clock / (MONTH_MS / 30)) + 1);
  const inGameMinute = Math.floor(((clock / (MONTH_MS / 30)) % 1) * 1440);
  const hour = Math.floor(inGameMinute / 60);
  const minute = inGameMinute % 60;
  const clockLabel = String(hour).padStart(2, '0') + ':' + String(minute).padStart(2, '0');
  const monthPart = Math.floor(clock / MONTH_MS * 100);
  const pauseMovement = () => {
    walkVector.current = { x: 0, y: 0 };
    setMovement({ x: 0, y: 0 });
  };
  const direction = (x: number, y: number) => {
    const next = { x, y };
    walkVector.current = next;
    setMovement(next);
  };
  const saveMission = () => {
    const title = safeText(missionTitle).slice(0, 80);
    if (!title) return;
    setMissions(previous => [...previous, {
      id: String(Date.now()), title,
      description: safeText(missionDescription),
      createdAge: ageMonths, completed: false,
    }].slice(-60));
    setMissionTitle(''); setMissionDescription('');
  };

  return (
    <View style={[s.root, { width, height }]} testID="liveit-continuous-pixel-life">
      <View style={s.world} onLayout={event => {
        const { width: w, height: h } = event.nativeEvent.layout;
        if (w !== size.width || h !== size.height) setSize({ width: w, height: h });
      }}>
        <Animated.View pointerEvents="none"
          style={[s.map, { width: worldWidth, height: worldHeight },
            { transform: camera.getTranslateTransform() }]}>
          {tiles}
          <View style={[s.npcShadow, { left: npc.x * TILE + 8, top: npc.y * TILE + 37 }]} />
          <Image source={actorArt(2, 'down')} resizeMode="stretch"
            style={{ position: 'absolute', left: npc.x * TILE, top: npc.y * TILE,
              width: TILE, height: TILE }} />
          <Animated.View style={[s.hero, {
            transform: [
              ...pose.getTranslateTransform(),
              { translateY: bob },
            ],
          }]}>
            <View style={s.heroShadow} />
            <Image source={actorArt(1, facing)} resizeMode="stretch"
              style={{ width: TILE, height: TILE }} />
          </Animated.View>
        </Animated.View>
        <Animated.View pointerEvents="none" style={[s.daylight, { opacity: glow }]} />
        <View style={s.topHud} pointerEvents="box-none">
          <View style={s.brand}>
            <Text style={s.brandName}>LIVEIT <Text style={{color: COLORS.gold}}>✦</Text></Text>
            <Text style={s.sub}>{place === 'street' ? 'BELLWEATHER MARKET' : 'THE OLD CAFÉ'}</Text>
          </View>
          <View style={s.clockBox}>
            <Text style={s.clockText}>☀ {clockLabel}</Text>
            <Text style={s.sub}>DAY {dayWithinMonth}/30 · AGE {(ageMonths / 12).toFixed(1)}</Text>
            <View style={s.clockTrack}><View style={[s.clockFill, {width: monthPart + '%'}]} /></View>
          </View>
        </View>
        <View style={s.leftButtons}>
          <HudButton title="☷" detail="MISSION" onPress={() => {pauseMovement(); setPanel('missions');}} />
          <HudButton title="♫" detail="PEOPLE" onPress={() => onNavigate('people')} />
          <HudButton title="⚙" detail="LOCAL AI" onPress={() => {pauseMovement(); setPanel('settings');}} />
        </View>
        <View style={s.bottomHud} pointerEvents="box-none">
          <View style={s.toast}><Text style={s.toastText} numberOfLines={2}>{notice}</Text></View>
          <View style={s.controlRow}>
            <View style={s.dpad} accessibilityLabel="Directional movement controls">
              <View style={s.padRow}><View style={s.padBlank} /><DirectionButton label="▲" onDown={() => direction(0,-1)} onUp={pauseMovement} active={movement.y < 0} /><View style={s.padBlank} /></View>
              <View style={s.padRow}><DirectionButton label="◀" onDown={() => direction(-1,0)} onUp={pauseMovement} active={movement.x < 0}/><View style={s.padBlank} /><DirectionButton label="▶" onDown={() => direction(1,0)} onUp={pauseMovement} active={movement.x > 0}/></View>
              <View style={s.padRow}><View style={s.padBlank}/><DirectionButton label="▼" onDown={() => direction(0,1)} onUp={pauseMovement} active={movement.y > 0}/><View style={s.padBlank}/></View>
            </View>
            <View style={s.actions}>
              <Pressable onPress={startChat} style={s.talkButton} accessibilityRole="button" accessibilityLabel="Talk to nearby NPC"><Text style={s.talkIcon}>✦</Text><Text style={s.actionLabel}>TALK</Text></Pressable>
              <Pressable onPress={() => {pauseMovement(); onNavigate('stories');}} style={s.storyButton} accessibilityRole="button" accessibilityLabel="Open story missions"><Text style={s.talkIcon}>✧</Text><Text style={s.actionLabel}>STORY</Text></Pressable>
            </View>
          </View>
          <View style={s.quickbar}>
            <Text style={s.quickText}>♥ {world.player.wellbeing}%</Text>
            <Text style={s.quickText}>£{(world.player.money / 100).toFixed(0)}</Text>
            <Text style={s.quickText}>{world.player.name}</Text>
            <Text style={s.quickText}>EXP {world.player.skill}</Text>
          </View>
        </View>
      </View>
      {panel !== 'none' && (
        <View style={s.modalCover}>
          <View style={s.modal}>
            <View style={s.modalHead}>
              <View>
                <Text style={s.modalTitle}>{panel === 'talk' ? 'AMELIA' : panel === 'missions' ? 'YOUR MISSIONS' : 'LOCAL CONVERSATION ENGINE'}</Text>
                <Text style={s.sub}>{panel === 'talk' ? 'A real conversation, not a three-choice menu.' : panel === 'missions' ? 'Make any day into an adventure.' : 'Runs on your machine. Never required to play.'}</Text>
              </View>
              <Pressable accessibilityLabel="Close panel" onPress={() => setPanel('none')} style={s.close}><Text style={s.closeText}>✕</Text></Pressable>
            </View>
            {panel === 'talk' ? (
              <>
                <ScrollView style={s.messages} contentContainerStyle={{paddingVertical: 12, gap: 10}}>
                  {messages.map((message, i) => (
                    <View key={i} style={[s.bubble, message.speaker === 'player' ? s.mine : s.theirs]}>
                      <Text style={s.speaker}>{message.speaker === 'player' ? world.player.name : 'AMELIA'}</Text>
                      <Text style={s.bubbleText}>{message.text}</Text>
                    </View>
                  ))}
                  {waiting && <Text style={s.waitText}>Amelia is thinking…</Text>}
                </ScrollView>
                <Text style={s.mode}>{modelMode === 'local' ? '● QWEN3 LOCAL' : '○ OFFLINE WRITTEN RESPONSES'}</Text>
                <View style={s.suggestions}>
                  {['How has your week been?', 'Do you know any work?', 'What should we do together?'].map(text =>
                    <Pressable key={text} style={s.suggestion} onPress={() => void submit(text)}><Text style={s.suggestionText}>{text}</Text></Pressable>)}
                </View>
                <View style={s.composer}>
                  <TextInput multiline style={s.composerInput}
                    value={draft} onChangeText={setDraft} placeholder="Say anything to Amelia…"
                    placeholderTextColor="#8e9c9e" maxLength={500} />
                  <Pressable onPress={() => void submit()} disabled={waiting || !draft.trim()} style={s.send}><Text style={s.sendText}>SEND ↗</Text></Pressable>
                </View>
                <Pressable style={s.storyLink} onPress={onTalk}><Text style={s.storyLinkText}>✦ Begin / continue Amelia's authored story mission →</Text></Pressable>
              </>
            ) : panel === 'missions' ? (
              <ScrollView style={s.messages} contentContainerStyle={{gap: 12, paddingVertical: 12}}>
                <Text style={s.help}>Missions live inside your Free Life and stay available until completed. They never replace your character or reset the world.</Text>
                {missions.map(m => (
                  <Pressable key={m.id} onPress={() => setMissions(all => all.map(a => a.id === m.id ? {...a, completed: !a.completed} : a))}
                    style={[s.quest, m.completed && { opacity: 0.55 }]}>
                    <Text style={s.questTitle}>{m.completed ? '✓ ' : '◇ '}{m.title}</Text>
                    <Text style={s.help}>{m.description || 'Explore and make your own meaning.'}</Text>
                  </Pressable>
                ))}
                <Text style={s.speaker}>CREATE A MISSION</Text>
                <TextInput style={s.field} value={missionTitle} onChangeText={setMissionTitle} placeholder="Mission title" placeholderTextColor="#a1a4ad" maxLength={80} />
                <TextInput style={[s.field, {minHeight: 90}]} multiline value={missionDescription} onChangeText={setMissionDescription} placeholder="What would you like to accomplish?" placeholderTextColor="#a1a4ad" maxLength={500}/>
                <Pressable style={s.add} onPress={saveMission}><Text style={s.addText}>+ ADD TO MY LIFE</Text></Pressable>
                <Pressable style={s.storyLink} onPress={onTalk}><Text style={s.storyLinkText}>Play the official Amelia quest →</Text></Pressable>
              </ScrollView>
            ) : (
              <View style={{gap:12}}>
                <Text style={s.help}>On your Mac, run: ollama pull qwen3:0.6b, then ollama serve. On an iPhone, enter the Mac's LAN IP (not localhost). If unavailable, the game uses clearly labelled offline dialogue.</Text>
                <Text style={s.speaker}>OLLAMA BASE URL</Text>
                <TextInput autoCapitalize="none" autoCorrect={false} style={s.field} value={endpoint} onChangeText={setEndpoint} placeholder="http://192.168.1.100:11434" placeholderTextColor="#919da3"/>
                <Pressable style={s.add} onPress={() => {void AsyncStorage.setItem('liveit.localOllamaEndpoint', endpoint); setPanel('none');}}><Text style={s.addText}>SAVE LOCAL CONNECTION</Text></Pressable>
                <Text style={s.help}>Model output is dialogue only. Money, identity, relationships, mission completion and saved facts remain controlled by the deterministic game engine.</Text>
              </View>
            )}
          </View>
        </View>
      )}
    </View>
  );
}
function DirectionButton({label,onDown,onUp,active}: {
  label:string; onDown:()=>void; onUp:()=>void; active:boolean;
}) {
  return <Pressable onPressIn={onDown} onPressOut={onUp} accessibilityRole="button"
    accessibilityLabel={'Move ' + label} style={[s.pad, active && s.padActive]}>
    <Text style={s.padText}>{label}</Text>
  </Pressable>;
}
function HudButton({title,detail,onPress}: {title:string;detail:string;onPress:()=>void}) {
  return <Pressable onPress={onPress} accessibilityRole="button" accessibilityLabel={detail} style={s.hudButton}>
    <Text style={s.hudIcon}>{title}</Text><Text style={s.hudDetail}>{detail}</Text>
  </Pressable>;
}
const s = StyleSheet.create({
  root: {backgroundColor:'#151c26', overflow:'hidden'},
  world: {flex:1, backgroundColor:COLORS.grass, overflow:'hidden'},
  map: {position:'absolute',left:0,top:0},
  hero: {position:'absolute',left:0,top:0,width:TILE,height:TILE},
  heroShadow: {position:'absolute',bottom:2,left:10,width:28,height:9,borderRadius:18,backgroundColor:'#1a1a2588'},
  npcShadow: {position:'absolute',width:28,height:9,borderRadius:18,backgroundColor:'#1a1a2588'},
  daylight: {position:'absolute',left:0,right:0,top:0,bottom:0,backgroundColor:'#192b62'},
  topHud: {position:'absolute',top:14,left:14,right:14,flexDirection:'row',justifyContent:'space-between',alignItems:'flex-start',gap:6},
  brand: {backgroundColor:COLORS.panel,borderWidth:2,borderColor:COLORS.border,borderRadius:12,paddingVertical:8,paddingHorizontal:12,maxWidth:'48%'},
  brandName: {fontSize:21,fontWeight:'900',color:COLORS.ink,letterSpacing:1},
  sub: {fontSize:10,fontWeight:'800',color:COLORS.dim,letterSpacing:1},
  clockBox: {backgroundColor:COLORS.panel,borderWidth:2,borderColor:COLORS.border,borderRadius:12,padding:10,minWidth:142,alignItems:'flex-end'},
  clockText: {fontSize:21,fontWeight:'900',color:COLORS.gold},
  clockTrack: {height:5,borderRadius:3,backgroundColor:'#725263',alignSelf:'stretch',marginTop:6,overflow:'hidden'},
  clockFill: {backgroundColor:COLORS.green,height:'100%'},
  leftButtons: {position:'absolute',top:103,left:12,gap:8},
  hudButton: {backgroundColor:COLORS.panel,borderWidth:1,borderColor:'#d7a66b88',borderRadius:12,minWidth:68,alignItems:'center',paddingHorizontal:8,paddingVertical:7},
  hudIcon: {fontSize:20,color:COLORS.gold,fontWeight:'900'},
  hudDetail: {fontSize:8,color:COLORS.ink,fontWeight:'900',letterSpacing:0.6},
  bottomHud: {position:'absolute',bottom:0,left:0,right:0,paddingHorizontal:16,paddingBottom:12},
  toast: {alignSelf:'center',paddingHorizontal:12,paddingVertical:7,backgroundColor:COLORS.panel,borderRadius:10,maxWidth:'90%',marginBottom:7},
  toastText: {color:COLORS.ink,fontSize:11,textAlign:'center',fontWeight:'700'},
  controlRow: {flexDirection:'row',justifyContent:'space-between',alignItems:'flex-end'},
  dpad: {backgroundColor:'#1f1a285c',borderRadius:18,padding:4},
  padRow: {flexDirection:'row'},
  padBlank: {width:45,height:45},
  pad: {width:45,height:45,backgroundColor:'#25243dcd',borderColor:'#f6cd8b',borderWidth:1,borderRadius:9,justifyContent:'center',alignItems:'center'},
  padActive: {backgroundColor:'#75516c'},
  padText: {color:COLORS.ink,fontWeight:'900',fontSize:21},
  actions: {flexDirection:'row',gap:10,paddingBottom:12},
  talkButton: {width:70,height:70,borderRadius:35,backgroundColor:'#eea86e',borderWidth:3,borderColor:'#ffe6ac',alignItems:'center',justifyContent:'center'},
  storyButton: {width:59,height:59,borderRadius:30,backgroundColor:'#6d747f',borderWidth:2,borderColor:'#dce2ce',alignItems:'center',justifyContent:'center',alignSelf:'flex-end'},
  talkIcon: {color:COLORS.brown,fontSize:24,fontWeight:'900'},
  actionLabel: {color:COLORS.brown,fontSize:10,fontWeight:'900'},
  quickbar: {flexDirection:'row',justifyContent:'space-around',gap:6,backgroundColor:COLORS.panel,borderColor:COLORS.border,borderWidth:1,padding:9,borderRadius:10,marginTop:6},
  quickText: {color:COLORS.ink,fontSize:11,fontWeight:'800'},
  modalCover: {position:'absolute',left:0,right:0,top:0,bottom:0,backgroundColor:'#0e0d17dd',alignItems:'center',justifyContent:'center',padding:14},
  modal: {width:'100%',maxWidth:720,maxHeight:'95%',minHeight:'58%',backgroundColor:'#272332',borderWidth:3,borderColor:COLORS.border,borderRadius:16,padding:15,flexShrink:1},
  modalHead: {flexDirection:'row',justifyContent:'space-between',alignItems:'flex-start',gap:10,marginBottom:10},
  modalTitle: {fontSize:21,color:COLORS.gold,fontWeight:'900',letterSpacing:1},
  close: {width:36,height:36,borderRadius:10,backgroundColor:'#403044',alignItems:'center',justifyContent:'center'},
  closeText: {color:COLORS.ink,fontSize:20,fontWeight:'900'},
  messages: {flexGrow:1,flexShrink:1},
  bubble: {maxWidth:'89%',borderRadius:12,paddingHorizontal:14,paddingVertical:10},
  mine: {alignSelf:'flex-end',backgroundColor:'#4c5062'},
  theirs: {alignSelf:'flex-start',backgroundColor:'#394a46'},
  speaker: {color:COLORS.gold,fontSize:10,fontWeight:'900',letterSpacing:1,marginBottom:4},
  bubbleText: {color:COLORS.ink,fontSize:15,lineHeight:23},
  waitText: {color:COLORS.dim,fontSize:12,fontStyle:'italic'},
  mode: {color:COLORS.green,fontSize:10,fontWeight:'900',marginVertical:7},
  suggestions: {flexDirection:'row',flexWrap:'wrap',gap:6,marginBottom:8},
  suggestion: {padding:7,borderWidth:1,borderColor:'#bea27d',borderRadius:8},
  suggestionText: {color:COLORS.ink,fontSize:11},
  composer: {flexDirection:'row',alignItems:'flex-end',gap:8},
  composerInput: {flex:1,minHeight:42,maxHeight:120,backgroundColor:'#171b2a',borderRadius:9,padding:10,color:COLORS.ink,fontSize:14,textAlignVertical:'top'},
  send: {borderRadius:8,backgroundColor:COLORS.gold,paddingHorizontal:11,paddingVertical:12},
  sendText: {color:COLORS.brown,fontWeight:'900'},
  storyLink: {marginTop:12,paddingVertical:10,alignItems:'center',borderTopWidth:1,borderTopColor:'#665566'},
  storyLinkText: {color:COLORS.gold,fontWeight:'800',fontSize:12},
  help: {color:COLORS.dim,fontSize:13,lineHeight:21},
  quest: {backgroundColor:'#3b394c',borderWidth:1,borderColor:'#ae8569',borderRadius:9,padding:12,gap:5},
  questTitle: {color:COLORS.ink,fontSize:15,fontWeight:'800'},
  field: {backgroundColor:'#171b2a',borderColor:'#625a5a',borderWidth:1,borderRadius:8,color:COLORS.ink,padding:12,fontSize:14},
  add: {backgroundColor:COLORS.gold,borderRadius:9,padding:12,alignItems:'center'},
  addText: {color:COLORS.brown,fontWeight:'900'},
});
