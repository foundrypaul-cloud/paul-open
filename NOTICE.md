PAUL Open
=========

PAUL Open is an open research initiative of Paul Foundry Technologies Private Limited.

Project identity
----------------

PAUL Open explores reproducible AI post-training and evaluation for multilingual knowledge work, science education, tutoring, teacher assistance, human-centered interaction, and scientific research.

The public research repository is:

https://github.com/foundrypaul-cloud/paul-open

The public website is:

https://open.paulfoundry.com/

The repository is the authoritative source for versioned research evidence. The website is a presentation and participation layer and does not replace repository provenance.

Current model provenance
------------------------

The current E4B research line uses:

google/gemma-4-E4B-it

PAUL Open model research is independently developed by Paul Foundry using the stated upstream model. PAUL Open is not an official Google model and is not affiliated with, endorsed by, or developed in collaboration with Google or Google DeepMind.

The current research record includes an SFT reference checkpoint and a technically valid DPO V2 Corrective checkpoint. DPO V2 has not been established as superior to SFT; see the versioned experiment documentation for the evidence boundary.

Immutable Step 2 research freeze
--------------------------------

Branch:
research-freeze/step2-dpo-v2-20260909

SHA:
ac899e879f930f25b2081550bd8c5dd5c983df35

This frozen revision is retained as immutable evidence of the Step 2 DPO V2 research state. Later documentation, evaluation infrastructure, and website-integration work may continue on main without changing the frozen experiment.

Licensing and third-party components
------------------------------------

The PAUL Open-authored source-code layer is distributed under the Apache License 2.0 unless a file or component states otherwise.

The current `google/gemma-4-E4B-it` model repository identifies the model as Apache-2.0 licensed. Third-party datasets, libraries, benchmarks, models, and other materials retain their respective licenses, notices, attribution requirements, and usage restrictions.

A dataset or model being publicly accessible does not by itself establish that it may be used for every training, redistribution, or release purpose. Permission to train on material and permission to redistribute the underlying content are separate questions. See `docs/DATASET_REGISTRY.md`, `docs/PUBLIC_REPOSITORY_BOUNDARY.md`, and the applicable upstream terms.

Public availability of PAUL Open source does not relicense third-party content, confidential information, proprietary research, or material a contributor did not have permission to submit. Contributors must not submit credentials, private reviewer information, sealed assurance material, proprietary/confidential material, or third-party content they are not permitted to redistribute.

The Apache License 2.0 does not grant trademark rights. Paul Foundry, PAUL Open, associated names, logos, and marks remain subject to applicable trademark law and any separate trademark policy.

This NOTICE does not replace or modify any third-party license.

Research claims
---------------

Technical training validity, automated evaluation results, behavioral quality, and overall model superiority are treated as separate evidence layers.

The current 50-case SFT-vs-DPO V2 comparison is diagnostic and contaminated for DPO V2. It must not be presented as clean held-out proof that DPO V2 is better than SFT.

See:

- docs/PROJECT_STATUS.md
- docs/EXPERIMENT_JOURNEY_E4B.md
- docs/E4B_DPO_V2_CORRECTIVE.md
- docs/HUMAN_EVALUATION_PROTOCOL.md
- docs/PUBLIC_REPOSITORY_BOUNDARY.md

Recommended attribution
-----------------------

For research publications, downstream projects, and derivative work, Paul Foundry recommends acknowledging PAUL Open with language such as:

"Based on PAUL Open by Paul Foundry Technologies Private Limited."

This is recommended attribution unless an applicable license requires different or additional attribution.
