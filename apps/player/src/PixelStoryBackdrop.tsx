import React, { useState } from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import { pixelArt } from './pixelArt';
import { gameTheme as t } from './gameTheme';

type Mood = 'reflective' | 'tense' | 'warm';
type Block = Readonly<{
  x: number;
  y: number;
  w: number;
  h: number;
  color: string;
}>;

/**
 * Original, full-resolution 2D pixel café stage for the emotional story mode.
 * Everything is blocks/palette/CC0 16-pixel sprites—no photograph, 3D mesh,
 * GPU skinning, or remote image. Render layers sit BEHIND the native readable
 * dialogue dock, so narrative and state logic stay intact.
 *
 * Design grid: 320 logical units. Block positions are always rounded to whole
 * source pixels before being scaled to the device's actual layout width.
 */
export function PixelStoryBackdrop({
  mood,
  stageHeight,
}: {
  mood: Mood;
  stageHeight: number;
}) {
  const [width, setWidth] = useState(320);
  const scale = width / 320;
  const warm = mood === 'warm';
  const tense = mood === 'tense';
  const palette = {
    wall: tense ? '#403444' : warm ? '#775644' : '#4d5265',
    wallLight: tense ? '#58475c' : warm ? '#a07455' : '#656e82',
    floor: tense ? '#352b40' : '#44372f',
    accent: tense ? '#f08798' : '#f5d28f',
    glass: tense ? '#292845' : warm ? '#4d5982' : '#293f66',
    night: tense ? '#171527' : '#142840',
    shadow: '#182433',
  };
  const shapes: Block[] = [];
  const add = (x: number, y: number, w: number, h: number, color: string) => {
    shapes.push({ x, y, w, h, color });
  };

  // The wall is visually built from deliberate horizontal strips and brick
  // seams, rather than a blurred texture or a random noise effect.
  add(0, 0, 320, 292, palette.wall);
  for (let y = 0; y <= 288; y += 16) {
    add(0, y, 320, 2, palette.wallLight);
    for (let x = (Math.floor(y / 16) % 2) * 14; x < 320; x += 28) {
      add(x, y + 2, 2, 14, palette.wallLight);
    }
  }

  // Deep-blue rainy-window vista, framed in rich café oak.
  add(20, 88, 126, 162, '#231e29');
  add(24, 92, 118, 154, '#a57755');
  add(29, 98, 108, 143, palette.glass);
  add(33, 103, 100, 134, palette.night);
  add(35, 166, 97, 71, palette.glass);
  add(75, 98, 6, 143, '#b38764');
  add(29, 160, 108, 6, '#b38764');
  add(24, 236, 118, 8, '#2d2631');
  add(35, 236, 100, 2, '#f0b87b');
  // Distant skyline. Yellow lit windows reveal the city beyond the scene.
  const buildings = [
    { x: 36, h: 42 },
    { x: 57, h: 59 },
    { x: 84, h: 35 },
    { x: 104, h: 51 },
  ];
  for (const b of buildings) {
    add(b.x, 236 - b.h, 17, b.h, '#27364e');
    for (let y = 236 - b.h + 8; y < 232; y += 15) {
      add(b.x + 5, y, 4, 5, palette.accent);
    }
  }
  for (let i = 0; i < 12; i++) {
    const x = 40 + ((i * 29) % 90);
    const y = 110 + ((i * 37) % 108);
    add(x, y, 2, 10, '#849bb6');
  }

  // Shelf and café coffee bar, seen side-on behind two character portraits.
  add(205, 98, 91, 152, '#201f29');
  add(211, 103, 79, 142, '#694538');
  add(216, 126, 68, 5, '#d29a67');
  add(216, 177, 68, 5, '#d29a67');
  add(216, 222, 68, 5, '#d29a67');
  for (const x of [222, 235, 248, 261, 274]) {
    add(x, 105, 6, 19, '#a3a36c');
    add(x, 156, 7, 19, '#d4a47b');
    add(x, 202, 5, 18, '#88a19c');
  }
  add(178, 261, 130, 14, '#342733');
  add(178, 275, 130, 54, '#6e4b3e');
  add(184, 282, 116, 7, '#8a5c49');
  add(188, 292, 106, 5, '#ba7657');
  add(174, 248, 141, 14, '#c69565');
  add(178, 245, 133, 4, '#f1cb90');
  // A white pixel mug and small ceramic saucer.
  add(205, 236, 18, 10, '#f6e7ca');
  add(222, 239, 5, 4, '#f6e7ca');
  add(209, 235, 10, 3, '#3d2e29');
  add(203, 246, 25, 3, '#e5c5a5');

  // Tungsten pendant with deliberately blocky radial illumination.
  add(164, 0, 3, 93, '#231e29');
  add(155, 88, 22, 8, '#302431');
  add(146, 97, 39, 10, '#db9a62');
  add(153, 107, 25, 6, '#ffde9b');
  add(159, 113, 11, 4, '#fff3c8');
  add(144, 119, 43, 4, warm ? '#dfab65' : '#ba8158');

  // Foreground mosaic floor and café table framing.
  add(0, 325, 320, 400, palette.floor);
  for (let y = 327; y < 600; y += 25) {
    add(0, y, 320, 3, '#584338');
    for (let x = (Math.floor(y / 25) % 2) * 38; x < 320; x += 64) {
      add(x, y + 3, 3, 22, '#302a2c');
    }
  }
  add(37, 340, 118, 12, '#c79461');
  add(40, 351, 8, 76, '#553b33');
  add(140, 351, 8, 76, '#553b33');
  add(52, 352, 88, 5, '#f4ca91');
  add(75, 331, 15, 8, '#f5e9cf');
  add(90, 332, 4, 5, '#f5e9cf');

  // Tiny coat stand/plant creates a readable side silhouette.
  add(308, 298, 3, 56, '#302632');
  add(295, 351, 27, 5, '#302632');
  add(294, 318, 22, 30, '#594638');
  add(289, 303, 25, 24, '#456749');
  add(302, 287, 14, 28, '#67945f');
  add(287, 295, 15, 26, '#7ea16e');

  return (
    <View
      testID="pixel-story-background"
      accessibilityLabel="Original two-dimensional pixel-art café, with rainy window, warm lamp, mugs and nighttime Bellweather skyline"
      style={[styles.stage, { height: stageHeight }]}
      onLayout={(e) => {
        const next = Math.round(e.nativeEvent.layout.width);
        if (next > 0 && next !== width) setWidth(next);
      }}
      pointerEvents="none"
    >
      {shapes.map((part, i) => (
        <View
          key={i}
          style={{
            position: 'absolute',
            left: Math.round(part.x * scale),
            top: Math.round(part.y * scale),
            width: Math.max(1, Math.round(part.w * scale)),
            height: Math.max(1, Math.round(part.h * scale)),
            backgroundColor: part.color,
          }}
        />
      ))}
      {/* A few actual source PNG fragments tie the story color language to the town. */}
      <Image
        source={pixelArt.plant}
        resizeMode="stretch"
        style={{
          position: 'absolute',
          top: Math.round(298 * scale),
          left: Math.round(284 * scale),
          width: Math.round(24 * scale),
          height: Math.round(24 * scale),
        }}
      />
      <View style={styles.pixelPlacard}>
        <Text style={styles.pixelLabel}>BELLWEATHER · CORNER CAFÉ</Text>
      </View>
      <View style={[styles.moodBar, { backgroundColor: palette.accent }]} />
    </View>
  );
}
const styles = StyleSheet.create({
  stage: {
    width: '100%',
    overflow: 'hidden',
    backgroundColor: '#161c31',
    borderRadius: 8,
    borderColor: t.border,
    borderWidth: 2,
    position: 'relative',
  },
  pixelPlacard: {
    position: 'absolute',
    top: 64,
    left: 12,
    backgroundColor: '#101827E0',
    borderWidth: 1,
    borderColor: '#b78468',
    paddingHorizontal: 8,
    paddingVertical: 5,
  },
  pixelLabel: {
    fontSize: 10,
    fontWeight: '900',
    color: '#ffddac',
    letterSpacing: 1,
  },
  moodBar: { height: 4, width: '100%', position: 'absolute', bottom: 0 },
});
