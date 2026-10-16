import React, { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import {
  APPEARANCE_GROUPS, EYE_COLORS, HAIR_COLORS, OUTFIT_COLORS, SKIN_COLORS,
  type Appearance,
} from '@living/world-schema';
import { AvatarPortrait } from './AvatarPortrait';

type Key = keyof Appearance;
const OPTIONS: { [K in Key]: readonly Appearance[K][] } = {
  skinTone:['porcelain','ivory','peach','sand','golden','olive','tan','caramel','cocoa','mahogany','umber','espresso'],
  face:['oval','round','heart','square','long'],
  eyes:['almond','round','hooded','upturned','downturned'],
  eyeColor:['brown','hazel','amber','green','blue','gray','violet'],
  nose:['soft','straight','button','broad'],
  lips:['natural','full','thin','smile'],
  brows:['soft','arched','straight','bold'],
  hair:['pixie','buzz','bob','lob','waves','curls','coils','afro','ponytail','braids','locs','sidepart','shag','long'],
  hairColor:['midnight','black','espresso','chestnut','auburn','copper','blonde','ash','silver','rose','blue','violet'],
  body:['slim','average','athletic','broad'],
  outfit:['casual','streetwear','smart','formal','cozy','athletic','vintage','creative','evening'],
  outfitColor:['navy','charcoal','forest','burgundy','cream','plum','teal','rose','gold'],
  accessory:['none','glasses','earrings','necklace','freckles'],
};
const GROUP_ICONS: Record<Key,string> = {
  skinTone:'◒', face:'◯', eyes:'◉', eyeColor:'✦', nose:'⌁',
  lips:'♡', brows:'⌃', hair:'♛', hairColor:'✧', body:'♙',
  outfit:'✂', outfitColor:'◆', accessory:'◇',
};
function colorFor(k: Key, value: string): string | undefined {
  if(k==='skinTone') return SKIN_COLORS[value as keyof typeof SKIN_COLORS];
  if(k==='eyeColor') return EYE_COLORS[value as keyof typeof EYE_COLORS];
  if(k==='hairColor') return HAIR_COLORS[value as keyof typeof HAIR_COLORS];
  if(k==='outfitColor') return OUTFIT_COLORS[value as keyof typeof OUTFIT_COLORS];
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
  const entry = APPEARANCE_GROUPS.find(x => x.key === selected)!;
  const choices = OPTIONS[selected] as readonly string[];
  return (
    <View style={styles.shell}>
      <View style={styles.header}>
        <View style={{ flex: 1, gap: 7 }}>
          <Text style={styles.kicker}>LIVEIT · CHARACTER STUDIO</Text>
          <Text style={styles.title}>{heading}</Text>
          <Text style={styles.help}>
            Your look is yours to change. All skin tones, hair, body shapes and
            clothes are available from the beginning—no tickets, gems or paid outfits.
          </Text>
        </View>
      </View>
      <View style={styles.layout}>
        <View style={[styles.preview, compact && { minHeight: 260 }]}>
          <View style={styles.spotlight} />
          <Text style={styles.previewLabel}>LIVE CHARACTER PREVIEW</Text>
          <AvatarPortrait appearance={appearance} size={compact ? 168 : 220} />
          <View style={styles.previewBar}>
            <Text style={styles.previewSubtitle}>MY CHARACTER</Text>
            <Text style={styles.previewHint}>Changes appear instantly</Text>
          </View>
        </View>
        <View style={styles.controls}>
          <Text style={styles.controlHeading}>CUSTOMIZE</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.groups} accessibilityLabel="Appearance categories">
            {APPEARANCE_GROUPS.map(group => (
              <Pressable
                accessibilityRole="tab"
                accessibilityLabel={group.label}
                accessibilityState={{ selected: selected === group.key }}
                onPress={() => setSelected(group.key)}
                key={group.key}
                style={[styles.group, selected === group.key && styles.groupActive]}
              >
                <Text style={styles.groupIcon}>{GROUP_ICONS[group.key]}</Text>
                <Text style={[styles.groupText, selected === group.key && styles.groupTextActive]}>{group.label}</Text>
              </Pressable>
            ))}
          </ScrollView>
          <View style={styles.optionHeading}>
            <Text style={styles.optionTitle}>{entry.label.toUpperCase()}</Text>
            <Text style={styles.optionCount}>{choices.length} free options</Text>
          </View>
          <View style={styles.options}>
            {choices.map(value => {
              const active = appearance[selected] === value;
              const swatch = colorFor(selected, value);
              return (
                <Pressable
                  key={value}
                  accessibilityRole="radio"
                  accessibilityLabel={`${entry.label}: ${value}`}
                  accessibilityState={{ selected: active, checked: active }}
                  onPress={() => onChange({ ...appearance, [selected]: value })}
                  style={[styles.option, active && styles.activeOption]}
                >
                  {swatch ? (
                    <View style={[styles.swatch, { backgroundColor: swatch }, active && styles.activeSwatch]} />
                  ) : (
                    <Text style={styles.optionGlyph}>{GROUP_ICONS[selected]}</Text>
                  )}
                  <Text numberOfLines={1} style={[styles.optionText, active && styles.activeText]}>
                    {value.replace(/([A-Z])/g, ' $1')}
                  </Text>
                  {active && <Text style={styles.tick}>✓</Text>}
                </Pressable>
              );
            })}
          </View>
          <Text style={styles.footer}>✧ Your appearance is cosmetic. It will never change your career chances, health or dialogue outcomes.</Text>
        </View>
      </View>
    </View>
  );
}
const styles = StyleSheet.create({
  shell:{ gap:16, width:'100%' },
  header:{ flexDirection:'row',gap:14 },
  kicker:{color:'#e6bc8f',fontSize:10,fontWeight:'800',letterSpacing:1.8},
  title:{color:'#ffead4',fontFamily:'serif',fontSize:27},
  help:{color:'#c1c8d4',lineHeight:20,fontSize:13,maxWidth:670},
  layout:{flexDirection:'row',flexWrap:'wrap',gap:14,alignItems:'stretch'},
  preview:{flexGrow:1,flexBasis:225,backgroundColor:'#20253b',borderWidth:1,borderColor:'#a67a61',borderRadius:14,minHeight:335,alignItems:'center',justifyContent:'flex-end',paddingTop:35,overflow:'hidden'},
  spotlight:{position:'absolute',width:210,height:250,borderRadius:110,backgroundColor:'#4e415d',top:39,opacity:.48},
  previewLabel:{position:'absolute',top:16,left:14,color:'#eec499',letterSpacing:1.4,fontSize:9,fontWeight:'800'},
  previewBar:{backgroundColor:'rgba(10,19,33,.95)',paddingVertical:12,paddingHorizontal:18,width:'100%',flexDirection:'row',justifyContent:'space-between',alignItems:'center',gap:6,flexWrap:'wrap'},
  previewSubtitle:{color:'#f6d4ac',fontSize:10,fontWeight:'800',letterSpacing:1.2},
  previewHint:{color:'#abb7c6',fontSize:10},
  controls:{flex:2,flexBasis:280,minWidth:0,gap:13,padding:15,borderWidth:1,borderColor:'#4d566b',backgroundColor:'#17263a',borderRadius:14},
  controlHeading:{fontSize:11,color:'#f2c38c',letterSpacing:2,fontWeight:'800'},
  groups:{gap:7,paddingBottom:5},
  group:{borderRadius:9,paddingHorizontal:12,paddingVertical:10,minHeight:66,minWidth:76,alignItems:'center',gap:6,borderWidth:1,borderColor:'#48536a',backgroundColor:'#1f2b40'},
  groupActive:{borderColor:'#eac18c',backgroundColor:'#5e403c'},
  groupIcon:{color:'#f9c996',fontSize:22},
  groupText:{color:'#c4cfdb',fontSize:10,fontWeight:'700'},
  groupTextActive:{color:'#ffe6c9'},
  optionHeading:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',gap:6},
  optionTitle:{color:'#e7b789',fontSize:11,letterSpacing:1.1,fontWeight:'800'},
  optionCount:{color:'#b1bdcb',fontSize:11},
  options:{flexDirection:'row',flexWrap:'wrap',gap:7},
  option:{flexBasis:102,flexGrow:1,maxWidth:165,minHeight:70,borderWidth:1,borderColor:'#536277',borderRadius:9,backgroundColor:'#263549',justifyContent:'center',alignItems:'center',padding:7,gap:3},
  activeOption:{backgroundColor:'#61443d',borderColor:'#ffc98f',borderWidth:2},
  swatch:{width:27,height:27,borderRadius:17,borderColor:'#ffffff66',borderWidth:1},
  activeSwatch:{borderColor:'#ffffff',borderWidth:2},
  optionGlyph:{fontSize:23,color:'#f5c38d'},
  optionText:{fontSize:11,color:'#d8dce6',textTransform:'capitalize',fontWeight:'700'},
  activeText:{color:'#ffe6be'},
  tick:{position:'absolute',right:6,top:4,color:'#ffe1a7',fontSize:13,fontWeight:'900'},
  footer:{color:'#9eaebf',fontSize:11,lineHeight:17},
});
