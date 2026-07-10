'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  MagnifyingGlass,
  FileText,
  Check,
  Circle,
  Download,
  ClipboardText,
  Envelope,
  Building,
  CalendarBlank,
} from '@phosphor-icons/react';
import { Skeleton } from '@/components/Skeleton/Skeleton';
import { SupportProgramBadge } from '@/components/SupportProgramBadge/SupportProgramBadge';
import type {
  DocumentTemplate,
  MeasureWithDocuments,
  DocumentStatus,
  SupportMeasure,
  SupportMeasureType,
} from '@/types';
import styles from './page.module.scss';

const docTypeLabels: Record<string, string> = {
  application: 'Заявление',
  business_plan: 'Бизнес-план',
  financial_report: 'Финансовая отчётность',
};

const statusConfig: Record<DocumentStatus, { icon: React.ReactNode; label: string; cls: string }> = {
  pending: { icon: <Circle weight="fill" size={14} />, label: 'Ожидает', cls: 'pending' },
  submitted: { icon: <Check weight="bold" size={14} />, label: 'Подан', cls: 'submitted' },
  approved: { icon: <Check weight="bold" size={14} />, label: 'Принят', cls: 'approved' },
};

export default function DocumentsPage() {
  const [templates, setTemplates] = useState<DocumentTemplate[]>([]);
  const [measures, setMeasures] = useState<MeasureWithDocuments[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [view, setView] = useState<'checklists' | 'templates'>('checklists');
  // Статусы документов: key = `${measureId}:${docName}`
  const [docStatuses, setDocStatuses] = useState<Record<string, DocumentStatus>>({});

  useEffect(() => {
    const loadData = async () => {
      try {
        const res = await fetch('/api/documents');
        if (res.ok) {
          const data = await res.json();

          // Маппинг snake_case → camelCase для шаблонов
          const mappedTemplates: DocumentTemplate[] = (data.templates || []).map(
            (t: Record<string, unknown>) => ({
              id: String(t.id),
              supportMeasureId: t.support_measure_id as number,
              supportMeasureName: (t.support_measure_name as string) ?? '',
              documentType: (t.document_type as string) ?? '',
              templateName: (t.template_name as string) ?? '',
              templateContent: (t.template_content as string) ?? '',
              requiredFields: (t.required_fields as string[]) ?? [],
            }),
          );

          // Маппинг snake_case → camelCase для мер поддержки
          const mappedMeasures: MeasureWithDocuments[] = (data.measures || []).map(
            (m: Record<string, unknown>) => ({
              id: m.id as number,
              name: (m.name as string) ?? '',
              measureType: (m.measure_type as SupportMeasureType) ?? 'financial',
              description: (m.description as string) ?? '',
              requiredDocuments: (m.required_documents as string[]) ?? [],
              responsibleAgency: (m.responsible_agency as string) ?? '',
              contactEmail: (m.contact_email as string) ?? '',
              maxAmount: (m.max_amount as number | null) ?? null,
              applicationDeadline: (m.application_deadline as string | null) ?? null,
            }),
          );

          setTemplates(mappedTemplates);
          setMeasures(mappedMeasures);
        }
      } catch (error) {
        console.error('Ошибка загрузки документов:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  // Циклическое переключение статуса документа: pending → submitted → approved → pending
  const toggleDocStatus = useCallback((measureId: number, docName: string) => {
    const key = `${measureId}:${docName}`;
    setDocStatuses((prev) => {
      const current = prev[key] || 'pending';
      const next: DocumentStatus =
        current === 'pending' ? 'submitted' : current === 'submitted' ? 'approved' : 'pending';
      return { ...prev, [key]: next };
    });
  }, []);

  // Фильтрация мер поддержки
  const filteredMeasures = measures.filter((m) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      m.name.toLowerCase().includes(q) ||
      (m.requiredDocuments ?? []).some((d) => d.toLowerCase().includes(q)) ||
      m.responsibleAgency.toLowerCase().includes(q)
    );
  });

  // Фильтрация шаблонов
  const filteredTemplates = templates.filter((t) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      t.templateName.toLowerCase().includes(q) ||
      t.documentType.toLowerCase().includes(q) ||
      t.supportMeasureName.toLowerCase().includes(q)
    );
  });

  // Подсчёт прогресса по мере поддержки
  const getProgress = (measure: MeasureWithDocuments) => {
    const docs = measure.requiredDocuments ?? [];
    if (!docs.length) return 0;
    const completed = docs.filter((doc) => {
      const key = `${measure.id}:${doc}`;
      return docStatuses[key] === 'submitted' || docStatuses[key] === 'approved';
    }).length;
    return Math.round((completed / docs.length) * 100);
  };

  return (
    <div className={styles.page}>
      {/* Header */}
      <div className={styles.header}>
        <div>
          <h1>Документы</h1>
          <p>Чек-листы обязательных документов и шаблоны для мер поддержки</p>
        </div>

        {/* View toggle */}
        <div className={styles.toggle}>
          <button
            className={`${styles.toggleBtn} ${view === 'checklists' ? styles.toggleActive : ''}`}
            onClick={() => setView('checklists')}
          >
            <ClipboardText weight="thin" size={18} />
            <span>Чек-листы</span>
          </button>
          <button
            className={`${styles.toggleBtn} ${view === 'templates' ? styles.toggleActive : ''}`}
            onClick={() => setView('templates')}
          >
            <FileText weight="thin" size={18} />
            <span>Шаблоны</span>
          </button>
        </div>
      </div>

      {/* Search */}
      <div className={styles.searchRow}>
        <div className={styles.searchBox}>
          <MagnifyingGlass weight="thin" size={18} />
          <input
            type="text"
            placeholder="Поиск по документам, мерам поддержки, ведомствам..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <span className={styles.resultCount}>
          {loading
            ? '...'
            : view === 'checklists'
              ? `${filteredMeasures.length} мер`
              : `${filteredTemplates.length} шаблонов`}
        </span>
      </div>

      {/* Content */}
      {view === 'checklists' ? (
        <div className={styles.grid}>
          {loading ? (
            Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className={styles.cardSkeleton}>
                <Skeleton height={28} width="70%" radius={8} />
                <div style={{ marginTop: 12, display: 'flex', flexDirection: 'column', gap: 8 }}>
                  <Skeleton height={14} width="90%" />
                  <Skeleton height={14} width="60%" />
                  <Skeleton height={40} radius={8} />
                </div>
              </div>
            ))
          ) : filteredMeasures.length === 0 ? (
            <div className={styles.empty}>
              <FileText weight="thin" size={48} />
              <p>Меры поддержки не найдены</p>
            </div>
          ) : (
            filteredMeasures.map((measure) => (
              <ChecklistCard
                key={measure.id}
                measure={measure}
                progress={getProgress(measure)}
                docStatuses={docStatuses}
                onToggle={toggleDocStatus}
              />
            ))
          )}
        </div>
      ) : (
        <div className={styles.grid}>
          {loading ? (
            Array.from({ length: 2 }).map((_, i) => (
              <div key={i} className={styles.cardSkeleton}>
                <Skeleton height={28} width="60%" radius={8} />
                <div style={{ marginTop: 12, display: 'flex', flexDirection: 'column', gap: 8 }}>
                  <Skeleton height={14} width="80%" />
                  <Skeleton height={36} radius={8} />
                </div>
              </div>
            ))
          ) : filteredTemplates.length === 0 ? (
            <div className={styles.empty}>
              <FileText weight="thin" size={48} />
              <p>Шаблоны не найдены</p>
            </div>
          ) : (
            filteredTemplates.map((template) => (
              <TemplateCard key={template.id} template={template} />
            ))
          )}
        </div>
      )}
    </div>
  );
}


