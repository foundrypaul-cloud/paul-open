# Security / Operational Incident — 2026-09-13

## Summary

On 2026-09-13, merging the public-repository boundary hardening change modified the DPO V3, V4 and V5 Kaggle production workflow files. Those workflows still had historical `push` triggers scoped to `main` and their own workflow/config/data paths. As a result, the hardening merge itself unintentionally launched new Kaggle bridge runs.

This incident is operational. It does **not** change the canonical PAUL Open research record, frozen experiment definitions, or promotion decisions.

## Affected GitHub Actions runs

- DPO V3: Actions run `34756197136`
- DPO V4: Actions run `34756197121`
- DPO V5: Actions run `34756197112`

The runs were launched by the merge commit that introduced the public-boundary hardening, rather than by a deliberate decision to conduct new canonical experiments.

## Disposition

### DPO V3

The Actions run was cancelled during preflight waiting. The production build and production launch steps were skipped. No V3 production run from this incident is part of the research record.

### DPO V4

The preflight completed and the production kernel launch occurred before the GitHub Actions run was cancelled. Any resulting V4 Kaggle output from this launch is classified as a **non-canonical operational side effect**. It must not be cited, promoted, or substituted for the versioned canonical experiment evidence.

The GitHub-side artifact path was already hardened to publish only sanitized allowlisted evidence.

### DPO V5

The duplicate V5 workflow completed before cancellation remediation was available. Any resulting V5 Kaggle output from this launch is likewise classified as a **non-canonical operational side effect** and must not be used as a new experiment result or promotion decision.

The workflow used the hardened public-boundary path, so its GitHub artifact publication was limited to sanitized aggregate evidence rather than the private Kaggle output tree.

## Public-boundary cleanup

A one-shot remediation workflow was executed as GitHub Actions run `34756373026`. Its verification step passed after it:

- requested cancellation of the unintended V3 and V4 bridge runs;
- deleted exposed legacy Actions artifact `10313363821`;
- deleted legacy Actions run `34744004957`;
- deleted stale working branch `h7-dhe-v5-binding-20260913`.

The temporary remediation workflow was removed after successful execution.

## Preventive change

DPO V3, V4 and V5 Kaggle production workflows, and the H6 failure-evidence workflow, are now `workflow_dispatch` only. Editing or merging those files can no longer launch expensive/research-significant Kaggle work automatically from a push to `main`.

Future canonical experiment execution must be an explicit action and must continue to obey the repository's public/private evidence boundary.

## Immutable evidence boundary

This incident does not modify or advance:

`research-freeze/step2-dpo-v2-20260909`

Frozen SHA:

`ac899e879f930f25b2081550bd8c5dd5c983df35`

No historical negative result, dataset, checkpoint, or canonical experiment evidence is rewritten by this incident record.
