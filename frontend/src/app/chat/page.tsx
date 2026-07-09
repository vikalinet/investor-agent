'use client';

import { useState, useEffect, useCallback } from 'react';
import { QuickActions } from '@/components/QuickActions/QuickActions';
import { ChatInterface } from '@/components/ChatInterface/ChatInterface';
import { Skeleton } from '@/components/Skeleton/Skeleton';
import type { ChatMessage, InvestmentProject } from '@/types';
import styles from './page.module.scss';

const initialMessages: ChatMessage[] = [
  {
    id: '1',
    role: 'agent',
    content: 'Здравствуйте! Я — ваш инвестиционный помощник по Свердловской области. Чем могу помочь?',
    timestamp: new Date().toISOString(),
  },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [chatLoading, setChatLoading] = useState(false);

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
          imageUrl: `https://placehold.co/600x400/0B1F3B/C8A96E?text=${encodeURIComponent(card.industry || 'Проект')}`,
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

  // Обработка клика по быстрому действию
  const handleQuickAction = useCallback((action: string) => {
    const prompts: Record<string, string> = {
      'Поиск проектов': 'Покажи лучшие инвестиционные проекты',
      'Просмотр мер': 'Какие меры поддержки доступны?',
      'Проверить': 'Хочу проверить документы на ошибки',
      'Написать': 'У меня вопрос к агенту',
    };
    
    const prompt = prompts[action] || action;
    handleSendMessage(prompt);
  }, [handleSendMessage]);

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1>Диалог с агентом</h1>
        <p>Задайте вопрос о инвестициях, мерах поддержки или проверке документов</p>
      </div>

      <div className={styles.layout}>
        <div className={styles.chatArea}>
          <ChatInterface 
            messages={messages} 
            onSendMessage={handleSendMessage}
            isLoading={chatLoading}
          />
        </div>

        <div className={styles.sidePanel}>
          <QuickActions onAction={handleQuickAction} />
        </div>
      </div>
    </div>
  );
}
