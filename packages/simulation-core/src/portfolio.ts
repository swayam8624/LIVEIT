import { WorldSchema, record, type World } from '@living/world-schema';

/**
 * OpenLife-inspired (not copied) deterministic asset market.
 * Money is stored as pence, not floating-point pounds. Every operation
 * validates a complete world and returns a new one: no partial purchases.
 */
export const CATALOG = {
  bicycle: { label: 'City bicycle', price: 25_000, annualUpkeep: 2_000, depreciation: 0.90, category: 'transport' },
  car: { label: 'Used hatchback', price: 450_000, annualUpkeep: 72_000, depreciation: 0.84, category: 'transport' },
  flat: { label: 'One-bedroom flat', price: 11_000_000, annualUpkeep: 165_000, depreciation: 1.025, category: 'property' },
  townhouse: { label: 'Townhouse', price: 29_000_000, annualUpkeep: 360_000, depreciation: 1.03, category: 'property' },
} as const;
export type AssetId = keyof typeof CATALOG;
const MAX_CASH = 100_000_000;
const boundedMoney = (n: number) => Math.max(-MAX_CASH, Math.min(MAX_CASH, Math.round(n)));

/** A legacy save without a portfolio is treated as owning nothing. */
export function portfolio(world: World) {
  return world.portfolio ?? { indexPence: 0, owned: [] };
}
export function assetValue(id: AssetId, years: number) {
  const item = CATALOG[id];
  // Used cars depreciate; property appreciates; never fabricate market prices
  // from a live feed. This is a fictional deterministic game economy.
  return Math.max(0, Math.round(item.price * item.depreciation ** Math.max(0, years)));
}
export function netWorth(world: World) {
  const p = portfolio(world);
  return world.player.money + p.indexPence + p.owned.reduce((sum, item) =>
    sum + assetValue(item.id, Math.floor((world.day - item.dayBought) / 365)), 0);
}
function validated(input: World) {
  const w = structuredClone(WorldSchema.parse(input));
  w.portfolio ??= { indexPence: 0, owned: [] };
  return w;
}

export function buyAsset(input: World, id: AssetId): World {
  if (!(id in CATALOG)) throw new Error('Unknown asset.');
  const w = validated(input);
  const item = CATALOG[id];
  if (w.player.ageDays < 18 * 365) throw new Error('You must be an adult to purchase assets.');
  if (w.portfolio!.owned.some((owned) => owned.id === id)) throw new Error('You already own this asset.');
  if (w.player.money < item.price) throw new Error('Not enough available cash for this purchase.');
  w.player.money -= item.price;
  w.portfolio!.owned.push({ id, dayBought: w.day });
  if (id === 'flat' || id === 'townhouse') {
    if (w.city) w.city.housing = id === 'flat' ? 'own_flat' : 'townhouse';
  }
  record(w, 'choice', `Bought ${item.label} for £${(item.price / 100).toLocaleString('en-GB')}.`);
  return WorldSchema.parse(w);
}
export function sellAsset(input: World, id: AssetId): World {
  if (!(id in CATALOG)) throw new Error('Unknown asset.');
  const w = validated(input);
  const index = w.portfolio!.owned.findIndex((asset) => asset.id === id);
  if (index === -1) throw new Error('You do not own that asset.');
  const purchase = w.portfolio!.owned[index]!;
  const years = Math.floor((w.day - purchase.dayBought) / 365);
  // 5% resale transaction cost. No ability to buy/sell repeatedly for gain.
  const proceeds = Math.round(assetValue(id, years) * 0.95);
  if (w.player.money + proceeds > MAX_CASH) throw new Error('Cash cap reached; cannot settle this sale.');
  w.portfolio!.owned.splice(index, 1);
  w.player.money += proceeds;
  if ((id === 'flat' || id === 'townhouse') && w.city) {
    w.city.housing = w.portfolio!.owned.some((x) => x.id === 'townhouse')
      ? 'townhouse' : w.portfolio!.owned.some((x) => x.id === 'flat')
      ? 'own_flat' : 'shared_flat';
  }
  record(w, 'choice', `Sold ${CATALOG[id].label} for £${(proceeds / 100).toLocaleString('en-GB')} after fees.`);
  return WorldSchema.parse(w);
}
export function investIndex(input: World, pence: number): World {
  if (!Number.isSafeInteger(pence) || pence < 5_000) throw new Error('Minimum index investment is £50.');
  const w = validated(input);
  if (w.player.ageDays < 18 * 365) throw new Error('You must be an adult to invest.');
  if (w.player.money < pence) throw new Error('Not enough cash to invest.');
  if (w.portfolio!.indexPence + pence > MAX_CASH) throw new Error('Portfolio limit reached.');
  w.player.money -= pence;
  w.portfolio!.indexPence += pence;
  record(w, 'choice', `Invested £${(pence / 100).toLocaleString('en-GB')} in the fictional broad-market index.`);
  return WorldSchema.parse(w);
}
export function withdrawIndex(input: World, pence: number): World {
  if (!Number.isSafeInteger(pence) || pence <= 0) throw new Error('Withdrawal must be positive.');
  const w = validated(input);
  if (w.portfolio!.indexPence < pence) throw new Error('Insufficient investment balance.');
  if (w.player.money + pence > MAX_CASH) throw new Error('Cash limit reached.');
  w.portfolio!.indexPence -= pence;
  w.player.money += pence;
  record(w, 'choice', `Withdrew £${(pence / 100).toLocaleString('en-GB')} from the index.`);
  return WorldSchema.parse(w);
}

/** Pure annual rebalance, invoked exactly once by the age-up transition. */
export function tickPortfolio(world: World): void {
  const p = world.portfolio;
  if (!p) return;
  const year = Math.floor(world.day / 365);
  const cycle = [1.04, 1.08, 0.93, 1.11] as const;
  const previous = p.indexPence;
  p.indexPence = Math.min(MAX_CASH, Math.round(previous * cycle[year % cycle.length]));
  const upkeep = p.owned.reduce((sum, asset) => sum + CATALOG[asset.id].annualUpkeep, 0);
  world.player.money = boundedMoney(world.player.money - upkeep);
  if (upkeep > 0) record(world, 'simulation',
    `Paid £${(upkeep / 100).toLocaleString('en-GB')} in yearly vehicle and property upkeep.`);
  if (previous > 0) record(world, 'simulation',
    `Index holdings changed from £${(previous / 100).toLocaleString('en-GB')} to £${(p.indexPence / 100).toLocaleString('en-GB')} through the simulated market cycle.`);
}
