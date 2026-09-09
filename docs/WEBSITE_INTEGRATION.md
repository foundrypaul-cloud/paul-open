# PAUL Open Website Integration Contract

**Website:** https://open.paulfoundry.com/  
**Research authority:** https://github.com/foundrypaul-cloud/paul-open

The PAUL Open website lives outside this public repository. This document defines how that presentation layer should consume PAUL Open research without creating a second source of truth.

## Design principle

The website should be a **renderer and participation gateway** for research state owned by this repository.

Do not maintain independent copies of experiment conclusions, checkpoint rankings, human-evaluation status, or research claims in the private website monorepo when they can be sourced from versioned public files here.

## Canonical public feeds

Website code should consume these files from the default branch:

- `public/research-status.json` — current public research summary and canonical document links.
- `public/human-evaluation.json` — public human-evaluation availability and safe respondent entry point.

The website may fetch them at build time or through a controlled server-side cache.

Recommended raw endpoints:

```text
https://raw.githubusercontent.com/foundrypaul-cloud/paul-open/main/public/research-status.json
https://raw.githubusercontent.com/foundrypaul-cloud/paul-open/main/public/human-evaluation.json
```

If either manifest is unavailable, malformed, or incompatible with the website schema, fail closed: show a neutral "research status temporarily unavailable" or "evaluation currently unavailable" state rather than using stale hard-coded claims.

## Suggested website information architecture

A minimal public implementation can expose:

- `/open` or the existing PAUL Open landing page — identity, current research state, links to source.
- `/open/research` — current checkpoint/evaluation status rendered from `research-status.json`.
- `/open/experiments/e4b-dpo-v2` — narrative summary linking to `docs/EXPERIMENT_JOURNEY_E4B.md` and immutable evidence.
- `/open/evaluate` — human-evaluation participation page driven by `human-evaluation.json`.
- `/open/contribute` — link to `CONTRIBUTING.md`, issues, discussions, and repository.

The exact routing can follow the private monorepo's conventions; the source-of-truth contract matters more than path names.

## Human-evaluation website behavior

The website must not turn a sandbox Form into a production study merely by linking to it.

`public/human-evaluation.json` controls whether participation is available.

### Safe states

- `preparing` — show protocol explanation and that no evaluation is currently open.
- `accepting_responses` — show the public reviewer entry point.
- `closed` — show that the current round is closed; do not keep a stale submit button.
- `paused` — show a neutral paused state without exposing an admin reason unless explicitly public.

### Reviewer URL safety

When `state` is `accepting_responses`, the website must validate the configured respondent URL before rendering it:

- HTTPS only;
- expected provider/domain;
- respondent-facing URL only;
- for Google Forms, URL must be a `/viewform` respondent URL;
- reject any URL containing `/edit`;
- never infer an editor link from a respondent link.

Do not expose Form IDs, response-sheet URLs, backup ledgers, admin/editor links, or Apps Script project links unless a separate public-release decision explicitly approves them.

## Blinding requirements

A reviewer-facing page must not disclose:

- model name;
- checkpoint name;
- SFT/DPO identity;
- which side is expected to win;
- benchmark scores;
- hidden A/B mapping;
- internal comparison IDs;
- DHE/SHAE labels.

Public explanatory copy may say that the study compares AI responses for accuracy, clarity, usefulness, and naturalness.

## Interaction model

For the current Google Forms implementation, the lowest-risk website integration is:

1. website presents a short, accessible explanation;
2. website renders a CTA to the reviewed respondent URL, or embeds the respondent page if Google permits it cleanly;
3. the actual submission continues through Google Forms;
4. Apps Script retains responsibility for normalization, backup, checksums, and recovery;
5. repository protocol remains authoritative.

Do **not** reverse-engineer Google Forms POST requests from the browser and build an unofficial submission client. If PAUL Open later needs a fully custom interactive evaluation UI, treat that as a new reviewed collection backend with explicit idempotency, storage, privacy, recovery, and verifier requirements.

## Website interactivity that is safe now

The private website can add useful interactivity without changing research semantics:

- progress cards showing current research stage;
- expandable experiment timelines;
- filterable target-capability cards;
- links to immutable GitHub evidence;
- "what this result does / does not prove" panels;
- evaluation availability state;
- reviewer instructions and estimated time;
- contribution links and issue/discussion entry points.

Avoid animated or gamified elements that imply one checkpoint is the winner before the evidence supports that conclusion.

## Research-status rendering rules

The website should visually distinguish:

- `reference` checkpoints;
- `experimental` checkpoints;
- `technically_valid` status;
- `superiority_established` boolean;
- evaluation contamination warnings;
- human-evaluation acceptance state.

If `superiority_established` is false, do not use labels such as "best", "improved model", "winner", "new flagship", or similar promotional language.

## Caching and freshness

Recommended behavior:

- fetch public manifests at build time and optionally revalidate server-side;
- display `status_as_of` from the manifest;
- retain a source link to the GitHub file/commit;
- do not silently display indefinitely cached status after fetch failures;
- if stale beyond the website's chosen threshold, show the status date prominently.

## Search / SEO copy

Public description should stay factual and evidence-bounded. Suggested wording:

> PAUL Open is Paul Foundry's open research initiative for reproducible post-training and evaluation of open AI models across multilingual, educational, scientific, and human-centered tasks.

Avoid saying DPO V2 is the current best model. At the present evidence state, SFT remains the reference checkpoint.

## Private monorepo implementation rule

The private website repository may contain components, styles, caching logic, and integration code, but it should not become the only copy of PAUL Open research context.

Any Antigravity/IDE agent working in that monorepo should first read from this repository:

1. `AGENTS.md`
2. `docs/PROJECT_STATUS.md`
3. `public/research-status.json`
4. `public/human-evaluation.json`
5. this document

Then it should inspect the private monorepo and implement the UI against these contracts.

## Release checklist for website changes

Before publishing a PAUL Open website update:

- [ ] research status matches `public/research-status.json`;
- [ ] no stronger model claim appears in UI copy;
- [ ] all detailed claims link back to public evidence;
- [ ] no Google Form `/edit` URL or spreadsheet URL is present;
- [ ] reviewer blinding is preserved;
- [ ] evaluation CTA follows `public/human-evaluation.json` state;
- [ ] no DHE/SHAE material has been exposed accidentally;
- [ ] no private adapter/checkpoint/credential information appears in client bundles;
- [ ] website gracefully handles manifest fetch failure;
- [ ] repository remains the declared research source of truth.
