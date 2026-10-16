import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import {
  DEFAULT_APPEARANCE, SKIN_COLORS, HAIR_COLORS, EYE_COLORS,
  OUTFIT_COLORS, type Appearance,
} from '@living/world-schema';

type Rect = { x: number; y: number; w: number; h: number; radius?: number; rotate?: string };
function Piece({ form, color, border }: { form: Rect; color: string; border?: string }) {
  return <View style={{
    position: 'absolute', left: form.x, top: form.y, width: form.w, height: form.h,
    backgroundColor: color, borderRadius: form.radius ?? 0,
    transform: form.rotate ? [{ rotate: form.rotate }] : undefined,
    ...(border ? { borderColor: border, borderWidth: 1 } : {}),
  }} />;
}
/** Offline, illustrated paper-doll portrait. No runtime generation, network
 * assets or protected Episode graphics. Later rigged textures can replace the
 * renderer without migrating players' saved appearance presets.
 */
export function AvatarPortrait({
  appearance = DEFAULT_APPEARANCE,
  size = 200,
  label,
  expression = 'neutral',
}: { appearance?: Appearance; size?: number; label?: string; expression?: 'neutral' | 'happy' | 'sad' | 'tense' }) {
  const a = appearance;
  const skin = SKIN_COLORS[a.skinTone];
  const hair = HAIR_COLORS[a.hairColor];
  const iris = EYE_COLORS[a.eyeColor];
  const shirt = OUTFIT_COLORS[a.outfitColor];
  const dark = '#262332';
  const faceH = a.face === 'long' ? 149 : a.face === 'round' ? 129 : 141;
  const jaw = a.face === 'square' ? 46 : a.face === 'heart' ? 78 : a.face === 'round' ? 85 : 69;
  const hairLong = ['long','waves','curls','coils','braids','locs','ponytail','lob','shag'].includes(a.hair);
  const fringe = ['bob','lob','pixie','waves','curls','coils','shag','sidepart','long','afro'].includes(a.hair);
  const eyeW = a.eyes === 'round' ? 23 : a.eyes === 'hooded' ? 24 : 27;
  const eyeH = a.eyes === 'round' ? 16 : a.eyes === 'hooded' ? 8 : 12;
  const bodyW = a.body === 'broad' ? 209 : a.body === 'athletic' ? 193 : a.body === 'slim' ? 155 : 177;
  const base = 244;
  const scale = size / base;
  return (
    <View
      accessibilityRole="image"
      accessibilityLabel={label ?? `Character with ${a.hairColor} ${a.hair}, ${a.skinTone} skin and ${a.outfit} clothes`}
      style={{ width: size, height: 285 * scale, overflow: 'hidden', alignSelf: 'center' }}
    >
      <View style={{ width: base, height: 285, transform: [{ scale }], transformOrigin: 'top left' }}>
        {/* Depth behind the silhouette. */}
        <Piece form={{ x: 14, y: 36, w: 218, h: 224, radius: 105 }} color="#202b42" />
        <Piece form={{ x: 30, y: 21, w: 188, h: 233, radius: 100 }} color="#33364e" />
        {/* Long hair is physically behind neck and jacket. */}
        {hairLong && <Piece form={{ x: 52, y: 31, w: 141, h: a.hair === 'long' ? 225 : 185, radius: 60 }} color={hair} />}
        {a.hair === 'ponytail' && <Piece form={{ x: 174, y: 48, w: 46, h: 158, radius: 29, rotate: '-15deg' }} color={hair} />}
        {/* Outfit and shoulder silhouettes: renderer can swap all pieces later. */}
        <Piece form={{ x: (244-bodyW)/2, y: 218, w: bodyW, h: 105, radius: a.outfit === 'formal' ? 32 : 65 }} color={shirt} />
        <Piece form={{ x: 97, y: 196, w: 51, h: 53, radius: 17 }} color={skin} />
        {['formal','smart','vintage','evening'].includes(a.outfit) && <>
          <Piece form={{ x: 65, y: 225, w: 51, h: 70, radius: 6, rotate: '-15deg' }} color="#eee0cf" />
          <Piece form={{ x: 128, y: 225, w: 51, h: 70, radius: 6, rotate: '15deg' }} color="#eee0cf" />
        </>}
        {a.outfit === 'streetwear' && <Piece form={{ x: 78, y: 242, w: 90, h: 49, radius: 16 }} color="#111c2a" />}
        {a.outfit === 'athletic' && <Piece form={{ x: 116, y: 243, w: 11, h: 42, radius: 4 }} color="#f2ede0" />}
        {a.outfit === 'creative' && <Piece form={{ x: 106, y: 261, w: 32, h: 13, radius: 6 }} color="#f0b785" />}
        {a.outfit === 'cozy' && <Piece form={{ x: 74, y: 218, w: 97, h: 46, radius: 26 }} color={shirt} />}
        {/* Hair mass behind front of the face, and anatomically distinct jaw shape. */}
        <Piece form={{ x: 55, y: 24, w: 135, h: 176, radius: a.hair === 'buzz' ? 62 : 69 }} color={hair} />
        <Piece form={{ x: 69, y: 69, w: 106, h: faceH, radius: jaw }} color={skin} />
        {a.face === 'heart' && <Piece form={{ x: 99, y: 180, w: 48, h: 27, radius: 23 }} color={skin} />}
        {/* Ears are behind face but visible for accessories. */}
        <Piece form={{ x: 60, y: 119, w: 19, h: 35, radius: 12 }} color={skin} />
        <Piece form={{ x: 166, y: 119, w: 19, h: 35, radius: 12 }} color={skin} />
        {/* Soft cheek shadows. */}
        <Piece form={{ x: 79, y: 148, w: 23, h: 11, radius: 12 }} color="#a85e5b44" />
        <Piece form={{ x: 143, y: 148, w: 23, h: 11, radius: 12 }} color="#a85e5b44" />
        {/* Brows and iris colors respond to separate options. */}
        {[89,144].map((x) => <React.Fragment key={x}>
          <Piece form={{ x: x-5, y: (a.brows === 'arched' ? 109 : 114) + (expression === 'tense' ? -5 : expression === 'sad' ? 4 : 0), w: 33, h: a.brows === 'bold' ? 7 : 4, radius: 6, rotate: a.brows === 'arched' ? (x === 89 ? '-12deg' : '12deg') : undefined }} color={hair} />
          <Piece form={{ x, y: 126, w: eyeW, h: eyeH, radius: a.eyes === 'upturned' ? 3 : 12, rotate: a.eyes === 'upturned' ? (x === 89 ? '-9deg' : '9deg') : a.eyes === 'downturned' ? '7deg' : undefined }} color="#fff9ed" border="#544238" />
          <Piece form={{ x: x+8, y: 128, w: 10, h: 11, radius: 6 }} color={iris} />
          <Piece form={{ x: x+11, y: 129, w: 5, h: 8, radius: 4 }} color="#22202c" />
          <Piece form={{ x: x+10, y: 129, w: 3, h: 3, radius: 4 }} color="#ffffff" />
        </React.Fragment>)}
        {/* Nose and lips, both independently customizable. */}
        <Piece form={{ x: a.nose === 'broad' ? 115 : 118, y: 136, w: a.nose === 'broad' ? 16 : 10, h: a.nose === 'straight' ? 29 : 22, radius: 10 }} color="#9b5b4d44" />
        <Piece form={{ x: 113, y: 157, w: a.nose === 'broad' ? 23 : a.nose === 'button' ? 13 : 18, h: 5, radius: 4 }} color="#8f574744" />
        <Piece form={{ x: a.lips === 'full' ? 104 : 109, y: expression === 'happy' ? 174 : expression === 'sad' ? 181 : 176, w: a.lips === 'full' ? 38 : a.lips === 'thin' ? 24 : 29, h: a.lips === 'full' ? 12 : a.lips === 'thin' ? 4 : 7, radius: 14 }} color={a.lips === 'smile' ? '#ab5b55' : '#a65d5a'} />
        {a.accessory === 'freckles' && [89,95,103,145,151,159].map(x => <Piece key={x} form={{ x,y:152+(x%3)*3,w:3,h:3,radius:3 }} color="#7d4c39" />)}
        {/* Optional cosmetics: compatible with old saves where fields are absent. */}
        {a.makeup === 'bold' && <Piece form={{x:100,y:170,w:45,h:16,radius:11}} color="#a34c72" />}
        {a.makeup === 'gloss' && <Piece form={{x:111,y:178,w:24,h:4,radius:4}} color="#f49aaa" />}
        {a.makeup === 'soft' && <>
          <Piece form={{x:79,y:153,w:22,h:9,radius:10}} color="#cb708855"/>
          <Piece form={{x:146,y:153,w:22,h:9,radius:10}} color="#cb708855"/>
        </>}
        {a.facialHair === 'stubble' && <Piece form={{x:90,y:181,w:64,h:24,radius:18}} color="#44353255" />}
        {a.facialHair === 'goatee' && <Piece form={{x:111,y:188,w:24,h:30,radius:11}} color={hair} />}
        {a.facialHair === 'beard' && <>
          <Piece form={{x:75,y:166,w:26,h:39,radius:18}} color={hair}/>
          <Piece form={{x:145,y:166,w:26,h:39,radius:18}} color={hair}/>
          <Piece form={{x:91,y:188,w:62,h:32,radius:20}} color={hair}/>
        </>}
        {a.facialHair === 'moustache' && <>
          <Piece form={{x:100,y:168,w:22,h:8,radius:6}} color={hair}/>
          <Piece form={{x:124,y:168,w:22,h:8,radius:6}} color={hair}/>
        </>}
        {/* Hairline, fringe and hair styling drawn ABOVE facial features. */}
        {a.hair === 'buzz' && <Piece form={{ x: 63, y: 50, w: 122, h: 45, radius: 55 }} color={hair} />}
        {fringe && <Piece form={{ x: 57, y: 34, w: 133, h: a.hair === 'afro' ? 80 : 68, radius: a.hair === 'afro' ? 60 : 42, rotate: a.hair === 'shag' ? '-7deg' : undefined }} color={hair} />}
        {fringe && <Piece form={{ x: 56, y: 77, w: a.hair === 'sidepart' ? 45 : 35, h: 72, radius: 20, rotate: '13deg' }} color={hair} />}
        {fringe && <Piece form={{ x: 167, y: 70, w: 27, h: a.hair === 'bob' ? 109 : 63, radius: 18, rotate: '-8deg' }} color={hair} />}
        {a.hair === 'pixie' && <Piece form={{ x: 56, y: 53, w: 128, h: 58, radius: 46 }} color={hair} />}
        {a.hair === 'sidepart' && <Piece form={{ x: 61, y: 36, w: 97, h: 64, radius: 24, rotate: '-13deg' }} color={hair} />}
        {a.hair === 'afro' && [-1,0,1,2,3,4].map(i => <Piece key={i} form={{ x: 50 + i*24, y: i%2?23:9, w: 51, h: 63, radius: 32 }} color={hair} />)}
        {['braids','locs'].includes(a.hair) && [0,1,2,3].map(i => <Piece key={i} form={{ x: i<2 ? 56+i*19 : 157+(i-2)*19, y: 93, w: a.hair === 'locs' ? 13 : 10, h: 122-(i%2)*24, radius: 9 }} color={hair} />)}
        {/* Separate headwear layer atop hair. No gameplay stat bonus. */}
        {a.headwear === 'beanie' && <Piece form={{x:57,y:17,w:132,h:59,radius:42}} color="#a76874"/>}
        {a.headwear === 'cap' && <>
          <Piece form={{x:59,y:30,w:124,h:45,radius:36}} color="#3a6484"/>
          <Piece form={{x:106,y:66,w:94,h:15,radius:10}} color="#3a6484"/>
        </>}
        {a.headwear === 'beret' && <Piece form={{x:62,y:17,w:135,h:47,radius:32,rotate:'-13deg'}} color="#8b4a60"/>}
        {a.headwear === 'headband' && <Piece form={{x:55,y:72,w:135,h:10,radius:8}} color="#d6a45f"/>}
        {/* Piercings and eyewear belong to an independent equipment layer. */}
        {a.accessory === 'earrings' && <><Piece form={{x:63,y:148,w:10,h:15,radius:9}} color="#e9c17b"/><Piece form={{x:172,y:148,w:10,h:15,radius:9}} color="#e9c17b"/></>}
        {a.accessory === 'necklace' && <Piece form={{x:119,y:225,w:10,h:13,radius:9}} color="#f5ca81"/>}
        {a.accessory === 'glasses' && <>
          {[83,137].map(x=><View key={x} style={{ position:'absolute',left:x,top:122,width:39,height:27,borderRadius:11,borderWidth:3,borderColor:dark,backgroundColor:'transparent' }}/>)}
          <Piece form={{x:122,y:132,w:16,h:4,radius:2}} color={dark} />
        </>}
        {/* Clothing always stays visually in front of the stage framing. */}
        <View pointerEvents="none" style={styles.hilight}><Text style={styles.hilightText}>✧</Text></View>
      </View>
    </View>
  );
}
const styles = StyleSheet.create({
  hilight:{position:'absolute',top:13,right:23,opacity:0.8},
  hilightText:{fontSize:19,color:'#f3d6a1'},
});
