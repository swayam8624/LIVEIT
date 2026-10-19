import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { PixelStoryBackdrop } from './PixelStoryBackdrop';
import { gameTheme as t } from './gameTheme';

/**
 * Pixel-only stage shared by Free Life features and authored conversations.
 * The photographic dusk JPG is no longer rendered. This component does not
 * mutate simulation or story state; its children remain interactive overlays.
 */
export function GameStage({
  children,
  mode,
  mood = 'reflective',
  compact = false,
  stageHeight,
}: {
  children?: React.ReactNode;
  mode: 'life' | 'story';
  mood?: 'reflective' | 'tense' | 'warm';
  compact?: boolean;
  stageHeight?: number;
}) {
  const height = stageHeight ?? (compact ? 270 : mode === 'story' ? 480 : 410);
  return (
    <View
      style={[styles.stage, { height }]}
      accessibilityLabel={
        mode === 'story'
          ? 'An original animated-style pixel café scene in Bellweather'
          : 'A retro pixel interior in the city of Bellweather'
      }
    >
      <PixelStoryBackdrop stageHeight={height} mood={mood} />
      <View pointerEvents="none" style={styles.location}>
        <Text style={styles.locationTitle}>BELLWEATHER</Text>
        <Text style={styles.locationCaption}>
          {mode === 'story'
            ? 'THE CORNER CAFÉ · A CONVERSATION THAT MATTERS'
            : 'A CITY OF POSSIBILITIES · YOUR LIFE, YOUR PACE'}
        </Text>
      </View>
      <View style={styles.content}>{children}</View>
    </View>
  );
}
const styles = StyleSheet.create({
  stage: {
    width: '100%',
    overflow: 'hidden',
    borderRadius: 9,
    borderWidth: 1,
    borderColor: t.border,
    position: 'relative',
    backgroundColor: t.background,
    justifyContent: 'flex-end',
  },
  location: {
    position: 'absolute',
    bottom: 12,
    left: 10,
    right: 10,
    backgroundColor: '#101827B8',
    paddingHorizontal: 9,
    paddingVertical: 5,
    gap: 2,
  },
  locationTitle: {
    fontFamily: t.font.hud,
    fontSize: 10,
    color: t.neon,
    fontWeight: '900',
    letterSpacing: 2,
  },
  locationCaption: {
    fontFamily: t.font.hud,
    fontSize: 9,
    color: t.ink,
    letterSpacing: 0.8,
  },
  content: {
    position: 'absolute',
    top: 85,
    left: 0,
    right: 0,
    bottom: 10,
    justifyContent: 'flex-end',
    paddingHorizontal: 20,
    paddingBottom: 20,
    gap: 12,
  },
});
