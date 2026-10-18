import React, { useEffect, useRef, useState } from 'react';
import {
  AccessibilityInfo,
  Animated,
  Image,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
  useWindowDimensions,
} from 'react-native';
import { type World } from '@living/world-schema';
import { type Story } from '@living/story-schema';
import { conditionMet, currentScene } from '@living/narrative-core';
import { AvatarPortrait } from './AvatarPortrait';
import { GameStage } from './GameStage';

// Licensed original concept portrait bundled offline for the official Amelia
// episodes. Creator stories can choose a different character actor manifest.
// eslint-disable-next-line @typescript-eslint/no-require-imports
const ameliaImage = require('../assets/amelia-portrait.jpg');

/**
 * A full-stage visual-novel player: actors and dialogue share the SAME stage.
 * No website cards or separate text columns. Shared narrative core decides
 * all choices and consequences; this component handles presentation only.
 */
export function StoryPlayer({
  world,
  story,
  integrated,
  onChoose,
  onClose,
  onFinish,
}: {
  world: World;
  story: Story;
  integrated: boolean;
  onChoose: (choiceId: string) => void;
  onClose: () => void;
  onFinish: () => void;
}) {
  const { width } = useWindowDimensions();
  const compact = width < 600;
  const scene = currentScene(world, story);
  const [historyOpen, setHistoryOpen] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(true);
  const fade = useRef(new Animated.Value(1)).current;
  useEffect(() => {
    let mounted = true;
    void AccessibilityInfo.isReduceMotionEnabled()
      .then((flag) => {
        if (mounted) setReducedMotion(flag);
      })
      .catch(() => {});
    return () => {
      mounted = false;
    };
  }, []);
  useEffect(() => {
    fade.stopAnimation();
    if (reducedMotion) {
      fade.setValue(1);
      return;
    }
    fade.setValue(0);
    Animated.timing(fade, {
      toValue: 1,
      duration: 330,
      useNativeDriver: false,
    }).start();
  }, [fade, scene.id, reducedMotion]);

  const current = world.progress.find((p) => p.storyId === story.id);
  const progression = current ? current.choices.length + 1 : 1;
  const past = world.history
    .filter((h) => h.kind === 'choice' && h.text.startsWith(story.title + ':'))
    .slice(-7);
  const speakerIsPlayer =
    scene.speaker.toLowerCase() === world.player.name.toLowerCase() ||
    ['you', 'player'].includes(scene.speaker.toLowerCase());
  const moodExpression =
    scene.mood === 'warm'
      ? 'happy'
      : scene.mood === 'tense'
        ? 'tense'
        : 'neutral';
  return (
    <View
      testID="story-stage"
      accessibilityLabel={story.title + ' interactive cinematic scene'}
      style={styles.shell}
    >
      <GameStage
        mode="story"
        mood={scene.mood}
        stageHeight={compact ? 650 : 705}
      />
      <Animated.View
        testID="story-actors"
        pointerEvents="none"
        style={[
          styles.actors,
          compact && styles.actorsCompact,
          {
            opacity: fade,
            transform: [
              {
                translateY: fade.interpolate({
                  inputRange: [0, 1],
                  outputRange: [18, 0],
                }),
              },
            ],
          },
        ]}
      >
        <View style={styles.playerActor}>
          <AvatarPortrait
            appearance={world.player.appearance}
            size={compact ? 154 : 217}
            expression={moodExpression}
            label={'Customized player character in ' + scene.mood + ' scene'}
          />
        </View>
        {scene.speaker.toLowerCase() === 'amelia' ? (
          <View style={[styles.npcActor, compact && styles.npcActorCompact]}>
            <Image
              source={ameliaImage}
              style={[styles.npcImage, compact && styles.npcImageCompact]}
              accessibilityLabel="Amelia's illustrated portrait"
            />
          </View>
        ) : !speakerIsPlayer && scene.speaker.toLowerCase() !== 'narrator' ? (
          <View style={styles.npcUnknown}>
            <Text style={styles.npcLetter}>
              {scene.speaker.slice(0, 1).toUpperCase()}
            </Text>
          </View>
        ) : null}
      </Animated.View>
      <View style={styles.topControls}>
        <View style={styles.topTitle}>
          <Text numberOfLines={1} style={styles.eyebrow}>
            ✦ LIVEIT STORIES
          </Text>
          <Text numberOfLines={1} style={styles.chapterName}>
            {story.title}
          </Text>
          <Text style={styles.sceneNumber}>
            SCENE {progression.toString().padStart(2, '0')} ·{' '}
            {integrated ? 'YOUR LIFE' : 'STANDALONE'}
          </Text>
        </View>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Save & leave scene"
          style={styles.exitButton}
          onPress={onClose}
        >
          <Text style={styles.exitText}>✕ LEAVE</Text>
        </Pressable>
      </View>
      <Animated.View
        testID="story-dialogue-overlay"
        key={scene.id}
        style={[
          styles.dialogueDock,
          compact && styles.dialogueCompact,
          { opacity: fade },
        ]}
      >
        <View style={styles.speakerLine}>
          <View style={styles.speakerAccent} />
          <Text style={styles.speakerName}>{scene.speaker.toUpperCase()}</Text>
          <View style={{ flex: 1 }} />
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={
              historyOpen ? 'Close dialogue history' : 'Open dialogue history'
            }
            onPress={() => setHistoryOpen((v) => !v)}
            style={styles.historyButton}
          >
            <Text style={styles.historyLabel}>
              {historyOpen ? 'CLOSE' : '◷ HISTORY'}
            </Text>
          </Pressable>
        </View>
        {historyOpen ? (
          <ScrollView style={styles.historyScroll} nestedScrollEnabled>
            <Text style={styles.historyHeading}>YOUR RECENT CHOICES</Text>
            {past.length === 0 ? (
              <Text style={styles.dialogueText}>
                This chapter has just begun.
              </Text>
            ) : (
              past.map((entry) => (
                <Text key={entry.id} style={styles.historyEntry}>
                  ✦ {entry.text}
                </Text>
              ))
            )}
          </ScrollView>
        ) : (
          <ScrollView style={styles.dialogueScroll} nestedScrollEnabled>
            <Text
              accessibilityLiveRegion="polite"
              style={[
                styles.dialogueText,
                compact && styles.dialogueTextCompact,
              ]}
            >
              {scene.text}
            </Text>
            {scene.choices.length > 0 && (
              <View style={styles.choices}>
                {scene.choices.map((choice, i) => {
                  const valid = choice.conditions.every((c) =>
                    conditionMet(world, c),
                  );
                  return (
                    <Pressable
                      key={choice.id}
                      accessibilityRole="button"
                      accessibilityLabel={choice.label}
                      disabled={!valid}
                      onPress={() => onChoose(choice.id)}
                      style={({ pressed }) => [
                        styles.choice,
                        pressed && styles.choicePressed,
                        !valid && styles.choiceDisabled,
                      ]}
                    >
                      <Text style={styles.choiceNumber}>
                        {String(i + 1).padStart(2, '0')}
                      </Text>
                      <Text style={styles.choiceText}>
                        {choice.label}
                        {valid ? '' : ' · Not available yet'}
                      </Text>
                      <Text style={styles.choiceArrow}>↗</Text>
                    </Pressable>
                  );
                })}
              </View>
            )}
            {scene.ending && (
              <View style={styles.ending}>
                <Text style={styles.endingLabel}>✧ CHAPTER COMPLETE</Text>
                <Text style={styles.endingCaption}>
                  Your decisions and relationships remain in this timeline.
                </Text>
                <Pressable
                  accessibilityRole="button"
                  accessibilityLabel={
                    integrated
                      ? 'Return to your life'
                      : 'Continue living in this timeline'
                  }
                  style={styles.continueButton}
                  onPress={onFinish}
                >
                  <Text style={styles.continueText}>
                    {integrated ? 'Return to your life' : 'Continue living'} →
                  </Text>
                </Pressable>
              </View>
            )}
          </ScrollView>
        )}
      </Animated.View>
    </View>
  );
}
const styles = StyleSheet.create({
  shell: {
    position: 'relative',
    width: '100%',
    backgroundColor: '#131d2e',
    borderRadius: 16,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#83614c',
  },
  actors: {
    position: 'absolute',
    top: 94,
    left: 30,
    right: 30,
    height: 260,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
  },
  actorsCompact: { left: 8, right: 8, top: 92, height: 218 },
  playerActor: { alignSelf: 'flex-end' },
  npcActor: {
    width: 190,
    height: 235,
    borderRadius: 90,
    overflow: 'hidden',
    borderWidth: 2,
    borderColor: '#ad8a71',
    backgroundColor: '#262238',
  },
  npcImage: { width: 190, height: 235, resizeMode: 'cover' },
  npcActorCompact: { width: 136, height: 180, borderRadius: 66 },
  npcImageCompact: { width: 136, height: 180 },
  npcUnknown: {
    width: 150,
    height: 195,
    backgroundColor: '#35384e',
    borderRadius: 72,
    alignItems: 'center',
    justifyContent: 'center',
    borderColor: '#ae8f77',
    borderWidth: 2,
  },
  npcLetter: { fontSize: 75, color: '#e5c39d', fontFamily: 'serif' },
  topControls: {
    position: 'absolute',
    left: 14,
    right: 14,
    top: 14,
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
    alignItems: 'flex-start',
  },
  topTitle: { flex: 1, gap: 5 },
  eyebrow: {
    fontSize: 9,
    color: '#f5bc81',
    letterSpacing: 2,
    fontWeight: '800',
  },
  chapterName: { fontFamily: 'serif', fontSize: 20, color: '#fff0d9' },
  sceneNumber: { fontSize: 10, color: '#c8ccd5', letterSpacing: 1 },
  exitButton: {
    backgroundColor: 'rgba(10,17,29,.84)',
    borderColor: '#a98268',
    borderWidth: 1,
    paddingHorizontal: 13,
    minHeight: 43,
    borderRadius: 9,
    justifyContent: 'center',
  },
  exitText: { fontSize: 11, color: '#f6d3aa', fontWeight: '800' },
  dialogueDock: {
    position: 'absolute',
    bottom: 16,
    left: 17,
    right: 17,
    maxHeight: 343,
    padding: 17,
    backgroundColor: 'rgba(11,20,34,.96)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#c39265',
    gap: 9,
  },
  dialogueCompact: {
    bottom: 9,
    left: 7,
    right: 7,
    maxHeight: 360,
    padding: 13,
  },
  speakerLine: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  speakerAccent: {
    width: 6,
    height: 17,
    borderRadius: 3,
    backgroundColor: '#e9ae7e',
  },
  speakerName: {
    color: '#f9c790',
    fontSize: 12,
    fontWeight: '900',
    letterSpacing: 1.4,
  },
  historyButton: {
    minHeight: 35,
    justifyContent: 'center',
    paddingHorizontal: 7,
  },
  historyLabel: { fontSize: 10, color: '#cbd3e0', fontWeight: '800' },
  historyScroll: { maxHeight: 255 },
  historyHeading: {
    color: '#e3b689',
    fontSize: 10,
    letterSpacing: 1.2,
    marginBottom: 10,
  },
  historyEntry: {
    color: '#f0e2d5',
    fontSize: 12,
    lineHeight: 20,
    marginBottom: 9,
  },
  dialogueScroll: { maxHeight: 285 },
  dialogueText: {
    fontSize: 18,
    lineHeight: 28,
    color: '#fff2e5',
    fontFamily: 'serif',
    marginBottom: 12,
  },
  dialogueTextCompact: { fontSize: 17, lineHeight: 24 },
  choices: { gap: 8, paddingBottom: 3 },
  choice: {
    minHeight: 50,
    backgroundColor: 'rgba(57,51,67,.9)',
    borderRadius: 8,
    borderColor: '#b28e75',
    borderWidth: 1,
    paddingVertical: 10,
    paddingHorizontal: 12,
    flexDirection: 'row',
    gap: 13,
    alignItems: 'center',
  },
  choicePressed: { backgroundColor: '#8d593e' },
  choiceDisabled: { opacity: 0.38 },
  choiceNumber: { fontSize: 10, color: '#e5ae7e', fontWeight: '900' },
  choiceText: { fontSize: 13, lineHeight: 20, color: '#fff5e9', flex: 1 },
  choiceArrow: { color: '#edba84', fontSize: 20 },
  ending: { gap: 9 },
  endingLabel: {
    color: '#f8d6a6',
    fontSize: 11,
    letterSpacing: 1.5,
    fontWeight: '900',
  },
  endingCaption: { color: '#c3cad6', fontSize: 12, lineHeight: 19 },
  continueButton: {
    backgroundColor: '#985537',
    borderRadius: 8,
    padding: 14,
    minHeight: 49,
    justifyContent: 'center',
  },
  continueText: {
    color: '#fff0de',
    fontSize: 13,
    fontWeight: '800',
    textAlign: 'center',
  },
});
