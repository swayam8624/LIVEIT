# Contributing

Read README.md, docs/PRODUCT_SPEC.md, docs/ARCHITECTURE.md, SECURITY.md, CODE_OF_CONDUCT.md, and applicable AGENTS.md instructions before changes. This is a new foundation; no prior pull requests or existing implementation conventions were available during initialization.

Explain the issue, root cause, affected packages and verification plan before editing. Keep patches focused; preserve save and story contracts or add an explicit migration. Do not add dependencies without an approved feature need. Story authors supply data, never executable scripts.

Use strict TypeScript, descriptive camelCase functions and variables, PascalCase types, and kebab-case package names. Prettier controls formatting. Use semantic commit subjects such as `fix: preserve timeline isolation` when the owner authorizes a commit. No commit, push, or PR creation is part of the foundation task.

Add regression tests in tests/ for state transitions, compatibility rules, or persistence changes. Run `npm run check`, `npm run build:player`, and `npm run build:studio`. Report exact commands and untested platforms. Avoid snapshot-only tests for core rules. Prefer pure transformations and integer money values. React components must not implement separate gameplay formulas.
