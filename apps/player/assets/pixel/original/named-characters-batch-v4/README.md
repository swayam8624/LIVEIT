# Named characters batch v4

This isolated concept package adds five original Bellweather named-role actor
families from the active pixel-world catalog: shopkeeper, nurse, physician,
transit worker, and cafe owner. It contains no archive ZIP contents, internet
art, or third-party sprite material.

Each role has 24 individually exported 24×32 RGBA frames: four independently
drawn cardinal views (`south`, `west`, `east`, `north`), four gait phases
(`contact-a`, `passing-a`, `contact-b`, `passing-b`), plus `idle` and a
role-specific `interact` pose. The shared feet pivot is `(12, 31)`. Every role
has its own silhouette, palette, outfit details, and work prop: market basket,
care clipboard, stethoscope, route flag, or coffee mug.

`manifest.json` maps all 120 frames to the exact catalog IDs:

- `liveit.prod.v1.pixel.sprite.named.shopkeeper`
- `liveit.prod.v1.pixel.sprite.named.nurse`
- `liveit.prod.v1.pixel.sprite.named.physician`
- `liveit.prod.v1.pixel.sprite.named.transit-worker`
- `liveit.prod.v1.pixel.sprite.named.cafe-owner`

`build_named_characters.py` is deterministic and uses only Pillow primitives.
The manifest records SHA-256 hashes for each frame, per-role atlas, preview, and
the contact sheet. `provenance.json` records the rights boundary and confirms
that no source archives or external images were used.

All records remain `runtimeReady: false`. These are concept exports pending
human identity/palette review, collision and pivot review, renderer import, and
native visual QA.
