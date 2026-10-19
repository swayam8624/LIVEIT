import React, { useEffect, useRef, useState } from 'react';
import { Image, Pressable, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { World } from '@living/world-schema';
import { pixelArt, actorArt, type PixelArtKey } from './pixelArt';
import {
  INITIAL_POSITION, CAFE_WIDTH, CAFE_HEIGHT, STREET_WIDTH, STREET_HEIGHT,
  isNpcAdjacent, movePixel, npcAt, pixelCell, validPixelPosition,
  type Facing, type PixelPosition,
} from './pixelTownLogic';

const TILE = 28;
const ink = '#F5F2D9';
const mint = '#97E6AC';
const board = '#101827';
const control = '#273a49';

export function PixelTown({ world, onTalk }: { world: World; onTalk?: () => void }) {
  const { width } = useWindowDimensions();
  const cols = width < 390 ? 9 : 11;
  const rows = 9;
  const storageKey = 'liveit.pixel-town.' + world.timelineId;
  const [position, setPosition] = useState<PixelPosition>(INITIAL_POSITION);
  const [ready, setReady] = useState(false);
  const [message, setMessage] = useState('Walk through Bellweather. Find Amelia or enter the café.');
  const pendingWrite = useRef<Promise<unknown>>(Promise.resolve());
  const currentPosition = useRef<PixelPosition>(INITIAL_POSITION);
  const holdTimer = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    let mounted = true;
    setReady(false);
    currentPosition.current = INITIAL_POSITION;
    setPosition(INITIAL_POSITION);
    void AsyncStorage.getItem(storageKey).then((raw) => {
      if (!mounted) return;
      let loaded: unknown = INITIAL_POSITION;
      try { loaded = raw ? JSON.parse(raw) : INITIAL_POSITION; } catch { /* corrupt data */ }
      const next = validPixelPosition(loaded) ? loaded : INITIAL_POSITION;
      currentPosition.current = next;
      setPosition(next);
      setReady(true);
    }).catch(() => {
      if (mounted) {
        currentPosition.current = INITIAL_POSITION;
        setReady(true);
        setMessage('Walking works, but local coordinate storage is unavailable.');
      }
    });
    return () => { mounted = false; };
  }, [storageKey]);

  const move = (direction: Facing) => {
    if (!ready) return;
    const result = movePixel(currentPosition.current, direction);
    currentPosition.current = result.position;
    setPosition(result.position);
    const snapshot = JSON.stringify(result.position);
    pendingWrite.current = pendingWrite.current.catch(() => undefined)
      .then(() => AsyncStorage.setItem(storageKey, snapshot));
    void pendingWrite.current.catch(() => setMessage('Could not save this position.'));
    if (result.event === 'entered-cafe') setMessage('The café bell rings. Amelia might be nearby.');
    else if (result.event === 'left-cafe') setMessage('Back on Bellweather Market street.');
    else if (result.event === 'npc-nearby') setMessage('Amelia is right beside you. Press TALK.');
    else if (result.event === 'blocked') setMessage('That way is blocked.');
    else setMessage('Move beside Amelia to talk. The café door is on the south wall.');
  };

  // Long-press movement remains deterministic: each repeat reads the latest
  // tile ref, rather than a stale React render captured at press time.
  const stopHeldWalk = () => {
    if (holdTimer.current) clearInterval(holdTimer.current);
    holdTimer.current = null;
  };
  const startHeldWalk = (direction: Facing) => {
    stopHeldWalk();
    if (!ready) return;
    holdTimer.current = setInterval(() => move(direction), 135);
  };
  useEffect(() => () => {
    if (holdTimer.current) clearInterval(holdTimer.current);
  }, []);

  const talk = () => {
    if (!ready) return;
    if (!isNpcAdjacent(position)) {
      setMessage('Move next to Amelia, then press TALK.');
      return;
    }
    if (onTalk) onTalk();
    else setMessage('Amelia is ready to talk, but the story callback is missing.');
  };

  const mapWidth = position.place === 'street' ? STREET_WIDTH : CAFE_WIDTH;
  const mapHeight = position.place === 'street' ? STREET_HEIGHT : CAFE_HEIGHT;
  const left = Math.min(Math.max(0, position.x - Math.floor(cols / 2)), Math.max(0, mapWidth - cols));
  const top = Math.min(Math.max(0, position.y - Math.floor(rows / 2)), Math.max(0, mapHeight - rows));
  const npc = npcAt(position.place);
  const cells: React.ReactElement[] = [];
  for (let ry = 0; ry < rows; ry++) {
    for (let rx = 0; rx < cols; rx++) {
      const x = rx + left;
      const y = ry + top;
      const tile = pixelCell(position.place, x, y);
      const actorHere = position.x === x && position.y === y;
      const npcHere = npc.x === x && npc.y === y;
      const sourceKey: PixelArtKey = tile.prop && tile.prop in pixelArt
        ? tile.prop as PixelArtKey
        : tile.terrain === 'grass2' ? 'grass' : tile.terrain;
      const distance = Math.abs(x - position.x) + Math.abs(y - position.y);
      const tap = npcHere ? talk : tile.portal && distance === 1
        ? () => move(x < position.x ? 'left' : x > position.x ? 'right' : y < position.y ? 'up' : 'down')
        : undefined;
      cells.push(
        <Pressable
          key={x + ':' + y}
          onPress={tap}
          accessible={Boolean(tap)}
          accessibilityRole={tap ? 'button' : undefined}
          accessibilityLabel={npcHere ? 'Talk to Amelia' : tile.portal ? 'Café door' : actorHere ? 'Player' : undefined}
          style={s.tile}
        >
          <Image resizeMode="stretch" source={{ uri: pixelArt[sourceKey] }} style={s.image} />
          {actorHere || npcHere ? (
            <Image
              source={{ uri: actorArt(actorHere ? 1 : 2, actorHere ? position.facing : 'down') }}
              resizeMode="stretch"
              style={s.image}
            />
          ) : null}
        </Pressable>,
      );
    }
  }
  return (
    <View style={s.root} testID="liveit-pixel-world">
      <View style={s.header}>
        <View>
          <Text style={s.eyebrow}>◈ LIVEIT / PIXEL LIFE</Text>
          <Text style={s.title}>{position.place === 'street' ? 'BELLWEATHER MARKET' : 'THE MARKET CAFÉ'}</Text>
        </View>
        <Text style={s.eyebrow}>DAY {world.day + 1}{'\n'}{position.x},{position.y}</Text>
      </View>
      <View
        style={[s.viewport, { width: cols * TILE, height: rows * TILE }]}
        accessibilityLabel={'Walkable pixel map: ' + position.place + ', position ' + position.x + ', ' + position.y}
      >
        {cells}
        <View pointerEvents="none" style={s.mapTag}><Text style={s.tagText}>{position.place === 'street' ? 'MARKET / EXTERIOR' : 'MARKET / CAFÉ'}</Text></View>
      </View>
      <View style={s.notice} accessibilityLiveRegion="polite"><Text style={s.noticeText}>{message}</Text></View>
      <View style={s.controls}>
        <View>
          <View style={s.padRow}><View style={s.empty} /><Pad direction="up" glyph="▲" disabled={!ready} onPress={() => move('up')} onLongPress={() => startHeldWalk('up')} onPressOut={stopHeldWalk} /><View style={s.empty} /></View>
          <View style={s.padRow}><Pad direction="left" glyph="◀" disabled={!ready} onPress={() => move('left')} onLongPress={() => startHeldWalk('left')} onPressOut={stopHeldWalk} /><View style={s.empty} /><Pad direction="right" glyph="▶" disabled={!ready} onPress={() => move('right')} onLongPress={() => startHeldWalk('right')} onPressOut={stopHeldWalk} /></View>
          <View style={s.padRow}><View style={s.empty} /><Pad direction="down" glyph="▼" disabled={!ready} onPress={() => move('down')} onLongPress={() => startHeldWalk('down')} onPressOut={stopHeldWalk} /><View style={s.empty} /></View>
        </View>
        <Pressable accessibilityRole="button" accessibilityLabel="Talk to Amelia" disabled={!ready} onPress={talk} style={s.talk}>
          <Text style={s.talkLetter}>A</Text><Text style={s.talkLabel}>TALK</Text>
        </Pressable>
        <View><Text style={s.eyebrow}>AMELIA</Text><Text style={s.hint}>{isNpcAdjacent(position) ? '● NEAR YOU' : '○ FIND HER'}</Text><Text style={s.hint}>TAP DOORS</Text></View>
      </View>
      <Text style={s.footer}>CC0 pixel art · Real collisions · Position saved locally</Text>
    </View>
  );
}
function Pad({ direction, glyph, onPress, onLongPress, onPressOut, disabled }: {
  direction: Facing; glyph: string; onPress: () => void; onLongPress: () => void; onPressOut: () => void; disabled: boolean;
}) {
  return (
    <Pressable testID={'pixel-move-' + direction} accessibilityRole="button" accessibilityLabel={'Walk ' + direction}
      disabled={disabled} onPress={onPress} onLongPress={onLongPress} onPressOut={onPressOut}
      delayLongPress={310} style={({ pressed }) => [s.pad, pressed && { opacity: 0.6 }]}>
      <Text style={s.padText}>{glyph}</Text>
    </Pressable>
  );
}
const s = StyleSheet.create({
  root: { backgroundColor: board, borderColor: '#507174', borderWidth: 2, borderRadius: 10, padding: 10, gap: 10, alignItems: 'center' },
  header: { width: '100%', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  eyebrow: { color: mint, fontWeight: '800', fontSize: 10, letterSpacing: 1 },
  title: { color: ink, fontWeight: '900', fontSize: 17, letterSpacing: 0.5 },
  viewport: { backgroundColor: '#375c58', overflow: 'hidden', flexDirection: 'row', flexWrap: 'wrap' },
  tile: { width: TILE, height: TILE, overflow: 'hidden', position: 'relative' },
  image: { width: TILE, height: TILE, position: 'absolute' },
  mapTag: { backgroundColor: '#101827E0', padding: 4, position: 'absolute', top: 4, left: 4 },
  tagText: { color: ink, fontSize: 9, fontWeight: '900' },
  notice: { width: '100%', minHeight: 40, justifyContent: 'center', backgroundColor: '#25384a', borderLeftWidth: 3, borderLeftColor: '#ffd28a', padding: 8 },
  noticeText: { color: ink, fontSize: 12 },
  controls: { flexDirection: 'row', gap: 12, justifyContent: 'space-evenly', alignItems: 'center', width: '100%' },
  padRow: { flexDirection: 'row' },
  empty: { width: 42, height: 42 },
  pad: { width: 42, height: 42, backgroundColor: control, borderWidth: 1, borderColor: '#507174', alignItems: 'center', justifyContent: 'center', borderRadius: 5 },
  padText: { color: ink, fontSize: 19, fontWeight: '800' },
  talk: { width: 74, height: 74, backgroundColor: mint, borderRadius: 40, alignItems: 'center', justifyContent: 'center', borderWidth: 3, borderColor: '#d1ffd8' },
  talkLetter: { color: board, fontSize: 26, fontWeight: '900' },
  talkLabel: { color: board, fontSize: 10, fontWeight: '900' },
  hint: { fontSize: 10, color: ink, marginTop: 4 },
  footer: { color: '#b6c6c8', textAlign: 'center', fontSize: 10 },
});
