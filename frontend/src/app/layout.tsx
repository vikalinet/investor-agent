import type { Metadata } from 'next';
import { Montserrat, IBM_Plex_Sans } from 'next/font/google';
import './globals.scss';

const montserrat = Montserrat({
  subsets: ['latin', 'cyrillic'],
  weight: ['600', '700'],
  variable: '--font-montserrat',
  display: 'swap',
});

const ibmPlexSans = IBM_Plex_Sans({
  subsets: ['latin', 'cyrillic'],
  weight: ['400', '500', '600'],
  variable: '--font-ibm-plex',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'Инвестиционный помощник — Свердловская область',
  description: 'AI-агент для поддержки инвесторов: анализ практик, поиск потенциала, подготовка документов',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru" className={`${montserrat.variable} ${ibmPlexSans.variable}`}>
      <body>{children}</body>
    </html>
  );
}
