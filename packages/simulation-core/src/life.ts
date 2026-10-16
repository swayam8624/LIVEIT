import {
  WorldSchema, record, type World, type CareerPath, type Employment,
} from '@living/world-schema';
import { cityState, initialCityState, scheduleCityOpportunity } from './city';
import { NPC_BEATS, tickNPCs } from './npc';

const clamp = (n:number) => Math.max(0,Math.min(100,Math.round(n)));
const fields = {
  technology: { company: 'Northstar Systems', title:'Junior Developer', salary:3_400_000 },
  creative: { company: 'Aster Studio', title:'Junior Designer', salary:2_800_000 },
  business: { company: 'Bellweather Trading', title:'Sales Associate', salary:3_000_000 },
  community: { company: 'Bellweather Civic Center', title:'Community Coordinator', salary:2_500_000 },
} as const;
type Field = Exclude<CareerPath,'undecided'>;

export function applyForJob(input:World, field:Field):World {
  const w=structuredClone(WorldSchema.parse(input));
  const c=w.city??(w.city=initialCityState());
  const role=fields[field];
  if(!role) throw new Error('Unknown career path');
  if(c.employment && c.employment.stage!=='applied')
    throw new Error('Resign from your current position before applying elsewhere.');
  if(c.employment?.stage==='applied') throw new Error('You already have a pending interview.');
  if(c.careerPath!=='undecided' && c.careerPath!==field) {
    c.milestones.push(`career-switch:${c.careerPath}:${field}`);
  }
  c.careerPath=field;
  c.employment={
    field,stage:'applied',company:role.company,jobTitle:role.title,
    salaryAnnual:role.salary,experience:0,interviews:0,
    hiredDay:null,lastPromotionDay:null,
  };
  record(w,'simulation',`Applied for ${role.title} at ${role.company}. An interview is waiting.`);
  return WorldSchema.parse(w);
}

export function attendJobInterview(input:World):World {
  const w=structuredClone(WorldSchema.parse(input));
  const c=w.city;
  const employment=c?.employment;
  if(!employment || employment.stage!=='applied') throw new Error('No pending job interview.');
  employment.interviews++;
  const score=w.player.skill + c.reputation/5 + c.connections/8 - c.stress/12;
  const threshold={technology:32,creative:28,business:26,community:24}[employment.field];
  if(score>=threshold) {
    employment.stage='employed';
    employment.hiredDay=w.day;
    w.player.career='employed';
    c.reputation=clamp(c.reputation+3);
    record(w,'simulation',`Hired as ${employment.jobTitle} at ${employment.company}. Salary: £${Math.round(employment.salaryAnnual/100).toLocaleString('en-GB')} per year.`);
  } else {
    const title=employment.jobTitle;
    c.employment=undefined;
    w.player.career='seeking';
    w.player.skill=clamp(w.player.skill+2);
    record(w,'simulation',`The interview for ${title} did not work out. You learned from it and can apply again.`);
  }
  return WorldSchema.parse(w);
}

export function requestPromotion(input:World):World {
  const w=structuredClone(WorldSchema.parse(input));
  const c=w.city;
  const job=c?.employment;
  if(!job || job.stage==='applied') throw new Error('You need a job before requesting a promotion.');
  if(job.stage==='lead') throw new Error('You already hold the most senior available position.');
  if(job.experience<5 || w.player.skill<25)
    throw new Error('Keep working and developing skills before asking for promotion.');
  job.stage=job.stage==='employed'?'senior':'lead';
  job.salaryAnnual=Math.round(job.salaryAnnual*(job.stage==='lead'?1.3:1.24));
  job.jobTitle=(job.stage==='lead'?'Lead ':'Senior ')+fields[job.field].title.replace(/^Junior /,'');
  job.experience=0;
  job.lastPromotionDay=w.day;
  c.reputation=clamp(c.reputation+6);
  record(w,'simulation',`Promoted to ${job.jobTitle}; your annual salary is now £${Math.round(job.salaryAnnual/100).toLocaleString('en-GB')}.`);
  return WorldSchema.parse(w);
}

export function resignFromJob(input:World):World {
  const w=structuredClone(WorldSchema.parse(input));
  const c=w.city;
  if(!c?.employment || c.employment.stage==='applied')
    throw new Error('You have no position to resign from.');
  const lastTitle=c.employment.jobTitle;
  c.milestones.push(`resigned:${c.employment.field}:${w.day}`);
  c.employment=undefined;
  w.player.career='seeking';
  record(w,'simulation',`You resigned from ${lastTitle}. New opportunities await.`);
  return WorldSchema.parse(w);
}

/**
 * Economically coherent annual transition instead of executing 365 stat-spam
 * actions in React. Fast deterministic transition; no network, timers, LLM.
 * Age-up cannot grant multiple rewards through a double-tap if the caller
 * applies one action per authoritative state revision.
 */
export function ageUp(input:World):World {
  const w=structuredClone(WorldSchema.parse(input));
  const c=w.city??(w.city=initialCityState());
  const age=Math.floor(w.player.ageDays/365);
  if(age>=100) throw new Error('The current simulation covers ages up to 100.');
  const priorDay=w.day;
  const toDay=priorDay+365;
  // Apply discrete off-screen career and life events once, chronologically.
  for(const beat of NPC_BEATS){
    if(beat.day>priorDay && beat.day<=toDay){
      w.day=beat.day;
      tickNPCs(w);
    }
  }
  w.day=toDay;
  w.player.ageDays+=365;
  const hired=Boolean(c.employment && c.employment.stage!=='applied');
  const gross=hired ? c.employment!.salaryAnnual : 850_000;
  // Approximate simulation taxes; not tax guidance.
  const tax=hired?Math.round(gross*0.20):Math.round(gross*.08);
  const living=365*2800;
  w.player.money=Math.max(-100000000,Math.min(100000000,w.player.money+gross-tax-living));
  if(hired && c.employment) {
    c.employment.experience=Math.min(20000,c.employment.experience+12);
    w.player.skill=clamp(w.player.skill+5);
    c.reputation=clamp(c.reputation+2);
  } else {
    w.player.skill=clamp(w.player.skill+2);
  }
  c.stress=clamp(c.stress+(hired?5:9));
  w.player.wellbeing=clamp(w.player.wellbeing+(hired?-2:0)-(c.stress>70?9:0));
  for(const relation of w.relationships){
    if(w.day-relation.lastContactDay>=365)
      relation.trust=clamp(relation.trust-3);
  }
  c.opportunities=c.opportunities.filter(o=>o.expiresDay>=w.day);
  scheduleCityOpportunity(w);
  const newAge=Math.floor(w.player.ageDays/365);
  const net=(gross-tax-living)/100;
  const earning=net>=0?'+':'−';
  const text=`Age ${newAge}: a year passes. ${hired?`You continued your work at ${c.employment?.company}.`:'You found occasional freelance work.'} Net finances ${earning}£${Math.abs(Math.round(net)).toLocaleString('en-GB')} after routine living costs and estimated taxes.`;
  record(w,'simulation',text);
  return WorldSchema.parse(w);
}
