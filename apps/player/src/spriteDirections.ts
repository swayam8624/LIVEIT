/** Exact column order verified against the supplied 384×32 Modern Interiors
 * character RUN sheets (24 columns × 16 pixels; each actor 16×32).
 * columns 0–5 = facing RIGHT, 6–11 = UP, 12–17 = LEFT, 18–23 = DOWN.
 * Keep this independently tested so regressions cannot silently flip actors.
 */
export const MODERN_DIRECTIONS = { right: 0, up: 1, left: 2, down: 3 } as const;
export function modernSpriteColumn(
  facing: keyof typeof MODERN_DIRECTIONS, phase: number,
): number {
  const step = Number.isFinite(phase) ? Math.abs(Math.floor(phase)) % 6 : 0;
  return MODERN_DIRECTIONS[facing] * 6 + step;
}
