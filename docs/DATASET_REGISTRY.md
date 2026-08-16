# PAUL Open Model — Dataset & Resource Registry

This registry provides a rigorous, verified audit of all candidate datasets, corpora, and resources under consideration for the PAUL Open Model project.

> **CRITICAL LEGAL & RESEARCH POLICY**:
> 1. **No Automatic Pre-Approval**: No dataset is classified as "approved for unrestricted training and public weights" solely based on its surface-level license. All prospective training resources are classified as **"Candidate for training; public model release requires provenance/license review."**
> 2. **Multi-Dimensional Provenance Audit**: Every entry explicitly audits eight legal and technical dimensions:
>    - **Package / Dataset License**: The formal license applied to the packaged dataset repository.
>    - **Underlying Content Provenance**: How the underlying raw text, images, or problems were created, collected, mined, or synthesized.
>    - **Permitted Training Use**: Whether model training (machine learning optimization) is permitted under the terms.
>    - **Permitted Commercial Use**: Whether commercial deployment/commercial derived artifacts are permitted.
>    - **Redistribution Rights**: Terms governing redistribution of raw data vs processed artifacts.
>    - **Attribution Requirements**: Explicit citation, copyright notice, or disclaimer obligations.
>    - **Restrictions on Derived Model Weights**: Whether training restricts weights distribution (e.g., Non-Commercial, ShareAlike, or commercial bans).
>    - **Public-Release Status**: Project classification status for our open weights release.
> 3. **Non-Commercial Datasets are Evaluation-Only**: Any dataset bearing a Non-Commercial (`NC`) license or research-only terms is strictly quarantined to **Evaluation-Only (Benchmark)** status unless separate legal review establishes that its terms permit training and our intended public release.
> 4. **Google DeepMind / Gemma Separation**: Official DeepMind projects (MedGemma, TxGemma, DataGemma) are referenced for **methodology and inspiration**; underlying data is audited strictly per individual source license.

---

## Google DeepMind / Gemma Resource Audit Matrix

| Project | Official Methodology / Inspiration | Reusable Open Resources | Resources Requiring Separate License Review |
|---|---|---|---|
| **MedGemma** | Multimodal medical grounding, clinical QA formatting, image-text alignment. | • **PubMedQA** (MIT)<br>• **MedMCQA** (Apache-2.0) | Proprietary hospital EHR records, closed clinical imaging sets, non-public medical benchmark splits. |
| **TxGemma** | Therapeutics instruction-tuning format across small molecules, protein targets, and disease endpoints. | • **TDC Open Subsets** (MIT/BSD/CC-BY)<br>• **Reactome Knowledgebase** (CC-BY-4.0)<br>• **ChEMBL 34+ Data** (CC-BY-SA 4.0) | Non-permissive TDC benchmark subsets, proprietary binding assay datasets. |
| **DataGemma** | Retrieval-Interleaved Generation (RIG) and statistical table grounding. | • **Data Commons Open Data** (Public Domain / CC0 / CC-BY / OGDL open government statistical data) | Proprietary statistical data feeds, closed third-party databases. |
| **Gemmaverse / Cookbooks** | SFTTrainer configurations, QLoRA recipes, Gemma 4 chat template conventions. | • **Gemma Cookbook Recipes** (Apache-2.0)<br>• **TRL/PEFT Open Implementations** (Apache-2.0) | Any third-party proprietary data used in community demonstrations. |

---

## Detailed Dataset Audits

---

### 1. Indian Multilingual & Translation Resources

#### 1.1 IndicCorp v2
- **Canonical Source**: AI4Bharat (`ai4bharat/indiccorp_v2`)
- **Package / Dataset License**: CC0-1.0 (Public Domain Dedication)
- **Underlying Content Provenance**: Web-crawled news, articles, and public domain text across 24 Indian languages and English. Mined and cleaned by AI4Bharat.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes (per CC0 dedication of corpus packaging)
- **Redistribution Rights**: Unrestricted
- **Attribution Requirements**: AI4Bharat academic citation requested.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**
- **Notes**: Prioritize for Indic language vocabulary coverage and domain adaptation.

