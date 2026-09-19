# PAUL Open — Current Research Status

**Status date:** 2026-09-20  
**Public research repository:** `foundrypaul-cloud/paul-open`

## Current position

PAUL Open has completed technically valid development training through DPO V6 Synthetic Corrective. The historical SFT adapter remains the reference checkpoint because no DPO checkpoint has yet passed the full clean held-out, preservation, blinded-human, and sealed-assurance evidence chain required for promotion.

DPO V5 passed its data and production-validity gates but produced mixed automated evidence. H7 matched generation completed, after which the planned multi-reviewer H7 collection was intentionally discontinued without a human preference result.

DPO V6 was then authored as a separate 24-record synthetic corrective development iteration without using H7 blinded responses, hidden mappings, evaluator output, or SHAE material. Its canonical production run completed successfully on 2026-09-19. All 516 intended trainable tensors changed and the matched 50-case diagnostic produced a positive aggregate heuristic signal relative to SFT. That result advances V6 to fresh development evaluation; it does not establish superiority.

A 12-case fresh H8 Development Human Evaluation prompt set was precommitted for SFT-vs-V6 comparison before H8 response generation. Canonical matched generation completed successfully on 2026-09-19. The blinded reviewer batch contains 12 eligible cases, 0 identical pairs were skipped, canonical benchmark leakage is clean 12/12, and development-separation similarity remains below the frozen `<0.35` threshold. Private blinded collection closed at 36 case-level judgments and controlled unblinding completed successfully. H8 preferred SFT on 6 cases and V6 on 3; 2 cases were judged poor on both sides and 1 was about equal. V6 therefore fails the precommitted promotion gate. Reviewer identity-level independence is not technically verifiable from the instrument, so that limitation remains attached to H8. SHAE remains sealed.

## Experiment lineage

- **DPO V2 / H4:** technically valid; H4 mixed; no promotion.
- **DPO V3 / H5:** technically valid; H5 ended 9–9 in judgments and failed the pre-specified STEM/Hindi preservation objective; no promotion.
- **DPO V4 / H6:** H6 collected 18 judgments. SFT was preferred on five cases (15 judgments); all three Educator judgments selected neither response; no promotion.
- **DPO V5 / P10–P12:** 30-record corrective dataset passed the data/production gates; 516/516 intended LoRA tensors changed. Automated evidence was mixed and V5 was cleared only for H7 DHE.
- **H7:** matched generation completed; planned multi-reviewer human collection was intentionally discontinued on 2026-09-19; no H7 human result and no promotion decision.
- **DPO V6:** 24-record synthetic corrective dataset; canonical production completed successfully; 516/516 intended tensors changed; matched 50-case diagnostic favored V6 on the aggregate heuristic signal; not promoted.
- **H8:** complete. Controlled unblinding after the blinded lock produced case-level outcomes of SFT 6, V6 3, neither 2, equal 1. V6 is not promoted; SFT remains reference.

The immutable Step-2 freeze remains `research-freeze/step2-dpo-v2-20260909` at `ac899e879f930f25b2081550bd8c5dd5c983df35`.

## DPO V6 canonical production evidence

Canonical production:

- source revision: `c4c942d3c455c8745d4756ca2a775772b1215a4a`
- GitHub Actions run: `35446312134`
- job: `105905727395`
- public Actions artifact: `10586544611`
- artifact digest: `sha256:78e32163461051ee625ca79aaf99e6b7fefd1884caae89ed9cc41818b76404da`
- training records: 24
- dataset SHA-256: `eca6b25c27f8c03d221854b2e7aee59f5da0e4f128cd2b9605c10453723dc732`
- configured epochs: 4
- trainer global step: 8
- final train loss: `0.646148681640625`
- intended trainable tensors changed: 516 / 516
- final V6 adapter safetensors SHA-256: `c6505d38987f4509017063fe044ec06f731badbb514bb47ccef788e63aa0a1e4`

The sanitized public evidence is permanently copied to `artifacts/public-evidence/dpo-v6-production.json`.

## DPO V6 matched diagnostic

Both SFT and V6 completed 50/50 cases with zero execution failures.

