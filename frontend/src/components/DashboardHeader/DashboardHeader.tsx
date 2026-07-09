'use client';

import {
  Briefcase,
  CurrencyRub,
  Gift,
  Users,
  TrendUp,
  TrendDown,
  Minus,
} from '@phosphor-icons/react';
import type { KPI } from '@/types';
import styles from './DashboardHeader.module.scss';

const defaultKPIs: KPI[] = [
  {
    id: 'projects',
    label: 'Активные проекты',
    value: '24',
    trend: { direction: 'up', value: '12%' },
  },
  {
    id: 'budget',
    label: 'Общий бюджет',
    value: '3.65',
    unit: 'млрд ₽',
    trend: { direction: 'up', value: '8%' },
  },
  {
    id: 'grants',
    label: 'Доступные гранты',
    value: '12',
    trend: { direction: 'stable', value: '0%' },
  },
  {
    id: 'jobs',
    label: 'Создано рабочих мест',
    value: '770',
    trend: { direction: 'up', value: '15%' },
  },
];

interface DashboardHeaderProps {
  kpis?: KPI[];
}

const trendIcon = {
  up: <TrendUp weight="thin" size={14} />,
  down: <TrendDown weight="thin" size={14} />,
  stable: <Minus weight="thin" size={14} />,
};

const trendColor = {
  up: styles.trendUp,
  down: styles.trendDown,
  stable: styles.trendStable,
};

export function DashboardHeader({ kpis = defaultKPIs }: DashboardHeaderProps) {
  return (
    <header className={styles.header}>
      <div className={styles.content}>
        <div className={styles.title}>
          <h1>Инвестиционный помощник</h1>
          <p>Свердловская область</p>
        </div>

        <div className={styles.kpiGrid}>
          {kpis.map((kpi) => (
            <div key={kpi.id} className={styles.kpiCard}>
              <div className={styles.kpiIcon}>
                {kpi.id === 'projects' && <Briefcase weight="thin" size={20} />}
                {kpi.id === 'budget' && <CurrencyRub weight="thin" size={20} />}
                {kpi.id === 'grants' && <Gift weight="thin" size={20} />}
                {kpi.id === 'jobs' && <Users weight="thin" size={20} />}
              </div>

              <div className={styles.kpiBody}>
                <span className={styles.kpiLabel}>{kpi.label}</span>
                <div className={styles.kpiValue}>
                  <span className={styles.kpiNumber}>{kpi.value}</span>
                  {kpi.unit && <span className={styles.kpiUnit}>{kpi.unit}</span>}
                </div>
                {kpi.trend && (
                  <span className={`${styles.kpiTrend} ${trendColor[kpi.trend.direction]}`}>
                    {trendIcon[kpi.trend.direction]}
                    {kpi.trend.value}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </header>
  );
}
