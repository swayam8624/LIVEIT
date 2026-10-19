import React, { useEffect, useState } from 'react';
import { View } from 'react-native';
import {
  DEFAULT_APPEARANCE,
  EYE_COLORS,
  HAIR_COLORS,
  OUTFIT_COLORS,
  SKIN_COLORS,
  type Appearance,
} from '@living/world-schema';

export type PixelEmotion = 'neutral' | 'happy' | 'tense' | 'sad' | 'shocked';
type PixelRect = { x: number; y: number; w: number; h: number; color: string };
const INK = '#171e30';
const OUTLINE = '#1b1c2b';
const shine = '#e4d2bd';
const npcAppearance: Appearance = {
  ...DEFAULT_APPEARANCE,
  skinTone: 'ivory',
  hair: 'bob',
  hairColor: 'chestnut',
  eyeColor: 'green',
  outfit: 'cozy',
  outfitColor: 'burgundy',
};

/**
 * A fully 2D, resolution-independent *pixel block* portrait. It is not
 * rasterized photography or a disguised 3D object. Character palette and
 * outfit values are driven by the saved Appearance schema.
 *
 * Animation is frame-based with blinking / speaking mouth, disabled for
 * reduced-motion users. This simple native layer is a first pixel-acting
 * system; bespoke authored portrait sheets can replace the block geometry.
 */
export function PixelPortrait({
  appearance = DEFAULT_APPEARANCE,
  size = 154,
  mood = 'neutral',
  speaking = false,
  reducedMotion = false,
  label = 'Pixel character portrait',
}: {
  appearance?: Appearance;
  size?: number;
  mood?: PixelEmotion;
  speaking?: boolean;
  reducedMotion?: boolean;
  label?: string;
}) {
  const [blink, setBlink] = useState(false);
  const [mouthOpen, setMouthOpen] = useState(false);
  useEffect(() => {
    if (reducedMotion) {
      setBlink(false);
      setMouthOpen(false);
      return;
    }
    const blinkInterval = setInterval(() => {
      setBlink(true);
    }, 2800);
    const openInterval = setInterval(() => {
      setMouthOpen((value) => !value);
    }, 260);
    const blinkStop = setInterval(() => {
      setBlink(false);
    }, 2890);
    return () => {
      clearInterval(blinkInterval);
      clearInterval(openInterval);
      clearInterval(blinkStop);
    };
  }, [reducedMotion]);
  const pixel = Math.max(2, Math.floor(size / 48));
  const hair = HAIR_COLORS[appearance.hairColor];
  const skin = SKIN_COLORS[appearance.skinTone];
  const eyes = EYE_COLORS[appearance.eyeColor];
  const clothes = OUTFIT_COLORS[appearance.outfitColor];
  const longHair = ['bob', 'lob', 'waves', 'curls', 'coils', 'afro', 'ponytail', 'braids', 'locs', 'shag', 'long'].includes(appearance.hair);
  const shortHair = ['buzz', 'pixie'].includes(appearance.hair);
  const happy = mood === 'happy';
  const sad = mood === 'sad';
  const shocked = mood === 'shocked';
  const angry = mood === 'tense';
  const parts: PixelRect[] = [
    // Soft dark outline, torso and sleeves in the saved outfit palette.
    { x: 9, y: 38, w: 30, h: 26, color: OUTLINE },
    { x: 12, y: 39, w: 24, h: 25, color: clothes },
    { x: 7, y: 45, w: 5, h: 19, color: clothes },
    { x: 36, y: 45, w: 5, h: 19, color: clothes },
    { x: 18, y: 43, w: 12, h: 2, color: '#ffffff55' },
    // Back hair silhouette.
    ...(longHair ? [
      { x: 10, y: 10, w: 28, h: 34, color: hair },
      { x: 10, y: 25, w: 5, h: 17, color: hair },
      { x: 33, y: 25, w: 5, h: 17, color: hair },
    ] : []),
    { x: 18, y: 35, w: 12, h: 9, color: OUTLINE },
    { x: 20, y: 36, w: 8, h: 8, color: skin },
    { x: 13, y: 13, w: 23, h: 25, color: OUTLINE },
    { x: 15, y: 15, w: 19, h: 22, color: skin },
    // Subtle cheeks and ears.
    { x: 11, y: 23, w: 4, h: 7, color: skin },
    { x: 34, y: 23, w: 4, h: 7, color: skin },
    { x: 15, y: 30, w: 5, h: 2, color: '#aa685640' },
    { x: 29, y: 30, w: 5, h: 2, color: '#aa685640' },
    // Hair, with original visible side fringe.
    { x: 12, y: 10, w: 25, h: shortHair ? 6 : 9, color: hair },
    { x: 13, y: 17, w: 7, h: shortHair ? 1 : 5, color: hair },
    { x: 29, y: 17, w: 7, h: shortHair ? 1 : 5, color: hair },
    { x: 17, y: 11, w: 9, h: 2, color: shine },
    // Brows.
    { x: 18, y: angry ? 23 : 22, w: 5, h: 2, color: hair },
    { x: 27, y: angry ? 23 : 22, w: 5, h: 2, color: hair },
    // Eyes. Tiny frames work at handheld scale.
    { x: 19, y: 25, w: 4, h: blink ? 1 : shocked ? 5 : 3, color: eyes },
    { x: 27, y: 25, w: 4, h: blink ? 1 : shocked ? 5 : 3, color: eyes },
    { x: 20, y: 25, w: 1, h: 1, color: '#f2f3fa' },
    { x: 28, y: 25, w: 1, h: 1, color: '#f2f3fa' },
    // Nose and animated mouth.
    { x: 24, y: 29, w: 2, h: 2, color: '#8f6858' },
    { x: happy ? 21 : 22, y: sad ? 34 : 33, w: happy ? 8 : 6, h: shocked || (speaking && mouthOpen) ? 4 : 2, color: INK },
    ...(happy ? [{ x: 24, y: 35, w: 3, h: 1, color: '#f5c0a8' }] : []),
    ...(sad ? [{ x: 23, y: 33, w: 5, h: 1, color: skin }] : []),
  ];
  return (
    <View
      accessible
      accessibilityRole="image"
      accessibilityLabel={label + ': ' + mood + (speaking ? ', speaking' : '')}
      style={{
        width: 48 * pixel,
        height: 64 * pixel,
        backgroundColor: '#2a3949',
        borderWidth: pixel,
        borderColor: '#101827',
        overflow: 'hidden',
      }}
    >
      {parts.map((part, index) => (
        <View
          key={index}
          style={{
            position: 'absolute',
            left: part.x * pixel,
            top: part.y * pixel,
            width: part.w * pixel,
            height: part.h * pixel,
            backgroundColor: part.color,
          }}
        />
      ))}
    </View>
  );
}
export const AMELIA_PIXEL_APPEARANCE = npcAppearance;
