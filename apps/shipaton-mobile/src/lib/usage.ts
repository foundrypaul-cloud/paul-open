const KEY = 'paul-open-daily-usage-v1';
const FREE_LIMIT = 5;
const PRO_LIMIT = 40;

interface UsageState {
  date: string;
  count: number;
}

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

function readState(): UsageState {
  try {
    const parsed = JSON.parse(localStorage.getItem(KEY) || '{}') as Partial<UsageState>;
    if (parsed.date === today() && typeof parsed.count === 'number') {
      return { date: parsed.date, count: Math.max(0, parsed.count) };
    }
  } catch {
    // A corrupt local counter should not break the learning experience.
  }
  return { date: today(), count: 0 };
}

export function dailyLimit(isPro: boolean): number {
  return isPro ? PRO_LIMIT : FREE_LIMIT;
}

export function remainingToday(isPro: boolean): number {
  const state = readState();
  return Math.max(0, dailyLimit(isPro) - state.count);
}

export function recordUse(): number {
  const state = readState();
  const next = { ...state, count: state.count + 1 };
  localStorage.setItem(KEY, JSON.stringify(next));
  return next.count;
}
