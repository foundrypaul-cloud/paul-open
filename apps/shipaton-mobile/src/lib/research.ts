import type { ResearchSnapshot } from '../types';

const SOURCE =
  'https://raw.githubusercontent.com/foundrypaul-cloud/paul-open/main/public/research-status.json';

export async function loadResearchSnapshot(): Promise<ResearchSnapshot> {
  const response = await fetch(SOURCE, { cache: 'no-store' });
  if (!response.ok) throw new Error('Research status is temporarily unavailable.');

  const data = (await response.json()) as any;
  const totals = data?.human_evaluation?.h8_case_totals || data?.dpo_v6?.h8_case_totals || {};

  return {
    updatedAt: String(data?.status_as_of || 'unknown'),
    referenceCheckpoint: String(data?.model_research?.reference_checkpoint || 'See repository'),
    currentConclusion: String(
      data?.model_research?.current_conclusion ||
        'Read the versioned PAUL Open repository for the current research conclusion.',
    ),
    superiorityEstablished: Boolean(data?.model_research?.superiority_established),
    h8CandidatePreferred:
      typeof totals?.candidate_preferred === 'number' ? totals.candidate_preferred : null,
    h8ReferencePreferred:
      typeof totals?.reference_preferred === 'number' ? totals.reference_preferred : null,
    h8AboutEqual: typeof totals?.about_equal === 'number' ? totals.about_equal : null,
    h8NeitherGood: typeof totals?.neither_good === 'number' ? totals.neither_good : null,
    sourceUrl: 'https://github.com/foundrypaul-cloud/paul-open',
  };
}