// --- Checklist Card Component ---

interface ChecklistCardProps {
  measure: MeasureWithDocuments;
  progress: number;
  docStatuses: Record<string, DocumentStatus>;
  onToggle: (measureId: number, docName: string) => void;
}

function ChecklistCard({ measure, progress, docStatuses, onToggle }: ChecklistCardProps) {
  const supportMeasure: SupportMeasure = {
    id: String(measure.id),
    name: measure.name,
    type: measure.measureType as SupportMeasureType,
    maxAmount: measure.maxAmount ?? undefined,
  };

  return (
    <article className={styles.card}>
      {/* Top: badge + measure name */}
      <div className={styles.cardTop}>
        <SupportProgramBadge measure={supportMeasure} />
      </div>

      <h3 className={styles.cardTitle}>{measure.name}</h3>
      <p className={styles.cardDesc}>{measure.description}</p>

      {/* Progress */}
      <div className={styles.progressRow}>
        <div className={styles.progressBar}>
          <div className={styles.progressFill} style={{ width: `${progress}%` }} />
        </div>
        <span className={styles.progressValue}>{progress}%</span>
      </div>

      {/* Document checklist */}
      <div className={styles.docList}>
        {(measure.requiredDocuments ?? []).map((doc) => {
          const key = `${measure.id}:${doc}`;
          const status = docStatuses[key] || 'pending';
          const cfg = statusConfig[status];
          return (
            <button
              key={doc}
              className={`${styles.docItem} ${styles[`doc_${cfg.cls}`]}`}
              onClick={() => onToggle(measure.id, doc)}
            >
              <span className={styles.docCheck}>{cfg.icon}</span>
              <span className={styles.docName}>{doc}</span>
              <span className={styles.docStatusLabel}>{cfg.label}</span>
            </button>
          );
        })}
      </div>

      {/* Footer: agency + deadline */}
      <div className={styles.cardFooter}>
        <div className={styles.footerItem}>
          <Building weight="thin" size={14} />
          <span>{measure.responsibleAgency}</span>
        </div>
        {measure.applicationDeadline && (
          <div className={styles.footerItem}>
            <CalendarBlank weight="thin" size={14} />
            <span>До {measure.applicationDeadline}</span>
          </div>
        )}
        <div className={styles.footerItem}>
          <Envelope weight="thin" size={14} />
          <a href={`mailto:${measure.contactEmail}`}>{measure.contactEmail}</a>
        </div>
      </div>
    </article>
  );
}


