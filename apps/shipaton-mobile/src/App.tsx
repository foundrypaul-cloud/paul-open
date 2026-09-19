import { useEffect, useMemo, useState } from 'react';
import type {
  AppLanguage,
  AppTab,
  AssistResponse,
  ResearchSnapshot,
  StudyMode,
  SubscriptionState,
} from './types';
import { askCompanion } from './lib/api';
import { dailyLimit, recordUse, remainingToday } from './lib/usage';
import { loadResearchSnapshot } from './lib/research';
import {
  openCustomerCenter,
  presentUpgrade,
  refreshSubscription,
  restorePurchases,
} from './lib/revenuecat';

const languages: AppLanguage[] = ['English', 'Hindi', 'Bengali'];

const quickPrompts: Record<AppLanguage, string[]> = {
  English: [
    'Why does pressure rise when a sealed syringe is compressed?',
    'Why do induction cooktops heat some pans but not glass?',
    'Help me test whether a correlation is actually causal.',
  ],
  Hindi: [
    'इंडक्शन चूल्हा धातु के बर्तन को कैसे गरम करता है?',
    'दबाव और आयतन का संबंध आसान भाषा में समझाइए।',
    'मुझे ऊर्जा संरक्षण पर एक छोटा अभ्यास कराइए।',
  ],
  Bengali: [
    'গরম রাস্তায় মরীচিকা কেন দেখা যায়?',
    'চাপ ও আয়তনের সম্পর্ক সহজভাবে বোঝান।',
    'শক্তি সংরক্ষণ নিয়ে আমাকে প্রশ্ন করে শেখান।',
  ],
};

const modeCopy: Record<StudyMode, { title: string; detail: string }> = {
  explain: {
    title: 'Explain',
    detail: 'Clear concepts, assumptions and physical intuition.',
  },
  tutor: {
    title: 'Tutor me',
    detail: 'A diagnostic question, then guidance that checks understanding.',
  },
  research: {
    title: 'Research lens',
    detail: 'Evidence, confounders, uncertainty and a practical validation plan.',
  },
};

const initialSubscription: SubscriptionState = {
  available: false,
  configured: false,
  isPro: false,
  platform: 'web',
};