#### 1.2 BPCC (Bharat Parallel Corpus Collection)
- **Canonical Source**: AI4Bharat (`ai4bharat/BPCC`)
- **Package / Dataset License**: CC0-1.0 (AI4Bharat waives rights to mined/packaged corpus)
- **Underlying Content Provenance**: Curated and mined parallel sentence pairs from open web sources, government repositories, and translated pairs across 22 Indic languages and English.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes (per CC0 packaging terms)
- **Redistribution Rights**: Unrestricted
- **Attribution Requirements**: Academic citation to AI4Bharat (Gala et al., 2023).
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**
- **Notes**: Primary candidate for bidirectional English ↔ Indic translation training.

#### 1.3 IN22 Benchmark (IN22-Gen & IN22-Conv)
- **Canonical Source**: AI4Bharat (`ai4bharat/IN22-Gen`, `ai4bharat/IN22-Conv`)
- **Package / Dataset License**: CC-BY-4.0
- **Underlying Content Provenance**: Manually translated multi-domain sentences (general news, government, conversation) across 22 Indic languages created explicitly for benchmarking.
- **Permitted Training Use**: Permitted under CC-BY-4.0, but quarantined to prevent evaluation contamination.
- **Permitted Commercial Use**: Yes with attribution.
- **Redistribution Rights**: Permitted with attribution.
- **Attribution Requirements**: Credit Gala et al., 2023.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Strictly Evaluation-Only (Benchmark).**
- **Notes**: Must NOT be included in training data to preserve clean evaluation integrity.

#### 1.4 Samanantar
- **Canonical Source**: AI4Bharat (`ai4bharat/samanantar`)
- **Package / Dataset License**: CC-BY-NC-4.0 (Creative Commons Non-Commercial)
- **Underlying Content Provenance**: Large-scale mined parallel corpus across 11 Indic languages and English.
- **Permitted Training Use**: Non-commercial research only.
- **Permitted Commercial Use**: No (NC restriction).
- **Redistribution Rights**: Non-commercial distribution only.
- **Attribution Requirements**: Credit Ramesh et al., 2022.
- **Restrictions on Derived Model Weights**: NC restriction may attach to derived model weights.
- **Public-Release Status**: **Strictly Evaluation-Only (Non-Commercial / License-Restricted).**
- **Notes**: Excluded from open-weights training mixture to ensure permissive model release.

#### 1.5 Aksharantar
- **Canonical Source**: AI4Bharat (`ai4bharat/Aksharantar`)
- **Package / Dataset License**: CC0-1.0 (Corpus packaging) / CC-BY-NC-4.0 (Original repo metadata note)
- **Underlying Content Provenance**: Word-level transliteration pairs mined and curated across 21 Indic languages.
- **Permitted Training Use**: Permitted for CC0 mined pairs.
- **Permitted Commercial Use**: Requires verification of CC0 mined subsets vs NC components.
- **Redistribution Rights**: Permitted for verified CC0 components.
- **Attribution Requirements**: Credit Madhani et al., 2023.
- **Restrictions on Derived Model Weights**: Requires verification.
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**
- **Notes**: Critical for code-switching and transliteration handling (e.g., Roman script Indic).

---

### 2. Science Education & Mathematics Resources

#### 2.1 OpenBookQA
- **Canonical Source**: Allen Institute for AI (`allenai/openbookqa`)
- **Package / Dataset License**: Apache-2.0
- **Underlying Content Provenance**: 5,957 multiple-choice elementary science questions created by human experts, modeled after open-book exams and grounded in 1,326 core science facts.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted (include Apache-2.0 copyright notice)
- **Attribution Requirements**: AI2 copyright notice.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**
- **Notes**: High-quality benchmark for multi-hop science reasoning.

#### 2.2 ARC (AI2 Reasoning Challenge)
- **Canonical Source**: Allen Institute for AI (`allenai/ai2_arc`)
- **Package / Dataset License**: CC-BY-SA-4.0 (ShareAlike)
- **Underlying Content Provenance**: 7,787 genuine grade-school science exam questions (grades 3–9) across Challenge and Easy partitions.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes, subject to ShareAlike requirements on adaptations.
- **Redistribution Rights**: Permitted under CC-BY-SA 4.0.
- **Attribution Requirements**: Credit Clark et al., 2018.
- **Restrictions on Derived Model Weights**: Dataset derivative works must be CC-BY-SA; model weight interpretation varies by jurisdiction.
- **Public-Release Status**: **Strictly Evaluation-Only (Benchmark)** for core track; ShareAlike training candidate for specific research variants.

