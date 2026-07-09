'use client';

import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import type { Territory } from './page';
import styles from './Map.module.scss';

// Fix default marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Territory coordinates
const territoryCoords: Record<string, [number, number]> = {
  'Екатеринбург': [56.8389, 60.6057],
  'Нижний Тагил': [57.9190, 59.9650],
  'ТОСЭР Краснотурьинск': [59.7490, 60.2030],
  'Сысертский район': [56.5000, 60.2500],
  'Арамиль': [56.6928, 60.9397],
};

// Marker colors by infrastructure score
function getMarkerColor(score: number): string {
  if (score >= 8) return '#2E9B72';
  if (score >= 6) return '#C8A96E';
  return '#C8514B';
}

interface MapProps {
  territories: Territory[];
  onSelect: (t: Territory) => void;
}

// Center map on Sverdlovsk region
function MapCenter({ center }: { center: [number, number] }) {
  const map = useMap();
  map.setView(center, 7);
  return null;
}

export function Map({ territories, onSelect }: MapProps) {
  return (
    <MapContainer
      center={[57.5, 60.0]}
      zoom={7}
      style={{ height: '100%', width: '100%', borderRadius: '12px', zIndex: 0, position: 'relative' }}
      scrollWheelZoom
      zoomControl={true}
      attributionControl={false} // Убираем attribution с флагом
    >
      <MapCenter center={[57.5, 60.0]} />

      {/* OpenStreetMap — русские названия для городов РФ */}
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="© OpenStreetMap"
        maxZoom={19}
      />

      {territories.map((territory) => {
        const coords = territoryCoords[territory.territory_name];
        if (!coords) return null;

        const color = getMarkerColor(territory.infrastructure_score);

        // Создаем иконку с нужным цветом
        const markerIcon = new L.DivIcon({
          className: 'territory-marker',
          html: `<div style="
            width: 24px;
            height: 24px;
            background: ${color};
            border: 3px solid #0B1F3B;
            border-radius: 50%;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          "></div>`,
          iconSize: [24, 24],
          iconAnchor: [12, 12],
          popupAnchor: [0, -12],
        });

        return (
          <Marker
            key={territory.id}
            position={coords}
            icon={markerIcon}
            eventHandlers={{
              click: () => onSelect(territory),
            }}
          >
            <Popup>
              <div className={styles.popup}>
                <strong className={styles.popupTitle}>{territory.territory_name}</strong>
                <div className={styles.popupRow}>
                  <span className={styles.popupLabel}>Тип:</span>
                  <span>{territory.territory_type}</span>
                </div>
                <div className={styles.popupRow}>
                  <span className={styles.popupLabel}>Инфраструктура:</span>
                  <span>
                    {territory.infrastructure_score}/10
                    <span
                      className={styles.scoreDot}
                      style={{ background: color }}
                    />
                  </span>
                </div>
                <div className={styles.popupRow}>
                  <span className={styles.popupLabel}>Участков:</span>
                  <span>{territory.available_lots}</span>
                </div>
                <div className={styles.popupRow}>
                  <span className={styles.popupLabel}>Отрасли:</span>
                  <span>{territory.key_industries.join(', ')}</span>
                </div>
              </div>
            </Popup>
          </Marker>
        );
      })}
      
      {/* Легенда карты */}
      <div className={styles.legend}>
        <div className={styles.legendItem}>
          <span className={styles.legendDot} style={{ background: '#2E9B72' }} />
          <span>Высокая оценка (8-10)</span>
        </div>
        <div className={styles.legendItem}>
          <span className={styles.legendDot} style={{ background: '#C8A96E' }} />
          <span>Средняя оценка (6-8)</span>
        </div>
        <div className={styles.legendItem}>
          <span className={styles.legendDot} style={{ background: '#C8514B' }} />
          <span>Низкая оценка (&lt;6)</span>
        </div>
      </div>
    </MapContainer>
  );
}
