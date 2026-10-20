# Original actor and overlay design prompts

Created 2026-10-20 for `exclusive-scene-actor-staging-v2`. These prompts
describe the original character designs and staging intent rendered by the
deterministic integer-pixel builder. No supplied ZIP, downloaded image,
third-party asset, external visual reference, font, logo, or image-generation
service was used.

## First paycheck diner

- **Mika, first-shift worker:** Original young diner worker with short swept
  dark curls, coral work shirt, teal trousers, warm tired eyes; expressive
  grounded pixel bust and relaxed working-class body language. Body poses:
  seated counting, standing proud, and offering coffee.
- **Ren, night cook:** Original older diner cook with close-cropped
  silver-brown hair, deep blue apron over a pale shirt, kind lined face;
  sturdy shoulders and understated supportive gestures. Body poses: leaning
  at the counter, raising a mug, and a quiet congratulation.
- **Foreground overlay:** Low stool, mug, and amber saucer details at the
  lower-left edge, below the central actor block.

## Rainy reconciliation bus stop

- **Asha, returning friend:** Original returning friend in a muted teal
  raincoat with long dark hair tied low, rain-speckled but not wet-rendered;
  careful remorseful eyes and hesitant open-hand gesture. Body poses: lowered
  umbrella, open-hand apology, and tentative reach.
- **Jules, waiting friend:** Original friend who waited through the rain,
  auburn cropped hair, plum scarf and slate coat, guarded expression softening
  into cautious welcome; avoid melodramatic tears. Body poses: hands in
  pockets, listening as expression softens, and offering a paper cup.
- **Foreground overlay:** Restrained puddle, paper cup, and reflected light
  near the lower-left curb.

## Harvest-table gathering

- **Noor, garden host:** Original middle-aged garden host with a
  salt-and-pepper headwrap, leaf-green cardigan, bright attentive face and
  generous open posture. Body poses: passing a bowl, welcoming a guest, and
  lifting a toast.
- **Eli, garden neighbor:** Original young adult neighbor with warm brown
  locs gathered back, amber overshirt and dark plum trousers; joyful but
  natural smile, carrying the shared meal. Body poses: carrying produce,
  laughing with relaxed shoulders, and sharing bread.
- **Foreground overlay:** Small produce crate and garden leaves at the lower
  edge, kept out of the dialogue-safe band.

## Fresh-start apartment

- **Sam, new tenant:** Original newly single tenant with soft black bob,
  lavender sweater and teal trousers; calm agency replacing sadness,
  expressive brows and practical gentle posture. Body poses: unpacking a box,
  holding a key toward the light, and watering the first plant.
- **Bea, neighbor:** Original friendly neighbor with short textured copper
  hair, muted sage cardigan and plum skirt; quiet welcoming expression, hands
  offering a small plant. Body poses: knocking gently, offering a plant, and
  sitting near the window.
- **Foreground overlay:** Open moving box and small potted plant at the
  lower-left edge.

## Rendering constraints

Actors are distinct scene-specific concepts, not canonical save identities.
Each body pose is supplied in south/east/north/west views on a transparent
48×80 canvas; each actor also has four 64×64 bust views. Pixels use the
backdrop's scene palette mood and binary alpha, with no antialiasing. The
transparent 320×256 prop plates use advisory foreground placement. `prompts.md`
documents artistic intent; `build_actor_staging.js` is the executable source
of the authored pixel output.