#### 2.3 SciTail
- **Canonical Source**: Allen Institute for AI (`allenai/scitail`)
- **Package / Dataset License**: CC-BY-4.0
- **Underlying Content Provenance**: 27k scientific textual entailment pairs derived from science exam questions and web sentences.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with attribution.
- **Attribution Requirements**: Credit Khot et al., 2018.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 2.4 SciQ
- **Canonical Source**: Allen Institute for AI (`allenai/sciq`)
- **Package / Dataset License**: CC-BY-NC 3.0 (Non-Commercial)
- **Underlying Content Provenance**: 13,679 crowdsourced science exam questions with supporting explanation passages.
- **Permitted Training Use**: Non-commercial research only.
- **Permitted Commercial Use**: No (NC restriction).
- **Redistribution Rights**: Non-commercial only.
- **Attribution Requirements**: Credit Welbl et al., 2017.
- **Restrictions on Derived Model Weights**: NC restriction may infect weights.
- **Public-Release Status**: **Strictly Evaluation-Only (Non-Commercial / License-Restricted).**

#### 2.5 GSM8K (Grade School Math 8K)
- **Canonical Source**: OpenAI (`openai/gsm8k`)
- **Package / Dataset License**: MIT License
- **Underlying Content Provenance**: 8,500 grade-school math word problems created by human problem writers with multi-step natural language solutions.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with MIT notice.
- **Attribution Requirements**: OpenAI MIT copyright notice.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**
- **Notes**: Standard foundation for step-by-step math reasoning.

#### 2.6 MATH Dataset
- **Canonical Source**: Hendrycks et al. / UC Berkeley (`hendrycks/competition_math`)
- **Package / Dataset License**: MIT License
- **Underlying Content Provenance**: 12,500 challenging high-school math competition problems (AMC 10, AMC 12, AIME) with full LaTeX step-by-step solutions.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with MIT notice.
- **Attribution Requirements**: Credit Hendrycks et al., 2021.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

---

### 3. Student Tutoring & Socratic Pedagogy Resources

#### 3.1 Socratic Method Conversations
- **Canonical Source**: Hugging Face (`sanjaypantdsd/socratic-method-conversations`)
- **Package / Dataset License**: MIT License
- **Underlying Content Provenance**: Curated and synthetic multi-turn question-driven dialogues demonstrating inquiry-based concept scaffolding.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with MIT notice.
- **Attribution Requirements**: Standard MIT notice.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 3.2 MathDial
- **Canonical Source**: Macina et al. / ETH Zurich (`eth-nlped/mathdial`)
- **Package / Dataset License**: CC-BY-SA-4.0 (ShareAlike)
- **Underlying Content Provenance**: ~3,000 teacher-student math tutoring dialogues annotated with teacher pedagogical intents, student errors, and guiding hints.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes, under ShareAlike terms for data derivatives.
- **Redistribution Rights**: Permitted under CC-BY-SA 4.0.
- **Attribution Requirements**: Credit Macina et al., 2023.
- **Restrictions on Derived Model Weights**: Packaging of derived dataset must remain CC-BY-SA 4.0.
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 3.3 PRM800K (Process Supervision for Math)
- **Canonical Source**: OpenAI (`openai/prm800k`)
- **Package / Dataset License**: MIT License
- **Underlying Content Provenance**: 800,000 step-level correctness labels for math problem solving, generated via human feedback on model solution steps.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with MIT notice.
- **Attribution Requirements**: OpenAI MIT copyright notice.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 3.4 Khan Academy Tutoring Accuracy Dataset
- **Canonical Source**: Khan Academy (`Khan/tutoring-accuracy-dataset`)
- **Package / Dataset License**: Custom Evaluation Dataset License (Restricted)
- **Underlying Content Provenance**: Real and synthetic tutoring interaction logs annotated for pedagogical accuracy.
- **Permitted Training Use**: No (Prohibited by terms).
- **Permitted Commercial Use**: No.
- **Redistribution Rights**: Prohibited.
- **Attribution Requirements**: N/A
- **Restrictions on Derived Model Weights**: Model training is strictly prohibited.
- **Public-Release Status**: **Strictly Excluded from Project** (Reference only for qualitative evaluation metrics).

