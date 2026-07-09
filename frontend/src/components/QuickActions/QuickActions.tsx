'use client';

import {
  MagnifyingGlass,
  FileText,
  CheckCircle,
  ChatCircleText,
} from '@phosphor-icons/react';
import styles from './QuickActions.module.scss';

interface QuickAction {
  id: string;
  icon: React.ReactNode;
  title: string;
  description: string;
  action: string;
}

const defaultActions: QuickAction[] = [
  {
    id: '1',
    icon: <MagnifyingGlass weight="thin" size={20} />,
    title: 'Найти проект',
    description: 'Поиск инвестиционных возможностей по отрасли',
    action: 'Поиск проектов',
  },
  {
    id: '2',
    icon: <FileText weight="thin" size={20} />,
    title: 'Меры поддержки',
    description: 'Гранты, субсидии, налоговые льготы',
    action: 'Просмотр мер',
  },
  {
    id: '3',
    icon: <CheckCircle weight="thin" size={20} />,
    title: 'Проверить документы',
    description: 'Валидация пакета документов на ошибки',
    action: 'Проверить',
  },
  {
    id: '4',
    icon: <ChatCircleText weight="thin" size={20} />,
    title: 'Задать вопрос',
    description: 'Получить консультацию у агента',
    action: 'Написать',
  },
];

interface QuickActionsProps {
  actions?: QuickAction[];
  onAction?: (action: string) => void;
}

export function QuickActions({ actions = defaultActions, onAction }: QuickActionsProps) {
  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Быстрые действия</h3>

      <div className={styles.grid}>
        {actions.map((action) => (
          <button
            key={action.id}
            className={styles.card}
            onClick={() => onAction?.(action.action)}
          >
            <div className={styles.icon}>{action.icon}</div>
            <div className={styles.body}>
              <span className={styles.title}>{action.title}</span>
              <span className={styles.description}>{action.description}</span>
            </div>
            <div className={styles.arrow}>→</div>
          </button>
        ))}
      </div>
    </div>
  );
}
