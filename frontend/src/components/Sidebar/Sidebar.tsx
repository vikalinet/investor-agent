'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Plus, ChatCircle, ChartLine, MapPin, FileText } from '@phosphor-icons/react';
import type { SidebarHistoryItem } from '@/types';
import styles from './Sidebar.module.scss';

interface SidebarProps {
  history?: SidebarHistoryItem[];
  activeId?: string;
  onSelect?: (id: string) => void;
}

const defaultHistory: SidebarHistoryItem[] = [
  {
    id: '1',
    title: 'Анализ IT-кластера',
    date: '09.07.2024',
    preview: 'Инвестиционный потенциал Екатеринбурга...',
  },
  {
    id: '2',
    title: 'ТОСЭР Краснотурьинск',
    date: '08.07.2024',
    preview: 'Налоговые льготы для резидентов...',
  },
  {
    id: '3',
    title: 'Субсидия на оборудование',
    date: '05.07.2024',
    preview: 'Подготовка документов на меру поддержки...',
  },
  {
    id: '4',
    title: 'Логистика Урал',
    date: '02.07.2024',
    preview: 'Лучшие практики в логистике...',
  },
];

const navItems = [
  { icon: <ChartLine weight="thin" size={18} />, label: 'Дашборд', href: '/' },
  { icon: <ChatCircle weight="thin" size={18} />, label: 'Чат с агентом', href: '/chat' },
  { icon: <MapPin weight="thin" size={18} />, label: 'Территории', href: '/territories' },
  { icon: <FileText weight="thin" size={18} />, label: 'Документы', href: '/documents' },
];

export function Sidebar({
  history = defaultHistory,
  activeId = '1',
  onSelect,
}: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside className={styles.sidebar}>
      <div className={styles.logo}>
        <div className={styles.logoIcon}>
          <ChartLine weight="fill" size={18} />
        </div>
        <div className={styles.logoText}>
          <span className={styles.logoTitle}>ИнвестУрал</span>
          <span className={styles.logoSubtitle}>AI-помощник</span>
        </div>
      </div>

      <Link href="/chat" className={styles.newChat}>
        <Plus weight="thin" size={18} />
        <span>Новый диалог</span>
      </Link>

      <nav className={styles.nav}>
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.label}
              href={item.href}
              className={`${styles.navItem} ${isActive ? styles.navItemActive : ''}`}
            >
              {item.icon}
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className={styles.historySection}>
        <span className={styles.historyTitle}>История</span>
        <ul className={styles.historyList}>
          {history.map((item) => (
            <li key={item.id}>
              <button
                className={`${styles.historyItem} ${item.id === activeId ? styles.active : ''}`}
                onClick={() => onSelect?.(item.id)}
              >
                <ChatCircle weight="thin" size={16} />
                <div className={styles.historyContent}>
                  <span className={styles.historyName}>{item.title}</span>
                  <span className={styles.historyDate}>{item.date}</span>
                </div>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}
