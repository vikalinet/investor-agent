'use client';

import { MapPin, TrendUp, Users, Calendar } from '@phosphor-icons/react';
import type { InvestmentProject } from '@/types';
import { SupportProgramBadge } from '../SupportProgramBadge/SupportProgramBadge';
import styles from './InvestmentCard.module.scss';

interface InvestmentCardProps {
  project: InvestmentProject;
  compact?: boolean;
}

const statusLabels: Record<InvestmentProject['status'], string> = {
  idea: 'Идея',
  planning: 'Планирование',
  approved: 'Одобрено',
  implemented: 'Реализовано',
  ongoing: 'В процессе',
};

export function InvestmentCard({ project, compact = false }: InvestmentCardProps) {
  return (
    <article className={styles.card} data-compact={compact}>
      <div className={styles.imageWrapper}>
        <img
          src={project.imageUrl}
          alt={project.name}
          className={styles.image}
          loading="lazy"
        />
        <span className={styles.statusBadge} data-status={project.status}>
          {statusLabels[project.status]}
        </span>
      </div>

      <div className={styles.content}>
        <div className={styles.header}>
          <h3 className={styles.title}>{project.name}</h3>
          <div className={styles.location}>
            <MapPin weight="thin" size={14} />
            <span>{project.location}</span>
          </div>
        </div>

        <p className={styles.industry}>{project.industry}</p>

        <div className={styles.metrics}>
          <div className={styles.metric}>
            <TrendUp weight="thin" size={16} />
            <div className={styles.metricBody}>
              <span className={styles.metricLabel}>IRR</span>
              <span className={styles.metricValue}>{project.irr}%</span>
            </div>
          </div>

          <div className={styles.metric}>
            <Calendar weight="thin" size={16} />
            <div className={styles.metricBody}>
              <span className={styles.metricLabel}>NPV</span>
              <span className={styles.metricValue}>{project.npv} ₽</span>
            </div>
          </div>

          <div className={styles.metric}>
            <Users weight="thin" size={16} />
            <div className={styles.metricBody}>
              <span className={styles.metricLabel}>Мест</span>
              <span className={styles.metricValue}>{project.jobsCreated}</span>
            </div>
          </div>
        </div>

        <div className={styles.progressSection}>
          <div className={styles.progressHeader}>
            <span className={styles.progressLabel}>Прогресс реализации</span>
            <span className={styles.progressValue}>{project.progress}%</span>
          </div>
          <div className={styles.progressBar}>
            <div
              className={styles.progressFill}
              style={{ width: `${project.progress}%` }}
            />
          </div>
        </div>

        {!compact && project.supportMeasures.length > 0 && (
          <div className={styles.badges}>
            {project.supportMeasures.map((measure) => (
              <SupportProgramBadge key={measure.id} measure={measure} compact />
            ))}
          </div>
        )}
      </div>
    </article>
  );
}
