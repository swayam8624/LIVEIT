import { gameTheme as t } from './gameTheme';
import React, { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import {
  APPEARANCE_GROUPS,
  EYE_COLORS,
  HAIR_COLORS,
  OUTFIT_COLORS,
  SKIN_COLORS,
  type Appearance,
} from '@living/world-schema';
import { AvatarPortrait } from './AvatarPortrait';

type Key = keyof Appearance;
const OPTIONS: { [K in Key]: readonly Appearance[K][] } = {
  skinTone: [
    'porcelain',
    'ivory',
    'peach',
    'sand',
    'golden',
    'olive',
    'tan',
    'caramel',
    'cocoa',
    'mahogany',
    'umber',
    'espresso',
  ],
  face: ['oval', 'round', 'heart', 'square', 'long'],
  eyes: ['almond', 'round', 'hooded', 'upturned', 'downturned'],
  eyeColor: ['brown', 'hazel', 'amber', 'green', 'blue', 'gray', 'violet'],
  nose: ['soft', 'straight', 'button', 'broad'],
  lips: ['natural', 'full', 'thin', 'smile'],
  brows: ['soft', 'arched', 'straight', 'bold'],
  hair: [
    'pixie',
    'buzz',
    'bob',
    'lob',
    'waves',
    'curls',
    'coils',
    'afro',
    'ponytail',
    'braids',
    'locs',
    'sidepart',
    'shag',
    'long',
  ],
  hairColor: [
    'midnight',
    'black',
    'espresso',
    'chestnut',
    'auburn',
    'copper',
    'blonde',
    'ash',
    'silver',
    'rose',
    'blue',
    'violet',
  ],
  body: ['slim', 'average', 'athletic', 'broad'],
  outfit: [
    'casual',
    'streetwear',
    'smart',
    'formal',
    'cozy',
    'athletic',
    'vintage',
    'creative',
    'evening',
  ],
  outfitColor: [
    'navy',
    'charcoal',
    'forest',
    'burgundy',
    'cream',
    'plum',
    'teal',
    'rose',
    'gold',
  ],
  accessory: ['none', 'glasses', 'earrings', 'necklace', 'freckles'],
  facialHair: ['none', 'stubble', 'goatee', 'beard', 'moustache'],
  headwear: ['none', 'beanie', 'cap', 'headband', 'beret'],
  makeup: ['none', 'soft', 'bold', 'gloss'],
};
const LOOK_PRESETS: readonly {
  name: string;
  description: string;
  options: Partial<Appearance>;
}[] = [
  {
    name: 'City Noir',
    description: 'Sharp and understated',
    options: {
      skinTone: 'tan',
      hair: 'sidepart',
      hairColor: 'midnight',
      eyes: 'hooded',
      outfit: 'smart',
      outfitColor: 'charcoal',
    },
  },
  {
    name: 'Creative Soul',
    description: 'Artistic and warm',
    options: {
      skinTone: 'caramel',
      hair: 'locs',
      hairColor: 'copper',
      eyes: 'round',
      outfit: 'creative',
      outfitColor: 'teal',
    },
  },
  {
    name: 'Golden Hour',
    description: 'Soft and elegant',
    options: {
      skinTone: 'olive',
      hair: 'long',
      hairColor: 'chestnut',
      eyes: 'almond',
      outfit: 'evening',
      outfitColor: 'rose',
    },
  },
  {
    name: 'Weekend Wanderer',
    description: 'Relaxed and free',
    options: {
      skinTone: 'mahogany',
      hair: 'afro',
      hairColor: 'black',
      eyes: 'upturned',
      outfit: 'streetwear',
      outfitColor: 'forest',
    },
  },
  {
    name: 'Vintage Library',
    description: 'Classic and curious',
    options: {
      skinTone: 'ivory',
      hair: 'bob',
      hairColor: 'auburn',
      eyes: 'hooded',
      outfit: 'vintage',
      outfitColor: 'burgundy',
      accessory: 'glasses',
    },
  },
  {
    name: 'Silver Star',
    description: 'Expressive and bold',
    options: {
      skinTone: 'cocoa',
      hair: 'pixie',
      hairColor: 'silver',
      eyes: 'almond',
      eyeColor: 'gray',
      outfit: 'formal',
      outfitColor: 'plum',
    },
  },
];
const GROUP_ICONS: Record<Key, string> = {
  skinTone: '◒',
  face: '◯',
  eyes: '◉',
  eyeColor: '✦',
  nose: '⌁',
  lips: '♡',
  brows: '⌃',
  hair: '♛',
  hairColor: '✧',
  body: '♙',
  outfit: '✂',
  outfitColor: '◆',
  accessory: '◇',
  facialHair: '♟',
  headwear: '♧',
  makeup: '✿',
};
function colorFor(k: Key, value: string): string | undefined {
  if (k === 'skinTone') return SKIN_COLORS[value as keyof typeof SKIN_COLORS];
  if (k === 'eyeColor') return EYE_COLORS[value as keyof typeof EYE_COLORS];
  if (k === 'hairColor') return HAIR_COLORS[value as keyof typeof HAIR_COLORS];
  if (k === 'outfitColor')
    return OUTFIT_COLORS[value as keyof typeof OUTFIT_COLORS];
  return undefined;
}
export function AvatarEditor({
  appearance,
  onChange,
  heading = 'Make this character yours.',
  compact = false,
}: {
  appearance: Appearance;
  onChange: (next: Appearance) => void;
  heading?: string;
  compact?: boolean;
}) {
  const [selected, setSelected] = useState<Key>('hair');
  const [expression, setExpression] = useState<
    'neutral' | 'happy' | 'sad' | 'tense'
  >('neutral');
  const [history, setHistory] = useState<Appearance[]>([]);
  const [variation, setVariation] = useState(0);
  function change(next: Appearance) {
    setHistory((items) => [...items.slice(-9), appearance]);
    onChange(next);
  }
  function surprise() {
    // Deterministic on-device cycling, not remote AI portrait generation.
    const keys = Object.keys(OPTIONS) as Key[];
    const next = { ...appearance };
    for (let i = 0; i < keys.length; i++) {
      const key = keys[i]!;
      const options = OPTIONS[key] as readonly string[];
      const selectedOption =
        options[(variation * 7 + i * 11 + 3) % options.length]!;
      Object.assign(next, { [key]: selectedOption });
    }
    setVariation((v) => v + 1);
    change(next);
  }
  function undo() {
    const prior = history.at(-1);
    if (!prior) return;
    setHistory((items) => items.slice(0, -1));
    onChange(prior);
  }
  const entry = APPEARANCE_GROUPS.find((x) => x.key === selected)!;
  const choices = OPTIONS[selected] as readonly string[];
  return (
    <View style={styles.shell}>
      <View style={styles.header}>
        <View style={{ flex: 1, gap: 7 }}>
          <Text style={styles.kicker}>LIVEIT · CHARACTER STUDIO</Text>
          <Text style={styles.title}>{heading}</Text>
          <Text style={styles.help}>
            Your look is yours to change. All skin tones, hair, body shapes and
            clothes are available from the beginning—no tickets, gems or paid
            outfits.
          </Text>
        </View>
      </View>
      <View style={styles.quickActions}>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Surprise me with a new appearance"
          onPress={surprise}
          style={styles.quickButton}
        >
          <Text style={styles.quickText}>✦ SURPRISE ME</Text>
        </Pressable>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Undo appearance change"
          disabled={!history.length}
          onPress={undo}
          style={[styles.quickButton, !history.length && { opacity: 0.4 }]}
        >
          <Text style={styles.quickText}>↶ UNDO</Text>
        </Pressable>
      </View>
      <Text style={styles.presetHeading}>
        START WITH A LOOK · CUSTOMIZE EVERYTHING AFTERWARDS
      </Text>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.presetRow}
        accessibilityLabel="Character appearance presets"
      >
        {LOOK_PRESETS.map((preset) => (
          <Pressable
            key={preset.name}
            accessibilityRole="button"
            accessibilityLabel={'Try ' + preset.name + ' look'}
            onPress={() => change({ ...appearance, ...preset.options })}
            style={styles.presetButton}
          >
            <Text style={styles.presetName}>{preset.name}</Text>
            <Text style={styles.presetDescription}>{preset.description}</Text>
          </Pressable>
        ))}
      </ScrollView>
      <View style={styles.layout}>
        <View style={[styles.preview, compact && { minHeight: 260 }]}>
          <View style={styles.spotlight} />
          <Text style={styles.previewLabel}>LIVE CHARACTER PREVIEW</Text>
          <AvatarPortrait
            appearance={appearance}
            size={compact ? 168 : 220}
            expression={expression}
          />
          <View style={styles.expressionRow}>
            {(['neutral', 'happy', 'sad', 'tense'] as const).map((mood) => (
              <Pressable
                key={mood}
                accessibilityRole="button"
                accessibilityLabel={'Preview ' + mood + ' expression'}
                accessibilityState={{ selected: expression === mood }}
                style={[
                  styles.expressionButton,
                  expression === mood && styles.expressionSelected,
                ]}
                onPress={() => setExpression(mood)}
              >
                <Text style={styles.expressionText}>{mood.toUpperCase()}</Text>
              </Pressable>
            ))}
          </View>
          <View style={styles.previewBar}>
            <Text style={styles.previewSubtitle}>MY CHARACTER</Text>
            <Text style={styles.previewHint}>Changes appear instantly</Text>
          </View>
        </View>
        <View style={styles.controls}>
          <Text style={styles.controlHeading}>CUSTOMIZE</Text>
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={styles.groups}
            accessibilityLabel="Appearance categories"
          >
            {APPEARANCE_GROUPS.map((group) => (
              <Pressable
                accessibilityRole="tab"
                accessibilityLabel={group.label}
                accessibilityState={{ selected: selected === group.key }}
                onPress={() => setSelected(group.key)}
                key={group.key}
                style={[
                  styles.group,
                  selected === group.key && styles.groupActive,
                ]}
              >
                <Text style={styles.groupIcon}>{GROUP_ICONS[group.key]}</Text>
                <Text
                  style={[
                    styles.groupText,
                    selected === group.key && styles.groupTextActive,
                  ]}
                >
                  {group.label}
                </Text>
              </Pressable>
            ))}
          </ScrollView>
          <View style={styles.optionHeading}>
            <Text style={styles.optionTitle}>{entry.label.toUpperCase()}</Text>
            <Text style={styles.optionCount}>
              {choices.length} free options
            </Text>
          </View>
          <View style={styles.options}>
            {choices.map((value) => {
              const active = appearance[selected] === value;
              const swatch = colorFor(selected, value);
              return (
                <Pressable
                  key={value}
                  accessibilityRole="radio"
                  accessibilityLabel={`${entry.label}: ${value}`}
                  accessibilityState={{ selected: active, checked: active }}
                  onPress={() => change({ ...appearance, [selected]: value })}
                  style={[styles.option, active && styles.activeOption]}
                >
                  {swatch ? (
                    <View
                      style={[
                        styles.swatch,
                        { backgroundColor: swatch },
                        active && styles.activeSwatch,
                      ]}
                    />
                  ) : (
                    <Text style={styles.optionGlyph}>
                      {GROUP_ICONS[selected]}
                    </Text>
                  )}
                  <Text
                    numberOfLines={1}
                    style={[styles.optionText, active && styles.activeText]}
                  >
                    {value.replace(/([A-Z])/g, ' $1')}
                  </Text>
                  {active && <Text style={styles.tick}>✓</Text>}
                </Pressable>
              );
            })}
          </View>
          <Text style={styles.footer}>
            ✧ Your appearance is cosmetic. It will never change your career
            chances, health or dialogue outcomes.
          </Text>
        </View>
      </View>
    </View>
  );
}
const styles = StyleSheet.create({
  quickActions: { flexDirection: 'row', flexWrap: 'wrap', gap: 9 },
  quickButton: {
    padding: 12,
    borderRadius: 9,
    backgroundColor: t.neonDeep,
    borderColor: t.neon,
    borderWidth: 1,
    minHeight: 44,
    justifyContent: 'center',
  },
  quickText: { color: t.ink, fontWeight: '800', fontSize: 12 },
  expressionRow: {
    width: '100%',
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 4,
    justifyContent: 'center',
    padding: 8,
  },
  expressionButton: {
    borderRadius: 6,
    backgroundColor: t.panelRaised,
    paddingVertical: 9,
    paddingHorizontal: 6,
    flexGrow: 1,
    alignItems: 'center',
  },
  expressionSelected: {
    backgroundColor: t.neonDeep,
    borderWidth: 1,
    borderColor: t.neon,
  },
  expressionText: { fontSize: 9, color: t.ink, fontWeight: '700' },

  presetHeading: {
    color: t.muted,
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 1.4,
  },
  presetRow: { gap: 9, paddingBottom: 3 },
  presetButton: {
    minWidth: 141,
    minHeight: 70,
    backgroundColor: t.panel,
    borderColor: t.border,
    borderWidth: 1,
    borderRadius: 9,
    padding: 12,
    justifyContent: 'center',
    gap: 6,
  },
  presetName: { fontSize: 13, fontWeight: '800', color: t.ink },
  presetDescription: { color: t.muted, fontSize: 10 },

  shell: { gap: 16, width: '100%' },
  header: { flexDirection: 'row', gap: 14 },
  kicker: {
    fontFamily: t.font.hud,
    color: t.neon,
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 1.8,
  },
  title: { color: t.ink, fontFamily: t.font.display, fontSize: 27 },
  help: { color: t.muted, lineHeight: 20, fontSize: 13, maxWidth: 670 },
  layout: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 14,
    alignItems: 'stretch',
  },
  preview: {
    flexGrow: 1,
    flexBasis: 225,
    backgroundColor: t.panel,
    borderWidth: 1,
    borderColor: t.border,
    borderRadius: 14,
    minHeight: 335,
    alignItems: 'center',
    justifyContent: 'flex-end',
    paddingTop: 35,
    overflow: 'hidden',
  },
  spotlight: {
    position: 'absolute',
    width: 210,
    height: 250,
    borderRadius: 110,
    backgroundColor: t.water,
    top: 39,
    opacity: 0.48,
  },
  previewLabel: {
    fontFamily: t.font.hud,
    position: 'absolute',
    top: 16,
    left: 14,
    color: t.amber,
    letterSpacing: 1.4,
    fontSize: 9,
    fontWeight: '800',
  },
  previewBar: {
    backgroundColor: 'rgba(10,19,33,.95)',
    paddingVertical: 12,
    paddingHorizontal: 18,
    width: '100%',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 6,
    flexWrap: 'wrap',
  },
  previewSubtitle: {
    color: t.amber,
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 1.2,
  },
  previewHint: { color: t.muted, fontSize: 10 },
  controls: {
    flex: 2,
    flexBasis: 280,
    minWidth: 0,
    gap: 13,
    padding: 15,
    borderWidth: 1,
    borderColor: t.border,
    backgroundColor: t.panel,
    borderRadius: 14,
  },
  controlHeading: {
    fontFamily: t.font.hud,
    fontSize: 11,
    color: t.neon,
    letterSpacing: 2,
    fontWeight: '800',
  },
  groups: { gap: 7, paddingBottom: 5 },
  group: {
    borderRadius: 9,
    paddingHorizontal: 12,
    paddingVertical: 10,
    minHeight: 66,
    minWidth: 76,
    alignItems: 'center',
    gap: 6,
    borderWidth: 1,
    borderColor: t.border,
    backgroundColor: t.panel,
  },
  groupActive: { borderColor: t.neon, backgroundColor: t.neonDeep },
  groupIcon: { color: t.amber, fontSize: 22 },
  groupText: { color: t.muted, fontSize: 10, fontWeight: '700' },
  groupTextActive: { color: t.ink },
  optionHeading: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 6,
  },
  optionTitle: {
    fontFamily: t.font.hud,
    color: t.amber,
    fontSize: 11,
    letterSpacing: 1.1,
    fontWeight: '800',
  },
  optionCount: { color: t.muted, fontSize: 11 },
  options: { flexDirection: 'row', flexWrap: 'wrap', gap: 7 },
  option: {
    flexBasis: 102,
    flexGrow: 1,
    maxWidth: 165,
    minHeight: 70,
    borderWidth: 1,
    borderColor: t.border,
    borderRadius: 9,
    backgroundColor: t.panelRaised,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 7,
    gap: 3,
  },
  activeOption: {
    backgroundColor: t.neonDeep,
    borderColor: t.neon,
    borderWidth: 2,
  },
  swatch: {
    width: 27,
    height: 27,
    borderRadius: 17,
    borderColor: '#ffffff66',
    borderWidth: 1,
  },
  activeSwatch: { borderColor: '#ffffff', borderWidth: 2 },
  optionGlyph: { fontSize: 23, color: t.amber },
  optionText: {
    fontSize: 11,
    color: t.ink,
    textTransform: 'capitalize',
    fontWeight: '700',
  },
  activeText: { color: t.ink },
  tick: {
    position: 'absolute',
    right: 6,
    top: 4,
    color: t.amber,
    fontSize: 13,
    fontWeight: '900',
  },
  footer: { color: t.muted, fontSize: 11, lineHeight: 17 },
});