---

### 4. Teacher Assistance & Educational Content

#### 4.1 Open Curriculum Frameworks (NCERT / CBSE / State Boards)
- **Canonical Source**: NCERT & Open Government Data India
- **Package / Dataset License**: Open Government Data (OGD) / Public Educational Materials
- **Underlying Content Provenance**: Official Indian national educational frameworks, learning outcomes, syllabus structures, and public educational texts.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes (subject to standard OGD attribution guidelines)
- **Redistribution Rights**: Permitted with attribution.
- **Attribution Requirements**: Attribution to NCERT / Ministry of Education, Govt. of India.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 4.2 Synthetic Teacher Assistant Suite (PAUL Open Native)
- **Canonical Source**: In-house PAUL Open synthesis pipeline
- **Package / Dataset License**: Apache-2.0
- **Underlying Content Provenance**: Synthetic pedagogical templates for 5E lesson planning, rubric generation, Bloom's taxonomy question design, and differentiated instruction.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted under Apache-2.0.
- **Attribution Requirements**: PAUL Open Model Contributors.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

---

### 5. Empathy, Human-Centered Interaction & Safety

#### 5.1 HelpSteer2
- **Canonical Source**: NVIDIA (`nvidia/HelpSteer2`)
- **Package / Dataset License**: CC-BY-4.0
- **Underlying Content Provenance**: 10,000 multi-attribute human ratings (helpfulness, correctness, coherence, complexity, verbosity, toxicity) on conversational responses.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with attribution.
- **Attribution Requirements**: Credit Wang et al. / NVIDIA (2024).
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 5.2 Anthropic Helpful & Harmless RLHF Dataset
- **Canonical Source**: Anthropic (`Anthropic/hh-rlhf`)
- **Package / Dataset License**: MIT License
- **Underlying Content Provenance**: 160k human preference pairs generated from crowdworkers interacting with AI assistants, rated for helpfulness and safety.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with MIT notice.
- **Attribution Requirements**: Anthropic MIT copyright notice.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 5.3 ESConv (Emotional Support Conversation)
- **Canonical Source**: Tsinghua CoAI (`thu-coai/esconv`)
- **Package / Dataset License**: CC-BY-NC-4.0 (Non-Commercial)
- **Underlying Content Provenance**: 1,053 crowdsourced multi-turn emotional support dialogues annotated with supportive strategy stages.
- **Permitted Training Use**: Non-commercial research only.
- **Permitted Commercial Use**: No (NC restriction).
- **Redistribution Rights**: Non-commercial only.
- **Attribution Requirements**: Credit Liu et al., 2021.
- **Restrictions on Derived Model Weights**: NC restriction attaches to weights.
- **Public-Release Status**: **Strictly Evaluation-Only (Non-Commercial / License-Restricted).**

#### 5.4 Synthetic Anti-Anthropomorphism & Persona Alignment Suite
- **Canonical Source**: In-house PAUL Open alignment pipeline
- **Package / Dataset License**: Apache-2.0
- **Underlying Content Provenance**: Synthetic dialogues testing human-centered boundaries: supportive attunement without claiming human identity, feelings, or memories.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted under Apache-2.0.
- **Attribution Requirements**: PAUL Open Model Contributors.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

---

### 6. Scientific Research Assistance & Literature

