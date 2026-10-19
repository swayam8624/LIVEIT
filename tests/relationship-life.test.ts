import {describe,it,expect} from 'vitest';
import {createWorld,createBirthWorld,actOnRelationship,relationshipStatus} from '@living/simulation-core';
import {decodeSave,encodeSave} from '@living/save-system';
describe('consensual adult relationship actions',()=>{
  it('rejects dating and intimacy for a child',()=>{
    const infant=createBirthWorld('Kim');
    expect(()=>actOnRelationship(infant,'be_intimate',0)).toThrow();
    const young=createWorld('Kim');young.player.ageDays=17*365;
    expect(()=>actOnRelationship(young,'ask_date',0)).toThrow('restricted');
    expect(()=>actOnRelationship(young,'be_intimate',0)).toThrow('restricted');
  });
  it('builds friendship, dates, proposal and marriage with persistent state',()=>{
    let w=createWorld();
    expect(relationshipStatus(w)).toBe('acquaintance');
    expect(()=>actOnRelationship(w,'ask_date',0)).toThrow();
    for(let i=0;i<3;i++) w=actOnRelationship(w,'befriend',i);
    w=actOnRelationship(w,'ask_date',3);
    expect(relationshipStatus(w)).toBe('dating');
    for(let i=4;i<15;i++) w=actOnRelationship(w,'befriend',i);
    w=actOnRelationship(w,'propose',15);
    expect(relationshipStatus(w)).toBe('engaged');
    w=actOnRelationship(w,'marry',16);
    expect(relationshipStatus(w)).toBe('married');
    expect(decodeSave(encodeSave({version:1,active:'life',life:w,story:null})).life).toEqual(w);
  });
  it('requires a trusting adult partner for fade-to-black intimacy',()=>{
    let w=createWorld();
    expect(()=>actOnRelationship(w,'be_intimate',0)).toThrow();
    for(let i=0;i<4;i++)w=actOnRelationship(w,'befriend',i);
    w=actOnRelationship(w,'ask_date',5);
    for(let i=6;i<11;i++)w=actOnRelationship(w,'befriend',i);
    w=actOnRelationship(w,'be_intimate',12);
    expect(w.history.at(-1)?.text).toContain('fades to black');
  });
});
