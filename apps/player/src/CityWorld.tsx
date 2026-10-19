import React, { useState } from 'react';
import {
  Image,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
/* Isometric city pieces by Kenney, CC0-1.0. Exact hashes in art registry. */
/* eslint-disable @typescript-eslint/no-require-imports */
const DISTRICT_BUILDINGS = [
  require('../assets/buildings/building-002.png'),
  require('../assets/buildings/building-003.png'),
  require('../assets/buildings/building-004.png'),
  require('../assets/buildings/building-010.png'),
  require('../assets/buildings/building-000.png'),
];
/* eslint-enable @typescript-eslint/no-require-imports */
// Independently verified Kenney CC0 assets, bundled offline from pinned source.
// eslint-disable-next-line @typescript-eslint/no-require-imports
const playIcon = require('../assets/kenney-play.png');
// eslint-disable-next-line @typescript-eslint/no-require-imports
const downIcon = require('../assets/kenney-down.png');
import {
  DISTRICTS,
  availableCityOpportunities,
  cityState,
  chooseCareer,
  resolveCityOpportunity,
  visitDistrict,
} from '@living/simulation-core';
import type { CareerPath, World } from '@living/world-schema';
import { PixelTown } from './PixelTown';
import { gameTheme as t, districtColors } from './gameTheme';

const CAREERS: {
  id: Exclude<CareerPath, 'undecided'>;
  name: string;
  description: string;
}[] = [
  {
    id: 'technology',
    name: 'Technology',
    description: 'Build useful things that change the city.',
  },
  {
    id: 'creative',
    name: 'Creative',
    description: 'Make art and stories people remember.',
  },
  {
    id: 'business',
    name: 'Business',
    description: 'Find an opportunity others missed.',
  },
  {
    id: 'community',
    name: 'Community',
    description: 'Work with people, not just for them.',
  },
];

/**
 * Standalone responsive city interactions; reads only validated World state
 * and delegates actual changes to the deterministic shared simulation engine.
 */
export function CityWorld({
  world,
  onAction,
  onTalk,
}: {
  world: World;
  onAction: (operation: (world: World) => World) => void;
  onTalk?: () => void;
}) {
  const [focused, setFocused] = useState<string | null>(null);
  const [careerOpen, setCareerOpen] = useState(false);
  const [showDistrictCards, setShowDistrictCards] = useState(false);
  const city = cityState(world);
  const events = availableCityOpportunities(world);
  const selected =
    events.find((event) => event.id === focused) ?? events[0] ?? null;
  return (
    <View style={styles.root} accessibilityLabel="Bellweather playable pixel town and city opportunities">
      <View style={styles.heading}>
        <View style={{ flex: 1, gap: 3 }}>
          <Text style={styles.eyebrow}>BELLWEATHER / PIXEL FREE ROAM</Text>
          <Text style={styles.title}>VISIT THE CITY</Text>
          <Text style={styles.caption}>
            Go somewhere. Meet someone. Choose what matters.
          </Text>
        </View>
        <View style={styles.cityHud}>
          <Text style={styles.hudLabel}>CITY REPUTATION</Text>
          <Text style={styles.hudValue}>{city.reputation}/100</Text>
          <Text style={styles.hudLabel}>
            CONNECTIONS {city.connections} · STRESS {city.stress}
          </Text>
        </View>
      </View>
      <View style={styles.mapControls}>
        <Text style={styles.eyebrow}>WORLD MAP · INTERACTIVE PIXEL LIFE</Text>
        <Pressable
          accessibilityRole="button"
          onPress={() => setShowDistrictCards((v) => !v)}
          style={styles.mapToggle}
        >
          <Text style={styles.mapToggleText}>
            {showDistrictCards ? '◈ BACK TO STREET' : '▤ DISTRICT TRAVEL'}
          </Text>
        </Pressable>
      </View>
      {!showDistrictCards ? (
        <PixelTown world={world} onTalk={onTalk} />      ) : (
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.districts}
          accessibilityLabel="City neighborhoods"
        >
          {DISTRICTS.map((district, index) => (
            <Pressable
              key={district.id}
              accessibilityRole="button"
              accessibilityState={{ selected: city.district === district.id }}
              onPress={() => onAction((w) => visitDistrict(w, district.id))}
              style={({ pressed }) => [
                styles.district,
                {
                  backgroundColor: districtColors[index],
                },
                city.district === district.id && styles.districtActive,
                pressed && { opacity: 0.8 },
              ]}
            >
              <Image
                source={DISTRICT_BUILDINGS[index]}
                style={styles.buildingSprite}
                resizeMode="contain"
                accessibilityLabel={
                  district.title + ' illustrated district building'
                }
              />
              <Text style={styles.districtSymbol}>
                {['☕', '✎', '⌘', '✦', '❀'][index]}
              </Text>
              <Text style={styles.districtName}>{district.title}</Text>
              <Text style={styles.districtSubtitle}>{district.tagline}</Text>
              <Text style={styles.districtAction}>
                {city.district === district.id
                  ? '● YOU ARE HERE'
                  : 'EXPLORE  →'}
              </Text>
            </Pressable>
          ))}
        </ScrollView>
      )}
      <View style={styles.storyHeading}>
        <View style={{ flex: 1, gap: 5 }}>
          <Text style={styles.eyebrow}>STORIES THE CITY TELLS</Text>
          <Text style={styles.titleSmall}>At a crossroads.</Text>
        </View>
        <Text style={styles.counter}>{events.length} waiting</Text>
      </View>
      {!selected ? (
        <View style={styles.empty}>
          <Text style={styles.emptyTitle}>
            Not every day has to be extraordinary.
          </Text>
          <Text style={styles.caption}>
            Spend time working, studying, resting or seeing friends. New
            encounters emerge as your life evolves, without tickets or real-time
            waiting.
          </Text>
        </View>
      ) : (
        <View style={styles.encounter}>
          <View style={styles.encounterTop}>
            <Text style={styles.eyebrow}>
              {DISTRICTS.find(
                (d) => d.id === selected.district,
              )?.title.toUpperCase()}{' '}
              · LIMITED MOMENT
            </Text>
            <Text style={styles.counter}>DAY {world.day + 1}</Text>
          </View>
          <Text style={styles.eventTitle}>{selected.title}</Text>
          <Text style={styles.eventDescription}>{selected.description}</Text>
          {events.length > 1 && (
            <View style={styles.eventPills}>
              {events.map((e) => (
                <Pressable
                  key={e.id}
                  accessibilityRole="button"
                  onPress={() => setFocused(e.id)}
                  style={[
                    styles.eventPill,
                    selected.id === e.id && styles.eventPillActive,
                  ]}
                >
                  <Text style={styles.eventPillText}>{e.title}</Text>
                </Pressable>
              ))}
            </View>
          )}
          <View style={styles.options}>
            {selected.choices.map((choice, i) => (
              <Pressable
                key={choice.id}
                accessibilityRole="button"
                accessibilityLabel={choice.label}
                onPress={() => {
                  onAction((w) =>
                    resolveCityOpportunity(w, selected.id, choice.id),
                  );
                  setFocused(null);
                }}
                style={({ pressed }) => [
                  styles.option,
                  pressed && styles.optionPressed,
                ]}
              >
                <Text style={styles.optionIndex}>0{i + 1}</Text>
                <Text style={styles.optionText}>{choice.label}</Text>
                <Image
                  source={playIcon}
                  style={styles.choiceIcon}
                  accessibilityLabel="Choose this option"
                />
              </Pressable>
            ))}
          </View>
          <Text style={styles.note}>
            Consequences are saved to this timeline. The choice will not be
            repeated.
          </Text>
        </View>
      )}
      <View style={styles.careerCard}>
        <View style={styles.careerTop}>
          <View style={{ flex: 1, gap: 4 }}>
            <Text style={styles.eyebrow}>YOUR AMBITIONS</Text>
            <Text style={styles.careerTitle}>
              {city.careerPath === 'undecided'
                ? 'What will you build?'
                : CAREERS.find((c) => c.id === city.careerPath)?.name}
            </Text>
            <Text style={styles.caption}>
              {city.careerPath === 'undecided'
                ? 'Choose a direction. It will shape future stories, rather than guarantee success.'
                : 'You have chosen a direction. Your progress still depends on what you do every day.'}
            </Text>
          </View>
          {city.careerPath === 'undecided' && (
            <Pressable
              accessibilityRole="button"
              onPress={() => setCareerOpen((p) => !p)}
              style={styles.careerButton}
            >
              <View style={styles.careerButtonRow}>
                <Text style={styles.careerButtonText}>
                  {careerOpen ? 'Hide fields' : 'Choose a field'}
                </Text>
                <Image source={downIcon} style={styles.dropIcon} />
              </View>
            </Pressable>
          )}
        </View>
        {careerOpen && city.careerPath === 'undecided' && (
          <View style={styles.careerList}>
            {CAREERS.map((career) => (
              <Pressable
                key={career.id}
                accessibilityRole="button"
                onPress={() => {
                  onAction((w) => chooseCareer(w, career.id));
                  setCareerOpen(false);
                }}
                style={styles.careerOption}
              >
                <Text style={styles.careerOptionTitle}>{career.name}</Text>
                <Text style={styles.caption}>{career.description}</Text>
              </Pressable>
            ))}
          </View>
        )}
      </View>
    </View>
  );
}
const styles = StyleSheet.create({
  mapControls: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 15,
  },
  mapToggle: {
    borderWidth: 1,
    borderColor: t.neon,
    backgroundColor: t.panel,
    paddingVertical: 9,
    paddingHorizontal: 14,
    borderRadius: 8,
    minHeight: 42,
    justifyContent: 'center',
  },
  mapToggleText: {
    fontFamily: t.font.hud,
    color: t.amber,
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 1,
  },

  buildingSprite: {
    width: 123,
    height: 119,
    position: 'absolute',
    top: 3,
    right: 3,
  },
  choiceIcon: { width: 18, height: 18, resizeMode: 'contain' },
  careerButtonRow: { flexDirection: 'row', gap: 9, alignItems: 'center' },
  dropIcon: { width: 15, height: 15, resizeMode: 'contain' },
  root: { gap: 17 },
  heading: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: 12,
  },
  eyebrow: {
    fontFamily: t.font.hud,
    color: t.neon,
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 1.8,
  },
  title: { color: t.ink, fontFamily: t.font.display, fontSize: 28 },
  titleSmall: { color: t.ink, fontFamily: 'serif', fontSize: 26 },
  caption: { color: t.muted, fontSize: 13, lineHeight: 20 },
  cityHud: {
    backgroundColor: t.panel,
    borderWidth: 1,
    borderColor: t.border,
    padding: 12,
    borderRadius: 9,
    gap: 3,
    minWidth: 170,
  },
  hudLabel: {
    fontFamily: t.font.hud,
    color: t.muted,
    letterSpacing: 0.7,
    fontSize: 9,
  },
  hudValue: { color: t.amber, fontSize: 22, fontWeight: '800' },
  districts: { gap: 10, paddingVertical: 3, paddingHorizontal: 1 },
  district: {
    width: 195,
    minHeight: 235,
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: t.border,
    gap: 7,
    justifyContent: 'flex-end',
  },
  districtActive: { borderColor: t.neon, borderWidth: 2 },
  districtSymbol: { fontSize: 26, color: t.amber },
  districtName: { fontSize: 16, color: t.ink, fontWeight: '800' },
  districtSubtitle: {
    fontSize: 11,
    color: t.muted,
    lineHeight: 16,
    minHeight: 35,
  },
  districtAction: {
    fontFamily: t.font.hud,
    marginTop: 4,
    fontSize: 9,
    fontWeight: '800',
    color: t.neon,
    letterSpacing: 1,
  },
  storyHeading: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  counter: { fontFamily: t.font.hud, color: t.muted, fontSize: 12 },
  empty: {
    padding: 22,
    minHeight: 120,
    gap: 10,
    borderWidth: 1,
    borderColor: t.border,
    borderRadius: 12,
    backgroundColor: t.background,
  },
  emptyTitle: { color: t.amber, fontFamily: 'serif', fontSize: 21 },
  encounter: {
    backgroundColor: t.panel,
    padding: 22,
    gap: 16,
    borderRadius: 13,
    borderWidth: 1,
    borderColor: t.border,
  },
  encounterTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 10,
  },
  eventTitle: { fontFamily: 'serif', fontSize: 28, color: t.amber },
  eventDescription: {
    color: t.ink,
    fontSize: 17,
    lineHeight: 27,
    maxWidth: 760,
  },
  eventPills: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  eventPill: {
    backgroundColor: t.panelRaised,
    borderRadius: 8,
    padding: 9,
    borderWidth: 1,
    borderColor: t.border,
  },
  eventPillActive: { borderColor: t.neon },
  eventPillText: { color: t.ink, fontSize: 11 },
  options: { gap: 10 },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 13,
    padding: 16,
    borderWidth: 1,
    borderColor: t.border,
    backgroundColor: t.panelRaised,
    borderRadius: 10,
    minHeight: 58,
  },
  optionPressed: { backgroundColor: t.neonDeep },
  optionIndex: {
    fontFamily: t.font.hud,
    color: t.neon,
    fontWeight: '800',
    fontSize: 11,
  },
  optionText: { flex: 1, color: t.ink, fontSize: 14, lineHeight: 22 },
  arrow: { color: t.amber, fontSize: 20 },
  note: { color: t.muted, fontSize: 11, lineHeight: 17 },
  careerCard: {
    padding: 19,
    gap: 13,
    borderWidth: 1,
    borderColor: t.border,
    backgroundColor: t.panel,
    borderRadius: 12,
  },
  careerTop: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: 13,
  },
  careerTitle: { fontFamily: 'serif', color: t.amber, fontSize: 24 },
  careerButton: { backgroundColor: t.neonDeep, padding: 14, borderRadius: 8 },
  careerButtonText: { color: t.ink, fontWeight: '800', fontSize: 12 },
  careerList: { gap: 8 },
  careerOption: {
    borderWidth: 1,
    borderColor: t.border,
    backgroundColor: t.panelRaised,
    borderRadius: 9,
    padding: 15,
    gap: 5,
  },
  careerOptionTitle: { color: t.amber, fontSize: 16, fontWeight: '800' },
});
