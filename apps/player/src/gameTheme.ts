import { Platform } from 'react-native';

/**
 * LIVEIT "Arcade After Dark": tactile city-sim UI, not a hard-to-read
 * imitation of an 8-bit monitor. Contrast is checked on dark surfaces.
 * All fonts are built into the target OS; no unlicensed font files.
 */
export const gameTheme = {
  background: '#101827',
  panel: '#1A2737',
  panelRaised: '#223449',
  midnight: '#101827',
  ink: '#F5F2D9',
  muted: '#B6C6C8',
  border: '#507174',
  neon: '#97E6AC',
  neonDeep: '#356D62',
  amber: '#FFD28A',
  coral: '#F49A82',
  danger: '#FF7588',
  water: '#2B617A',
  park: '#427969',
  road: '#243543',
  font: {
    display: Platform.select({
      ios: 'AvenirNextCondensed-DemiBold',
      android: 'sans-serif-condensed',
      default: 'system-ui',
    }),
    hud: Platform.select({
      ios: 'Menlo-Bold',
      android: 'monospace',
      default: 'monospace',
    }),
    body: Platform.select({
      ios: 'AvenirNext-Medium',
      android: 'sans-serif-medium',
      default: 'system-ui',
    }),
  },
} as const;

export const districtColors = [
  '#2D6578',
  '#4C5D8D',
  '#A16854',
  '#805778',
  '#41765F',
] as const;