| Metric | SFT | DPO V6 | Delta |
|---|---:|---:|---:|
| Mean heuristic rubric | 89.18 | 90.62 | +1.44 |
| Mean keyword coverage | 0.730 | 0.765 | +0.035 |
| Automated safety adherence | 100% | 100% | 0 |
| Cases flagged for human review | 20 | 19 | -1 |
| Mean latency | 37.527 s | 40.109 s | +2.582 s |

This is a positive matched diagnostic signal. It remains heuristic development evidence, not a clean held-out human-preference result.

The SFT aggregate has varied across separately executed diagnostics, so cross-run headline scores must not be treated as one fixed leaderboard. Matched comparisons and case-level evaluation remain the relevant evidence.

See [DPO_V6_PRODUCTION_DIAGNOSTIC_RESULTS.md](DPO_V6_PRODUCTION_DIAGNOSTIC_RESULTS.md) and [DPO_V6_CANDIDATE_FREEZE.md](DPO_V6_CANDIDATE_FREEZE.md).

## Current development gate

V6 is development-frozen to the exact production identity documented in `DPO_V6_CANDIDATE_FREEZE.md`.

Canonical H8 matched generation is complete:

- run: `35457211935`
- reviewer-safe artifact: `10588896454`
- artifact digest: `sha256:79f130d0e20fa612540d3787ffbb13d1327860a5ec6a1ccb9247500187271588`
- batch: `HEB1-B6BE09E2D6DB`
- eligible cases: 12
- identical pairs skipped: 0
- canonical benchmark leakage: PASS, 12/12 clean
- development separation: PASS, max token-set Jaccard `0.3235294117647059 < 0.35`

H8 controlled unblinding is complete. The safe case-level result is:

- SFT preferred: 6 cases
- DPO V6 preferred: 3 cases
- neither good: 2 cases
- about equal: 1 case
- not sure: 0 cases

All 12 cases had 3-of-3 agreement in the collected response set. The corresponding raw judgment totals are 18 SFT, 9 V6, 6 neither, and 3 equal. The directional 3-of-9 V6 case-win fraction is too imprecise for a strong statistical claim (`p = 0.5078125` two-sided exact binomial; exact 95% interval about `0.0749–0.7007`).

The H8 advancement gate is not met. V6 is not promoted and is not frozen as an assurance candidate. SFT remains reference and SHAE stays sealed.

See `docs/H8_DHE_V6_PILOT_V1_RESULTS.md`.

No V7 checkpoint may be substituted into H8 under the V6 label. Any later training iteration requires a new experiment identity and evaluation round.

SHAE remains sealed and may not be opened merely because the V6 diagnostic was positive.

## Claim boundary

Supported:

- DPO V2–V6 are technically valid trained development checkpoints.
- H4–H6 are completed DHE rounds.
- H7 matched generation completed but human collection was discontinued without a result.
- V6 canonical production completed with 516/516 intended trainable tensors changed.
- The matched 50-case V6 diagnostic produced 90.62 versus 89.18 for SFT, with 100% automated safety adherence for both.
- V6 is frozen as the candidate identity for H8 development evaluation.
- H8 development evaluation completed: SFT was preferred on 6 cases, V6 on 3, 2 were neither-good, and 1 was equal.
- SFT remains the reference checkpoint.
- SHAE remains sealed.

Not supported:

- DPO V6 is broadly superior to SFT.
- DPO V6 passed the H8 promotion gate or is superior to SFT.
- DPO V6 is assurance-frozen or promoted.
- H8 establishes V6 superiority, or reviewer identity-level independence is technically verified from the current instrument.
- SHAE may be opened, has started, or has passed.

## Operational boundary

The 2026-09-13 accidental duplicate V4/V5 Kaggle launches remain documented non-canonical operational side effects. Research-significant Kaggle production workflows are manual-dispatch only.

Private Kaggle outputs, checkpoints, reviewer mappings, raw human-evaluation responses, and SHAE material remain outside the public repository. Only explicitly sanitized aggregate evidence and cryptographic digests may cross the public boundary.

## Public website state

The website is a presentation layer and should consume the machine-readable files under `public/`. No public human-evaluation round is currently accepting responses. Reviewer links, response sheets, private A/B mappings, and SHAE material remain non-public.
