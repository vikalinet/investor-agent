'use client';

import { useState, useEffect } from 'react';
import { DashboardHeader } from '@/components/DashboardHeader/DashboardHeader';
import { InvestmentCard } from '@/components/InvestmentCard/InvestmentCard';
import { Skeleton } from '@/components/Skeleton/Skeleton';
import type { InvestmentProject, KPI } from '@/types';
import styles from './page.module.scss';

export default function HomePage() {
  const [projects, setProjects] = useState<InvestmentProject[]>([]);
  const [kpis, setKpis] = useState<KPI[]>([]);
  const [loading, setLoading] = useState(true);

  // Загрузка данных при монтировании
  useEffect(() => {
    const loadData = async () => {
      try {
        const [projectsRes, kpisRes] = await Promise.all([
          fetch('/api/projects'),
          fetch('/api/kpi'),
        ]);
        
        if (projectsRes.ok) {
          const data = await projectsRes.json();
          setProjects(data);
        }
        
        if (kpisRes.ok) {
          const data = await kpisRes.json();
          setKpis(data);
        }
      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  return (
    <div className={styles.page}>
      <DashboardHeader kpis={kpis} />

      <div className={styles.content}>
        <div className={styles.cardsSection}>
          <div className={styles.sectionHeader}>
            <h2>Инвестиционные объекты</h2>
            <span className={styles.sectionCount}>
              {loading ? <Skeleton width={60} height={16} /> : `${projects.length} проектов`}
            </span>
          </div>
          <div className={styles.cardsGrid}>
            {loading ? (
              // Скелетоны при загрузке
              Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className={styles.cardSkeleton}>
                  <Skeleton height={180} radius={12} />
                  <div style={{ marginTop: 16, display: 'flex', flexDirection: 'column', gap: 8 }}>
                    <Skeleton height={20} />
                    <Skeleton height={14} width="60%" />
                    <Skeleton height={40} />
                  </div>
                </div>
              ))
            ) : (
              projects.map((project) => (
                <InvestmentCard key={project.id} project={project} />
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
