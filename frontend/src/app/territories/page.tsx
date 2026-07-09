'use client';

import { useState, useEffect, useCallback } from 'react';
import { MagnifyingGlass, MapPin, Users, Buildings, SquaresFour, ChatCircleDots, Envelope } from '@phosphor-icons/react';
import { Skeleton } from '@/components/Skeleton/Skeleton';
import dynamic from 'next/dynamic';
import styles from './page.module.scss';

// Map loaded dynamically (SSR disabled — Leaflet needs window)
const Map = dynamic(() => import('./Map').then((m) => m.Map), {
  ssr: false,
  loading: () => <Skeleton height="100%" radius={12} />,
});

export interface Territory {
  id: string;
  territory_name: string;
  territory_type: string;
  area_km2: number;
  population: number;
  key_industries: string[];
  available_lots: number;
  infrastructure_score: number;
  tax_benefits: string;
  contact: {
    person: string;
    email: string;
  };
}

const typeLabels: Record<string, string> = {
  'город': 'Город',
  'район': 'Район',
  'ТОСЭР': 'ТОСЭР',
  'ОЭЗ': 'ОЭЗ',
};

const typeColors: Record<string, string> = {
  'город': '#3B7CC8',
  'район': '#2E9B72',
  'ТОСЭР': '#8B5CF6',
  'ОЭЗ': '#D4943B',
};

export default function TerritoriesPage() {
  const [territories, setTerritories] = useState<Territory[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [view, setView] = useState<'map' | 'list'>('map');
  const [selected, setSelected] = useState<Territory | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const res = await fetch('/api/territories');
        if (res.ok) {
          const data = await res.json();
          setTerritories(data);
        }
      } catch (error) {
        console.error('Ошибка загрузки территорий:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const filtered = territories.filter((t) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      t.territory_name.toLowerCase().includes(q) ||
      t.territory_type.toLowerCase().includes(q) ||
      t.key_industries.some((ind: string) => ind.toLowerCase().includes(q))
    );
  });

  const handleSelect = useCallback((t: Territory) => {
    setSelected(t);
  }, []);

  return (
    <div className={styles.page}>
      {/* Header */}
      <div className={styles.header}>
        <div>
          <h1>Территории с потенциалом</h1>
          <p>Выберите регион для размещения инвестиционного проекта</p>
        </div>

        {/* View toggle */}
        <div className={styles.toggle}>
          <button
            className={`${styles.toggleBtn} ${view === 'map' ? styles.toggleActive : ''}`}
            onClick={() => setView('map')}
          >
            <MapPin weight="thin" size={18} />
            <span>Карта</span>
          </button>
          <button
            className={`${styles.toggleBtn} ${view === 'list' ? styles.toggleActive : ''}`}
            onClick={() => setView('list')}
          >
            <SquaresFour weight="thin" size={18} />
            <span>Список</span>
          </button>
        </div>
      </div>

      {/* Search */}
      <div className={styles.searchRow}>
        <div className={styles.searchBox}>
          <MagnifyingGlass weight="thin" size={18} />
          <input
            type="text"
            placeholder="Поиск по названию или отрасли..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <span className={styles.resultCount}>
          {loading ? '...' : `${filtered.length} территорий`}
        </span>
      </div>

      {/* Content */}
      {view === 'map' ? (
        <div className={styles.mapLayout}>
          {/* Map */}
          <div className={styles.mapContainer}>
            <Map
              territories={filtered}
              onSelect={handleSelect}
            />
          </div>

          {/* Detail panel */}
          {selected && (
            <div className={styles.detailPanel}>
              <TerritoryCard territory={selected} onClose={() => setSelected(null)} />
            </div>
          )}
        </div>
      ) : (
        <div className={styles.grid}>
          {loading ? (
            Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className={styles.cardSkeleton}>
                <Skeleton height={40} radius={8} />
                <div style={{ marginTop: 12, display: 'flex', flexDirection: 'column', gap: 8 }}>
                  <Skeleton height={16} width="70%" />
                  <Skeleton height={14} width="50%" />
                  <Skeleton height={40} radius={8} />
                </div>
              </div>
            ))
          ) : filtered.length === 0 ? (
            <div className={styles.empty}>
              <MapPin weight="thin" size={48} />
              <p>Территории не найдены</p>
            </div>
          ) : (
            filtered.map((t) => (
              <TerritoryCard key={t.id} territory={t} />
            ))
          )}
        </div>
      )}
    </div>
  );
}


// --- Territory Card Component ---

function TerritoryCard({ territory, onClose }: { territory: Territory; onClose?: () => void }) {
  const typeColor = typeColors[territory.territory_type] || '#666';

  return (
    <article className={styles.card}>
      {/* Top: name + type badge + close */}
      <div className={styles.cardTop}>
        <h3 className={styles.cardName}>{territory.territory_name}</h3>
        <div className={styles.cardTopRight}>
          <span className={styles.typeBadge} style={{ background: typeColor }}>
            {typeLabels[territory.territory_type] || territory.territory_type}
          </span>
          {onClose && (
            <button className={styles.closeBtn} onClick={onClose}>✕</button>
          )}
        </div>
      </div>

      {/* Stats row */}
      <div className={styles.statsRow}>
        <div className={styles.statItem}>
          <span className={styles.statIcon}><SquaresFour weight="bold" size={14} /></span>
          <span className={styles.statNum}>{territory.area_km2}</span>
          <span className={styles.statUnit}>км²</span>
        </div>
        <div className={styles.statItem}>
          <span className={styles.statIcon}><Users weight="bold" size={14} /></span>
          <span className={styles.statNum}>{(territory.population / 1000).toFixed(0)}</span>
          <span className={styles.statUnit}>тыс.</span>
        </div>
        <div className={styles.statItem}>
          <span className={styles.statIcon}><Buildings weight="bold" size={14} /></span>
          <span className={styles.statNum}>{territory.available_lots}</span>
          <span className={styles.statUnit}>уч.</span>
        </div>
      </div>

      {/* Infrastructure score */}
      <div className={styles.scoreRow}>
        <span className={styles.scoreLabel}>Инфраструктура</span>
        <div className={styles.scoreBar}>
          <div
            className={styles.scoreFill}
            style={{ width: `${territory.infrastructure_score * 10}%` }}
          />
        </div>
        <span className={styles.scoreValue}>{territory.infrastructure_score}/10</span>
      </div>

      {/* Industries */}
      <div className={styles.tagsRow}>
        {territory.key_industries.map((ind: string) => (
          <span key={ind} className={styles.tag}>{ind}</span>
        ))}
      </div>

      {/* Tax benefits */}
      <div className={styles.taxBox}>
        <span className={styles.taxLabel}>Налоговые льготы</span>
        <p className={styles.taxText}>{territory.tax_benefits}</p>
      </div>

      {/* Contacts */}
      {territory.contact && (
        <div className={styles.contactRow}>
          <div className={styles.contactItem}>
            <ChatCircleDots weight="thin" size={14} />
            <span>{territory.contact.person}</span>
          </div>
          <div className={styles.contactItem}>
            <Envelope weight="thin" size={14} />
            <a href={`mailto:${territory.contact.email}`}>{territory.contact.email}</a>
          </div>
        </div>
      )}
    </article>
  );
}
