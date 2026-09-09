# PAUL Open — Agent / IDE Operating Context

This file is the first context document for coding agents, IDE agents, and automation working on PAUL Open or on external applications that present PAUL Open research.

## 1. Authority and source of truth

The public repository `foundrypaul-cloud/paul-open` is the canonical research source of truth.

Authority order:

1. Immutable experiment evidence: frozen commits/branches, manifests, dataset hashes, configs, and result artifacts.
2. Versioned research documentation in this repository.
3. `docs/PROJECT_STATUS.md` and machine-readable files under `public/` for the current public summary.
4. External presentation layers such as `https://open.paulfoundry.com/`.

A website, private monorepo, slide deck, social post, or agent-generated summary must never override repository evidence.

## 2. Current research state

Read [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) before making research-facing changes.

As of 2026-09-10:

- base research model: `google/gemma-4-E4B-it`;
- historical SFT adapter remains the reference checkpoint;
- DPO V2 Corrective is technically valid but is **not established as behaviorally superior**;
- the existing 50-case SFT-vs-DPO V2 comparison is diagnostic and contaminated for DPO V2;
- Step 2 immutable freeze: `research-freeze/step2-dpo-v2-20260909` at `ac899e879f930f25b2081550bd8c5dd5c983df35`;
- human-evaluation collection/normalization/backup and verifier paths have been exercised with genuine sandbox submissions;
- formal H2 completion still requires the live Apps Script runtime to be synchronized with the repository patch and the remaining recovery/closure acceptance checks to pass.

Never convert any of the above into a stronger claim without new repository evidence.

## 3. Immutable research boundary

Do **not** modify or advance:

`research-freeze/step2-dpo-v2-20260909`

The exact frozen SHA is:

`ac899e879f930f25b2081550bd8c5dd5c983df35`

If current `main` differs from the freeze, that is expected. Documentation, human-evaluation infrastructure, CI, and other later work may continue on `main`; the Step 2 experiment freeze remains immutable.

## 4. Research-claim rules

Do not claim:

- that DPO V2 is better than SFT;
- that a higher aggregate benchmark number proves model superiority;
- that the current 50-case comparison is clean held-out evidence;
- that an automated metric proves human usefulness;
- that H2 human evaluation is formally complete until all acceptance items are evidenced.

Use the language and evidence boundaries in:

- `docs/EXPERIMENT_JOURNEY_E4B.md`
- `docs/E4B_DPO_V2_CORRECTIVE.md`
- `docs/HUMAN_EVALUATION_PROTOCOL.md`
- `docs/PROJECT_STATUS.md`

## 5. Evaluation and contamination rules

Evaluation material is a protected research boundary.

- Do not reuse held-out evaluation prompts, close paraphrases, templates, or concepts as training examples without the documented contamination audit.
- DHE material is development-exposed and must be labeled accordingly.
- SHAE material is sealed final-assurance material and must not be exposed during model development.
- Do not publish hidden A/B model mappings before a blinded human-evaluation packet is closed and analyzed.
- Do not silently repair, paraphrase, or "improve" frozen evaluation stimuli.

## 6. Human-evaluation rules

The repository owns the protocol and instrument specification. A Google Form or website is only a collection/presentation surface.

Never expose publicly:

- Google Form `/edit` URLs;
- response spreadsheets or backup ledgers;
- hidden model/checkpoint identity;
- hidden A/B variant mappings;
- internal reviewer linkage data;
- DHE/SHAE material not approved for release.

Reviewer-facing links must be respondent links (`/viewform`) only.

Optional reviewer comments must remain optional unless the protocol is deliberately revised through a reviewed repository change.

For website integration, follow [`docs/WEBSITE_INTEGRATION.md`](docs/WEBSITE_INTEGRATION.md) and the state in [`public/human-evaluation.json`](public/human-evaluation.json).

## 7. Public website contract

`https://open.paulfoundry.com/` is not the research authority. It should consume or mirror public repository state.

Preferred implementation:

- build website research status from `public/research-status.json`;
- build evaluation CTA/state from `public/human-evaluation.json`;
- link detailed claims back to versioned repository documents;
- show a safe degraded/closed state if the manifest is unavailable or invalid;
- never hard-code scientific claims in the private website monorepo when they can be sourced from this repository.

A private website commit is not experimental evidence.

## 8. Secrets and private artifacts

Never commit, print, log, or expose:

- API tokens or credentials;
- private Kaggle outputs;
- private adapters/checkpoints unless a deliberate release review approves them;
- Google admin/editor URLs;
- private reviewer contact information;
- secrets from `.env` or CI secret stores.

Use `.env.example` only for variable names and safe examples.

## 9. Normal development workflow

For non-trivial changes:

1. inspect current `main` and relevant evidence first;
2. create a focused branch;
3. make the smallest change consistent with the research boundary;
4. run the relevant tests/verification workflows;
5. open a PR with explicit research-impact notes;
6. merge only after checks pass and the diff does not alter a frozen experiment unintentionally.

Documentation-only changes must still avoid rewriting historical evidence.

## 10. Website / external-agent handoff checklist

An external IDE agent updating the PAUL Open website should first read, in this order:

1. `AGENTS.md`
2. `docs/PROJECT_STATUS.md`
3. `public/research-status.json`
4. `public/human-evaluation.json`
5. `docs/WEBSITE_INTEGRATION.md`
6. `README.md`

Then inspect the private website codebase and implement only presentation/integration changes. Do not duplicate or mutate research source data inside the private monorepo.
