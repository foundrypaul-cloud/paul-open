# Dataset Inventory & Licensing

## Third-Party Dataset License Tracking

| Dataset | License / current signal | Type | Languages | Status |
|---|---|---|---|---|
| FLORES-200 | CC-BY-SA-4.0 | Evaluation | 200 languages | Candidate; verify upstream terms before use |
| Samanantar | **License signals conflict:** Hugging Face metadata says CC-BY-NC-4.0; upstream project text has also described CC0 packaging | Evaluation-only pending provenance/license resolution | 11 Indic | **Do not train or redistribute in PAUL Open until resolved** |
| IndicCorp v2 | CC0-1.0 | Candidate training (monolingual) | 24 Indic | Candidate; provenance review still required |
| IN22 | CC-BY-4.0 | Evaluation (parallel) | 22 Indic | Evaluation-only to preserve benchmark integrity |
| SciQ | CC-BY-NC-3.0 | Evaluation-only | English | **No PAUL Open training / public redistribution** |
| ARC | CC-BY-SA-4.0 | Evaluation (QA) | English | Candidate; attribution/ShareAlike review required |
| OpenBookQA | Apache-2.0 | Evaluation (QA) | English | Candidate; keep benchmark contamination boundary |

**Status**: These are planning candidates, not evidence that third-party dataset payloads are present in this repository. Training permission and redistribution permission are separate decisions. The more detailed and controlling project classification is maintained in [`DATASET_REGISTRY.md`](DATASET_REGISTRY.md).

## License Compatibility Notes

- PAUL Open-authored code: Apache-2.0 unless stated otherwise.
- CC-BY / CC-BY-SA material: attribution and any ShareAlike obligations must be reviewed for the exact artifact being used or redistributed.
- NC/research-only material: evaluation-only by PAUL Open policy unless separate legal review establishes compatibility with the intended training and release.
- Public availability is not a redistribution grant; underlying-content provenance can impose obligations beyond package metadata.
- The current `google/gemma-4-E4B-it` model repository identifies the model as Apache-2.0 licensed; upstream terms must still be checked at release time.

## Current corrections from the 2026-09-13 audit

Earlier versions of this file and `configs/data/*.yaml` incorrectly described Samanantar as CC-BY-4.0/training and SciQ as a training candidate. Those planning labels were unsafe and have been corrected without modifying any frozen experiment dataset or result.
