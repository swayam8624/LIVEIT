import React, { useEffect, useRef } from 'react';
import {
  Animated,
  ImageBackground,
  Platform,
  StyleSheet,
  Text,
  View,
} from 'react-native';

/**
 * First art-backed stage for LIVEIT.
 *
 * Stage content uses a bundled, original environment plate rather than remote
 * images or generated-at-runtime assets. The JPG is intentionally a low-res
 * preview. Replace it with licensed, layered production plates later without
 * changing the simulation or narrative contracts.
 */
export function GameStage({
  children,
  mode,
  mood = 'reflective',
  compact = false,
}: {
  children?: React.ReactNode;
  mode: 'life' | 'story';
  mood?: 'reflective' | 'tense' | 'warm';
  compact?: boolean;
}) {
  const pulse = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    const animation = Animated.loop(
      Animated.sequence([
        Animated.timing(pulse, {
          toValue: 1,
          duration: 3500,
          useNativeDriver: Platform.OS !== 'web',
        }),
        Animated.timing(pulse, {
          toValue: 0,
          duration: 3500,
          useNativeDriver: Platform.OS !== 'web',
        }),
      ]),
    );
    animation.start();
    return () => animation.stop();
  }, [pulse]);
  const tint =
    mood === 'tense'
      ? 'rgba(62,16,38,0.25)'
      : mood === 'warm'
        ? 'rgba(105,55,15,0.08)'
        : 'rgba(9,17,39,0.2)';
  return (
    <ImageBackground
      accessibilityLabel={
        mode === 'story'
          ? 'An atmospheric cafe illuminated at dusk, rain falling over Bellweather outside'
          : 'Your next chapter in the city of Bellweather'
      }
      resizeMode="cover"
      // Metro requires a static asset require for bundled offline images.
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      source={require('../assets/cafe-dusk.jpg')}
      imageStyle={styles.image}
      style={[
        styles.stage,
        { minHeight: compact ? 270 : mode === 'story' ? 480 : 410 },
      ]}
    >
      <View
        pointerEvents="none"
        style={[StyleSheet.absoluteFillObject, { backgroundColor: tint }]}
      />
      <View pointerEvents="none" style={styles.vignetteTop} />
      <View pointerEvents="none" style={styles.vignetteBottom} />
      <View pointerEvents="none" style={styles.letterboxTop} />
      <View pointerEvents="none" style={styles.letterboxBottom} />
      <Animated.View
        pointerEvents="none"
        style={[
          styles.glow,
          {
            opacity: pulse.interpolate({
              inputRange: [0, 1],
              outputRange: [0.12, 0.25],
            }),
          },
        ]}
      />
      <View pointerEvents="none" style={styles.location}>
        <Text style={styles.locationTitle}>BELLWEATHER</Text>
        <Text style={styles.locationCaption}>
          THE CORNER CAFÉ · AN EVENING IN OCTOBER
        </Text>
      </View>
      <View style={styles.content}>{children}</View>
    </ImageBackground>
  );
}
const styles = StyleSheet.create({
  stage: {
    width: '100%',
    overflow: 'hidden',
    backgroundColor: '#142035',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#6f4a39',
    position: 'relative',
    justifyContent: 'flex-end',
  },
  image: { borderRadius: 15 },
  vignetteTop: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 94,
    backgroundColor: 'rgba(7,13,26,0.61)',
  },
  vignetteBottom: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 146,
    backgroundColor: 'rgba(6,11,21,0.73)',
  },
  letterboxTop: {
    position: 'absolute',
    top: 0,
    right: 0,
    left: 0,
    height: 8,
    backgroundColor: '#080e18',
  },
  letterboxBottom: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    left: 0,
    height: 8,
    backgroundColor: '#080e18',
  },
  location: { position: 'absolute', top: 25, left: 24, right: 24, gap: 4 },
  locationTitle: {
    color: '#f6d4a3',
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 4,
  },
  locationCaption: {
    color: '#eee3d5',
    fontSize: 9,
    fontWeight: '600',
    letterSpacing: 1.5,
  },
  glow: {
    position: 'absolute',
    top: '32%',
    left: '17%',
    width: 110,
    height: 110,
    borderRadius: 60,
    backgroundColor: '#efa13d',
  },
  content: {
    width: '100%',
    paddingHorizontal: 20,
    paddingBottom: 25,
    paddingTop: 85,
    gap: 12,
  },
});
