'use client';

import { useState, useRef, useEffect } from 'react';
import { PaperPlaneRight, Sparkle } from '@phosphor-icons/react';
import type { ChatMessage, InvestmentProject } from '@/types';
import { InvestmentCard } from '../InvestmentCard/InvestmentCard';
import styles from './ChatInterface.module.scss';

interface ChatInterfaceProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
}

export function ChatInterface({ messages, onSendMessage, isLoading = false }: ChatInterfaceProps) {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    onSendMessage(inputValue.trim());
    setInputValue('');
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('ru-RU', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className={styles.container}>
      <div className={styles.messages}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.message} ${styles[message.role]}`}
          >
            {message.role === 'agent' && (
              <div className={styles.agentAvatar}>
                <Sparkle weight="fill" size={16} />
              </div>
            )}

            <div className={styles.messageContent}>
              <p className={styles.messageText}>{message.content}</p>

              {message.embeddedCards && message.embeddedCards.length > 0 && (
                <div className={styles.embeddedCards}>
                  {message.embeddedCards.map((project) => (
                    <InvestmentCard key={project.id} project={project} compact />
                  ))}
                </div>
              )}

              <span className={styles.messageTime}>
                {formatTime(message.timestamp)}
              </span>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className={`${styles.message} ${styles.agent} ${styles.loading}`}>
            <div className={styles.agentAvatar}>
              <Sparkle weight="fill" size={16} />
            </div>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span />
                <span />
                <span />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className={styles.inputForm} onSubmit={handleSubmit}>
        <input
          ref={inputRef}
          type="text"
          className={styles.input}
          placeholder="Введите ваш вопрос..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          disabled={isLoading}
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={!inputValue.trim() || isLoading}
          aria-label="Отправить сообщение"
        >
          <PaperPlaneRight weight="thin" size={18} />
        </button>
      </form>
    </div>
  );
}
