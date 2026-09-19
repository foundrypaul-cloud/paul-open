import type { AssistRequest, AssistResponse } from '../types';

const endpoint = (import.meta.env.VITE_PAUL_AI_ENDPOINT as string | undefined)?.replace(/\/$/, '');

export async function askCompanion(payload: AssistRequest): Promise<AssistResponse> {
  if (!endpoint) {
    throw new Error(
      'AI service is not configured on this build. Set VITE_PAUL_AI_ENDPOINT to the deployed PAUL Open Companion API.',
    );
  }

  const response = await fetch(`${endpoint}/v1/assist`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = (await response.json().catch(() => null)) as
    | { answer?: string; providerLabel?: string; requestId?: string; note?: string; error?: string }
    | null;

  if (!response.ok || !data?.answer) {
    throw new Error(data?.error || `AI service request failed (${response.status}).`);
  }

  return {
    answer: data.answer,
    providerLabel: data.providerLabel || 'Hosted AI',
    requestId: data.requestId || 'unknown',
    note: data.note || 'AI can make mistakes. Verify important details.',
  };
}
