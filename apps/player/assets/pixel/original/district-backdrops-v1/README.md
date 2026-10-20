# Bellweather district backdrops v1

Five original pixel-art concept backdrops cover the active Bellweather districts: Market, Riverside, University, Studio, and Gardens. Each has its preserved generated source, a 320×256 nearest-neighbor concept export, and a transparent dialogue-safe layout guide.

## Files and provenance

`manifest.json` is the combined index for all five districts. It records source/export/guide paths, dimensions, color modes through the role contract, SHA-256 hashes, dialogue-safe bands, and `runtimeReady: false` for every record. `prompts.md` preserves the exact prompts for University, Studio, and Gardens. `provenance.json` records source dimensions, crops, and resampling for Market and Riverside; the original exact prompt text for those two was lost when the shared prompt file was overwritten, so `market-riverside-prompts-reconstructed.md` is explicitly a reconstructed prompt summary, not a verbatim transcript. Original generated sources remain preserved unchanged in each district folder.

## Art direction

- Market: warm late-morning street with café and market stalls, shopfronts, planters, and a quiet lower path.
- Riverside: blue-hour river walk with water, bridge, reeds, willows, lamps, and an open lower path.
- University: late-afternoon brick academic quad with central fountain, library wing, arched walkway, trees, and benches.
- Studio: warm brick creative workspace opening onto a loading courtyard, with tables, easels, canvas stacks, and stage lights.
- Gardens: sunlit community courtyard with raised beds, pergola, fountain, shed, vines, and a central path.

All five are environment-only, with no characters, UI, text, logos, signs, or watermarks. The lower band at rows 204–255 is kept quieter for later dialogue composition.

## Limits

These are concept plates and layout guides, not authored maps, tilesets, collision/portal data, composable actor layers, or shipped assets. They need palette review, pixel-cluster cleanup, HUD contrast checks, actor compositing, target crop review, and renderer validation before integration. Every asset remains `runtimeReady: false`.