// --- Template Card Component ---

function TemplateCard({ template }: { template: DocumentTemplate }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <article className={styles.card}>
      <div className={styles.cardTop}>
        <div className={styles.templateIcon}>
          <FileText weight="thin" size={20} />
        </div>
        <span className={styles.templateType}>
          {docTypeLabels[template.documentType] || template.documentType}
        </span>
      </div>

      <h3 className={styles.cardTitle}>{template.templateName}</h3>

      {template.supportMeasureName && (
        <p className={styles.templateMeasure}>{template.supportMeasureName}</p>
      )}

      {/* Required fields */}
      <div className={styles.fieldsRow}>
        <span className={styles.fieldsLabel}>Поля для заполнения:</span>
        <div className={styles.fieldsList}>
          {template.requiredFields.map((field) => (
            <span key={field} className={styles.fieldTag}>{field}</span>
          ))}
        </div>
      </div>

      {/* Preview (expandable) */}
      {expanded && (
        <pre className={styles.templatePreview}>{template.templateContent}</pre>
      )}

      <div className={styles.templateActions}>
        <button className={styles.previewBtn} onClick={() => setExpanded(!expanded)}>
          {expanded ? 'Скрыть' : 'Просмотр'}
        </button>
        <button className={styles.downloadBtn}>
          <Download weight="thin" size={16} />
          <span>Скачать</span>
        </button>
      </div>
    </article>
  );
}