#### 6.1 PubMedQA
- **Canonical Source**: BioNLP (`pubmed_qa`, `bigbio/pubmed_qa`)
- **Package / Dataset License**: MIT License
- **Underlying Content Provenance**: 273k biomedical QA instances collected from PubMed abstracts where answers are deduced from research conclusions.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with MIT notice.
- **Attribution Requirements**: Credit Jin et al., 2019.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 6.2 QASPER
- **Canonical Source**: Allen Institute for AI (`allenai/qasper`)
- **Package / Dataset License**: CC-BY-4.0
- **Underlying Content Provenance**: 5,049 questions over 1,585 full open-access NLP research papers with paragraph-level evidence spans.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with attribution.
- **Attribution Requirements**: Credit Dasigi et al., 2021.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 6.3 SciTLDR
- **Canonical Source**: Allen Institute for AI (`allenai/scitldr`)
- **Package / Dataset License**: Apache-2.0
- **Underlying Content Provenance**: 5,400 scientific publication summaries (1-sentence TLDRs) written and vetted by domain experts.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted under Apache-2.0.
- **Attribution Requirements**: Credit Cachola et al., 2020.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 6.4 SciFact
- **Canonical Source**: Allen Institute for AI (`allenai/scifact`)
- **Package / Dataset License**: CC-BY-NC 2.0 (Non-Commercial)
- **Underlying Content Provenance**: 1.4k expert-written scientific claims paired with research abstracts and evidence labels.
- **Permitted Training Use**: Non-commercial research only.
- **Permitted Commercial Use**: No (NC restriction).
- **Redistribution Rights**: Non-commercial only.
- **Attribution Requirements**: Credit Wadden et al., 2020.
- **Restrictions on Derived Model Weights**: NC restriction attaches to weights.
- **Public-Release Status**: **Strictly Evaluation-Only (Non-Commercial / License-Restricted).**

---

### 7. Life Sciences, Genomics & Biomedical Resources

#### 7.1 MedMCQA
- **Canonical Source**: Indian Institute of Science & AIIMS (`openlifescience/medmcqa`)
- **Package / Dataset License**: Apache-2.0
- **Underlying Content Provenance**: 194k high-yield medical entrance examination questions (AIIMS PG, NEET PG) covering 21 subjects across basic and clinical sciences.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted under Apache-2.0.
- **Attribution Requirements**: Credit Pal et al., 2022.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 7.2 Therapeutics Data Commons (TDC) Open Subsets
- **Canonical Source**: TDC Initiative (`tdcommons.ai`)
- **Package / Dataset License**: MIT / BSD / CC-BY (Subsets vary)
- **Underlying Content Provenance**: Systematic machine learning benchmark datasets for small molecule properties, drug-target binding, ADMET, and target disease indications.
- **Permitted Training Use**: Yes for permissive subsets.
- **Permitted Commercial Use**: Yes for MIT/BSD/CC-BY subsets.
- **Redistribution Rights**: Governed by individual benchmark licenses.
- **Attribution Requirements**: Credit Huang et al., 2021.
- **Restrictions on Derived Model Weights**: None for permissive subsets.
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 7.3 Reactome & Gene Ontology Open Knowledge
- **Canonical Source**: Reactome Knowledgebase & Gene Ontology Consortium
- **Package / Dataset License**: CC-BY-4.0 / CC0
- **Underlying Content Provenance**: Expert-curated biological pathway reactions, molecular functions, and cellular component annotations.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with attribution.
- **Attribution Requirements**: Official Reactome / GO citation.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 7.4 ChEMBL & PubChem Open Bioactivity Data
- **Canonical Source**: EMBL-EBI & NCBI
- **Package / Dataset License**: CC-BY-SA 4.0 (ChEMBL) / CC0 (PubChem)
- **Underlying Content Provenance**: Curated bioactivity assays, molecular SMILES, targets, and drug mechanism descriptions.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted under respective terms.
- **Attribution Requirements**: Standard EMBL-EBI / NCBI citation.
- **Restrictions on Derived Model Weights**: ChEMBL derived datasets require CC-BY-SA.
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

---

### 8. General Reasoning & Instruction Tuning

#### 8.1 UltraFeedback & UltraChat
- **Canonical Source**: OpenBMB (`openbmb/UltraFeedback`, `openbmb/UltraChat`)
- **Package / Dataset License**: MIT License
- **Underlying Content Provenance**: High-diversity multi-turn instruction dialogues generated with diverse prompts and annotated with fine-grained aspect ratings.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with MIT notice.
- **Attribution Requirements**: OpenBMB MIT copyright notice.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 8.2 StrategyQA
- **Canonical Source**: Geva et al. (`wics/strategyqa`)
- **Package / Dataset License**: Apache-2.0
- **Underlying Content Provenance**: Multi-step implicit reasoning questions created by human annotators.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted under Apache-2.0.
- **Attribution Requirements**: Credit Geva et al., 2021.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

