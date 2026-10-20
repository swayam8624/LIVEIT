# Named characters batch v3

This isolated original pixel-art study covers the five planned P0 named actor
families in `content/production-assets/v1/pixel-world.json`: boss, coworker,
friend one, friend two, and neighbor. Each family has 24 transparent RGBA
frames on a 24×32 logical canvas: four independently authored cardinal views,
four walk phases (`contact-a`, `passing-a`, `contact-b`, `passing-b`), one idle
state, and one role-appropriate interaction state.

The roles are intentionally recognizable without relying on recolor clones:
the boss carries a clipboard and wears a blazer pin; the coworker has a
lanyard badge and notebook; friend one carries a takeaway mug; friend two has a
coral phone and auburn curls; the neighbor carries a small terracotta plant.
The interaction frames raise or present those objects while keeping every
cluster inside the actor bounds.

`build_named_characters.py` is deterministic and writes per-role frames,
4×6 atlases, nearest-neighbor previews, a contact sheet, exact catalog-ID
mapping, per-frame SHA-256 values, a complete PNG hash list, and provenance.
No supplied ZIP, downloaded art, model output, or third-party raster was used.

This remains concept art: every manifest is `runtimeReady: false`. Before
runtime promotion, perform human pixel cleanup, identity review, collision and
pivot review, nearest-neighbor importer validation, device capture, and visual
approval. The current generated views are intentionally small working sprites,
not a claim of catalog completion.