function App() {
  const [tab, setTab] = useState<AppTab>('learn');
  const [language, setLanguage] = useState<AppLanguage>('English');
  const [mode, setMode] = useState<StudyMode>('explain');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<AssistResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState('');
  const [subscription, setSubscription] = useState<SubscriptionState>(initialSubscription);
  const [usageTick, setUsageTick] = useState(0);
  const [research, setResearch] = useState<ResearchSnapshot | null>(null);
  const [researchError, setResearchError] = useState('');

  const remaining = useMemo(
    () => remainingToday(subscription.isPro),
    [subscription.isPro, usageTick],
  );

  useEffect(() => {
    refreshSubscription()
      .then(setSubscription)
      .catch((error) =>
        setSubscription((current) => ({
          ...current,
          message: error instanceof Error ? error.message : 'Purchase status unavailable.',
        })),
      );

    loadResearchSnapshot()
      .then(setResearch)
      .catch((error) =>
        setResearchError(error instanceof Error ? error.message : 'Research status unavailable.'),
      );
  }, []);

  async function submitQuestion() {
    const clean = question.trim();
    if (clean.length < 3 || busy) return;

    if (!subscription.isPro && remaining <= 0) {
      setNotice('Your free daily learning sessions are used. Upgrade to continue today.');
      setTab('pro');
      return;
    }

    if (mode === 'research' && !subscription.isPro) {
      setNotice('Research lens is a Pro feature.');
      setTab('pro');
      return;
    }

    setBusy(true);
    setNotice('');
    setAnswer(null);
    try {
      const result = await askCompanion({ question: clean, language, mode });
      recordUse();
      setUsageTick((value) => value + 1);
      setAnswer(result);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : 'Could not reach the learning service.');
    } finally {
      setBusy(false);
    }
  }

  async function upgrade() {
    setBusy(true);
    setNotice('');
    try {
      const next = await presentUpgrade();
      setSubscription(next);
      setNotice(
        next.isPro
          ? 'PAUL Open Pro is active.'
          : next.message || 'The secure store paywall was closed without changing access.',
      );
    } catch (error) {
      setNotice(error instanceof Error ? error.message : 'Could not open the purchase flow.');
    } finally {
      setBusy(false);
    }
  }

  async function restore() {
    setBusy(true);
    setNotice('');
    try {
      const next = await restorePurchases();
      setSubscription(next);
      setNotice(next.isPro ? 'Purchase restored. Pro is active.' : 'No active Pro entitlement found.');
    } catch (error) {
      setNotice(error instanceof Error ? error.message : 'Restore failed.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand" onClick={() => setTab('learn')} aria-label="PAUL Open home">
          <span className="brand-mark" aria-hidden="true">P</span>
          <span>
            <strong>PAUL Open</strong>
            <small>Understand · Question · Verify</small>
          </span>
        </button>
        <button className="status-pill" onClick={() => setTab('pro')}>
          <span className={subscription.isPro ? 'status-dot pro' : 'status-dot'} />
          {subscription.isPro ? 'Pro' : `${remaining}/${dailyLimit(false)} free`}
        </button>
      </header>

      <main>
        {tab === 'learn' && (
          <section className="screen learn-screen">
            <div className="hero">
              <div className="eyebrow">MULTILINGUAL SCIENCE COMPANION</div>
              <h1>Learn the idea, not just the answer.</h1>
              <p>
                Ask a science question in English, Hindi or Bengali. Choose a direct explanation,
                guided tutoring, or an evidence-first research lens.
              </p>
            </div>

            <div className="language-row" aria-label="Response language">
              {languages.map((item) => (
                <button
                  key={item}
                  className={language === item ? 'chip active' : 'chip'}
                  onClick={() => setLanguage(item)}
                >
                  {item}
                </button>
              ))}
            </div>

            <div className="mode-grid">
              {(Object.keys(modeCopy) as StudyMode[]).map((item) => {
                const locked = item === 'research' && !subscription.isPro;
                return (
                  <button
                    key={item}
                    className={mode === item ? 'mode-card selected' : 'mode-card'}
                    onClick={() => {
                      if (locked) {
                        setNotice('Research lens is included with Pro.');
                        setTab('pro');
                        return;
                      }
                      setMode(item);
                    }}
                  >
                    <span className="mode-title">
                      {modeCopy[item].title}
                      {locked && <em>PRO</em>}
                    </span>
                    <span>{modeCopy[item].detail}</span>
                  </button>
                );
              })}
            </div>

            <div className="composer">
              <label htmlFor="question">What are you trying to understand?</label>
              <textarea
                id="question"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder={
                  language === 'Hindi'
                    ? 'अपना सवाल यहाँ लिखें…'
                    : language === 'Bengali'
                      ? 'আপনার প্রশ্ন এখানে লিখুন…'
                      : 'Ask a concept, misconception, experiment, or research question…'
                }
                maxLength={2000}
                rows={5}
              />
              <div className="composer-footer">
                <span>{question.length}/2000</span>
                <button
                  className="primary"
                  disabled={busy || question.trim().length < 3}
                  onClick={submitQuestion}
                >
                  {busy ? 'Thinking…' : modeCopy[mode].title}
                </button>
              </div>
            </div>

            <div className="quick-block">
              <span className="section-label">Try a starting point</span>
              <div className="quick-list">
                {quickPrompts[language].map((prompt) => (
                  <button key={prompt} onClick={() => setQuestion(prompt)}>
                    {prompt}
                  </button>
                ))}
              </div>
            </div>

            {notice && <div className="notice" role="status">{notice}</div>}

            {answer && (
              <article className="answer-card">
                <div className="answer-head">
                  <span>{modeCopy[mode].title}</span>
                  <small>{answer.providerLabel}</small>
                </div>
                <div className="answer-text">{answer.answer}</div>
                <footer>
                  <span>{answer.note}</span>
                  <code>#{answer.requestId.slice(0, 8)}</code>
                </footer>
              </article>
            )}

            <div className="trust-strip">
              <strong>Evidence before hype.</strong>
              <span>
                The app does not pretend PAUL Open experimental checkpoints are production models.
                Research claims are loaded from the versioned public repository.
              </span>
              <button onClick={() => setTab('research')}>See research status</button>
            </div>
          </section>
        )}

        {tab === 'research' && (
          <section className="screen research-screen">
            <div className="eyebrow">OPEN RESEARCH</div>
            <h1>See what the evidence actually says.</h1>
            <p className="lede">
              PAUL Open separates technical training validity, automated diagnostics and human
              preference evidence. The production companion currently uses a hosted Gemini service;
              it does not serve the experimental DPO V6 checkpoint.
            </p>

            {research ? (
              <>
                <div className="research-summary">
                  <span>Reference checkpoint</span>
                  <strong>{research.referenceCheckpoint}</strong>
                  <small>Repository status · {research.updatedAt}</small>
                </div>

                <div className="evidence-grid">
                  <div>
                    <span>H8 · SFT preferred</span>
                    <strong>{research.h8ReferencePreferred ?? '—'}</strong>
                  </div>
                  <div>
                    <span>H8 · V6 preferred</span>
                    <strong>{research.h8CandidatePreferred ?? '—'}</strong>
                  </div>
                  <div>
                    <span>About equal</span>
                    <strong>{research.h8AboutEqual ?? '—'}</strong>
                  </div>
                  <div>
                    <span>Neither good</span>
                    <strong>{research.h8NeitherGood ?? '—'}</strong>
                  </div>
                </div>

                <article className="research-card">
                  <h2>Current conclusion</h2>
                  <p>{research.currentConclusion}</p>
                  <p className="boundary">
                    Broad superiority established: <strong>{research.superiorityEstablished ? 'Yes' : 'No'}</strong>
                  </p>
                </article>

                <a className="external-link" href={research.sourceUrl} target="_blank" rel="noreferrer">
                  Open the versioned research repository ↗
                </a>
              </>
            ) : (
              <div className="notice">{researchError || 'Loading the current repository status…'}</div>
            )}

            <div className="principles">
              <h2>What this changes in the product</h2>
              <p>
                We do not promote a model because one aggregate score improved. The companion is
                designed around explanation quality, uncertainty, multilingual access and explicit
                validation — the same failure modes the research evaluates.
              </p>
            </div>
          </section>
        )}

        {tab === 'pro' && (
          <section className="screen pro-screen">
            <div className="eyebrow">PAUL OPEN PRO</div>
            <h1>More room to learn deeply.</h1>
            <p className="lede">
              Keep the free tier genuinely useful. Pro expands daily access and unlocks the
              evidence-first Research lens. Localized pricing is shown by the app store.
            </p>

            <div className="plan-grid">
              <div className="plan-card">
                <span>Free</span>
                <strong>5 sessions/day</strong>
                <ul>
                  <li>Explain mode</li>
                  <li>Tutor mode</li>
                  <li>English, Hindi and Bengali</li>
                  <li>Live research-status transparency</li>
                </ul>
              </div>
              <div className="plan-card featured">
                <span>Pro</span>
                <strong>40 sessions/day</strong>
                <ul>
                  <li>Everything in Free</li>
                  <li>Research lens</li>
                  <li>Higher daily learning limit</li>
                  <li>Store-managed subscription controls</li>
                </ul>
              </div>
            </div>

            <button className="primary wide" disabled={busy || subscription.isPro} onClick={upgrade}>
              {subscription.isPro ? 'Pro is active' : 'View secure store offer'}
            </button>

            <div className="secondary-actions">
              <button disabled={busy} onClick={restore}>Restore purchases</button>
              {subscription.isPro && (
                <button
                  disabled={busy}
                  onClick={() =>
                    openCustomerCenter().catch((error) =>
                      setNotice(error instanceof Error ? error.message : 'Customer Center unavailable.'),
                    )
                  }
                >
                  Manage subscription
                </button>
              )}
            </div>

            {subscription.message && <div className="notice">{subscription.message}</div>}
            {notice && <div className="notice">{notice}</div>}

            <div className="purchase-note">
              Purchases are handled by the native app store through RevenueCat. The web preview
              intentionally cannot start a purchase.
            </div>
          </section>
        )}
      </main>

      <nav className="bottom-nav" aria-label="Primary">
        <button className={tab === 'learn' ? 'active' : ''} onClick={() => setTab('learn')}>
          <span aria-hidden="true">✦</span> Learn
        </button>
        <button className={tab === 'research' ? 'active' : ''} onClick={() => setTab('research')}>
          <span aria-hidden="true">◫</span> Research
        </button>
        <button className={tab === 'pro' ? 'active' : ''} onClick={() => setTab('pro')}>
          <span aria-hidden="true">◇</span> Pro
        </button>
      </nav>
    </div>
  );
}

export default App;
