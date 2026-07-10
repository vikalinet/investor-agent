'use client';

import { Check, Circle, Clock, X } from '@phosphor-icons/react';
import type { ApplicationStep } from '@/types';
import styles from './ApplicationStatus.module.scss';

interface ApplicationStatusProps {
  steps: ApplicationStep[];
  title?: string;
}

const defaultSteps: ApplicationStep[] = [
  {
    id: '1',
    title: 'Подготовка документов',
    status: 'completed',
    description: 'Сбор и проверка пакета документов',
    date: '15.06.2026',
  },
  {
    id: '2',
    title: 'Подача заявки',
    status: 'completed',
    description: 'Отправка в министерство',
    date: '18.06.2026',
  },
  {
    id: '3',
    title: 'Рассмотрение',
    status: 'current',
    description: 'Проверка комиссией',
  },
  {
    id: '4',
    title: 'Решение',
    status: 'pending',
    description: 'Уведомление о результате',
  },
];

const statusIcons = {
  completed: <Check weight="bold" size={12} />,
  current: <Clock weight="fill" size={12} />,
  pending: <Circle weight="fill" size={12} />,
  rejected: <X weight="bold" size={12} />,
};

export function ApplicationStatus({
  steps = defaultSteps,
  title = 'Статус заявки',
}: ApplicationStatusProps) {
  return (
    <div className={styles.container}>
      <h3 className={styles.title}>{title}</h3>

      <div className={styles.timeline}>
        {steps.map((step, index) => (
          <div key={step.id} className={styles.step}>
            {/* Левая колонка: кружок + линия */}
            <div className={styles.stepIconWrapper}>
              <div className={`${styles.stepIcon} ${styles[step.status]}`}>
                {statusIcons[step.status]}
              </div>
              {index < steps.length - 1 && (
                <div className={styles.line} />
              )}
            </div>

            {/* Правая колонка: контент */}
            <div className={styles.stepContent}>
              <div className={styles.stepHeader}>
                <span className={styles.stepTitle}>{step.title}</span>
                {step.date && <span className={styles.stepDate}>{step.date}</span>}
              </div>
              {step.description && (
                <p className={styles.stepDescription}>{step.description}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
