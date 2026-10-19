import { WorldSchema, record, type World, type School, type Household } from '@living/world-schema';

const clamp=(v:number)=>Math.max(0,Math.min(100,Math.round(v)));
export function initialHousehold(): Household {
  return {home:'family_home',balancePence:240000,incomePence:310000,
    expensesPence:255000,dependents:1,lastSettledMonth:0,arrearsMonths:0};
}
export function initialSchool(): School {
  return {phase:'not_started',grade:55,attendance:95,engagement:50,
    discipline:0,studySessions:0,club:null,lastTermMonth:0,graduatedWith:null};
}
export type SchoolAction = 'study'|'join_science'|'join_arts'|'join_music'|'join_sports'|
  'attend_class'|'make_friend'|'skip_class'|'ask_help';
/** A clear daily school decision, not an annual stat-only button.
 * School actions change grades, attendance, interests and real relationships. */
export function performSchoolAction(input:World, action:SchoolAction, dayOffset:number):World {
  const w=structuredClone(WorldSchema.parse(input));
  const years=w.player.ageDays/365;
  if(years<5||years>=18)throw Error('School actions require ages 5 through 17.');
  if(!w.school || w.school.phase==='not_started'||w.school.phase==='graduated')
    throw Error('Not enrolled in school yet.');
  if(!Number.isInteger(dayOffset)||dayOffset<0||dayOffset>29)
    throw Error('Invalid school day.');
  if(!['study','join_science','join_arts','join_music','join_sports','attend_class','make_friend','skip_class','ask_help'].includes(action))
    throw Error('Unrecognized school activity.');
  const day=w.day+dayOffset, marker='school.action:'+day+':'+action;
  if(w.facts.includes(marker))throw Error('You already did that school activity today.');
  // Enrollment and guardianship are validated on the *canonical* life.
  const school=w.school;
  let message='';
  switch(action){
    case 'study':
      school.grade=clamp(school.grade+4);
      school.engagement=clamp(school.engagement+2);
      school.studySessions+=1;
      w.player.skill=clamp(w.player.skill+2);
      w.player.wellbeing=clamp(w.player.wellbeing-2);
      message='You studied a difficult subject and improved your grades.';break;
    case 'attend_class':
      school.attendance=clamp(school.attendance+3);
      school.engagement=clamp(school.engagement+1);
      school.grade=clamp(school.grade+1);
      message='You attended classes, listened and practised.';break;
    case 'skip_class':
      school.attendance=clamp(school.attendance-10);
      school.grade=clamp(school.grade-4);
      school.discipline=clamp(school.discipline+6);
      w.player.wellbeing=clamp(w.player.wellbeing+1);
      message='You skipped class. The school noticed your absence.';break;
    case 'ask_help':
      school.grade=clamp(school.grade+2);
      school.engagement=clamp(school.engagement+3);
      w.player.wellbeing=clamp(w.player.wellbeing+2);
      message='A teacher helped you understand something you had struggled with.';break;
    case 'make_friend': {
      const r=w.relationships.find(r=>r.characterId==='childhood_friend');
      if(r){r.trust=clamp(r.trust+6);r.lastContactDay=day;}
      else w.relationships.push({characterId:'childhood_friend',trust:42,lastContactDay:day});
      school.engagement=clamp(school.engagement+2);
      w.player.wellbeing=clamp(w.player.wellbeing+3);
      message='You got to know a classmate and made a shared memory.';break;
    }
    default: {
      const club=action.replace('join_','') as 'science'|'arts'|'music'|'sports';
      school.club=club;
      school.engagement=clamp(school.engagement+5);
      w.player.skill=clamp(w.player.skill+1);
      message='You joined the '+club+' club. A new interest begins.';break;
    }
  }
  // Recycle only old school cooldowns when near schema's fact storage limit.
  if(w.facts.length>=9500)w.facts=w.facts.filter(f=>!f.startsWith('school.action:')).slice(-9300);
  w.facts.push(marker);
  record(w,'choice',message);
  return WorldSchema.parse(w);
}

/** Run once for each completed month after aging. Fully deterministic.
 * Guard against multiple charges if the user reloads or retries a tick.
 */
export function settleHouseholdAndSchoolMonth(w:World):void {
  const month=Math.floor(w.player.ageDays*12/365);
  const budget=w.household;
  if(budget && budget.lastSettledMonth<month){
    for(let period=budget.lastSettledMonth+1;period<=month;period++){
      budget.balancePence=Math.max(-100000000,Math.min(100000000,
        budget.balancePence+budget.incomePence-budget.expensesPence));
      if(budget.balancePence<0){
        budget.arrearsMonths=Math.min(1200,budget.arrearsMonths+1);
        if(budget.arrearsMonths===1||budget.arrearsMonths%6===0){
          record(w,'simulation','The household is behind on bills. Your family has to make difficult budget choices.');
          w.player.wellbeing=clamp(w.player.wellbeing-2);
        }
      }else budget.arrearsMonths=0;
    }
    budget.lastSettledMonth=month;
    if(month%12===0){
      record(w,'simulation','The family reviewed its annual finances. Household savings: £'+
        (budget.balancePence/100).toFixed(2)+'.');
    }
  }
  const school=w.school;
  if(!school||school.phase==='graduated')return;
  const age=Math.floor(w.player.ageDays/365);
  if(age>=18 && school.phase!=='graduated'){
    school.phase='graduated';
    school.graduatedWith=clamp(Math.round((school.grade*0.75+school.attendance*0.25)-
      school.discipline*0.15));
    w.facts.push('education:school_completed');
    record(w,'simulation','You finished secondary school with a final score of '+
      school.graduatedWith+'/100. Your choices shaped this outcome.');
    return;
  }
  if(age>=13 && school.phase!=='secondary'){
    school.phase='secondary';
    record(w,'simulation','A new secondary school term begins. Old friends and new subjects await.');
  }else if(age>=5 && school.phase==='not_started'){
    school.phase='primary';
    record(w,'simulation','You started primary school. Your classmates and teachers will remember your choices.');
  }
  if(school.phase==='primary'||school.phase==='secondary'){
    if(school.lastTermMonth<month) {
      // Engagement and attendance influence grades, while missed school
      // reduces opportunities rather than forcing progress by age alone.
      const monthlyChange=Math.round((school.engagement-50)/24+
        (school.attendance-85)/20-school.discipline/30);
      school.grade=clamp(school.grade+Math.max(-4,Math.min(3,monthlyChange)));
      school.lastTermMonth=month;
      if(month%3===0)record(w,'simulation',
        'School term report: grades '+school.grade+
        '/100, attendance '+school.attendance+'/100, club '+
        (school.club??'none')+'.');
    }
  }
}
