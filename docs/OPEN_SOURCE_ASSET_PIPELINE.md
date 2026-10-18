# LIVEIT — Free/Open Asset Intake (16 October 2026)

The game is intended for commercial distribution on iOS, Android and web. **Free to download is not necessarily free to redistribute commercially.** Use assets only after checking the exact license attached to the individual pack/file. A repository or asset list containing downloads is not blanket permission to use everything inside it.

## Verified candidate libraries

| Source                                 | Official URL                                    | License indicated at source                   | Fit                                                                                                |
| -------------------------------------- | ----------------------------------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Kenney UI Pack                         | https://kenney.nl/assets/ui-pack                | CC0-1.0                                       | Strong option for HUD/panel building blocks, to restyle in LIVEIT's dark palette                   |
| Kenney Pixel UI Pack                   | https://kenney.nl/assets/pixel-ui-pack          | CC0-1.0                                       | Pixel-only prototype, not the main illustrated scene                                               |
| Kenney RPG Urban Kit                   | https://kenney-assets.itch.io/rpg-urban-kit     | CC0-1.0                                       | Excellent tile library for an **optional pixel city map**, 480+ pieces and six animated characters |
| Poly Haven                             | https://polyhaven.com/license                   | CC0-1.0 for site assets                       | Texture/HDRI source for original 2D environment painting or optional 3D                            |
| OpenGameArt CC0 backgrounds collection | https://opengameart.org/content/cc0-backgrounds | Mixed individual pages: **verify one by one** | Curated leads only, not auto-approved for redistribution                                           |

Kenney confirms commercial CC0 use and optional attribution at https://kenney.nl/support . Poly Haven's assets are CC0 and redistributable at https://polyhaven.com/license . OpenGameArt warns that attribution/license terms differ per work at https://opengameart.org/node/5571 .

**Do not download** the paid Kenney All-in-1 bundle under the assumption that every pack can be freely bulk-fetched. The individual listed free packs are the relevant route. Do not scrape websites to circumvent access controls.

## Safe import workflow

1. Open the **official publisher page** for one pack.
2. Download its genuine free archive; inspect the included license and any exceptions.
3. Run:
   ```sh
   python3 tools/import_cc0_pack.py kenney-ui ~/Downloads/Kenney_UI.zip --confirm-license
   ```
4. The importer checks paths for ZIP traversal, ignores executable/HTML/SVG files, limits total size and file counts, and writes a hash/provenance manifest to `assets/third_party/<source-id>/manifest.json`.
5. Review individual assets for quality, third-party marks/logos, potentially trademarked characters and compatibility with LIVEIT's art style. CC0 does not guarantee freedom from _trademark, privacy or publicity_ claims.
6. Convert only approved assets into the **bundled player asset folder**, with explicit static `require()` paths, sizes and licensing records. Expo cannot bundle images merely because a ZIP contains them.
7. Keep any original license notices. Where a future asset uses OFL or CC BY, preserve required credits and exact license documentation.

An imported pack isn't automatically adopted into the app. This separation is intentional: don't ship thousands of irrelevant files that bloat iOS/Android downloads or make our semi-realistic scene a mixture of incompatible art styles.

## Art direction policy

LIVEIT Story Mode uses a painterly 2.5D cinematic style. Free Life can expose a city map built from licensed/CC0 modular tiles, but either use a consistent art direction or keep pixel mode clearly separate. Prefer a small number of high-quality, reusable location plates to enormous piles of unrelated images.

An original AI-generated café and portrait are already embedded at prototype resolution. The previous original high-resolution concept ZIP can be imported with `tools/install_concept_art.py`, after rights review. Those original pieces are not third-party CC0 and should have their own provenance entry.

## Music, fonts, video and sound

Do not treat `freesound.org` or `opengameart.org` as single-license catalogues. Check each work: licensing, attribution and any distribution restrictions vary. We should prefer verified CC0 sound effects, use local assets at runtime, and never require network generation for ordinary gameplay.

If using SIL Open Font License fonts, preserve the OFL text and copyright notice. Do not distribute fonts separately to users or sell them as standalone products.

## Creator uploads

User-uploaded story packages are validated restricted data. Arbitrary external image uploads, hotlinked URLs, animation scripts and audio are **not yet enabled** because we still need rights declarations, file scanning, review queues, takedowns, abuse prevention and creator terms.

## Asset approval checklist

For each binary asset record: official source URL, creator, exact license, archived license text when required, SHA-256 of original and transformed content, dimensions/format, intended use, clear restrictions, reviewer, review date, and approved-for-shipping flag. Commit reviewed manifests alongside source assets.
