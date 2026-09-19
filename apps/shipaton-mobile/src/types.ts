export type AppLanguage = 'English' | 'Hindi' | 'Bengali';
export type StudyMode = 'explain' | 'tutor' | 'research';
export type AppTab = 'learn' | 'research' | 'pro';

export interface AssistRequest {
  question: string;
  language: AppLanguage;
  mode: StudyMode;
}

export interface AssistResponse {
  answer: string;
  providerLabel: string;
  requestId: string;
  note: string;
}

export interface ResearchSnapshot {
  updatedAt: string;
  referenceCheckpoint: string;
  currentConclusion: string;
  superiorityEstablished: boolean;
  diagnosticCases: number;
  diagnosticV6MeanRubric: number;
  diagnosticSftMeanRubric: number;
  h8CandidatePreferred: number | null;
  h8ReferencePreferred: number | null;
  h8AboutEqual: number | null;
  h8NeitherGood: number | null;
  sourceUrl: string;
}

export interface SubscriptionState {
  available: boolean;
  configured: boolean;
  isPro: boolean;
  platform: string;
  message?: string;
}
