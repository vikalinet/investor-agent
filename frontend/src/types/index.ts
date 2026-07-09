// ============================================================================
//  Типы данных — Investor Assistant
// ============================================================================

export type SupportMeasureType = 'financial' | 'tax' | 'infrastructure' | 'advisory';

export type ProjectStatus = 'idea' | 'planning' | 'approved' | 'implemented' | 'ongoing';

export type ApplicationStage = 'draft' | 'submitted' | 'review' | 'approved' | 'rejected';

export interface KPI {
  id: string;
  label: string;
  value: string;
  unit?: string;
  trend?: {
    direction: 'up' | 'down' | 'stable';
    value: string;
  };
}

export interface SupportMeasure {
  id: string;
  name: string;
  type: SupportMeasureType;
  maxAmount?: number;
}

export interface InvestmentProject {
  id: string;
  name: string;
  industry: string;
  location: string;
  imageUrl: string;
  investmentAmount: number; // млн руб.
  irr: number; // Internal Rate of Return, %
  npv: number; // Net Present Value, млн руб.
  paybackPeriod: number; // месяцев
  jobsCreated: number;
  status: ProjectStatus;
  progress: number; // 0-100
  supportMeasures: SupportMeasure[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
  embeddedCards?: InvestmentProject[];
}

export interface ApplicationStep {
  id: string;
  title: string;
  status: 'completed' | 'current' | 'pending';
  description?: string;
  date?: string;
}

export interface SidebarHistoryItem {
  id: string;
  title: string;
  date: string;
  preview: string;
}
