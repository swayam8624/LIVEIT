import React, { useState } from 'react';
import { Image, Pressable, StyleSheet, Text, View } from 'react-native';
import { DISTRICTS } from '@living/simulation-core';
import type { District } from '@living/world-schema';

/**
 * A small explorable world map rather than a row of website cards.
 * Isometric buildings licensed CC0-1.0 by Kenney.
 * Positions are normalized to the stage width so touch targets stay stable
 * on portrait phones, tablets and desktop monitors.
 */

/* eslint-disable @typescript-eslint/no-require-imports */
const buildings = [
  require('../assets/buildings/building-002.png'),
  require('../assets/buildings/building-003.png'),
  require('../assets/buildings/building-004.png'),
  require('../assets/buildings/building-010.png'),
  require('../assets/buildings/building-000.png'),
];
const groundTiles = [
  require('../assets/city/tile-000.png'),
  require('../assets/city/tile-004.png'),
  require('../assets/city/tile-010.png'),
  require('../assets/city/tile-012.png'),
];
/* eslint-enable @typescript-eslint/no-require-imports */

const positions = [
  { x: 0.19, y: 0.2 },
  { x: 0.51, y: 0.14 },
  { x: 0.82, y: 0.25 },
  { x: 0.34, y: 0.66 },
  { x: 0.7, y: 0.68 },
] as const;
export function CityMap({
  selected,
  onVisit,
}: {
  selected: District;
  onVisit: (district: District) => void;
}) {
  const [width, setWidth] = useState(350);
  const compact = width < 520;
  const height = compact ? 340 : 430;
  const sprite = compact ? 83 : 126;
  const hit = compact ? 116 : 171;
  return (
    <View
      accessibilityLabel="Explorable Bellweather isometric city map"
      style={[styles.map, { height }]}
      onLayout={(event) => setWidth(event.nativeEvent.layout.width)}
    >
      <View pointerEvents="none" style={styles.mapGrid}>
        {[0, 1, 2, 3, 4, 5].map((row) => (
          <View key={row} style={styles.roadRow}>
            {[0, 1, 2, 3, 4, 5, 6].map((col) => (
              <Image
                key={col}
                source={groundTiles[(row + col) % groundTiles.length]}
                style={{
                  width: compact ? 56 : 84,
                  height: compact ? 56 : 84,
                  opacity: 0.18,
                }}
                resizeMode="contain"
              />
            ))}
          </View>
        ))}
      </View>
      <View pointerEvents="none" style={styles.mapCaption}>
        <Text style={styles.kicker}>✦ CITY OF BELLWEATHER</Text>
        <Text style={styles.subtitle}>
          Five neighborhoods. A lifetime of possibilities.
        </Text>
      </View>
      {DISTRICTS.map((district, index) => {
        const pos = positions[index]!;
        const active = selected === district.id;
        return (
          <Pressable
            key={district.id}
            accessibilityRole="button"
            accessibilityLabel={'Travel to ' + district.title}
            accessibilityState={{ selected: active }}
            onPress={() => onVisit(district.id)}
            style={({ pressed }) => [
              styles.mapStop,
              {
                width: hit,
                left: Math.max(
                  0,
                  Math.min(width - hit, width * pos.x - hit / 2),
                ),
                top: height * pos.y - (compact ? 26 : 28),
              },
              pressed && { opacity: 0.82 },
            ]}
          >
            <Image
              source={buildings[index]}
              style={{ width: sprite, height: sprite }}
              resizeMode="contain"
            />
            <View style={[styles.mapLabel, active && styles.mapLabelSelected]}>
              <Text style={styles.mapName} numberOfLines={1}>
                {district.title}
              </Text>
              <Text style={styles.mapActivity} numberOfLines={1}>
                {active ? '● YOUR LOCATION' : 'TAP TO VISIT ↗'}
              </Text>
            </View>
          </Pressable>
        );
      })}
      <View pointerEvents="none" style={styles.mapFooter}>
        <Text style={styles.mapFooterText}>
          EXPLORE THE CITY · THERE ARE NO TRAVEL TICKETS
        </Text>
      </View>
    </View>
  );
}
const styles = StyleSheet.create({
  map: {
    width: '100%',
    borderRadius: 17,
    backgroundColor: '#1a2c3d',
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#886c58',
    position: 'relative',
  },
  mapGrid: {
    position: 'absolute',
    left: -40,
    top: 13,
    right: 0,
    bottom: 0,
    opacity: 0.7,
    transform: [{ rotate: '-11deg' }],
  },
  roadRow: { flexDirection: 'row', gap: 2, marginTop: -4 },
  mapCaption: { position: 'absolute', left: 14, top: 13, right: 14 },
  kicker: {
    color: '#f5c68f',
    letterSpacing: 2,
    fontSize: 11,
    fontWeight: '800',
  },
  subtitle: { color: '#c6d2de', fontSize: 10, marginTop: 3 },
  mapStop: {
    position: 'absolute',
    alignItems: 'center',
    gap: 1,
    minHeight: 105,
    justifyContent: 'center',
    zIndex: 2,
  },
  mapLabel: {
    backgroundColor: 'rgba(9,19,31,.92)',
    borderColor: '#6e8597',
    borderWidth: 1,
    paddingVertical: 5,
    paddingHorizontal: 8,
    alignItems: 'center',
    borderRadius: 8,
    minWidth: 101,
  },
  mapLabelSelected: {
    backgroundColor: '#55342e',
    borderColor: '#f3bd7c',
    borderWidth: 2,
  },
  mapName: { color: '#fff0dc', fontSize: 11, fontWeight: '800' },
  mapActivity: {
    color: '#f4c68a',
    fontSize: 8,
    fontWeight: '800',
    marginTop: 2,
    letterSpacing: 0.3,
  },
  mapFooter: { position: 'absolute', bottom: 8, left: 10, right: 10 },
  mapFooterText: {
    color: '#d0c6b8',
    fontSize: 9,
    letterSpacing: 1,
    textAlign: 'center',
  },
});
