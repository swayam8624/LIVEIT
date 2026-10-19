import { WorldSchema, record, type World } from '@living/world-schema';
export type RelationshipAction = 'befriend'|'ask_date'|'kiss'|'be_intimate'|'propose'|'marry'|'break_up';
export type RelationshipStatus = 'acquaintance'|'dating'|'engaged'|'married';
const KEY='life_relationship:amelia:';
export function relationshipStatus(w: World): RelationshipStatus {
  if(w.facts.includes(KEY+'married')) return 'married';
  if(w.facts.includes(KEY+'engaged')) return 'engaged';
  if(w.facts.includes(KEY+'dating')) return 'dating';
  return 'acquaintance';
}
/** Consent is an explicit rule, not an LLM prediction. Both parties must be
 * adults; Amelia is an adult character. Intimacy is non-graphic/fade to black.
 */
export function actOnRelationship(input:World,action:RelationshipAction,offset:number):World {
  const w=structuredClone(WorldSchema.parse(input));
  if(!Number.isSafeInteger(offset)||offset<0||offset>29) throw Error('Invalid day');
  if(!['befriend','ask_date','kiss','be_intimate','propose','marry','break_up'].includes(action))
    throw Error('Unknown relationship action');
  const relation=w.relationships.find(r=>r.characterId==='amelia');
  if(!relation) throw Error('You have not met Amelia yet.');
  if(w.player.ageDays<18*365&&action!=='befriend')
    throw Error('Romantic and intimate actions are restricted to adults.');
  const marker='relationship_action:'+(w.day+offset)+':amelia:'+action;
  if(w.facts.includes(marker)) throw Error('Already done today.');
  const status=relationshipStatus(w);
  let event='';
  switch(action){
    case 'befriend': relation.trust=Math.min(100,relation.trust+4);
      event='You listened to Amelia and strengthened your friendship.';break;
    case 'ask_date':
      if(status!=='acquaintance'||relation.trust<45)
        throw Error('A date requires a free, trusting relationship. Build friendship first.');
      w.facts.push(KEY+'dating');relation.trust=Math.min(100,relation.trust+3);
      event='Amelia agrees to a date. You get to know each other.';break;
    case 'kiss':
      if(status==='acquaintance'||relation.trust<55)
        throw Error('A kiss requires an established trusting relationship.');
      relation.trust=Math.min(100,relation.trust+2);
      event='You ask before kissing Amelia. She agrees, and you share a gentle moment.';break;
    case 'be_intimate':
      if(status==='acquaintance'||relation.trust<65)
        throw Error('Both adults must have an established trusting partnership.');
      relation.trust=Math.min(100,relation.trust+1);
      event='After discussing boundaries and mutual consent, you share a private evening. The scene fades to black.';break;
    case 'propose':
      if(status!=='dating'||relation.trust<80) throw Error('A proposal requires mutual trust and steady dating.');
      w.facts.push(KEY+'engaged');event='You propose to Amelia. She says yes.';break;
    case 'marry':
      if(status!=='engaged') throw Error('Become engaged first.');
      w.facts.push(KEY+'married');event='You and Amelia marry in Bellweather.';break;
    case 'break_up':
      if(status==='acquaintance') throw Error('Not currently partners.');
      w.facts=w.facts.filter(f=>!f.startsWith(KEY));
      relation.trust=Math.max(0,relation.trust-12);
      event='You and Amelia part ways. Shared memories remain.';break;
  }
  w.facts.push(marker);
  relation.lastContactDay=w.day+offset;
  record(w,'simulation',event);
  return WorldSchema.parse(w);
}
