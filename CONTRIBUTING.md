# Contributing to PAUL Open

Thank you for contributing to PAUL Open. This repository is both a software project and a public research record, so research-facing changes have stricter requirements than ordinary application code.

## Before you start

Read:

1. [`AGENTS.md`](AGENTS.md)
2. [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md)
3. the relevant experiment/protocol document for your change

If your contribution touches training data, evaluation, model claims, human evaluation, or reproducibility, also read the experiment journey and contamination notes in [`docs/EXPERIMENT_JOURNEY_E4B.md`](docs/EXPERIMENT_JOURNEY_E4B.md).

## Contribution principles

### Preserve evidence

Do not rewrite historical results because a newer interpretation is preferred. Add a new evidence layer, correction, or explicit superseding note.

### Keep evaluation isolated

Do not introduce training examples derived from held-out evaluation prompts, close paraphrases, templates, or concepts without the documented contamination review.

### Do not overclaim

A training run passing technical gates does not establish behavioral superiority. Automated aggregate scores are supporting evidence, not the final research conclusion.

### Protect the immutable Step 2 freeze

Do not modify or advance:

`research-freeze/step2-dpo-v2-20260909`

Frozen SHA:

`ac899e879f930f25b2081550bd8c5dd5c983df35`

### Protect secrets and private artifacts

Never commit credentials, tokens, private adapters/checkpoints, private Kaggle outputs, Google Form editor/admin links, response spreadsheets, reviewer contact information, or sealed evaluation material.

## Development setup

```bash
git clone https://github.com/foundrypaul-cloud/paul-open.git
cd paul-open
uv sync
uv run pytest
```

Useful checks may also include:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
```

Run the smallest relevant verification set for your change. Research/runtime changes should also exercise the corresponding repository verification workflow where available.

## Branch and pull-request workflow

Use a focused branch and open a pull request against `main`.

A good PR should state:

- what changed;
- why it changed;
- what evidence or bug report motivated it;
- which research claims are affected, if any;
- whether any dataset/evaluation boundary changed;
- what tests or verification ran;
- whether public website status or machine-readable manifests need synchronization.

The PR template contains additional checks.

## Research-data contributions

Any proposed training or evaluation data should document:

- origin and provenance;
- license/usage terms;
- transformation steps;
- intended split and role;
- contamination checks against protected evaluation material;
- hash or other stable identity for the accepted artifact;
- whether redistribution is permitted.

A dataset being publicly downloadable does not automatically make it suitable for training or redistribution.

## Evaluation contributions

New evaluation work should prefer task-specific metrics and evidence over one composite score.

For human evaluation:

- preserve blinding;
- never expose model/checkpoint identity to reviewers;
- use respondent-facing links only;
- keep optional comments optional unless the protocol is deliberately changed;
- do not expose DHE/SHAE material outside its intended boundary;
- preserve raw, normalized, and durability/recovery evidence.

## Public website contributions

The PAUL Open website is maintained outside this repository. Website work must follow [`docs/WEBSITE_INTEGRATION.md`](docs/WEBSITE_INTEGRATION.md).

Scientific facts displayed on the website should derive from the repository, preferably from:

- [`public/research-status.json`](public/research-status.json)
- [`public/human-evaluation.json`](public/human-evaluation.json)

Do not make the private website monorepo an independent research source of truth.

## Documentation contributions

Documentation is part of the reproducibility surface. When updating public-facing text:

- distinguish current status from future intent;
- link claims to versioned evidence;
- keep known limitations visible;
- avoid deleting negative results or contamination findings;
- use exact checkpoint/experiment language where relevant.

## Security

For security-sensitive reports, follow [`SECURITY.md`](SECURITY.md) rather than opening a public issue with exploitable details.

## Code of conduct

Participation is governed by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
