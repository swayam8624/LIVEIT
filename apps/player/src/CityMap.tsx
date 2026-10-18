import React, { useMemo, useState } from 'react';
import { Image, Pressable, StyleSheet, Text, View } from 'react-native';
import {
  DISTRICTS,
  generateCityScene,
  projectCityBlock,
} from '@living/simulation-core';
import type { District } from '@living/world-schema';
import { gameTheme as t } from './gameTheme';

/* Original city layout with CC0 Kenney isometric sprite placeholders. */
/* eslint-disable @typescript-eslint/no-require-imports */
const buildings = [
  require('../assets/buildings/building-002.png'),
  require('../assets/buildings/building-003.png'),
  require('../assets/buildings/building-004.png'),
  require('../assets/buildings/building-010.png'),
  require('../assets/buildings/building-000.png'),
];
/* eslint-enable @typescript-eslint/no-require-imports */

const landmarks = [
  { x: 0.18, y: 0.27 },
  { x: 0.49, y: 0.16 },
  { x: 0.81, y: 0.3 },
  { x: 0.32, y: 0.69 },
  { x: 0.73, y: 0.71 },
] as const;

const preview = generateCityScene(0xb311);

export function CityMap({
  selected,
  onVisit,
  day,
  hotspots,
}: {
  selected: District;
  onVisit: (district: District) => void;
  day: number;
  hotspots: readonly District[];
}) {
  const [width, setWidth] = useState(350);
  const [zoom, setZoom] = useState(1);
  const [night, setNight] = useState(true);
  const compact = width < 520;
  const height = compact ? 405 : 500;
  const spriteSize = compact ? 62 : 84;
  const markerSize = compact ? 113 : 142;
  const blocks = useMemo(
    () =>
      preview.blocks
        .filter((_, index) => index % 2 === 0)
        .map((block) => ({
          block,
          position: projectCityBlock(block, width, height, zoom),
        }))
        .sort((a, b) => a.block.x + a.block.z - (b.block.x + b.block.z)),
    [width, height, zoom],
  );
  return (
    <View
      testID="city-viewport"
      accessibilityLabel="Explorable isometric Bellweather with selectable neighborhoods"
      style={[styles.viewport, { height }, night ? styles.night : styles.day]}
      onLayout={(e) => {
        const next = Math.round(e.nativeEvent.layout.width);
        if (next > 0 && next !== width) setWidth(next);
      }}
    >
      <View pointerEvents="none" style={styles.skyline} />
      <View pointerEvents="none" style={styles.island}>
        <View style={styles.avenueVertical} />
        <View style={styles.avenueHorizontal} />
        <View style={styles.river} />
        {blocks.map(({ block, position }) => {
          const size = (spriteSize * position.scale * zoom) / 1.35;
          return (
            <Image
              key={block.id}
              source={buildings[block.palette]}
              accessibilityLabel={`3D-style illustration of ${block.district} building`}
              resizeMode="contain"
              style={{
                position: 'absolute',
                width: size,
                height: size,
                left: position.left - size / 2,
                top: position.top - size / 2,
                opacity: night ? 0.83 : 0.95,
              }}
            />
          );
        })}
      </View>
      <View style={styles.header}>
        <View style={styles.titleGroup} pointerEvents="none">
          <Text style={styles.hud}>◆ BELLWEATHER / DAY {day + 1}</Text>
          <Text style={styles.heading}>CHOOSE YOUR DISTRICT</Text>
        </View>
        <View style={styles.toolbar}>
          <Pressable
            testID="city-camera-zoom-out"
            accessibilityRole="button"
            accessibilityLabel="Zoom city map out"
            disabled={zoom <= 0.8}
            onPress={() =>
              setZoom((value) => Math.max(0.8, +(value - 0.2).toFixed(1)))
            }
            style={({ pressed }) => [styles.control, pressed && styles.pressed]}
          >
            <Text style={styles.controlText}>−</Text>
          </Pressable>
          <Text style={styles.zoom}>{Math.round(zoom * 100)}%</Text>
          <Pressable
            testID="city-camera-zoom-in"
            accessibilityRole="button"
            accessibilityLabel="Zoom city map in"
            disabled={zoom >= 1.4}
            onPress={() =>
              setZoom((value) => Math.min(1.4, +(value + 0.2).toFixed(1)))
            }
            style={({ pressed }) => [styles.control, pressed && styles.pressed]}
          >
            <Text style={styles.controlText}>+</Text>
          </Pressable>
        </View>
      </View>
      {DISTRICTS.map((district, index) => {
        const pos = landmarks[index]!;
        const active = selected === district.id;
        return (
          <Pressable
            key={district.id}
            testID={`city-district-${district.id}`}
            accessibilityRole="button"
            accessibilityLabel={'Travel to ' + district.title}
            accessibilityState={{ selected: active }}
            onPress={() => onVisit(district.id)}
            style={({ pressed }) => [
              styles.landmark,
              {
                width: markerSize,
                left: Math.max(
                  0,
                  Math.min(width - markerSize, width * pos.x - markerSize / 2),
                ),
                top: height * pos.y - (compact ? 27 : 38),
              },
              pressed && styles.pressed,
            ]}
          >
            <Image
              source={buildings[index]}
              style={{ width: compact ? 62 : 88, height: compact ? 57 : 83 }}
              resizeMode="contain"
            />
            <View style={[styles.districtBadge, active && styles.active]}>
              <Text
                style={[styles.districtTitle, active && styles.activeTitle]}
                numberOfLines={1}
              >
                {district.title.toUpperCase()}
              </Text>
              <Text style={styles.districtAction}>
                {active ? '◆ CURRENT LOCATION' : hotspots.includes(district.id) ? '✦ EVENT AVAILABLE' : '○ ENTER DISTRICT'}
              </Text>
            </View>
          </Pressable>
        );
      })}
      <View style={styles.footer}>
        <Text style={styles.instructions}>◈ SELECT A BUILDING TO TRAVEL</Text>
        <Pressable
          testID="city-toggle-lighting"
          accessibilityRole="button"
          accessibilityLabel={
            night ? 'Preview city in daylight' : 'Preview city at night'
          }
          onPress={() => setNight((value) => !value)}
          style={({ pressed }) => [
            styles.lightToggle,
            pressed && styles.pressed,
          ]}
        >
          <Text style={styles.lightText}>{night ? '☾ NIGHT' : '☼ DAY'}</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  viewport: {
    width: '100%',
    borderRadius: 10,
    overflow: 'hidden',
    borderWidth: 2,
    borderColor: t.border,
    position: 'relative',
  },
  night: { backgroundColor: '#14283A' },
  day: { backgroundColor: '#4A7685' },
  skyline: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: '23%',
    height: '33%',
    backgroundColor: 'rgba(62,117,119,0.25)',
    transform: [{ skewY: '-7deg' }],
  },
  island: {
    position: 'absolute',
    width: '130%',
    height: '80%',
    left: '-15%',
    top: '19%',
    backgroundColor: '#355B58',
    borderWidth: 2,
    borderColor: '#5D9582',
    borderRadius: 26,
    transform: [{ rotate: '-2deg' }],
    overflow: 'hidden',
  },
  avenueVertical: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    left: '46%',
    width: '11%',
    backgroundColor: '#283D4D',
    transform: [{ rotate: '39deg' }],
    borderLeftWidth: 3,
    borderRightWidth: 3,
    borderColor: '#819D8B',
  },
  avenueHorizontal: {
    position: 'absolute',
    top: '49%',
    left: '-10%',
    width: '120%',
    height: '9%',
    backgroundColor: '#293E4C',
    transform: [{ rotate: '-22deg' }],
    borderTopWidth: 2,
    borderBottomWidth: 2,
    borderColor: '#728B83',
  },
  river: {
    position: 'absolute',
    left: '-7%',
    bottom: '5%',
    height: '15%',
    width: '140%',
    backgroundColor: '#2C7089',
    transform: [{ rotate: '-13deg' }],
    borderTopWidth: 3,
    borderColor: '#66B9BF',
  },
  header: {
    position: 'absolute',
    top: 10,
    left: 10,
    right: 10,
    flexDirection: 'row',
    gap: 6,
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  titleGroup: {
    flexShrink: 1,
    gap: 5,
    backgroundColor: 'rgba(12,25,35,0.88)',
    padding: 9,
    borderWidth: 1,
    borderColor: '#577B73',
  },
  hud: {
    color: t.neon,
    fontFamily: t.font.hud,
    fontSize: 9,
    letterSpacing: 0.5,
  },
  heading: {
    color: t.ink,
    fontFamily: t.font.display,
    fontSize: 14,
    fontWeight: '900',
  },
  toolbar: {
    flexDirection: 'row',
    gap: 3,
    alignItems: 'center',
    backgroundColor: '#122435',
    padding: 3,
    borderWidth: 1,
    borderColor: '#628A81',
  },
  control: {
    minWidth: 29,
    minHeight: 31,
    backgroundColor: t.panelRaised,
    alignItems: 'center',
    justifyContent: 'center',
  },
  controlText: { color: t.ink, fontSize: 20, fontWeight: '800' },
  pressed: { opacity: 0.72 },
  zoom: { fontSize: 9, color: t.amber, fontFamily: t.font.hud },
  landmark: {
    position: 'absolute',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 0,
    minHeight: 90,
  },
  districtBadge: {
    minWidth: 99,
    alignItems: 'center',
    paddingVertical: 6,
    paddingHorizontal: 5,
    borderRadius: 3,
    borderWidth: 1,
    backgroundColor: 'rgba(13,24,37,0.96)',
    borderColor: '#85A09A',
  },
  active: { borderColor: t.neon, borderWidth: 2, backgroundColor: '#18453F' },
  districtTitle: {
    color: t.ink,
    fontSize: 9,
    fontFamily: t.font.hud,
    fontWeight: '800',
  },
  activeTitle: { color: t.neon },
  districtAction: {
    color: t.amber,
    fontSize: 7,
    fontFamily: t.font.hud,
    marginTop: 4,
  },
  footer: {
    position: 'absolute',
    bottom: 9,
    left: 10,
    right: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 5,
  },
  instructions: {
    color: t.ink,
    fontSize: 8,
    fontFamily: t.font.hud,
    backgroundColor: '#132337DD',
    padding: 6,
    flexShrink: 1,
  },
  lightToggle: {
    backgroundColor: '#193F43',
    borderWidth: 1,
    borderColor: t.neon,
    padding: 8,
    minHeight: 30,
  },
  lightText: {
    color: t.neon,
    fontFamily: t.font.hud,
    fontSize: 10,
    fontWeight: '800',
  },
});
