# PAUL Open — Human Evaluation Reviewer-Link Policy

## Purpose

Human reviewers must interact only with the respondent-facing Google Form. They must never receive the Google Forms editor URL or any collaborator access.

This distinction is part of the research instrument, not merely a sharing preference: accidental edits to question text, answer options, ordering, or required-state can change the measurement instrument and invalidate comparability across reviewers.

## Distribution rule

For every human-evaluation form:

- **Reviewer link:** the published respondent URL, typically ending in `/viewform`. This is the only URL that may be distributed to reviewers.
- **Admin editor link:** the private Google Forms editor URL ending in `/edit`. This is restricted to the research administrator and must never be shared as a reviewer link.
- Do not use the editor screen itself as the reviewer UX test. For H2/H3 acceptance, open the direct respondent URL so the test matches what a real reviewer receives.

## Reviewer permissions

The evaluation instrument must satisfy all of the following:

- reviewers cannot edit form questions or answer options;
- reviewers cannot edit their submitted response;
- reviewers do not see model/checkpoint identities, benchmark IDs, or automated scores;
- reviewers may leave one optional free-text comment at the end of the form;
- required pairwise-choice questions retain the frozen five response options;
- reviewer email/name are not collected in the evaluation form.

A separate opt-in reviewer-panel registration form may collect contact information, but that registry remains physically separate from model-evaluation judgments.

## Research-integrity response to accidental edits

If an administrator accidentally edits a live evaluation form:

1. stop distributing the form;
2. restore the form from the frozen packet specification before collecting additional judgments;
3. inspect whether any responses were submitted while the altered version was live;
4. if yes, mark those responses as instrument-drift affected and exclude them from clean held-out analysis unless equivalence can be demonstrated;
5. do not silently mix judgments collected under materially different form versions.

For H2/H3 sandbox tests, synthetic responses may simply be discarded and the sandbox rerun after restoring the instrument.

## Operational convention

Any project control sheet or runbook should display the respondent URL prominently as **REVIEWER LINK — SHARE THIS ONLY**, while the editor URL should be explicitly labeled **ADMIN ONLY — DO NOT SHARE**.

This policy applies to H2 sandbox, H3 UX pilot, Development Human Evaluation (DHE), and Sealed Human Assurance Evaluation (SHAE).
