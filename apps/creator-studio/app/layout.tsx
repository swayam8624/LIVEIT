import type { ReactNode } from 'react';
import './style.css';
export const metadata = {
  title: 'Creator Studio · Living Universe',
  description: 'Write and validate an encounter for Living Universe.',
};
export default function Layout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
