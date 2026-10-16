import React, { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import {
  DISTRICTS, availableCityOpportunities, cityState, chooseCareer,
  resolveCityOpportunity, visitDistrict, type CityOpportunity,
} from '@living/simulation-core';
import type { CareerPath, World } from '@living/world-schema';

const CAREERS: { id: Exclude<CareerPath, 'undecided'>; name: string; description: string }[] = [
  { id: 'technology', name: 'Technology', description: 'Build useful things that change the city.' },
  { id: 'creative', name: 'Creative', description: 'Make art and stories people remember.' },
  { id: 'business', name: 'Business', description: 'Find an opportunity others missed.' },
  { id: 'community', name: 'Community', description: 'Work with people, not just for them.' },
];

/**
 * Standalone responsive city interactions; reads only validated World state
 * and delegates actual changes to the deterministic shared simulation engine.
 */
export function CityWorld({
  world,
  onAction,
}: {
  world: World;
  onAction: (operation: (world: World) => World) => void;
}) {
  const [focused, setFocused] = useState<string | null>(null);
  const [careerOpen, setCareerOpen] = useState(false);
  const city = cityState(world);
  const events = availableCityOpportunities(world);
  const selected = events.find(event => event.id === focused) ?? events[0] ?? null;
  return (
    <View style={styles.root}>
      <View style={styles.heading}>
        <View style={{ flex: 1, gap: 3 }}>
          <Text style={styles.eyebrow}>BELLWEATHER / AN OPEN CITY</Text>
          <Text style={styles.title}>Find your next chapter.</Text>
          <Text style={styles.caption}>Go somewhere. Meet someone. Choose what matters.</Text>
        </View>
        <View style={styles.cityHud}>
          <Text style={styles.hudLabel}>CITY REPUTATION</Text>
          <Text style={styles.hudValue}>{city.reputation}/100</Text>
          <Text style={styles.hudLabel}>CONNECTIONS {city.connections} · STRESS {city.stress}</Text>
        </View>
      </View>
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
            onPress={() => onAction(w => visitDistrict(w, district.id))}
            style={({pressed}) => [
              styles.district,
              { backgroundColor: ['#27374b','#2b3b4a','#4c353e','#323249','#304b42'][index] },
              city.district === district.id && styles.districtActive,
              pressed && { opacity: 0.8 },
            ]}
          >
            <Text style={styles.districtSymbol}>{['☕','✎','⌘','✦','❀'][index]}</Text>
            <Text style={styles.districtName}>{district.title}</Text>
            <Text style={styles.districtSubtitle}>{district.tagline}</Text>
            <Text style={styles.districtAction}>{city.district === district.id ? '● YOU ARE HERE' : 'EXPLORE  →'}</Text>
          </Pressable>
        ))}
      </ScrollView>
      <View style={styles.storyHeading}>
        <View style={{ flex: 1, gap: 5 }}>
          <Text style={styles.eyebrow}>STORIES THE CITY TELLS</Text>
          <Text style={styles.titleSmall}>At a crossroads.</Text>
        </View>
        <Text style={styles.counter}>{events.length} waiting</Text>
      </View>
      {!selected ? (
        <View style={styles.empty}>
          <Text style={styles.emptyTitle}>Not every day has to be extraordinary.</Text>
          <Text style={styles.caption}>Spend time working, studying, resting or seeing friends. New encounters emerge as your life evolves, without tickets or real-time waiting.</Text>
        </View>
      ) : (
        <View style={styles.encounter}>
          <View style={styles.encounterTop}>
            <Text style={styles.eyebrow}>{DISTRICTS.find(d => d.id === selected.district)?.title.toUpperCase()} · LIMITED MOMENT</Text>
            <Text style={styles.counter}>DAY {world.day + 1}</Text>
          </View>
          <Text style={styles.eventTitle}>{selected.title}</Text>
          <Text style={styles.eventDescription}>{selected.description}</Text>
          {events.length > 1 && (
            <View style={styles.eventPills}>
              {events.map((e) => (
                <Pressable key={e.id} accessibilityRole="button" onPress={() => setFocused(e.id)}
                  style={[styles.eventPill, selected.id === e.id && styles.eventPillActive]}>
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
                  onAction(w => resolveCityOpportunity(w, selected.id, choice.id));
                  setFocused(null);
                }}
                style={({pressed}) => [styles.option, pressed && styles.optionPressed]}
              >
                <Text style={styles.optionIndex}>0{i+1}</Text>
                <Text style={styles.optionText}>{choice.label}</Text>
                <Text style={styles.arrow}>↗</Text>
              </Pressable>
            ))}
          </View>
          <Text style={styles.note}>Consequences are saved to this timeline. The choice will not be repeated.</Text>
        </View>
      )}
      <View style={styles.careerCard}>
        <View style={styles.careerTop}>
          <View style={{flex:1,gap:4}}>
            <Text style={styles.eyebrow}>YOUR AMBITIONS</Text>
            <Text style={styles.careerTitle}>{city.careerPath === 'undecided' ? 'What will you build?' : CAREERS.find(c => c.id === city.careerPath)?.name}</Text>
            <Text style={styles.caption}>
              {city.careerPath === 'undecided' ? 'Choose a direction. It will shape future stories, rather than guarantee success.' : 'You have chosen a direction. Your progress still depends on what you do every day.'}
            </Text>
          </View>
          {city.careerPath === 'undecided' && (
            <Pressable accessibilityRole="button" onPress={() => setCareerOpen(p => !p)} style={styles.careerButton}>
              <Text style={styles.careerButtonText}>{careerOpen ? 'Hide fields' : 'Choose a field  ↗'}</Text>
            </Pressable>
          )}
        </View>
        {careerOpen && city.careerPath === 'undecided' && (
          <View style={styles.careerList}>
            {CAREERS.map(career => (
              <Pressable key={career.id} accessibilityRole="button" onPress={() => {
                onAction(w => chooseCareer(w, career.id));
                setCareerOpen(false);
              }} style={styles.careerOption}>
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
  root: { gap: 17 },
  heading: { flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', gap: 12 },
  eyebrow: { color: '#e7ad79', fontSize: 10, fontWeight: '800', letterSpacing: 1.8 },
  title: { color: '#f4e1c7', fontFamily: 'serif', fontSize: 28 },
  titleSmall: { color: '#f4e1c7', fontFamily: 'serif', fontSize: 26 },
  caption: { color: '#c4cbd4', fontSize: 13, lineHeight: 20 },
  cityHud: { backgroundColor: '#172538', borderWidth: 1, borderColor: '#5c5048', padding: 12, borderRadius: 9, gap: 3, minWidth: 170 },
  hudLabel: { color: '#adb9c9', letterSpacing: .7, fontSize: 9 },
  hudValue: { color: '#efd3a7', fontSize: 22, fontWeight: '800' },
  districts: { gap: 10, paddingVertical: 3, paddingHorizontal: 1 },
  district: { width: 178, minHeight: 166, padding: 16, borderRadius: 12, borderWidth: 1, borderColor: '#65758b', gap: 7, justifyContent: 'flex-end' },
  districtActive: { borderColor: '#f7c58c', borderWidth: 2 },
  districtSymbol: { fontSize: 26, color: '#f8d8a1' },
  districtName: { fontSize: 16, color: '#fff4df', fontWeight: '800' },
  districtSubtitle: { fontSize: 11, color: '#ded7d3', lineHeight: 16, minHeight: 35 },
  districtAction: { marginTop: 4, fontSize: 9, fontWeight: '800', color: '#efbc87', letterSpacing: 1 },
  storyHeading: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  counter: { color: '#d7d6d8', fontSize: 12 },
  empty: { padding: 22, minHeight: 120, gap: 10, borderWidth: 1, borderColor: '#47566b', borderRadius: 12, backgroundColor: '#142138' },
  emptyTitle: { color: '#eec28f', fontFamily: 'serif', fontSize: 21 },
  encounter: { backgroundColor: '#1e2a3e', padding: 22, gap: 16, borderRadius: 13, borderWidth: 1, borderColor: '#a57958' },
  encounterTop: { flexDirection: 'row', justifyContent: 'space-between', gap: 10 },
  eventTitle: { fontFamily: 'serif', fontSize: 28, color: '#f9d5aa' },
  eventDescription: { color: '#f3ecde', fontSize: 17, lineHeight: 27, maxWidth: 760 },
  eventPills: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  eventPill: { backgroundColor: '#26374a', borderRadius: 8, padding: 9, borderWidth: 1, borderColor: '#465469' },
  eventPillActive: { borderColor: '#e4b884' },
  eventPillText: { color: '#e8ded2', fontSize: 11 },
  options: { gap: 10 },
  option: { flexDirection: 'row', alignItems: 'center', gap: 13, padding: 16, borderWidth: 1, borderColor: '#756557', backgroundColor: '#2b3244', borderRadius: 10, minHeight: 58 },
  optionPressed: { backgroundColor: '#875037' },
  optionIndex: { color: '#edb47f', fontWeight: '800', fontSize: 11 },
  optionText: { flex: 1, color: '#f8ebdf', fontSize: 14, lineHeight: 22 },
  arrow: { color: '#d8a36e', fontSize: 20 },
  note: { color: '#a9afbd', fontSize: 11, lineHeight: 17 },
  careerCard: { padding: 19, gap: 13, borderWidth: 1, borderColor: '#4c5261', backgroundColor: '#18273a', borderRadius: 12 },
  careerTop: { flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center', gap: 13 },
  careerTitle: { fontFamily: 'serif', color: '#f2d6ac', fontSize: 24 },
  careerButton: { backgroundColor: '#945434', padding: 14, borderRadius: 8 },
  careerButtonText: { color: '#fff0e1', fontWeight: '800', fontSize: 12 },
  careerList: { gap: 8 },
  careerOption: { borderWidth: 1, borderColor: '#6d5d54', backgroundColor: '#26374c', borderRadius: 9, padding: 15, gap: 5 },
  careerOptionTitle: { color: '#f2d5ad', fontSize: 16, fontWeight: '800' },
});
