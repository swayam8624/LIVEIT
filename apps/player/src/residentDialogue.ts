import { stableSpriteHash } from './spriteIdentity';
import type { ResidentProfile } from './residentProfiles';
import type { RegionId } from './worldRegions';

/**
 * Original offline incidental dialogue. Local text works immediately, even
 * before optional on-device LLM weights are installed. It is deliberately
 * separate from canonical relationship changes and authored story dialogue.
 */
const OBSERVATIONS: Record<RegionId, readonly string[]> = {
  bellweather: [
    'The café is where half this town hears its news. The other half hears it outside.',
    'People call this a quiet market. It is, until the morning deliveries.',
    'You can always tell when the rain is coming. Everyone starts walking faster.',
  ],
  willowmere: [
    'The library stays busy well after the lectures finish.',
    'There is an old footpath behind the campus. Most students never find it.',
    'Everyone on campus is building something, even if it is just a new routine.',
  ],
  quayside: [
    'The first boats come in before most of the city wakes up.',
    'This harbour has its own clock. Weather matters more than the hour.',
    'The warehouses look the same, but every crew knows its own door.',
  ],
  larkspur: [
    'The walk uphill gets easier after the third visit. That is what I tell myself.',
    'You can see the city from the ridge on a clear morning.',
    'People come for the view. The locals stay for the quiet.',
  ],
  orchard: [
    'Harvest days change the whole rhythm of the market.',
    'The orchard paths look identical until you learn the older trees.',
    'Fresh fruit travels farther than you would think before it reaches a stall.',
  ],
  foundry: [
    'The workshops start early, and the best conversations happen at closing time.',
    'Some of the artists here used to work at the factories next door.',
    'Every studio in this quarter sounds different through an open window.',
  ],
  tideglass: [
    'The promenade is quieter when the tide is low.',
    'You do not need a boat to know the water. Just walk the shore every day.',
    'The fishermen and the cafés agree about one thing: mornings matter.',
  ],
  oldtown: [
    'There is always music somewhere in these streets after sunset.',
    'The old theatre keeps the lights on long after the last performance.',
    'This town remembers the little shops more than the grand buildings.',
  ],
  cedarwood: [
    'A forest has routines of its own. You notice them if you take the same walk.',
    'The paths are easier to follow after rain, strangely enough.',
    'Out here the busiest hour is whenever the birds decide it is.',
  ],
};

/** Day-varying but reproducible dialogue; never uses Math.random() or network. */
export function residentObservation(
  profile: ResidentProfile,
  residentId: string,
  worldDay: number,
): string {
  const lines = OBSERVATIONS[profile.homeRegion];
  const day = Number.isSafeInteger(worldDay) ? worldDay : 0;
  return lines[stableSpriteHash(day, residentId) % lines.length]!;
}
