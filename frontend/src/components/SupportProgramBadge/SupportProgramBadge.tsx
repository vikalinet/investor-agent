'use client';

import {
  CurrencyCircleDollar,
  Receipt,
  Building,
  ChatsCircle,
} from '@phosphor-icons/react';
import type { SupportMeasure, SupportMeasureType } from '@/types';
import styles from './SupportProgramBadge.module.scss';

interface SupportProgramBadgeProps {
  measure: SupportMeasure;
  compact?: boolean;
}

const typeConfig: Record<SupportMeasureType, { icon: React.ReactNode; label: string }> = {
  financial: {
    icon: <CurrencyCircleDollar weight="thin" size={14} />,
    label: 'Финансовая',
  },
  tax: {
    icon: <Receipt weight="thin" size={14} />,
    label: 'Налоговая',
  },
  infrastructure: {
    icon: <Building weight="thin" size={14} />,
    label: 'Инфраструктура',
  },
  advisory: {
    icon: <ChatsCircle weight="thin" size={14} />,
    label: 'Консультации',
  },
};

export function SupportProgramBadge({ measure, compact = false }: SupportProgramBadgeProps) {
  const config = typeConfig[measure.type];

  return (
    <span className={styles.badge} data-type={measure.type} data-compact={compact}>
      <span className={styles.icon}>{config.icon}</span>
      {!compact && <span className={styles.label}>{measure.name}</span>}
    </span>
  );
}