---

### 9. Multimodal Scientific & Diagram Resources

#### 9.1 ChartQA
- **Canonical Source**: Masry et al. (`ahmed-masry/chartqa`)
- **Package / Dataset License**: CC-BY-4.0
- **Underlying Content Provenance**: 32,886 QA pairs on 20,904 charts requiring visual comprehension and arithmetic reasoning over plots.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with attribution.
- **Attribution Requirements**: Credit Masry et al., 2022.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 9.2 MathVista
- **Canonical Source**: Lu et al. (`AI4Math/MathVista`)
- **Package / Dataset License**: CC-BY-SA-4.0 (ShareAlike)
- **Underlying Content Provenance**: 6,141 diverse multimodal math and science problems collected from 28 existing benchmarks and 3 new datasets.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes, under ShareAlike terms for data derivatives.
- **Redistribution Rights**: Permitted under CC-BY-SA 4.0.
- **Attribution Requirements**: Credit Lu et al., 2023.
- **Restrictions on Derived Model Weights**: Derived dataset adaptations require CC-BY-SA 4.0.
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 9.3 PlotQA
- **Canonical Source**: Chaudhry et al. (`plotqa`)
- **Package / Dataset License**: MIT License
- **Underlying Content Provenance**: 28M synthetic and web plot Q&A pairs testing structural understanding of scientific plots.
- **Permitted Training Use**: Yes
- **Permitted Commercial Use**: Yes
- **Redistribution Rights**: Permitted with MIT notice.
- **Attribution Requirements**: Standard MIT notice.
- **Restrictions on Derived Model Weights**: None
- **Public-Release Status**: **Candidate for training; public model release requires provenance/license review.**

#### 9.4 ScienceQA
- **Canonical Source**: Lu et al. (`derek-thomas/ScienceQA`)
- **Package / Dataset License**: CC-BY-NC-SA 4.0 (Non-Commercial ShareAlike)
- **Underlying Content Provenance**: 21,208 multimodal science questions with lectures and explanations across grades 1–12.
- **Permitted Training Use**: Non-commercial research only.
- **Permitted Commercial Use**: No (NC restriction).
- **Redistribution Rights**: Non-commercial ShareAlike only.
- **Attribution Requirements**: Credit Lu et al., 2022.
- **Restrictions on Derived Model Weights**: NC-SA restrictions attach to derived models.
- **Public-Release Status**: **Strictly Evaluation-Only (Non-Commercial / License-Restricted).**

---

## Dataset Audit Summary Table

