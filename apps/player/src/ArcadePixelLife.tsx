import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Animated, Image, Platform, Pressable, ScrollView, StyleSheet, Text,
  type ImageSourcePropType, type ImageStyle,
  TextInput, View, useWindowDimensions,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { World } from '@living/world-schema';
import { lifeStageOf, type ChildhoodActivity, type WorldActivity } from '@living/simulation-core';
import { pixelArt, actorArt, type PixelArtKey } from './pixelArt';
import { findTileRoute, targetForTap, type TilePoint } from './pixelPathfinding';
import { modernSpriteColumn } from './spriteDirections';
import { worldCell, seedFromTimeline, visibleWorldTiles, biomeAt, chunkOf } from './proceduralWorld';
import { MISSION_GOALS, missionExpired, newMission, parseMissions, resolveMissionEvent,
  type LifeMission, type MissionGoal, type MissionEvent } from './missionGoals';
import {
  INITIAL_POSITION, STREET_WIDTH, STREET_HEIGHT, CAFE_WIDTH, CAFE_HEIGHT,
  npcAt, validPixelPosition,
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
const TILE = 64; // 4x the source pixels; covers mobile viewports
const CRISP_STYLE: ImageStyle | undefined = Platform.OS === 'web'
  ? ({ imageRendering: 'pixelated' } as unknown as ImageStyle)
  : undefined;
const SPEED = 3.5;             // tiles per second, independent of monitor Hz
const MONTH_MS = 60 * 60 * 1000; // one real gameplay hour = 30 simulated days
const COLORS = {
  ink: '#fff4d6', dim: '#c4d8c9', brown: '#261a23',
  panel: '#211e30ee', border: '#d7a66b', gold: '#ffc678',
  coral: '#f99073', grass: '#648b73', green: '#b3e3ba',
};
type Point = { x: number; y: number };
type Message = { speaker: 'player' | 'npc'; text: string };
type Mission = LifeMission;

function safeText(text: string): string {
  return text.trim().slice(0, 500);
}
async function npcFromLocalModel(
  endpoint: string, model: string, history: Message[], player: string, month: number,
): Promise<string> {
  const url = endpoint.trim().replace(/\/+$/, '') + '/api/chat';
  if (!/^https?:\/\//i.test(url)) throw Error('Invalid local Ollama URL');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 40000);
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
      body: JSON.stringify({
        model,
        stream: false,
        think: false,
        options: { temperature: 0.75, num_predict: 380, num_ctx: 4096 },
        messages: [
          {
            role: 'system',
            content: 'You are Amelia, a believable 24-year-old person in Bellweather, a contemporary town. You are not a virtual assistant. Your personal plans, relationships, hopes, boundaries, and past change as months pass. You are talking directly to ' + player +
              ', who is age ' + month + ' months. Reply naturally with 2–6 substantive sentences where appropriate; avoid filler, repeat questions and excessive affirmation. Remember actual things in the conversation, ask at most one thoughtful question, and sometimes disagree. Never claim to have completed a quest, paid money, changed health or edited the game. No stage directions, no /think, no system messages.',
          },
          ...history.slice(-28).map(item => ({
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


/** A shaded roof/awning with restrained readable signage built from shapes.
 * Artwork is original game UI; the underlying streets remain Pulse CC0 PNGs.
 */
function PixelBuilding({
  x, y, w, h, roof, accent, label,
}: {
  x: number; y: number; w: number; h: number;
  roof: string; accent: string; label: string;
}) {
  const width = w * TILE;
  const height = h * TILE;
  return (
    <View pointerEvents="none" style={{
      position:'absolute', left:x*TILE-5, top:y*TILE-11,
      width:width+10, height, backgroundColor:'#322b3a',
      borderWidth:6, borderColor:'#292331',
      shadowColor:'#17141b', shadowOffset:{width:9,height:13},
      shadowOpacity:0.48, shadowRadius:3, elevation:7,
    }}>
      <View style={{ position:'absolute',left:0,right:0,top:0,
        bottom:12,backgroundColor:roof,borderBottomWidth:9,borderBottomColor:accent }}>
        <View style={{height:10,backgroundColor:'#ffffff23',margin:10}}/>
        <View style={{position:'absolute',top:'25%',left:12,right:12,
          height:3,backgroundColor:'#1a172733'}}/>
        <View style={{position:'absolute',bottom:'27%',left:12,right:12,
          height:3,backgroundColor:'#1a172733'}}/>
      </View>
      <View style={{position:'absolute',bottom:1,left:width*0.15,right:width*0.15,
        backgroundColor:'#281f32',paddingVertical:6,paddingHorizontal:5,
        borderWidth:2,borderColor:'#eab77e'}}>
        <Text numberOfLines={1} style={{textAlign:'center',fontSize:12,
          fontWeight:'900',letterSpacing:1.3,color:'#fff0c6'}}>{label}</Text>
      </View>
    </View>
  );
}

export function ArcadePixelLife({
  world, onTalk, onAdvanceMonth, onNavigate, onActivity, onChildAction, onSkipChildhood, paused = false,
}: {
  world: World;
  paused?: boolean;
  onTalk: () => void;
  onAdvanceMonth: () => void;
  onActivity: (activity: WorldActivity, dayOffset: number) => void;
  onChildAction: (activity: ChildhoodActivity, dayOffset: number) => void;
  onSkipChildhood: (years: 2 | 5 | 13 | 18) => void;
  onNavigate: (where: 'stories' | 'people' | 'journal' | 'life') => void;
}) {
  const { width, height } = useWindowDimensions();
  const worldSeed = useMemo(() => seedFromTimeline(world.timelineId), [world.timelineId]);
  const [size, setSize] = useState({ width, height });
  // Moving tile window: prefetch a two-tile border around the viewport.
  // Rendering the entire 30x23 town creates hundreds of native Image nodes
  // even when only about ten tiles are visible across a mobile screen.
  const [tileWindow, setTileWindow] = useState({ left: 0, top: 0, cols: 14, rows: 21 });
  const tileWindowRef = useRef(tileWindow);
  const [place, setPlace] = useState<PixelPlace>('street');
  const [facing, setFacing] = useState<Facing>('down');
  const [zone, setZone] = useState<'cafe' | 'market' | 'garden' | 'street'>('street');
  const zoneRef = useRef(zone);
  const [clock, setClock] = useState(0);
  const [notice, setNotice] = useState('Walk up to Amelia and press TALK. Explore the market and café.');
  const [panel, setPanel] = useState<'none' | 'talk' | 'missions' | 'settings'>('none');
  const [messages, setMessages] = useState<Message[]>([]);
  const [draft, setDraft] = useState('');
  const [missionTitle, setMissionTitle] = useState('');
  const [missionDescription, setMissionDescription] = useState('');
  const [missions, setMissions] = useState<Mission[]>([]);
  const [missionGoal, setMissionGoal] = useState<MissionGoal>('meet');
  const [missionTerm, setMissionTerm] = useState<'birthday' | 'five' | 'lifetime'>('birthday');
  const missionRef = useRef<Mission[]>([]);
  missionRef.current = missions;
  const ageRef = useRef(0);
  ageRef.current = Math.floor((world.player.ageDays * 12) / 365);
  // These sidecar goals have no authority to change the core save themselves.
  const missionEvent = useCallback((event: MissionEvent) => {
    const { missions: next, newlyCompleted } = resolveMissionEvent(
      missionRef.current, event, ageRef.current,
    );
    if (!newlyCompleted.length) return;
    missionRef.current = next;
    setMissions(next);
    setNotice('✦ MISSION COMPLETE: ' + newlyCompleted.map(m => m.title).join(', '));
  }, []);
  const lastZone = useRef('');

  const [endpoint, setEndpoint] = useState('http://localhost:11434');
  const [localModel, setLocalModel] = useState('qwen3:4b');
  const [pixelAvatar, setPixelAvatar] = useState<'adam'|'alex'|'bob'|'amelia'>('adam');
  const [modelMode, setModelMode] = useState<'unknown' | 'local' | 'error'>('unknown');
  const [aiError, setAiError] = useState('');
  const [aiStatus, setAiStatus] = useState('Local model not checked.');
  const [waiting, setWaiting] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [movement, setMovement] = useState<Point>({ x: 0, y: 0 });
  const walkVector = useRef<Point>({ x: 0, y: 0 });
  const routeRef = useRef<TilePoint[]>([]);
  const talkAfterWalk = useRef(false);
  const cameraPoint = useRef<Point>({ x: 0, y: 0 });
  const keys = useRef(new Set<string>());
  const hero = useRef({ x: INITIAL_POSITION.x, y: INITIAL_POSITION.y, place: INITIAL_POSITION.place });
  const pose = useRef(new Animated.ValueXY()).current;
  const camera = useRef(new Animated.ValueXY()).current;
  const bob = useRef(new Animated.Value(0)).current;
  const frameOffset = useRef(new Animated.Value(0)).current;
  const facingRef = useRef<Facing>('down');
  const localArt = pixelArt as Record<string, ImageSourcePropType>;
  const modernPlayer = (pixelAvatar === 'adam' ? localArt.player_modern : localArt['player_modern_' + pixelAvatar]) || localArt.player_modern;
  const modernNPC = localArt.npc_modern;
  const crisp = CRISP_STYLE;
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
      AsyncStorage.getItem('liveit.localOllamaModel'),
      AsyncStorage.getItem(gameKey + '.pixelAvatar'),
    ]).then(([location, elapsed, transcript, quests, customEndpoint, customModel, savedAvatar]) => {
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
        if (Array.isArray(saved)) setMissions(parseMissions(saved));
      } catch { /* No created missions yet. */ }
      if (customEndpoint) setEndpoint(customEndpoint);
      if (customModel && ['qwen3:0.6b','qwen3:1.7b','qwen3:4b'].includes(customModel)) setLocalModel(customModel);
      if (savedAvatar && ['adam','alex','bob','amelia'].includes(savedAvatar)) setPixelAvatar(savedAvatar as 'adam'|'alex'|'bob'|'amelia');
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
    void AsyncStorage.setItem(gameKey + '.missions', JSON.stringify(missions.slice(-500))).catch(() => {});
  }, [gameKey, loaded, missions]);

  const isNearNpc = useCallback(() => {
    const npc = npcAt(hero.current.place);
    return Math.hypot(hero.current.x - npc.x, hero.current.y - npc.y) <= 1.8;
  }, []);
  const startChat = useCallback(() => {
    if (world.player.ageDays < 18 * 365) {
      setNotice('This adult NPC encounter unlocks once you turn 18. Play your childhood and make friends first.');
      return;
    }
    if (!isNearNpc()) {
      setNotice('Move near Amelia to begin a conversation.');
      return;
    }
    missionEvent('meet');
    setPanel('talk');
    if (chatRef.current.length === 0) setMessages([{
      speaker: 'npc',
      text: 'Oh, hey! I thought I recognized you. How have you been?',
    }]);
  }, [isNearNpc, missionEvent, world.player.ageDays]);

  const submit = useCallback(async (suggested?: string) => {
    const sentence = safeText(suggested ?? draft);
    if (!sentence || busyRef.current) return;
    const updated = [...chatRef.current, { speaker: 'player' as const, text: sentence }];
    chatRef.current = updated;
    setMessages(updated);
    setDraft('');
    busyRef.current = true;
    setWaiting(true);
    setAiError('');
    try {
      const reply = await npcFromLocalModel(endpoint, localModel, updated, world.player.name,
        Math.floor(world.player.ageDays / 30));
      setModelMode('local');
      setAiStatus('Connected to ' + localModel);
      setMessages(existing => [...existing, { speaker: 'npc' as const, text: reply }].slice(-80));
      if (/\b(work|job|career|employment|rent|earnings)\b/i.test(sentence)) {
        missionEvent('work');
      }
    } catch (cause) {
      // Never impersonate an LLM with a handful of canned responses. Restore
      // unsent text and make the failure and remedy explicitly visible.
      setMessages(updated.slice(0, -1));
      chatRef.current = updated.slice(0, -1);
      setDraft(sentence);
      setModelMode('error');
      const reason = cause instanceof Error ? cause.message : String(cause);
      setAiError('Cannot reach local ' + localModel + ' at ' + endpoint +
        '. ' + reason + '. Start Ollama and allow the app origin, or correct the LAN URL in LOCAL AI.');
      setAiStatus('Disconnected — no AI reply was generated.');
    } finally {
      busyRef.current = false;
      setWaiting(false);
    }
  }, [draft, endpoint, localModel, missionEvent, world.player.ageDays, world.player.name]);

  // No setState inside the 60/120 Hz world loop. The movement animation and
  // following camera remain smooth even if no React component re-renders.
  useEffect(() => {
    if (!loaded || panel !== 'none' || paused) return;
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
      return worldCell(p, cx, cy, worldSeed).solid || (n.x === cx && n.y === cy);
    };
    const render = (timestamp: number) => {
      if (!active) return;
      const dt = last ? Math.min((timestamp - last) / 1000, 0.05) : 0;
      last = timestamp;
      const p = hero.current;
      const pad = walkVector.current;
      let vx = Number(keys.current.has('ArrowRight') || keys.current.has('KeyD')) -
        Number(keys.current.has('ArrowLeft') || keys.current.has('KeyA')) + pad.x;
      let vy = Number(keys.current.has('ArrowDown') || keys.current.has('KeyS')) -
        Number(keys.current.has('ArrowUp') || keys.current.has('KeyW')) + pad.y;
      if (Math.hypot(vx, vy) === 0 && routeRef.current.length) {
        const step = routeRef.current[0]!;
        const dx = step.x - p.x, dy = step.y - p.y;
        const distance = Math.hypot(dx, dy);
        if (distance <= 0.08) {
          p.x = step.x; p.y = step.y;
          routeRef.current.shift();
          if (routeRef.current.length === 0 && talkAfterWalk.current) {
            talkAfterWalk.current = false;
            startChat();
          }
        } else {
          // Avoid overshooting a waypoint on high-refresh-rate devices.
          const factor = Math.min(1, distance / Math.max(dt * SPEED, 0.0001));
          vx = dx / distance * factor;
          vy = dy / distance * factor;
        }
      }
      const magnitude = Math.hypot(vx, vy);
      if (magnitude > 0) {
        const dx = (vx / magnitude) * dt * SPEED;
        const dy = (vy / magnitude) * dt * SPEED;
        if (!blocks(p.x + dx, p.y)) p.x += dx;
        if (!blocks(p.x, p.y + dy)) p.y += dy;
        const nextFacing: Facing = Math.abs(vx) > Math.abs(vy)
          ? vx > 0 ? 'right' : 'left' : vy > 0 ? 'down' : 'up';
        facingRef.current = nextFacing;
        setFacing(previous => previous === nextFacing ? previous : nextFacing);
        bob.setValue(Math.sin(timestamp / 70) * 2);
        const faceOffset = modernPlayer ? modernSpriteColumn(nextFacing, 0) : 0;
        frameOffset.setValue(-TILE * (faceOffset + (Math.floor(timestamp / 125) % (modernPlayer ? 6 : 4))));
      } else {
        bob.setValue(Math.sin(timestamp / 440) * 0.7);
        frameOffset.setValue(modernPlayer ? -TILE * modernSpriteColumn(facingRef.current, 0) : 0);
      }
      // Portal transitions need to be detected by entering a tile, not by
      // colliding with the café's solid façade.
      const terrain = worldCell(p.place, Math.floor(p.x + 0.5), Math.floor(p.y + 0.5), worldSeed);
      if (terrain.portal === 'cafe') {
        p.place = 'cafe'; p.x = 5; p.y = 8;
        routeRef.current = []; talkAfterWalk.current = false;
        setPlace('cafe'); setNotice('The café smells of coffee and rain.');
        missionEvent('cafe');
      } else if (terrain.portal === 'street') {
        p.place = 'street'; p.x = 5; p.y = 7;
        routeRef.current = []; talkAfterWalk.current = false;
        setPlace('street'); setNotice('Back in Bellweather market.');
      }
      const currentZone = p.place === 'cafe' ? 'cafe'
        : p.x >= 17 && p.y >= 14 ? 'garden'
        : p.x >= 19 && p.y <= 13 ? 'market' : 'street';
      if (zoneRef.current !== currentZone) {
        zoneRef.current = currentZone;
        setZone(currentZone);
      }
      if (p.place === 'street' && p.x >= 17 && p.y >= 14 &&
          lastZone.current !== 'garden') {
        lastZone.current = 'garden';
        missionEvent('garden');
      } else if (!(p.place === 'street' && p.x >= 17 && p.y >= 14)) {
        lastZone.current = '';
      }
      const colsNeeded = p.place === 'street'
        ? Math.ceil(size.width / TILE) + 4
        : Math.min(CAFE_WIDTH, Math.ceil(size.width / TILE) + 4);
      const rowsNeeded = p.place === 'street'
        ? Math.ceil(size.height / TILE) + 4
        : Math.min(CAFE_HEIGHT, Math.ceil(size.height / TILE) + 4);
      const nextWindow = {
        left: p.place === 'street'
          ? Math.floor(p.x) - Math.floor(colsNeeded / 2)
          : Math.min(Math.max(0, Math.floor(p.x) - Math.floor(colsNeeded / 2)),
            CAFE_WIDTH - colsNeeded),
        top: p.place === 'street'
          ? Math.floor(p.y) - Math.floor(rowsNeeded / 2)
          : Math.min(Math.max(0, Math.floor(p.y) - Math.floor(rowsNeeded / 2)),
            CAFE_HEIGHT - rowsNeeded),
        cols: colsNeeded, rows: rowsNeeded,
      };
      const oldWindow = tileWindowRef.current;
      if (oldWindow.left !== nextWindow.left || oldWindow.top !== nextWindow.top ||
          oldWindow.cols !== nextWindow.cols || oldWindow.rows !== nextWindow.rows) {
        tileWindowRef.current = nextWindow;
        setTileWindow(nextWindow);
      }
      pose.setValue({ x: p.x * TILE, y: p.y * TILE });
      const worldWidth = (p.place === 'street' ? STREET_WIDTH : CAFE_WIDTH) * TILE;
      const worldHeight = (p.place === 'street' ? STREET_HEIGHT : CAFE_HEIGHT) * TILE;
      const cameraX = p.place === 'street'
        ? size.width / 2 - (p.x + 0.5) * TILE
        : Math.min(0, Math.max(size.width - worldWidth,
          size.width / 2 - (p.x + 0.5) * TILE));
      const cameraY = p.place === 'street'
        ? size.height / 2 - (p.y + 0.5) * TILE
        : Math.min(0, Math.max(size.height - worldHeight,
          size.height / 2 - (p.y + 0.5) * TILE));
      cameraPoint.current = { x: cameraX, y: cameraY };
      camera.setValue(cameraPoint.current);
      if (dt > 0) {
        clockRef.current += dt * 1000;
        if (clockRef.current >= MONTH_MS) {
          clockRef.current -= MONTH_MS;
          monthRef.current();
          missionEvent('month');
        }
      }
      if (timestamp - lastUi > 1000) {
        setClock(clockRef.current);
        const dayPhase = (clockRef.current % (MONTH_MS / 30)) / (MONTH_MS / 30);
        const solar = Math.cos((dayPhase - 0.5) * Math.PI * 2);
        glow.setValue(0.025 + 0.25 * Math.max(0, -solar));
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
  }, [bob, camera, frameOffset, gameKey, glow, loaded, missionEvent, modernPlayer, panel, paused, pose, size.height, size.width, startChat, worldSeed]);

  // Browser-only physical keyboard support. Text inputs must never move
  // the avatar; mobile touch pads write the same movement vector.
  useEffect(() => {
    if (Platform.OS !== 'web' || typeof window === 'undefined') return;
    const down = (e: KeyboardEvent) => {
      const target = e.target;
      if (target instanceof HTMLElement &&
        (target.isContentEditable || ['INPUT', 'TEXTAREA'].includes(target.tagName))) return;
      if (paused || panel !== 'none') return;
      if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyW','KeyA','KeyS','KeyD'].includes(e.code)) {
        e.preventDefault(); routeRef.current = []; talkAfterWalk.current = false;
        keys.current.add(e.code);
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
  }, [panel, paused, startChat]);

  // Spatial map tiles are created only when changing between the two maps.
  const tiles = useMemo(() => {
    const elements: React.ReactElement[] = [];
    for (const {x,y,cell:tile} of visibleWorldTiles(
      place,tileWindow.left,tileWindow.top,tileWindow.cols,tileWindow.rows,worldSeed
    )) {
      const base: PixelArtKey = tile.terrain === 'grass2' ? 'grass' : tile.terrain;
      const frame = { position: 'absolute' as const, left: x * TILE,
        top: y * TILE, width: TILE, height: TILE };
      elements.push(
        <View key={x + ':' + y} pointerEvents="none" style={frame}>
          <Image source={pixelArt[base]} resizeMode="stretch"
            style={[{ position: 'absolute', width: TILE, height: TILE }, crisp]} />
          {tile.prop && tile.prop in pixelArt
            ? <Image source={pixelArt[tile.prop]} resizeMode="stretch"
                style={[{ position: 'absolute', width: TILE, height: TILE }, crisp]} />
            : null}
        </View>,
      );
    }
    return elements;
  }, [crisp, place, tileWindow.cols, tileWindow.left, tileWindow.rows, tileWindow.top, worldSeed]);

  const npc = npcAt(place);
  const worldWidth = (place === 'street' ? 1 : CAFE_WIDTH) * TILE;
  const worldHeight = (place === 'street' ? 1 : CAFE_HEIGHT) * TILE;
  const ageMonths = Math.floor((world.player.ageDays * 12) / 365);
  const stage = lifeStageOf(world.player.ageDays);
  const ageYears = Math.floor(world.player.ageDays / 365);
  const openChunk = chunkOf(tileWindow.left, tileWindow.top);
  const biome = biomeAt(worldSeed, tileWindow.left, tileWindow.top);
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
    routeRef.current = []; talkAfterWalk.current = false;
    const next = { x, y };
    walkVector.current = next;
    setMovement(next);
  };
  const interact = () => {
    if (ageYears < 16) { setNotice('Market shifts and purchases unlock as you grow older.'); return; }
    if (!loaded || panel !== 'none' || paused) return;
    const interaction: WorldActivity | null = zone === 'cafe' ? 'cafe'
      : zone === 'garden' ? 'garden'
      : zone === 'market' ? 'gig' : null;
    if (!interaction) {
      setNotice('Walk to the market for work, the garden to rest, or the café for coffee.');
      return;
    }
    const offset = Math.min(29, Math.floor(clockRef.current / (MONTH_MS / 30)));
    const marker = 'free-life-action:' + (world.day + offset) + ':' + interaction;
    if (world.facts.includes(marker)) {
      setNotice('You have already done that today. Try another activity!');
      return;
    }
    if (interaction === 'cafe' && world.player.money < 450) {
      setNotice('You need £4.50 to buy coffee.');
      return;
    }
    onActivity(interaction, offset);
    setNotice(interaction === 'gig' ? 'Market shift completed — £35 earned.'
      : interaction === 'cafe' ? 'Coffee break — wellbeing restored.'
      : 'A peaceful afternoon in the gardens.');
  };
  const tapToWalk = (localX: number, localY: number) => {
    if (!loaded || paused || panel !== 'none') return;
    const p = hero.current;
    const tap = {
      x: Math.floor((localX - cameraPoint.current.x) / TILE),
      y: Math.floor((localY - cameraPoint.current.y) / TILE),
    };
    const from = { x: Math.round(p.x), y: Math.round(p.y) };
    const npc = npcAt(p.place);
    const talking = tap.x === npc.x && tap.y === npc.y;
    const target = targetForTap(p.place, tap, from);
    if (!target) {
      setNotice('That destination is blocked. Tap a clear path instead.');
      return;
    }
    const path = findTileRoute(p.place, from, target);
    if (!path.length && (target.x !== from.x || target.y !== from.y)) {
      setNotice('No route there yet. Try a different street.');
      return;
    }
    routeRef.current = path;
    talkAfterWalk.current = talking;
    if (talking && !path.length) startChat();
    else setNotice(talking ? 'Walking over to Amelia…' : 'Tap-to-walk · touch directions to steer manually');
  };
  const saveMission = () => {
    const title = safeText(missionTitle).slice(0, 80);
    if (!title) return;
    const term = missionTerm === 'lifetime'
      ? null : missionTerm === 'five'
        ? Math.floor(ageMonths / 12) + 5 : undefined;
    const goal = newMission(String(Date.now()) + ':' + Math.random().toString(36).slice(2, 7),
      title, missionDescription, missionGoal, ageMonths, term);
    setMissions(previous => [...previous, goal].slice(-500));
    setMissionTitle(''); setMissionDescription('');
    setNotice('New mission added: ' + title);
  };
  const togglePersonal = (id: string) => {
    setMissions(all => all.map(m =>
      m.id === id && m.goal === 'personal' && !missionExpired(m, ageMonths)
        ? { ...m, completed: !m.completed, completedAge: !m.completed ? ageMonths : undefined }
        : m,
    ));
  };

  return (
    <View style={[s.root, { width, height }]} testID="liveit-continuous-pixel-life">
      <View style={s.world} onLayout={event => {
        const { width: w, height: h } = event.nativeEvent.layout;
        if (w !== size.width || h !== size.height) setSize({ width: w, height: h });
      }}>
        <Animated.View pointerEvents="none"
          style={[s.map, { width: worldWidth, height: worldHeight, overflow: 'visible' },
            { transform: camera.getTranslateTransform() }]}>
          {tiles}
          {place === 'street' ? (
            <>
              <PixelBuilding x={3} y={2} w={6} h={4} roof="#a45a53"
                accent="#e3a769" label="MARKET CAFÉ" />
              <PixelBuilding x={20} y={2} w={8} h={6} roof="#6b7d89"
                accent="#ebc785" label="THE GENERAL STORE" />
              <PixelBuilding x={3} y={15} w={8} h={6} roof="#7b5985"
                accent="#d7a5ac" label="BELLWEATHER HOMES" />
            </>
          ) : null}
          <View style={[s.npcShadow, { left: npc.x * TILE + 8, top: npc.y * TILE + 37 }]} />
          {modernNPC ? (
            <View style={{ position: 'absolute', left: npc.x * TILE,
              top: (npc.y - 1) * TILE, width: TILE, height: TILE * 2,
              overflow: 'hidden' }}>
              <Image source={modernNPC} resizeMode="stretch" style={[{
                position: 'absolute', left: -18 * TILE, top: 0,
                width: TILE * 24, height: TILE * 2,
              }, crisp]} />
            </View>
          ) : (
            <Image source={actorArt(2, 'down')} resizeMode="stretch"
              style={[{ position: 'absolute', left: npc.x * TILE,
                top: npc.y * TILE, width: TILE, height: TILE }, crisp]} />
          )}
          <Animated.View style={[s.hero,
            modernPlayer ? { top: -TILE, height: TILE * 2 } : null,
            { transform: [
              ...pose.getTranslateTransform(),
              { translateY: bob },
            ] },
          ]}>
            <View style={s.heroShadow} />
            <View style={{ width: TILE, height: modernPlayer ? TILE * 2 : TILE,
              overflow: 'hidden' }}>
              <Animated.Image
                source={modernPlayer || pixelArt[('n1_' + facing + '_sheet') as PixelArtKey]}
                resizeMode="stretch"
                style={[{ width: TILE * (modernPlayer ? 24 : 4),
                  height: TILE * (modernPlayer ? 2 : 1),
                  transform: [{ translateX: frameOffset }] }, crisp]} />
            </View>
          </Animated.View>
        </Animated.View>
        <Animated.View pointerEvents="none" style={[s.daylight, { opacity: glow }]} />
        <Pressable accessibilityRole="button" accessibilityLabel="Tap town to walk or tap Amelia to talk"
          onPress={(event) => tapToWalk(event.nativeEvent.locationX, event.nativeEvent.locationY)}
          style={StyleSheet.absoluteFill} />
        <View style={s.topHud} pointerEvents="box-none">
          <View style={s.brand}>
            <Text style={s.brandName}>LIVEIT <Text style={{color: COLORS.gold}}>✦</Text></Text>
            <Text style={s.sub}>{place === 'cafe' ? 'THE OLD CAFÉ' : zone === 'garden'
              ? 'BELLWEATHER GARDENS' : zone === 'market'
                ? 'MARKET / SHOPS' : 'BELLWEATHER CITY'}</Text>
          </View>
          <View style={s.clockBox}>
            <Text style={s.clockText}>☀ {clockLabel}</Text>
            <Text style={s.sub}>DAY {dayWithinMonth}/30 · AGE {Math.floor(ageMonths / 12)}y {ageMonths % 12}m</Text>
            <Text style={s.sub}>{stage.toUpperCase()} · {biome.toUpperCase()} · {openChunk.cx},{openChunk.cy}</Text>
            <View style={s.clockTrack}><View style={[s.clockFill, {width: monthPart + '%'}]} /></View>
          </View>
        </View>
        <View style={s.leftButtons}>
          <HudButton title="☷" detail="MISSION" onPress={() => {pauseMovement(); setPanel('missions');}} />
          <HudButton title="✧" detail="STORIES" onPress={() => onNavigate('stories')} />
          <HudButton title="♫" detail="PEOPLE" onPress={() => onNavigate('people')} />
          <HudButton title="⚙" detail="LOCAL AI" onPress={() => {pauseMovement(); setPanel('settings');}} />
        </View>
        {ageYears < 18 ? (
          <View style={{
            position:'absolute',left:90,right:10,top:105,maxWidth:440,
            backgroundColor:'#292235ef',borderWidth:2,borderColor:'#f2c483',
            borderRadius:12,padding:12,gap:9,
          }}>
            <Text style={{fontSize:18,fontWeight:'900',color:'#ffdda4'}}>
              {stage === 'infant' ? 'YOUR FIRST YEARS' :
                stage === 'toddler' ? 'DISCOVER CHILDHOOD' :
                stage === 'child' ? 'SCHOOL & FRIENDS' : 'YOUR TEEN YEARS'}
            </Text>
            <Text style={{color:'#fff0cc',fontSize:12,lineHeight:19}}>
              {stage === 'infant' ? 'You were born in Bellweather. Your parents look after you while you learn to explore your world.'
                : stage === 'toddler' ? 'Meet people, play, and discover what you love.'
                : stage === 'child' ? 'Your days revolve around family, school, friends and curiosity.'
                : 'Adolescence brings independence, friendships, school and decisions about your future.'}
            </Text>
            <Text style={{color:'#e3d2c1',fontSize:11}}>
              WELLBEING {world.player.wellbeing}% · LEARNING {world.player.skill} · FAMILY {world.relationships[0]?.trust ?? 0}%
            </Text>
            <View style={{flexDirection:'row',flexWrap:'wrap',gap:6}}>
              {([
                ['bond','♥ FAMILY'],['play','✦ PLAY'],['rest','☾ REST'],
                ...(ageYears>=2 ? [['learn','⌁ LEARN']] : []),
                ...(ageYears>=5 ? [['study','✎ STUDY'],['make_friend','☻ FRIENDS']] : []),
              ] as Array<[ChildhoodActivity,string]>).map(([activity,label])=>(
                <Pressable key={activity} accessibilityRole="button"
                  onPress={() => {
                    const dayOffset=Math.min(29,Math.floor(clockRef.current/(MONTH_MS/30)));
                    const tag='child_act:'+(world.day+dayOffset)+':'+activity;
                    if(world.facts.includes(tag)) {
                      setNotice('You already did '+label.toLowerCase()+' today. Enjoy something else.');
                    } else {
                      onChildAction(activity,dayOffset);
                      setNotice(label+' — your childhood memory and stats have changed.');
                    }
                  }}
                  style={{backgroundColor:'#6e536d',paddingHorizontal:10,paddingVertical:9,borderRadius:8}}>
                  <Text style={{color:'#fff4db',fontWeight:'800',fontSize:12}}>{label}</Text>
                </Pressable>
              ))}
            </View>
            <Text style={{color:'#e3d2c1',fontSize:10}}>Active game time: one real hour ages one month. Optional skips preserve an age-appropriate milestone history.</Text>
            <View style={{flexDirection:'row',flexWrap:'wrap',gap:6}}>
              {([2,5,13,18] as const).filter(a=>a>ageYears).map(years=>(
                <Pressable key={years} onPress={()=>onSkipChildhood(years)} accessibilityRole="button"
                  style={{borderWidth:1,borderColor:'#b99a79',borderRadius:7,padding:7}}>
                  <Text style={{color:'#ffe6ae',fontSize:10,fontWeight:'800'}}>SKIP TO {years}Y</Text>
                </Pressable>
              ))}
            </View>
          </View>
        ) : null}

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
              <Pressable onPress={interact} style={s.storyButton} accessibilityRole="button"
                accessibilityLabel={zone === 'market' ? 'Work a market shift' : zone === 'garden' ? 'Rest in the garden' : zone === 'cafe' ? 'Buy coffee' : 'Explore'}>
                <Text style={s.talkIcon}>{zone === 'market' ? '⚒' : zone === 'garden' ? '☘' : zone === 'cafe' ? '☕' : '✧'}</Text>
                <Text style={s.actionLabel}>{zone === 'market' ? 'WORK' : zone === 'garden' ? 'REST' : zone === 'cafe' ? 'BUY' : 'ACT'}</Text>
              </Pressable>
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
                <Text style={s.mode}>{modelMode === 'local' ? '● ' + localModel.toUpperCase() + ' · CONNECTED' : modelMode === 'error' ? '● LOCAL AI OFFLINE — MESSAGE NOT SENT' : '○ LOCAL AI NOT YET VERIFIED'}</Text>
                {aiError ? <Text accessibilityRole="alert" style={[s.help,{color:'#ffbbad',marginBottom:8}]}>{aiError}</Text> : null}
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
                  <Pressable key={m.id} onPress={() => togglePersonal(m.id)}
                    disabled={(m.goal ?? 'personal') !== 'personal' || missionExpired(m, ageMonths)}
                    style={[s.quest, (m.completed || missionExpired(m, ageMonths)) && { opacity: 0.55 }]}>
                    <Text style={s.questTitle}>{m.completed ? '✓ ' : missionExpired(m, ageMonths) ? '⌛ EXPIRED · ' : '◇ '}{m.title}</Text>
                    <Text style={s.help}>{m.description || 'Explore and make your own meaning.'}</Text>
                    <Text style={s.mode}>{MISSION_GOALS.find(g => g.id === (m.goal ?? 'personal'))?.label ?? 'Personal objective'} · {m.expiresAge === undefined ? 'LIFETIME' : 'UNTIL AGE ' + Math.floor(m.expiresAge / 12)}</Text>
                  </Pressable>
                ))}
                <Text style={s.help}>Missions belong to your Free Life, not a separate campaign. Complete physical objectives by playing; personally defined tasks can be marked manually. Choose when a new mission expires.</Text>
                <Text style={s.speaker}>CREATE A MISSION</Text>
                <Text style={s.help}>WHAT COUNTS AS COMPLETION?</Text>
                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 6 }}>
                  {MISSION_GOALS.map(goal => (
                    <Pressable accessibilityRole="button"
                      accessibilityState={{ selected: goal.id === missionGoal }}
                      key={goal.id} onPress={() => setMissionGoal(goal.id)}
                      style={[s.suggestion, goal.id === missionGoal ? { backgroundColor: '#74516c' } : null]}>
                      <Text style={s.suggestionText}>{goal.label}</Text>
                    </Pressable>
                  ))}
                </View>
                <Text style={s.help}>{MISSION_GOALS.find(g => g.id === missionGoal)?.hint}</Text>
                <Text style={s.speaker}>HOW LONG IS THIS MISSION AVAILABLE?</Text>
                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 6 }}>
                  {([
                    ['birthday', 'Until next birthday'],
                    ['five', 'Five years'],
                    ['lifetime', 'Whole lifetime'],
                  ] as const).map(([id, label]) => (
                    <Pressable key={id} onPress={() => setMissionTerm(id)}
                      accessibilityRole="button"
                      accessibilityState={{selected: missionTerm === id}}
                      style={[s.suggestion, missionTerm === id ? {backgroundColor:'#74516c'} : null]}>
                      <Text style={s.suggestionText}>{label}</Text>
                    </Pressable>
                  ))}
                </View>
                <TextInput style={s.field} value={missionTitle} onChangeText={setMissionTitle} placeholder="Mission title" placeholderTextColor="#a1a4ad" maxLength={80} />
                <TextInput style={[s.field, {minHeight: 90}]} multiline value={missionDescription} onChangeText={setMissionDescription} placeholder="What would you like to accomplish?" placeholderTextColor="#a1a4ad" maxLength={500}/>
                <Pressable style={s.add} onPress={saveMission}><Text style={s.addText}>+ ADD TO MY LIFE</Text></Pressable>
                <Pressable style={s.storyLink} onPress={onTalk}><Text style={s.storyLinkText}>Play the official Amelia quest →</Text></Pressable>
              </ScrollView>
            ) : (
              <View style={{gap:12}}>
                <Text style={s.help}>The default is qwen3:4b (already downloaded on some development machines). On your Mac run: ollama pull qwen3:4b, then ollama serve. On an iPhone, enter the Mac's LAN IP (not localhost). If unavailable, the game uses clearly labelled offline dialogue.</Text>
                <Text style={s.speaker}>YOUR WALKABLE PIXEL AVATAR</Text>
                {localArt.player_modern ? (
                  <View style={{flexDirection:'row',flexWrap:'wrap',gap:7}}>
                    {(['adam','alex','bob','amelia'] as const).map(name => (
                      <Pressable accessibilityRole="button" key={name}
                        accessibilityState={{selected:pixelAvatar===name}}
                        onPress={() => setPixelAvatar(name)}
                        style={[s.suggestion,pixelAvatar===name ? {backgroundColor:'#74516c'} : null]}>
                        <Text style={s.suggestionText}>{name.toUpperCase()}</Text>
                      </Pressable>
                    ))}
                  </View>
                ) : <Text style={s.help}>Using the public CC0 pixel character.
                  Install your Modern Interiors ZIP locally to unlock four
                  additional animated character sheets; no raw art is uploaded.</Text>}
                <Text style={s.help}>Sprite selection is an interim override.
                  Full hairstyle, outfit and skin palette mapping from Character Creator
                  remains an unfinished part of the art system.</Text>
                <Text style={s.speaker}>MODEL QUALITY / LATENCY</Text>
                <View style={{flexDirection:'row', flexWrap:'wrap', gap:8}}>
                  {(['qwen3:0.6b','qwen3:1.7b','qwen3:4b'] as const).map(model => (
                    <Pressable key={model} accessibilityRole="button"
                      accessibilityState={{selected:localModel===model}}
                      onPress={() => setLocalModel(model)}
                      style={[s.suggestion, localModel===model ? {backgroundColor:'#74516c'} : null]}>
                      <Text style={s.suggestionText}>{model}</Text>
                    </Pressable>
                  ))}
                </View>
                <Text style={s.help}>0.6B is quickest; 1.7B balances quality and speed; 4B generally handles longer context better but takes more RAM. All run on your machine, not a paid cloud API.</Text>
                <Text style={s.speaker}>OLLAMA BASE URL</Text>
                <TextInput autoCapitalize="none" autoCorrect={false} style={s.field} value={endpoint} onChangeText={setEndpoint} placeholder="http://192.168.1.100:11434" placeholderTextColor="#919da3"/>
                <Pressable style={s.add} onPress={() => {void AsyncStorage.multiSet([['liveit.localOllamaEndpoint', endpoint], ['liveit.localOllamaModel', localModel], [gameKey + '.pixelAvatar', pixelAvatar]]); setPanel('none');}}><Text style={s.addText}>SAVE LOCAL CONNECTION</Text></Pressable>
                <Pressable style={[s.add,{backgroundColor:'#a6d7b7'}]} onPress={() => { void (async () => {
                  setAiStatus('Checking Ollama…');
                  try {
                    const res = await fetch(endpoint.trim().replace(/\/+$/, '') + '/api/tags');
                    if (!res.ok) throw new Error('HTTP ' + res.status);
                    const data: unknown = await res.json();
                    const models = (data as {models?:Array<{name?:string}>}).models ?? [];
                    if (!models.some(item => item.name === localModel))
                      throw new Error(localModel + ' is not installed. Run: ollama pull ' + localModel);
                    setAiStatus('Connected: ' + localModel + ' is installed and reachable.');
                    setAiError(''); setModelMode('local');
                  } catch(e) {
                    setAiStatus('Connection failed: ' + (e instanceof Error ? e.message : String(e)));
                    setModelMode('error');
                  }
                })(); }}><Text style={s.addText}>TEST ACTUAL OLLAMA CONNECTION</Text></Pressable>
                <Text style={s.help}>{aiStatus}</Text>
                <Text style={s.help}>On Mac web: run ollama serve and open this game from a permitted origin. For browser CORS launch the Ollama process with OLLAMA_ORIGINS=http://localhost:8081 (restart the daemon if already running). On your phone use the Mac's LAN address and bind Ollama to the LAN network deliberately; do not expose port 11434 to the public Internet.</Text>
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
