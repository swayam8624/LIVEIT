# LIVEIT — manually downloaded, license-verified art staging area

Use [docs/MANUAL_ASSET_DOWNLOAD_GUIDE.md](../../docs/MANUAL_ASSET_DOWNLOAD_GUIDE.md) for verified source links, manual-click/login sources, public-repository restrictions and the exact first playable 110-item asset list.

**Do NOT download every site and publish raw files to GitHub.** This directory is only for actual files with confirmed rights to redistribute publicly. Some assets may be commercially usable in compiled games but **not** redistributable as raw source files or downloadable standalone packs.

Suggested staging groups (create them when real verified files arrive): `cc0/pixel-city/`, `cc0/pixel-interiors/`, `cc0/rigged/`, `cc0/human-base/`, `cc0/props/`, `cc0/materials/`, `cc0/ui/`, `cc0/audio/`, `cc0/music/`, `mit/icons/`, `ofl/fonts/`, `attributed/`. Do not put private/restricted downloads in a public tracked directory.

Each included pack needs original publisher/source URL, download date, exact license and author, source archive SHA-256, file names, whether repository redistribution is authorized, required attribution/notices and a version. Keep `LICENSE`, `SOURCE.json` and any attribution notices alongside art; do not rename restricted files as CC0.

Do not count staged imports as LIVEIT production artwork automatically: use `npm run assets:validate`, QA and actual renderer/appearance/collision tests before promoting any catalog asset to `qa-passed` or `released`.

Do not add copyrighted Pokémon, Episode or ripped-game source assets.
