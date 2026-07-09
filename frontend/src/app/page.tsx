'use client';

import { useState, useEffect, useCallback } from 'react';
import { Sidebar } from '@/components/Sidebar/Sidebar';
import { DashboardHeader } from '@/components/DashboardHeader/DashboardHeader';
import { ChatInterface } from '@/components/ChatInterface/ChatInterface';
import { InvestmentCard } from '@/components/InvestmentCard/InvestmentCard';
import { ApplicationStatus } from '@/components/ApplicationStatus/ApplicationStatus';
import { Skeleton } from '@/components/Skeleton/Skeleton';
import type { ChatMessage, InvestmentProject, ApplicationStep, KPI } from '@/types';
import styles from './page.module.scss';

const initialMessages: ChatMessage[] = [
  {
    id: '1',
    role: 'agent',
    content: 'Здравствуйте! Я — ваш инвестиционный помощник по Свердловской области. Чем могу помочь?',
    timestamp: new Date().toISOString(),
  },
];

const applicationSteps: ApplicationStep[] = [
  { id: '1', title: 'Подготовка документов', status: 'completed', description: 'Сбор и проверка пакета документов', date: '15.06.2024' },
  { id: '2', title: 'Подача заявки', status: 'completed', description: 'Отправка в министерство', date: '18.06.2024' },
  { id: '3', title: 'Рассмотрение комиссией', status: 'current', description: 'Проверка заявки и документов' },
  { id: '4', title: 'Решение', status: 'pending', description: 'Уведомление о результате' },
];

export default function HomePage() {
  const [projects, setProjects] = useState<InvestmentProject[]>([]);
  const [kpis, setKpis] = useState<KPI[]>([]);
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [loading, setLoading] = useState(true);
  const [chatLoading, setChatLoading] = useState(false);

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

  // Обработка отправки сообщения в чат
  const handleSendMessage = useCallback(async (message: string) => {
    // Добавляем сообщение пользователя
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    
    setChatLoading(true);
    
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      
      if (res.ok) {
        const data = await res.json();
        
        // Преобразуем embeddedCards в InvestmentProject
        const embeddedCards: InvestmentProject[] = (data.embeddedCards || []).map((card: any, idx: number) => ({
          id: String(card.id || `card-${idx}`),
          name: card.company_name || card.territory_name || card.name || 'Неизвестно',
          industry: card.industry || 'Разное',
          location: card.location || '',
          imageUrl: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&q=80',
          investmentAmount: card.investment_amount || 0,
          irr: 15.5,
          npv: 100,
          paybackPeriod: 36,
          jobsCreated: card.jobs_created || 0,
          status: card.status === 'completed' ? 'implemented' : 'ongoing',
          progress: card.status === 'completed' ? 100 : 50,
          supportMeasures: [],
        }));
        
        const agentMessage: ChatMessage = {
          id: Date.now().toString(),
          role: 'agent',
          content: data.content,
          timestamp: data.timestamp || new Date().toISOString(),
          embeddedCards,
        };
        
        setMessages((prev) => [...prev, agentMessage]);
      }
    } catch (error) {
      console.error('Ошибка отправки сообщения:', error);
    } finally {
      setChatLoading(false);
    }
  }, []);

  return (
    <div className={styles.layout}>
      <Sidebar />

      <main className={styles.main}>
        <DashboardHeader kpis={kpis} />

        <div className={styles.content}>
          <div className={styles.topSection}>
            <div className={styles.chatArea}>
              <div className={styles.sectionHeader}>
                <h2>Диалог с агентом</h2>
              </div>
              <ChatInterface 
                messages={messages} 
                onSendMessage={handleSendMessage}
                isLoading={chatLoading}
              />
            </div>

            <div className={styles.sidePanel}>
              <ApplicationStatus steps={applicationSteps} />
            </div>
          </div>

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
      </main>
    </div>
  );
}
