# PAUL Open — DPO V6 Development Candidate Freeze

**Freeze date:** 2026-09-19  
**Freeze type:** development candidate identity freeze  
**Not:** SHAE / final-assurance freeze

## Candidate identity

The V6 candidate used for the next development comparison is fixed to:

- experiment: `paul_e4b_dpo_v6_synthetic_corrective`
- source revision: `c4c942d3c455c8745d4756ca2a775772b1215a4a`
- GitHub Actions production run: `35446312134`
- GitHub Actions job: `105905727395`
- public sanitized artifact: `10586544611`
- public artifact digest: `sha256:78e32163461051ee625ca79aaf99e6b7fefd1884caae89ed9cc41818b76404da`
- training dataset SHA-256: `eca6b25c27f8c03d221854b2e7aee59f5da0e4f128cd2b9605c10453723dc732`
- final adapter safetensors SHA-256: `c6505d38987f4509017063fe044ec06f731badbb514bb47ccef788e63aa0a1e4`
- final adapter bytes: `139602808`
- base model: `google/gemma-4-E4B-it`
- base revision: `ee0ef6023621cff504d758262d4e04895a5af4a2`

## Freeze semantics

H8 must compare this exact V6 adapter identity against the frozen SFT reference. No V7 training, adapter mutation, prompt-specific tuning, or response-informed checkpoint replacement may be substituted into H8 under the V6 label.

If a later training iteration is created, it receives a new experiment identity and a new evaluation round.

This freeze is a development-control mechanism only. It does not authorize a superiority claim and does not open SHAE.
