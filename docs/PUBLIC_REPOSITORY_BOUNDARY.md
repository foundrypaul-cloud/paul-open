# PAUL Open Public Repository Boundary

PAUL Open is intentionally public, reproducible research. Public does not mean that every internal artifact is publishable.

This document defines the fail-closed boundary for repository content, Git branches and pull requests, GitHub Actions logs/artifacts, releases, and machine-readable website manifests.

## Core publication rule

The only supported flow from a private source into public research evidence is:

```text
PRIVATE SOURCE
    |
    v
EXPLICIT ALLOWLIST / SANITIZER
    |
    v
PUBLIC SAFE OUTPUT
```

Never publish a private source first and sanitize it later. Never upload an entire private Kaggle output directory, checkpoint directory, reviewer export, or sealed-evaluation directory to a public GitHub Actions artifact.

For Kaggle result trees, use `scripts/sanitize_kaggle_public_evidence.py`. It copies only explicit aggregate fields and cryptographic digests; it intentionally omits raw cases, prompts, responses, mappings, seeds, filesystem paths, credentials, and model weights.

Before any same-repository branch is pushed, run:

```bash
python scripts/check_public_boundary.py
python -m unittest tests.test_public_boundary
```

CI runs the same checks, but CI is not a privacy barrier for a public repository: content on a same-repository branch is already public before a CI job starts. Local/pre-push checks and repository rulesets are therefore required defense in depth.

## Classification

### Public research

May be committed after ordinary scientific/provenance review:

- source code and configuration;
- intentionally released SFT/DPO development data;
- DHE material explicitly designated development-exposed;
- aggregate evaluation results and intentionally released diagnostic evidence;
- research methodology, negative results, limitations, hashes, and reproducibility metadata;
- public respondent-facing participation links that have been separately approved for publication.

Public research remains subject to third-party license and attribution requirements.

### Never public / private

Must not be committed, printed to Actions logs, attached to PRs, uploaded as public artifacts, embedded in releases, or exposed through website manifests:

- API tokens, passwords, cookies, OAuth refresh tokens, service-account credentials, SSH/private keys, `.env`, or `kaggle.json`;
- reviewer identities, email/phone/contact information, panel registration exports, response spreadsheets, backup ledgers, or raw reviewer-response sheets;
- Google Form editor/admin links and unnecessary private Form/Sheet identifiers;
- private A/B mappings, source mappings, candidate mappings, or blinding seeds before legitimate unblinding;
- private Kaggle raw outputs, raw source-labelled evaluation outputs, temporary forensic bundles, or hidden mappings;
- unreleased adapters, checkpoints, model weights, or confidential artifact bundles;
- proprietary/trade-secret/patent-sensitive PAUL Foundry material not deliberately released under the public project terms.

### Sealed assurance

SHAE is a stricter class than ordinary private material. Before legitimate unsealing, never publish or use for training:

- sealed prompts;
- expected answers;
- hidden scoring keys or hidden grader logic that would invalidate assurance;
- sealed candidate/source mappings;
- sealed generated responses;
- derivatives that reveal sealed assurance content.

DHE may be development-exposed when the protocol explicitly says so. SHAE must remain sealed until the protocol authorizes release.

### Legally restricted third-party material

Training permission and redistribution permission are separate questions. Do not commit third-party dataset content merely because it may be downloaded or used for training. NC, research-only, benchmark-restricted, proprietary, or otherwise incompatible material must stay outside the public repository unless its actual terms permit redistribution here.

The project dataset registry records candidate status, but upstream terms remain controlling and should be rechecked at the point of use or release.

## Data directory policy

The current repository contains intentionally tracked, versioned research datasets under `data/`. They are public because they are already part of the research record, not because every path under `data/` is presumptively public.

`.gitignore` therefore keeps new/untracked material under `data/` private by default. Never use `git add -f` to bypass that boundary without a documented provenance/license/publication review.

Never-public namespaces include:

- `data/private/`
- `data/sealed/`
- `data/reviewer-private/`
- `data/kaggle-private/`

Frozen experiment datasets must not be edited to improve historical results. Corrections belong in a new version with explicit linkage to the affected historical experiment.

## GitHub Actions rules

All workflows must use least privilege. In particular:

- use `permissions: contents: read` unless a documented job requires more;
- do not use `pull_request_target` for untrusted code without a separately reviewed security design;
- do not enable shell xtrace around secrets;
- do not run broad `env`/`printenv` dumps;
- do not `cat` private mappings, raw result objects, or credential-bearing files into logs;
- download private Kaggle outputs only into runner-private temporary storage;
- publish only a separate allowlisted/sanitized staging directory or file;
- set explicit artifact retention;
- do not upload entire workspace, Kaggle output, checkpoint, adapter, or evaluation-result directories;
- treat stack traces and exception strings as private by default because they can contain private paths or data snippets.

The preferred failure artifact is a fixed public explanation plus an allowlisted machine-readable status (`status`, failure stage, exception type), not a raw traceback.

Third-party Actions should be pinned to immutable commits for security-sensitive boundary checks. Existing mutable-tag Actions should be migrated deliberately rather than through an unreviewed bulk rewrite.

## Human evaluation

Reviewer collection and research judgments are separate data planes.

Public evaluation artifacts may contain aggregate, blinded research evidence where the protocol permits it. They must not contain reviewer identity/contact data, private linkage information, raw response sheets, administrator URLs, hidden mappings, or blinding seeds.

Controlled unblinding must publish only the fields explicitly approved by the protocol after the blinded packet is closed. Do not expose a hidden mapping merely because a workflow needs it internally.

## Website/public manifests

Files under `public/` are publication interfaces. They must fail closed and may not carry administrator URLs, Form/Sheet IDs, reviewer identifiers/contact information, blinding seeds, private mappings, secrets, or sealed material.

The website is a presentation layer, not a private data transport. If internal state is needed to construct a public manifest, transform it through an explicit allowlist first.

## Licensing and intellectual property

The repository's Apache-2.0 license applies to PAUL Open-authored source material where stated. It does not relicense third-party datasets, models, benchmarks, trademarks, confidential information, or material a contributor had no right to submit.

Contributors must not submit proprietary/confidential material, credentials, private reviewer information, sealed assurance material, or third-party content they lack permission to redistribute.

Paul Foundry names, logos, and trademarks are not granted merely because source code is Apache-2.0 licensed.

## Incident response

If private material reaches a public branch, PR, log, artifact, release, or manifest:

1. stop further propagation without printing the material again;
2. remove the public run/artifact/release or close the exposure surface where possible;
3. rotate any credential that may have been exposed;
4. preserve necessary forensic evidence privately;
5. document the public research impact without republishing the sensitive payload;
6. do not rewrite legitimate scientific history merely to conceal a benign public fact, but consider history rewriting if an actual secret or legally restricted payload requires it.

Deletion from GitHub does not revoke copies already viewed, cloned, cached, or downloaded. Treat any prior public disclosure as potentially irreversible.