| Category | Dataset Name | Package License | Provenance Type | Permitted Commercial Use | Public-Release Status |
|---|---|---|---|---|---|
| **Indic Multilingual** | IndicCorp v2 | CC0-1.0 | Web-mined Indic text | Yes | Candidate for training; public model release requires provenance/license review. |
| **Indic Multilingual** | BPCC | CC0-1.0 | Mined & translated pairs | Yes | Candidate for training; public model release requires provenance/license review. |
| **Indic Multilingual** | IN22-Gen / Conv | CC-BY-4.0 | Human translated benchmark | Yes | **Strictly Evaluation-Only (Benchmark).** |
| **Indic Multilingual** | Samanantar | CC-BY-NC-4.0 | Mined parallel text | No (NC) | **Strictly Evaluation-Only (Non-Commercial).** |
| **Indic Multilingual** | Aksharantar | CC0-1.0 / NC | Transliteration pairs | Verification Req. | Candidate for training; public model release requires provenance/license review. |
| **Science Education** | OpenBookQA | Apache-2.0 | Human-written science QA | Yes | Candidate for training; public model release requires provenance/license review. |
| **Science Education** | ARC Challenge/Easy | CC-BY-SA 4.0 | Real science exam questions | Yes (SA) | **Strictly Evaluation-Only (Benchmark).** |
| **Science Education** | SciTail | CC-BY-4.0 | Scientific entailment | Yes | Candidate for training; public model release requires provenance/license review. |
| **Science Education** | SciQ | CC-BY-NC 3.0 | Crowdsourced exam questions | No (NC) | **Strictly Evaluation-Only (Non-Commercial).** |
| **Science Education** | GSM8K | MIT | Human math word problems | Yes | Candidate for training; public model release requires provenance/license review. |
| **Science Education** | MATH | MIT | Competition math with LaTeX | Yes | Candidate for training; public model release requires provenance/license review. |
| **Tutoring & Socratic** | Socratic Conversations | MIT | Curated inquiry dialogues | Yes | Candidate for training; public model release requires provenance/license review. |
| **Tutoring & Socratic** | MathDial | CC-BY-SA 4.0 | Tutoring with teacher intents | Yes (SA) | Candidate for training; public model release requires provenance/license review. |
| **Tutoring & Socratic** | PRM800K | MIT | Step-level process labels | Yes | Candidate for training; public model release requires provenance/license review. |
| **Tutoring & Socratic** | Khan Tutoring Eval | Custom Restricted | Real/synthetic tutoring logs | No | **Strictly Excluded from Project.** |
| **Teacher Assistance** | NCERT / OER Frameworks | OGD / Public Domain | Official Indian curricula | Yes | Candidate for training; public model release requires provenance/license review. |
| **Teacher Assistance** | Synthetic Teacher Suite | Apache-2.0 | In-house synthetic templates | Yes | Candidate for training; public model release requires provenance/license review. |
| **Empathy & Safety** | HelpSteer2 | CC-BY-4.0 | Multi-attribute human ratings | Yes | Candidate for training; public model release requires provenance/license review. |
| **Empathy & Safety** | Anthropic HH-RLHF | MIT | Human safety preference pairs | Yes | Candidate for training; public model release requires provenance/license review. |
| **Empathy & Safety** | ESConv | CC-BY-NC-4.0 | Emotional support dialogues | No (NC) | **Strictly Evaluation-Only (Non-Commercial).** |
| **Empathy & Safety** | Synthetic Anti-Anthropomorphism | Apache-2.0 | In-house boundary dialogues | Yes | Candidate for training; public model release requires provenance/license review. |
| **Scientific Research** | PubMedQA | MIT | Biomedical abstract QA | Yes | Candidate for training; public model release requires provenance/license review. |
| **Scientific Research** | QASPER | CC-BY-4.0 | Paper QA with evidence spans | Yes | Candidate for training; public model release requires provenance/license review. |
| **Scientific Research** | SciTLDR | Apache-2.0 | Expert 1-sentence summaries | Yes | Candidate for training; public model release requires provenance/license review. |
| **Scientific Research** | SciFact | CC-BY-NC 2.0 | Claim verification benchmark | No (NC) | **Strictly Evaluation-Only (Non-Commercial).** |
| **Life Sciences** | MedMCQA | Apache-2.0 | Indian medical entrance QA | Yes | Candidate for training; public model release requires provenance/license review. |
| **Life Sciences** | TDC Open Subsets | MIT/BSD/CC-BY | Therapeutics ML benchmarks | Yes | Candidate for training; public model release requires provenance/license review. |
| **Life Sciences** | Reactome & GO | CC-BY-4.0 / CC0 | Biological pathways & ontology | Yes | Candidate for training; public model release requires provenance/license review. |
| **Life Sciences** | ChEMBL & PubChem | CC-BY-SA / CC0 | Chemical bioactivity & targets | Yes | Candidate for training; public model release requires provenance/license review. |
| **General Reasoning** | UltraFeedback / Chat | MIT | Multi-turn feedback pairs | Yes | Candidate for training; public model release requires provenance/license review. |
| **General Reasoning** | StrategyQA | Apache-2.0 | Multi-step implicit reasoning | Yes | Candidate for training; public model release requires provenance/license review. |
| **Multimodal Science** | ChartQA | CC-BY-4.0 | Scientific chart QA | Yes | Candidate for training; public model release requires provenance/license review. |
| **Multimodal Science** | MathVista | CC-BY-SA 4.0 | Visual math & science QA | Yes (SA) | Candidate for training; public model release requires provenance/license review. |
| **Multimodal Science** | PlotQA | MIT | Scientific plot structure QA | Yes | Candidate for training; public model release requires provenance/license review. |
| **Multimodal Science** | ScienceQA | CC-BY-NC-SA 4.0 | Multimodal school science QA | No (NC-SA) | **Strictly Evaluation-Only (Non-Commercial).** |
