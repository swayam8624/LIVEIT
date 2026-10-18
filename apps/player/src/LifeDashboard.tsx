import React, { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import {
  ageUp, applyForJob, attendJobInterview, requestPromotion, resignFromJob,
  CATALOG, portfolio, netWorth, buyAsset, sellAsset, investIndex, withdrawIndex,
  pendingLifeMoment, resolveLifeMoment,
} from '@living/simulation-core';
import type { World, CareerPath } from '@living/world-schema';
import { AvatarPortrait } from './AvatarPortrait';

const GOODS = ['bicycle','car','flat','townhouse'] as const;
const ROLES: { field: Exclude<CareerPath,'undecided'>; label:string; caption:string }[] = [
  {field:'technology',label:'Developer',caption:'Systems, software and practical problem-solving'},
  {field:'creative',label:'Designer',caption:'Visual arts, studios and creative projects'},
  {field:'business',label:'Business',caption:'Trading, negotiations and enterprise'},
  {field:'community',label:'Community',caption:'Local institutions and people-first work'},
];
function cash(pence:number) {
  return new Intl.NumberFormat('en-GB',{style:'currency',currency:'GBP',maximumFractionDigits:0}).format(pence/100);
}
export function LifeDashboard({ world, onAction }:{
  world:World;
  onAction:(apply:(current:World)=>World)=>void;
}) {
  const [careerOpen,setCareerOpen]=useState(false);
  const [assetsOpen,setAssetsOpen]=useState(false);
  const age=Math.floor(world.player.ageDays/365);
  const job=world.city?.employment;
  const last=world.history.at(-1);
  const moment=pendingLifeMoment(world);
  return <View style={styles.shell}>
    <View style={styles.hero}>
      <View style={styles.heroPortrait}>
        <AvatarPortrait appearance={world.player.appearance} size={130}/>
      </View>
      <View style={styles.heroContent}>
        <Text style={styles.eyebrow}>YOUR LIFE • AGE {age}</Text>
        <Text style={styles.name}>{world.player.name}</Text>
        <Text style={styles.tagline}>{job && job.stage!=='applied' ? job.jobTitle : 'Your next chapter is waiting'}</Text>
        <View style={styles.stats}>
          <View style={styles.stat}><Text style={styles.statLabel}>SAVINGS</Text><Text style={styles.statValue}>{cash(world.player.money)}</Text></View>
          <View style={styles.stat}><Text style={styles.statLabel}>WELLBEING</Text><Text style={styles.statValue}>{world.player.wellbeing}%</Text></View>
          <View style={styles.stat}><Text style={styles.statLabel}>EXPERIENCE</Text><Text style={styles.statValue}>{world.player.skill}/100</Text></View>
        </View>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Age up one year"
          onPress={() => onAction(ageUp)}
          disabled={Boolean(moment)}
          style={({pressed})=>[styles.ageButton,pressed&&styles.pressed,Boolean(moment)&&{opacity:0.45}]}
        >
          <View style={{flex:1,gap:3}}>
            <Text style={styles.ageButtonText}>{moment ? 'MAKE YOUR CHOICE FIRST' : `AGE UP  ➜  ${age+1}`}</Text>
            <Text style={styles.ageButtonHint}>Advance one year • discover new life events</Text>
          </View>
          <Text style={styles.ageIcon}>✧</Text>
        </Pressable>
      </View>
    </View>
    {moment && <View style={styles.momentCard}>
      <Text style={styles.momentLabel}>A MOMENT THAT COULD CHANGE YOUR LIFE</Text>
      <Text style={styles.momentTitle}>{moment.title}</Text>
      <Text style={styles.momentDescription}>{moment.situation}</Text>
      <View style={styles.jobs}>
        {moment.choices.map(choice => <Pressable
          key={choice.id}
          accessibilityRole="button"
          accessibilityLabel={choice.text}
          style={({pressed})=>[styles.momentChoice,pressed&&styles.pressed]}
          onPress={()=>onAction(w=>resolveLifeMoment(w,choice.id))}
        ><Text style={styles.momentChoiceText}>{choice.text}  ↗</Text></Pressable>)}
      </View>
      <Text style={styles.muted}>Your decision changes money, relationships, skills or wellbeing and stays in your life history.</Text>
    </View>}
    {last && <View style={styles.lifeReel}>
      <Text style={styles.eyebrow}>LATEST LIFE MOMENT</Text>
      <Text style={styles.reelText}>{last.text}</Text>
    </View>}
    <View style={styles.careerArea}>
      <View style={styles.careerHeading}>
        <View style={{flex:1,gap:4}}>
          <Text style={styles.eyebrow}>CAREER</Text>
          <Text style={styles.careerTitle}>{job ? job.jobTitle : 'Find your place in the world.'}</Text>
          <Text style={styles.muted}>{job && job.stage!=='applied'
            ? `${job.company} · ${cash(job.salaryAnnual)} / year · ${job.experience} workdays experience`
            : job ? `${job.company} has invited you to interview.`
            : 'Apply to an employer, interview, work and earn your promotions.'}</Text>
        </View>
      </View>
      {!job && <Pressable accessibilityRole="button" onPress={()=>setCareerOpen(v=>!v)} style={styles.careerButton}>
        <Text style={styles.buttonText}>{careerOpen ? 'Close job listings' : 'Search available jobs  ↗'}</Text>
      </Pressable>}
      {careerOpen && !job && <View style={styles.jobs}>
        {ROLES.map(role=><Pressable
          key={role.field}
          accessibilityRole="button"
          accessibilityLabel={'Apply for '+role.label}
          onPress={()=>{onAction(w=>applyForJob(w,role.field));setCareerOpen(false);}}
          style={({pressed})=>[styles.jobItem,pressed&&styles.pressed]}
        >
          <View style={{flex:1,gap:3}}>
            <Text style={styles.jobTitle}>{role.label}</Text>
            <Text style={styles.muted}>{role.caption}</Text>
          </View>
          <Text style={styles.actionMark}>APPLY ↗</Text>
        </Pressable>)}
      </View>}
      {job?.stage==='applied' && <Pressable
        accessibilityRole="button"
        accessibilityLabel="Attend job interview"
        onPress={()=>onAction(attendJobInterview)}
        style={styles.careerButton}
      ><Text style={styles.buttonText}>Attend the interview  ↗</Text></Pressable>}
      {job && job.stage!=='applied' && <View style={styles.careerButtons}>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Request promotion"
          onPress={()=>onAction(requestPromotion)}
          style={styles.careerButton}
        ><Text style={styles.buttonText}>Request promotion  ↗</Text></Pressable>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Resign from job"
          onPress={()=>onAction(resignFromJob)}
          style={styles.ghostButton}
        ><Text style={styles.muted}>Resign</Text></Pressable>
      </View>}
    </View>
    <View style={styles.careerArea}>
      <View style={styles.careerHeading}>
        <View style={{flex:1,gap:4}}>
          <Text style={styles.eyebrow}>ASSETS & INVESTMENTS</Text>
          <Text style={styles.careerTitle}>Net worth {cash(netWorth(world))}</Text>
          <Text style={styles.muted}>Cash {cash(world.player.money)} · Index {cash(portfolio(world).indexPence)} · {portfolio(world).owned.length} owned assets</Text>
        </View>
      </View>
      <Pressable accessibilityRole="button" accessibilityLabel="Open assets and investments"
        onPress={()=>setAssetsOpen(v=>!v)} style={styles.careerButton}>
        <Text style={styles.buttonText}>{assetsOpen ? 'Close portfolio' : 'Manage assets and investments  ↗'}</Text>
      </Pressable>
      {assetsOpen && <View style={styles.jobs}>
        <Text style={styles.muted}>
          Real purchases affect cash, yearly maintenance and resale value. The index uses a deterministic fictional market, not live trading.
        </Text>
        <View style={styles.careerButtons}>
          <Pressable accessibilityRole="button" accessibilityLabel="Invest 100 pounds"
            style={styles.careerButton} onPress={()=>onAction(w=>investIndex(w,10000))}>
            <Text style={styles.buttonText}>Invest £100</Text>
          </Pressable>
          <Pressable accessibilityRole="button" accessibilityLabel="Withdraw 100 pounds"
            style={styles.ghostButton} onPress={()=>onAction(w=>withdrawIndex(w,10000))}>
            <Text style={styles.muted}>Withdraw £100</Text>
          </Pressable>
        </View>
        {GOODS.map(id => {
          const product=CATALOG[id];
          const owned=portfolio(world).owned.some(asset=>asset.id===id);
          return <View key={id} style={styles.jobItem}>
            <View style={{flex:1,gap:3}}>
              <Text style={styles.jobTitle}>{product.label}</Text>
              <Text style={styles.muted}>Purchase {cash(product.price)} · Annual upkeep {cash(product.annualUpkeep)}</Text>
            </View>
            <Pressable accessibilityRole="button" accessibilityLabel={owned ? 'Sell '+product.label : 'Buy '+product.label}
              onPress={()=>onAction(w=>owned ? sellAsset(w,id) : buyAsset(w,id))}
              style={styles.ghostButton}>
              <Text style={styles.actionMark}>{owned ? 'SELL' : 'BUY'} ↗</Text>
            </Pressable>
          </View>;
        })}
      </View>}
    </View>
  </View>;
}
const styles=StyleSheet.create({
  shell:{gap:12},
  hero:{flexDirection:'row',flexWrap:'wrap',backgroundColor:'#172335',borderColor:'#906d52',borderWidth:1,borderRadius:16,overflow:'hidden'},
  heroPortrait:{flexGrow:1,flexBasis:138,minHeight:184,backgroundColor:'#313347',justifyContent:'flex-end',paddingTop:10},
  heroContent:{flexGrow:3,flexBasis:225,padding:16,gap:10},
  eyebrow:{fontSize:10,letterSpacing:1.6,fontWeight:'800',color:'#ddb183'},
  name:{fontSize:26,fontFamily:'serif',color:'#f9e7cc'},
  tagline:{fontSize:12,color:'#bec9d3'},
  stats:{flexDirection:'row',flexWrap:'wrap',gap:8,marginTop:4},
  stat:{flexBasis:85,flexGrow:1,gap:4,backgroundColor:'#243249',padding:9,borderRadius:7},
  statLabel:{fontSize:9,letterSpacing:.5,color:'#bac4d1'},
  statValue:{fontSize:15,fontWeight:'800',color:'#f8d3a5'},
  ageButton:{backgroundColor:'#965533',borderRadius:10,padding:14,flexDirection:'row',alignItems:'center',minHeight:66,borderWidth:1,borderColor:'#ffc28a'},
  ageButtonText:{fontSize:18,color:'#fff4e2',fontWeight:'900',letterSpacing:.4},
  ageButtonHint:{fontSize:11,color:'#f4d7b8'},
  ageIcon:{fontSize:29,color:'#ffe0ad'},
  pressed:{opacity:.7},
  momentCard:{padding:16,borderRadius:15,backgroundColor:'#292b42',borderWidth:1,borderColor:'#e6aa78',gap:12},
  momentLabel:{fontSize:10,fontWeight:'900',letterSpacing:1.2,color:'#f7be86'},
  momentTitle:{fontSize:25,fontFamily:'serif',fontWeight:'700',color:'#ffe1b8'},
  momentDescription:{fontSize:14,lineHeight:21,color:'#f9ede0'},
  momentChoice:{padding:14,minHeight:52,borderRadius:11,borderWidth:1,borderColor:'#c88e67',backgroundColor:'#50364a',justifyContent:'center'},
  momentChoiceText:{fontSize:14,color:'#ffead3',fontWeight:'700'},
  lifeReel:{backgroundColor:'#252639',borderLeftColor:'#e6aa78',borderLeftWidth:3,padding:13,gap:7,borderRadius:5},
  reelText:{color:'#f6e8d7',fontSize:13,lineHeight:21},
  careerArea:{padding:15,backgroundColor:'#192639',borderColor:'#4d5668',borderWidth:1,borderRadius:12,gap:12},
  careerHeading:{flexDirection:'row',gap:12,alignItems:'center'},
  careerTitle:{color:'#f5d7b5',fontFamily:'serif',fontSize:20},
  muted:{color:'#b8c4d2',fontSize:12,lineHeight:18},
  careerButton:{backgroundColor:'#774e39',borderColor:'#d9a478',borderWidth:1,borderRadius:9,paddingHorizontal:14,paddingVertical:12,minHeight:44,justifyContent:'center',alignSelf:'flex-start'},
  buttonText:{color:'#fff1df',fontSize:12,fontWeight:'800'},
  jobs:{gap:7},
  jobItem:{backgroundColor:'#273449',borderWidth:1,borderColor:'#59667b',borderRadius:9,padding:12,flexDirection:'row',alignItems:'center',gap:15},
  jobTitle:{color:'#f5d5ad',fontSize:15,fontWeight:'800'},
  actionMark:{color:'#f1b985',fontSize:10,fontWeight:'900'},
  careerButtons:{flexDirection:'row',flexWrap:'wrap',gap:8},
  ghostButton:{padding:12,minHeight:44,justifyContent:'center',borderRadius:9,borderWidth:1,borderColor:'#546175'},
});
