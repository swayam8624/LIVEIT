import React, { useEffect, useRef, useState } from 'react';
import {
  Animated, Easing, Image, Platform, StyleSheet, View,
  type ImageStyle,
} from 'react-native';
import { actorArt, pixelArt } from './pixelArt';
import type { AmbientPedestrian } from './ambientPedestrians';

const PIXELATED: ImageStyle | undefined =
  Platform.OS === 'web'
    ? ({ imageRendering: 'pixelated' } as unknown as ImageStyle)
    : undefined;

type Props = Readonly<{ person: AmbientPedestrian; tileSize: number }>;

/**
 * One independently animated resident. Native-driver translation interpolates
 * positions between low-frequency simulation snapshots. Rendering a stationary
 * resident never advances gait frames. We draw only reviewed CC0 actor sheets;
 * accessories are original simple 2D pixel geometry, not tinted source sprites.
 */
export const AmbientActor = React.memo(function AmbientActor({
  person,
  tileSize,
}: Props) {
  const transform = useRef(
    new Animated.ValueXY({ x: person.x * tileSize, y: person.y * tileSize }),
  ).current;
  const lastTarget = useRef({ x: person.x, y: person.y });
  const [moving, setMoving] = useState(false);
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const dx = person.x - lastTarget.current.x;
    const dy = person.y - lastTarget.current.y;
    lastTarget.current = { x: person.x, y: person.y };
    if (Math.hypot(dx, dy) < 0.001) {
      setMoving(false);
      return;
    }
    setMoving(true);
    const animation = Animated.timing(transform, {
      toValue: { x: person.x * tileSize, y: person.y * tileSize },
      duration: 950,
      easing: Easing.linear,
      useNativeDriver: true,
    });
    animation.start(({ finished }) => {
      if (finished) setMoving(false);
    });
    return () => animation.stop();
  }, [person.x, person.y, tileSize, transform]);

  useEffect(() => {
    if (!moving) {
      setPhase(0);
      return;
    }
    const timer = setInterval(() => setPhase((value) => (value + 1) % 4), 170);
    return () => clearInterval(timer);
  }, [moving]);

  const hasWalkSheet = person.spriteKey === 'pulse:n1';
  const frame = moving ? phase : 0;
  const direction = person.facing;
  const sheet = {
    up: pixelArt.n1_up_sheet,
    down: pixelArt.n1_down_sheet,
    left: pixelArt.n1_left_sheet,
    right: pixelArt.n1_right_sheet,
  }[direction];
  const cap = person.profile.accessory === 'cap';
  const satchel = person.profile.accessory === 'satchel';
  const unit = tileSize / 16;

  return (
    <Animated.View
      testID={'ambient-' + person.id}
      accessible
      accessibilityLabel={person.profile.name + ', ' + person.profile.role}
      style={[
        styles.actor,
        { width: tileSize, height: tileSize },
        { transform: transform.getTranslateTransform() },
      ]}
    >
      <View style={[styles.sprite, { width: tileSize, height: tileSize }]}>
        {hasWalkSheet ? (
          <Image
            source={sheet}
            resizeMode="stretch"
            style={[
              {
                position: 'absolute',
                width: tileSize * 4,
                height: tileSize,
                left: -frame * tileSize,
                top: 0,
              },
              PIXELATED,
            ]}
          />
        ) : (
          <Image
            source={actorArt(person.look, direction)}
            resizeMode="stretch"
            style={[{ width: tileSize, height: tileSize }, PIXELATED]}
          />
        )}
      </View>
      {cap ? (
        <View pointerEvents="none" style={{
          position: 'absolute',
          left: 4 * unit,
          top: 2 * unit,
          width: 8 * unit,
          height: 2 * unit,
          backgroundColor: person.profile.outfitColor,
        }} />
      ) : null}
      {satchel ? (
        <View pointerEvents="none" style={{
          position: 'absolute',
          left: (direction === 'left' ? 10 : 1) * unit,
          top: 9 * unit,
          width: 3 * unit,
          height: 4 * unit,
          backgroundColor: person.profile.outfitColor,
        }} />
      ) : null}
    </Animated.View>
  );
});

const styles = StyleSheet.create({
  actor: {
    position: 'absolute',
  },
  sprite: {
    overflow: 'hidden',
  },
});
