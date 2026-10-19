import {describe,it,expect} from 'vitest';
import {
  createWorld, createBirthWorld, advanceCalendarMonth,
  canTalkTo, buildNPCSystemPrompt, recordNPCConversation,
} from '@living/simulation-core';
import {startStory,choose} from '@living/narrative-core';
import {firstMorning} from '@living/content';
import {encodeSave,decodeSave} from '@living/save-system';

describe('world-grounded local NPC memories',()=>{
  it('has actual family cast access from birth and age-gates adult encounters',()=>{
    const newborn=createBirthWorld('Kit','kit-life');
    expect(canTalkTo(newborn,'parent_mara')).toBe(true);
    expect(canTalkTo(newborn,'parent_eli')).toBe(true);
    expect(canTalkTo(newborn,'amelia')).toBe(false);
    expect(()=>buildNPCSystemPrompt(newborn,'amelia')).toThrow(/age/);
    expect(buildNPCSystemPrompt(newborn,'parent_mara')).toContain('Mara');
  });

  it('makes authored childhood consequences available in later family conversations',()=>{
    const born=createBirthWorld('Ari','ari-life');
    const played=choose(startStory(born,firstMorning),firstMorning,'reach');
    const prompted=buildNPCSystemPrompt(played,'parent_mara');
    expect(prompted).toContain('Mara');
    expect(prompted).toContain('You reached toward Mara');
    expect(prompted).toContain('relationship trust');
    expect(prompted).toContain('Never claim you transferred money');
  });

  it('records only complete exchanges as persistent real-life memories',()=>{
    const original=createWorld('Robin','chat-persist');
    const one=recordNPCConversation(original,'amelia',
      'I want to open a bakery one day.',
      'That is ambitious. What kind of bread would you make?',5);
    expect(one.memories).toHaveLength(1);
    expect(one.memories[0]?.subject).toBe('amelia');
    expect(one.memories[0]?.text).toContain('bakery');
    expect(one.relationships.find(r=>r.characterId==='amelia')?.trust).toBe(36);
    expect(original.memories).toHaveLength(0);
    const two=recordNPCConversation(one,'amelia','Sourdough!','I would visit.',5);
    expect(two.memories).toHaveLength(2);
    expect(two.relationships.find(r=>r.characterId==='amelia')?.trust).toBe(36);
    expect(buildNPCSystemPrompt(two,'amelia')).toContain('bakery');
    expect(decodeSave(encodeSave({version:1,active:'life',life:two,story:null})).life).toEqual(two);
  });

  it('does not grant trust by sending malformed or imaginary model output',()=>{
    const world=createWorld();
    expect(()=>recordNPCConversation(world,'amelia','','Hello!',0)).toThrow();
    expect(()=>recordNPCConversation(world,'parent_mara','Hi','Hey',0)).toThrow();
    expect(world.relationships.find(r=>r.characterId==='amelia')?.trust).toBe(35);
  });

  it('keeps family memories after a full month and does not confuse NPC identities',()=>{
    let baby=createBirthWorld('Leo');
    baby=recordNPCConversation(baby,'parent_eli','I feel safe.','I am here.',0);
    baby=advanceCalendarMonth(baby);
    expect(buildNPCSystemPrompt(baby,'parent_eli')).toContain('I feel safe');
    expect(buildNPCSystemPrompt(baby,'parent_mara')).not.toContain('I feel safe');
  });
});
