import { CHUNK_SIZE, tileHash, worldCell } from './proceduralWorld';
import type { Facing } from './pixelTownLogic';

export type AmbientPedestrian=Readonly<{
  id:string;
  x:number;
  y:number;
  look:number;
  facing:Facing;
  shift:'commute'|'work'|'leisure'|'home';
}>;
/** Visual crowd simulation. The 32x32 region owns stable civilian IDs.
 * Their time-dependent routines are generated without server calls or
 * persistent NPC allocations, and are deliberately non-interactive until
 * an individual is promoted into a named, persisted NPC.
 */
export function ambientPedestrians(
  seed:number, left:number, top:number, cols:number, rows:number,
  minuteOfDay:number,
):AmbientPedestrian[] {
  if(![left,top,cols,rows,minuteOfDay].every(Number.isFinite)||
    cols<1||rows<1||cols*rows>2500)return [];
  const hour=Math.floor((((minuteOfDay%1440)+1440)%1440)/60);
  const shift=hour<6||hour>=22?'home':hour<9?'commute':
    hour<17?'work':'leisure';
  // Most people go home after ten. Peak foot traffic is on commute routes.
  const count=shift==='home'?1:shift==='commute'?4:3;
  const results:AmbientPedestrian[]=[];
  const firstX=Math.floor(left/CHUNK_SIZE),lastX=Math.floor((left+cols-1)/CHUNK_SIZE);
  const firstY=Math.floor(top/CHUNK_SIZE),lastY=Math.floor((top+rows-1)/CHUNK_SIZE);
  for(let cy=firstY;cy<=lastY;cy++)for(let cx=firstX;cx<=lastX;cx++){
    for(let i=0;i<count;i++){
      const hash=tileHash(seed^0x525449, cx*17+i*37,cy*13+i*53);
      // Every resident follows a repeatable daily loop on public sidewalks.
      // Use the same global roads as the chunk generator: no seam seams.
      const localX=hash%CHUNK_SIZE;
      const localY=(hash>>>7)%CHUNK_SIZE;
      const t=Math.floor(minuteOfDay/20);
      let x=cx*CHUNK_SIZE+localX;
      let y=cy*CHUNK_SIZE+localY;
      let facing:Facing='down';
      const direction=(hash>>>18)%4;
      // Commutes and leisurely walks follow predictable daily 20-minute
      // stepping; they avoid solid tiles, checking the authoritative map.
      if(shift!=='home'){
        const displacement=(t+(hash>>>25))%7-3;
        if(direction<2){x+=displacement;facing=displacement<0?'left':'right';}
        else{y+=displacement;facing=displacement<0?'up':'down';}
      }
      if(x<left||x>=left+cols||y<top||y>=top+rows)continue;
      if(worldCell('street',x,y,seed).solid)continue;
      if(x===10 && y===7)continue; // canonical Amelia spawn
      results.push({id:seed+':'+cx+':'+cy+':'+i,x,y,
        facing,look:(hash>>>13)%5,shift});
    }
  }
  return results;
}
