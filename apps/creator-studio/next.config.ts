import type { NextConfig } from 'next';
const config: NextConfig = {
  transpilePackages: [
    '@living/story-schema',
    '@living/world-schema',
    '@living/content',
  ],
};
export default config;
