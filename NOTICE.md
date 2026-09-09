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

The PAUL Open source-code layer is distributed under the Apache License 2.0 unless a file or component states otherwise.

Gemma 4 is released by Google under Apache 2.0. Third-party datasets, libraries, benchmarks, models, and other materials retain their respective licenses, notices, attribution requirements, and usage restrictions.

A dataset or model being publicly accessible does not by itself establish that it may be used for every training, redistribution, or release purpose. See DATASET_REGISTRY.md and the applicable upstream terms.

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

Recommended attribution
-----------------------

For research publications, downstream projects, and derivative work, Paul Foundry recommends acknowledging PAUL Open with language such as:

"Based on PAUL Open by Paul Foundry Technologies Private Limited."

This is recommended attribution unless an applicable license requires different or additional attribution.
