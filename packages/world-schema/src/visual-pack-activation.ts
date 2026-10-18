import {
  VisualPackSchema,
  indexVisualAssets,
  type VisualAsset,
  type VisualPack,
} from './visual-assets';

export type VisualPackActivation = Readonly<{
  packs: readonly VisualPack[];
  index: ReadonlyMap<string, VisualAsset>;
  newlyVerifiedBytes: number;
}>;

export type VisualAssetVerifier = Readonly<{
  /** Must read from a trusted, sandboxed pack staging directory, NOT arbitrary URLs. */
  read: (packId: string, path: string) => Promise<Uint8Array>;
  /** Platform-specific cryptographic SHA-256; return lowercase 64-character hex. */
  sha256: (bytes: Uint8Array) => Promise<string>;
}>;

function greaterVersion(current: string, minimum: string): boolean {
  const lhs = current.split('.').map(Number);
  const rhs = minimum.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    if (lhs[i]! !== rhs[i]!) return lhs[i]! > rhs[i]!;
  }
  return true;
}

/**
 * Validate a new pack set completely before it can be activated by storage.
 *
 * Returns an immutable candidate snapshot, never mutating existing packs.
 * The device storage layer must perform an atomic staged-file rename +
 * manifest pointer transaction AFTER this function succeeds. No network or
 * filesystem operations occur here, and no downloadable executable code runs.
 */
export async function prepareVisualPackActivation(
  previouslyInstalled: readonly VisualPack[],
  incoming: readonly unknown[],
  verifier: VisualAssetVerifier,
  gameVersion = '0.1.0',
): Promise<VisualPackActivation> {
  if (!/^\d+\.\d+\.\d+$/.test(gameVersion)) {
    throw new Error('Invalid runtime game version');
  }
  const replacements = new Map<string, VisualPack>();
  for (const candidate of incoming) {
    const pack = VisualPackSchema.parse(candidate);
    if (replacements.has(pack.id))
      throw new Error('Duplicate incoming visual pack');
    if (!greaterVersion(gameVersion, pack.minGameVersion)) {
      throw new Error('Pack requires newer game version: ' + pack.id);
    }
    replacements.set(pack.id, pack);
  }
  const previousById = new Map(
    previouslyInstalled.map((pack) => [pack.id, pack]),
  );
  for (const [id, candidate] of replacements) {
    const previous = previousById.get(id);
    if (previous && candidate.revision <= previous.revision) {
      throw new Error('Pack revisions must increase: ' + id);
    }
  }
  const packs = [
    ...previouslyInstalled.filter((pack) => !replacements.has(pack.id)),
    ...replacements.values(),
  ];
  const ids = new Set(packs.map((pack) => pack.id));
  if (ids.size !== packs.length)
    throw new Error('Duplicate installed visual pack');
  for (const pack of packs) {
    for (const required of pack.dependencies) {
      if (!ids.has(required))
        throw new Error('Missing required visual pack: ' + required);
    }
  }
  const index = indexVisualAssets(packs);
  // Do not allocate/download unlimited declared external resources.
  let total = 0;
  for (const pack of replacements.values()) {
    for (const asset of pack.assets) {
      if (asset.implementation.kind !== 'external') continue;
      const { path, bytes, sha256 } = asset.implementation;
      if (bytes > 96 * 1024 * 1024 || total + bytes > 256 * 1024 * 1024) {
        throw new Error('Pack exceeds staged download memory budget');
      }
      const payload = await verifier.read(pack.id, path);
      if (payload.byteLength !== bytes)
        throw new Error('Asset byte size mismatch: ' + asset.id);
      const actual = await verifier.sha256(payload);
      if (actual !== sha256)
        throw new Error('Asset digest mismatch: ' + asset.id);
      total += bytes;
    }
  }
  return { packs, index, newlyVerifiedBytes: total };
}
