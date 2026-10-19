import {
  DEFAULT_APPEARANCE,
  VisualSceneSchema,
  type Appearance,
  type VisualScene,
  type World,
} from '@living/world-schema';

export type CastMember = Readonly<{
  entityId: string;
  appearance: Appearance;
  ageYears: number;
  expression: VisualScene['actors'][number]['expression'];
}>;

function lifeStage(age: number): VisualScene['lighting']['lifeStage'] {
  if (age < 13) return 'child';
  if (age < 20) return 'teen';
  if (age < 36) return 'young-adult';
  if (age < 62) return 'midlife';
  return 'elder';
}

/**
 * The authoritative deterministic world is the ONLY identity source.
 * Renderers never create an NPC or grant consequences. A saved appearance
 * produces the same actor in portraits, episodes, city and AI chat surfaces.
 */
export function buildVisualScene(
  world: World,
  view: 'city' | 'story' | 'chat',
  cast: readonly CastMember[] = [],
): VisualScene {
  if (cast.some((person) => person.entityId === world.player.id)) {
    throw new Error('The player cannot be supplied as a duplicate cast member');
  }
  if (new Set(cast.map((person) => person.entityId)).size !== cast.length) {
    throw new Error('Duplicate visual actor identity');
  }
  const age = Math.floor(world.player.ageDays / 365);
  const actors: VisualScene['actors'] = [
    {
      entityId: world.player.id,
      rig: 'liveit.rig.prototype',
      appearance: world.player.appearance ?? DEFAULT_APPEARANCE,
      worldPosition: view === 'city' ? [0, 0, 0] : [-1.0, 0, 0],
      facing: 0,
      expression: 'neutral',
      animation: 'liveit.animation.idle',
      ageYears: age,
    },
    ...cast.map((person, index) => ({
      entityId: person.entityId,
      rig: 'liveit.rig.prototype',
      appearance: person.appearance,
      worldPosition: [1 + index * 1.4, 0, 0] as [number, number, number],
      facing: -0.35,
      expression: person.expression,
      animation: 'liveit.animation.idle',
      ageYears: person.ageYears,
    })),
  ];
  const timeOfDay =
    view === 'city' ? (world.day % 3 === 0 ? 'dusk' : 'day') : 'night';
  return VisualSceneSchema.parse({
    id:
      view === 'city'
        ? 'liveit.scene.city'
        : view === 'story'
          ? 'liveit.scene.story'
          : 'liveit.scene.chat',
    location: 'liveit.location.bellweather',
    day: world.day,
    camera: {
      preset:
        view === 'city'
          ? 'isometric'
          : view === 'story'
            ? 'conversation'
            : 'portrait',
      orbit: 0.78,
      zoom: view === 'city' ? 1 : 1.4,
    },
    lighting: { timeOfDay, weather: 'clear', lifeStage: lifeStage(age) },
    actors,
    props: [],
  });
}
