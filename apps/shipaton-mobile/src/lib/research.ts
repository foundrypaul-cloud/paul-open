import type { ResearchSnapshot } from '../types';

const SOURCE =
  'https://raw.githubusercontent.com/foundrypaul-cloud/paul-open/main/public/research-status.json';

function requireRecord(value: unknown, label: string): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error(`Invalid research manifest: ${label}.`);
  }
  return value as Record<string, unknown>;
}

function requireString(value: unknown, label: string): string {
  if (typeof value !== 'string' || value.length === 0) {
    throw new Error(`Invalid research manifest: ${label}.`);
  }
  return value;
}

function requireBoolean(value: unknown, label: string): boolean {
  if (typeof value !== 'boolean') {
    throw new Error(`Invalid research manifest: ${label}.`);
  }
  return value;
}

function requireNumber(value: unknown, label: string): number {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    throw new Error(`Invalid research manifest: ${label}.`);
  }
  return value;
}

function optionalNumber(value: unknown): number | null {
  return typeof value === 'number' && Number.isFinite(value) ? value : null;
}

export async function loadResearchSnapshot(): Promise<ResearchSnapshot> {
  const response = await fetch(SOURCE, { cache: 'no-store' });
  if (!response.ok) throw new Error('Research status is temporarily unavailable.');

  const data = requireRecord(await response.json(), 'root');
  if (data.schema_version !== '1.0') {
    throw new Error('Research status uses an unsupported schema.');
  }

  const model = requireRecord(data.model_research, 'model_research');
  const dpoV6 = requireRecord(data.dpo_v6, 'dpo_v6');
  const human = requireRecord(data.human_evaluation, 'human_evaluation');
  const totals = requireRecord(human.h8_case_totals, 'human_evaluation.h8_case_totals');

  return {
    updatedAt: requireString(data.status_as_of, 'status_as_of'),
    referenceCheckpoint: requireString(model.reference_checkpoint, 'model_research.reference_checkpoint'),
    currentConclusion: requireString(model.current_conclusion, 'model_research.current_conclusion'),
    superiorityEstablished: requireBoolean(
      model.superiority_established,
      'model_research.superiority_established',
    ),
    diagnosticCases: requireNumber(dpoV6.diagnostic_cases, 'dpo_v6.diagnostic_cases'),
    diagnosticV6MeanRubric: requireNumber(
      dpoV6.diagnostic_v6_mean_rubric,
      'dpo_v6.diagnostic_v6_mean_rubric',
    ),
    diagnosticSftMeanRubric: requireNumber(
      dpoV6.diagnostic_sft_mean_rubric,
      'dpo_v6.diagnostic_sft_mean_rubric',
    ),
    h8CandidatePreferred: optionalNumber(totals.candidate_preferred),
    h8ReferencePreferred: optionalNumber(totals.reference_preferred),
    h8AboutEqual: optionalNumber(totals.about_equal),
    h8NeitherGood: optionalNumber(totals.neither_good),
    sourceUrl: 'https://github.com/foundrypaul-cloud/paul-open',
  };
}
