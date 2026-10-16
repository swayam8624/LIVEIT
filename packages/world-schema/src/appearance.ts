import { z } from 'zod';

/**
 * Gameplay-neutral cosmetic character identity. No skin tone, body type,
 * hairstyle, gender expression or clothing grants stat bonuses.
 * Optional on v1 characters to keep all existing save files readable.
 */
export const SkinToneSchema = z.enum(['porcelain','ivory','peach','sand','golden','olive','tan','caramel','cocoa','mahogany','umber','espresso']);
export const FaceShapeSchema = z.enum(['oval','round','heart','square','long']);
export const EyeShapeSchema = z.enum(['almond','round','hooded','upturned','downturned']);
export const NoseShapeSchema = z.enum(['soft','straight','button','broad']);
export const LipShapeSchema = z.enum(['natural','full','thin','smile']);
export const BrowShapeSchema = z.enum(['soft','arched','straight','bold']);
export const HairStyleSchema = z.enum(['pixie','buzz','bob','lob','waves','curls','coils','afro','ponytail','braids','locs','sidepart','shag','long']);
export const HairColorSchema = z.enum(['midnight','black','espresso','chestnut','auburn','copper','blonde','ash','silver','rose','blue','violet']);
export const EyeColorSchema = z.enum(['brown','hazel','amber','green','blue','gray','violet']);
export const BodyFrameSchema = z.enum(['slim','average','athletic','broad']);
export const OutfitSchema = z.enum(['casual','streetwear','smart','formal','cozy','athletic','vintage','creative','evening']);
export const OutfitColorSchema = z.enum(['navy','charcoal','forest','burgundy','cream','plum','teal','rose','gold']);
export const AccessorySchema = z.enum(['none','glasses','earrings','necklace','freckles']);

export const FacialHairSchema = z.enum(['none','stubble','goatee','beard','moustache']);
export const HeadwearSchema = z.enum(['none','beanie','cap','headband','beret']);
export const MakeupSchema = z.enum(['none','soft','bold','gloss']);
export const AppearanceSchema = z.object({
  skinTone: SkinToneSchema,
  face: FaceShapeSchema,
  eyes: EyeShapeSchema,
  eyeColor: EyeColorSchema,
  nose: NoseShapeSchema,
  lips: LipShapeSchema,
  brows: BrowShapeSchema,
  hair: HairStyleSchema,
  hairColor: HairColorSchema,
  body: BodyFrameSchema,
  outfit: OutfitSchema,
  outfitColor: OutfitColorSchema,
  accessory: AccessorySchema,
  facialHair: FacialHairSchema.optional(),
  headwear: HeadwearSchema.optional(),
  makeup: MakeupSchema.optional(),
}).strict();

export type Appearance = z.infer<typeof AppearanceSchema>;

export const DEFAULT_APPEARANCE: Appearance = {
  skinTone: 'golden', face: 'oval', eyes: 'almond', eyeColor: 'brown',
  nose: 'soft', lips: 'natural', brows: 'soft', hair: 'waves',
  hairColor: 'espresso', body: 'average', outfit: 'casual',
  outfitColor: 'navy', accessory: 'none', facialHair: 'none',
  headwear: 'none', makeup: 'none',
};

export const SKIN_COLORS: Record<Appearance['skinTone'],string> = {
  porcelain:'#f6ddca', ivory:'#eecbad', peach:'#efbf9e', sand:'#dca983',
  golden:'#c98c5f', olive:'#b7865a', tan:'#aa7150', caramel:'#99603f',
  cocoa:'#784a32', mahogany:'#673b2d', umber:'#503025', espresso:'#382219',
};
export const HAIR_COLORS: Record<Appearance['hairColor'],string> = {
  midnight:'#141520', black:'#231c22', espresso:'#372522', chestnut:'#67402b',
  auburn:'#8d432e', copper:'#bc703c', blonde:'#d6ae63', ash:'#8d8075',
  silver:'#bfc2c9', rose:'#c98294', blue:'#4c6d99', violet:'#78547e',
};
export const EYE_COLORS: Record<Appearance['eyeColor'],string> = {
  brown:'#503122', hazel:'#8a672e', amber:'#b58a37', green:'#4e815e',
  blue:'#5a90be', gray:'#8b949c', violet:'#886b9f',
};
export const OUTFIT_COLORS: Record<Appearance['outfitColor'],string> = {
  navy:'#263c62', charcoal:'#3d414a', forest:'#3c6754',
  burgundy:'#873d54', cream:'#e3d4b7', plum:'#6a4a73',
  teal:'#39878c', rose:'#bf7484', gold:'#c3994a',
};
export const APPEARANCE_GROUPS = [
  { key: 'skinTone', label: 'Skin tone', color: 'skin' },
  { key: 'face', label: 'Face shape' },
  { key: 'eyes', label: 'Eye shape' },
  { key: 'eyeColor', label: 'Eye color', color: 'eyes' },
  { key: 'nose', label: 'Nose' },
  { key: 'lips', label: 'Lips' },
  { key: 'brows', label: 'Brows' },
  { key: 'hair', label: 'Hairstyle' },
  { key: 'hairColor', label: 'Hair color', color: 'hair' },
  { key: 'body', label: 'Body frame' },
  { key: 'outfit', label: 'Clothing style' },
  { key: 'outfitColor', label: 'Clothing color', color: 'outfit' },
  { key: 'accessory', label: 'Accessories' },
  { key: 'facialHair', label: 'Facial hair' },
  { key: 'headwear', label: 'Hats & headwear' },
  { key: 'makeup', label: 'Makeup' },
] as const satisfies readonly {key: keyof Appearance; label: string; color?: string}[];

/** Keep appearance validation pure so Creator Studio and player can share it. */
export function applyAppearance<T extends {player: {appearance?: Appearance}}>(
  input: T, appearance: Appearance,
): T {
  const validated = AppearanceSchema.parse(appearance);
  return {...input,player:{...input.player,appearance:validated}};
}
