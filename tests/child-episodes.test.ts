import {describe,it,expect} from 'vitest';
import {createBirthWorld,createWorld} from '@living/simulation-core';
import {startStory,choose} from '@living/narrative-core';
import {firstMorning,firstSchoolDay,thirteenSummers,reunion,OFFICIAL_STORIES} from '@living/content';
describe('birth-first integrated original chapters',()=>{
  it('has three original childhood and two adult episodes with age gates',()=>{
    expect(OFFICIAL_STORIES.length).toBe(5);
    const infant=createBirthWorld('Robin');
    expect(startStory(infant,firstMorning).progress).toHaveLength(1);
    expect(()=>startStory(infant,firstSchoolDay)).toThrow('incompatible');
    expect(()=>startStory(infant,thirteenSummers)).toThrow('incompatible');
    expect(()=>startStory(infant,reunion)).toThrow('incompatible');
  });
  it('branch choices alter parent trust and memory in same timeline',()=>{
    const born=createBirthWorld('Robin');
    const story=startStory(born,firstMorning);
    const result=choose(story,firstMorning,'reach');
    expect(result.relationships[0]!.trust).toBeGreaterThan(86);
    expect(result.memories.length).toBe(1);
    expect(result.progress.find(p=>p.storyId===firstMorning.id)?.completed).toBe(true);
    expect(born.memories.length).toBe(0);
  });
  it('keeps adult original stories age-gated while preserving old saves',()=>{
    const old=createWorld();
    expect(startStory(old,reunion).progress.length).toBe(1);
  });
});
