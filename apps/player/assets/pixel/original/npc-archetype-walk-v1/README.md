# NPC archetype walk concepts v1

This batch contains three original town and caregiver identities for LIVEIT's
2D pixel direction:

- `sari-caregiver`: middle-aged South Asian caregiver with a woven tote;
- `cane-neighbor`: older East Asian neighbor with a cardigan and cane;
- `garden-keeper`: adult Black nonbinary community gardener with a watering can.

Each identity has four directions (`front`, `back`, `left`, `right`) and four
walk phases per direction. The source sheet is the untouched ImageGen export at
`npc-archetypes-source.png`. Derived frames are 96x128 RGBA images with a
bottom-center pivot and are intentionally marked `runtimeReady: false`.

`generate_frames.py` is deterministic and can regenerate all derived frames,
atlases, previews, and manifests from the preserved source. It removes the
charcoal studio background and nearby disconnected row fragments, but the
generated poses still need a pixel-artist cleanup pass for silhouette rhythm,
phase timing, and engine-specific palette/indexing before runtime admission.

No supplied archive imagery was used.
