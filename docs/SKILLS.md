# PAUL Open Model — Capability & Skill Matrix

This document maps target capabilities to candidate resources, licensing terms, provenance considerations, training suitability, and evaluation benchmarks.

> **CRITICAL COMPLIANCE NOTICE**:
> 1. No dataset is pre-approved for public model release based solely on its surface license. All entries are classified as **"Candidate for training; public model release requires provenance/license review"** or **"Evaluation-Only (Non-Commercial / License-Restricted)"**.
> 2. Research-only/non-commercial datasets are strictly restricted to evaluation benchmarks unless separate legal review establishes that their terms permit training and our intended model release.
> 3. Google DeepMind projects (MedGemma, TxGemma, DataGemma) are referenced for **methodology and inspiration**; underlying resources are strictly evaluated under their own individual open licenses.

---

## 1. Indian Multilingual AI
*Capabilities: Fluency, grammar, nuance, cultural context, and vocabulary across target Indian languages (English, Hindi, Bengali, Assamese, Tamil, Telugu) with architecture designed for extensibility across all 22 scheduled Indian languages.*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **Monolingual Fluency & Pre-training** | IndicCorp v2 (AI4Bharat) | CC0-1.0 | Web-crawled articles and public domain text across 24 Indic languages; packaging released under CC0. | **Candidate for training; public model release requires provenance/license review.** | Perplexity across Indic languages; IndicGLUE cloze evaluation. |
| **Instruction Following in Indic Languages** | IndicInstruct / Anudesh (Curated open subsets) | Varies by subset (MIT / Apache-2.0 / CC-BY) | Curated multi-source translations of open instruction sets (e.g., Dolly, OpenAssistant). | **Candidate for training; public model release requires provenance/license review** (Filter out NC subsets). | IndicAlpacaEval; multi-turn instruction following in target languages. |
| **Multilingual Reading Comprehension** | IndicQA (AI4Bharat) | CC-BY-4.0 | Wikipedia articles manually annotated with QA pairs across 11 Indic languages. | **Candidate for training; public model release requires provenance/license review.** | F1 and Exact Match on IndicQA test splits. |
| **Cross-Lingual NLI & Semantics** | IndicXNLI (AI4Bharat) | CC-BY-4.0 | Professional translation of XNLI evaluation benchmark into Indic languages. | **Evaluation-Only (Benchmark)** | Accuracy on IndicXNLI test suite. |

---

## 2. Multilingual Translation & Code-Switching
*Capabilities: High-fidelity bidirectional translation (English ↔ Indic, Indic ↔ Indic), transliteration, and conversational code-switching (e.g., Hinglish, Tanglish, Benglish).*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **Parallel Translation (English ↔ Indic)** | BPCC (Bharat Parallel Corpus Collection, AI4Bharat) | CC0-1.0 (Packaging) | Curated and mined parallel sentence pairs from public sources; curation released under CC0. | **Candidate for training; public model release requires provenance/license review.** | sacreBLEU, chrF++, COMET on IN22-Gen and FLORES-200. |
| **Conversational Translation** | IN22-Conv (AI4Bharat) | CC-BY-4.0 | Manually translated conversational dialogues across 22 Indic languages. | **Evaluation-Only (Benchmark)** — Gold-standard evaluation split. | BLEU / chrF++ on IN22-Conv test splits. |
| **Multi-Way Translation Benchmark** | FLORES-200 (Meta) | CC-BY-SA 4.0 | Professionally translated Wikipedia sentences across 200 languages. | **Evaluation-Only (Benchmark)** | chrF++ / spBLEU across all 6 target language pairs. |
| **Transliteration & Code-Switching** | Aksharantar (AI4Bharat) | CC0-1.0 (Packaging) / CC-BY-NC-4.0 | Word-level transliteration pairs mined and curated across 21 Indic languages. | **Candidate for training; public model release requires provenance/license review** (Verify CC0 subset). | Top-1 / Top-5 transliteration accuracy; Hinglish/Tanglish dialogue comprehension. |
| **Samanantar Parallel Corpus** | Samanantar (AI4Bharat) | CC-BY-NC-4.0 | Large-scale mined parallel corpus across 11 Indic languages. | **Evaluation-Only (Non-Commercial)** — Non-commercial terms prevent unrestricted model release. | Research comparison benchmark only. |

---

## 3. Science Education (K-12 to Undergraduate)
*Capabilities: Accurate, conceptually sound explanations in Physics, Chemistry, Biology, Mathematics, and Environmental Science.*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **Science Question Answering & Explanations** | OpenBookQA (AllenAI) | Apache-2.0 | 5,957 human-written science exam questions paired with core science facts and commonsense knowledge. | **Candidate for training; public model release requires provenance/license review.** | Accuracy & explanation quality score on OpenBookQA test set. |
| **Complex Science Reasoning** | ARC (AI2 Reasoning Challenge - Challenge & Easy) | CC-BY-SA 4.0 | Genuine grade-school science exam questions (grades 3–9). | **Evaluation-Only (Benchmark)** / ShareAlike candidate for research variants. | ARC Challenge Accuracy (0-shot & 5-shot). |
| **Scientific Entailment & Verification** | SciTail (AllenAI) | CC-BY-4.0 | Science questions reformulated into sentence entailment pairs from web sentences. | **Candidate for training; public model release requires provenance/license review.** | Entailment accuracy and precision on SciTail test split. |
| **Curriculum-Aligned Multilingual Science** | NCERT / State Board open educational frameworks | Open Government Data / Public Domain | Official Indian school science learning outcomes, syllabi, and public educational texts. | **Candidate for training; public model release requires provenance/license review.** | Multilingual CBSE/State Board aligned exam benchmark. |
| **SciQ Science Exam Corpus** | SciQ (AllenAI) | CC-BY-NC 3.0 | Crowdsourced science exam questions with supporting explanation paragraphs. | **Evaluation-Only (Non-Commercial)** — CC-BY-NC restriction. | Non-commercial evaluation benchmark. |

---

## 4. Student Tutoring & Socratic Pedagogy
*Capabilities: Step-by-step guidance, Socratic probing, misconception diagnosis, level-adaptive language (primary, middle, secondary, higher secondary), and encouragement.*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **Socratic Dialogue & Inquiry** | Socratic Method Conversations (HF Open) | MIT | Synthetic and curated multi-turn inquiry dialogues demonstrating guiding questions. | **Candidate for training; public model release requires provenance/license review.** | Rubric-based Socratic Fidelity: Does the model guide rather than provide direct answers? |
| **Math Tutoring with Pedagogical Scaffolding** | MathDial (Macina et al.) | CC-BY-SA 4.0 | Semi-synthetic teacher-student tutoring dialogues with explicit teacher intents, student errors, and hints. | **Candidate for training; public model release requires provenance/license review** (Note ShareAlike derivative rules). | Pedagogical Alignment Score: Hint efficacy, sub-goal generation, and tone appropriateness. |
| **Math Step-by-Step Problem Solving** | GSM8K (OpenAI) | MIT | 8,500 grade-school math word problems with human-written step-by-step solutions. | **Candidate for training; public model release requires provenance/license review.** | GSM8K Accuracy (exact match on final answer + reasoning validity). |
| **Process-Level Math Verification** | PRM800K (OpenAI) | MIT | 800k step-level correctness labels for math problem solving (process supervision). | **Candidate for training; public model release requires provenance/license review.** | Step-level error identification accuracy. |
| **Diagnostic Misconception Data** | Synthetic Pedagogical Misconception Suite | Apache-2.0 | In-house synthetic student prompts with deliberate conceptual confusions and structured tutor responses. | **Candidate for training; public model release requires provenance/license review.** | Misconception Identification Rate & Corrective Guidance Quality. |

---

## 5. Teacher Assistance & Curriculum Engineering
*Capabilities: Lesson planning (5E model), assessment item generation, rubric design, Bloom's taxonomy mapping, and educational material creation.*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **Lesson Plan Generation** | Synthetic Teacher Suite (PAUL Open Native) | Apache-2.0 | Structured in-house synthetic lesson plans with learning outcomes, activities, and formative assessments. | **Candidate for training; public model release requires provenance/license review.** | Pedagogical expert evaluation: completeness, clarity, age-appropriateness, and curriculum fit. |
| **Quiz & Assessment Construction** | Curriculum-Aligned OER Frameworks | Public Domain / CC-BY-4.0 | Diverse question templates: multiple choice, assertion-reason, short answer, case-based. | **Candidate for training; public model release requires provenance/license review.** | Bloom's Taxonomy Distribution & Distractor Plausibility Score. |
| **Rubric & Grading Matrix Generation** | Open Educational Rubric Corpus | Apache-2.0 | Multi-criteria grading rubrics with descriptive performance levels (Beginning to Exemplary). | **Candidate for training; public model release requires provenance/license review.** | Rubric structural validity & inter-rater consistency alignment. |

---

## 6. Empathy & Human-Centered Interaction
*Capabilities: Warm, patient, respectful, emotionally aware responses; active listening; validation of student frustration; strict refusal of anthropomorphic deception under the **PAUL Human-Centered Interaction / Anti-Anthropomorphism Guideline**.*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **Constructive & Helpful Dialogue** | Anthropic HH-RLHF (Open subset) | MIT | Crowdsourced human preference pairs for helpful, non-judgmental, and safe interaction. | **Candidate for training; public model release requires provenance/license review.** | Helpfulness, Harmlessness & Respectfulness win-rate against baseline. |
| **Multi-Attribute Response Quality** | HelpSteer2 (NVIDIA) | CC-BY-4.0 | Multi-attribute human ratings on helpfulness, correctness, coherence, complexity, and verbosity. | **Candidate for training; public model release requires provenance/license review.** | HelpSteer2 Reward Model alignment and tone calibration. |
| **Emotional Support Strategy Dynamics** | ESConv (Tsinghua CoAI) | CC-BY-NC-4.0 | Crowdsourced multi-turn emotional support conversations with support strategy labels. | **Evaluation-Only (Non-Commercial)** — Strategy taxonomy used for inspiration; dataset restricted from public weights. | Strategy identification; supportive tone evaluation (non-commercial benchmark). |
| **Anti-Anthropomorphism & AI Identity** | Synthetic Persona Alignment Suite (PAUL Open) | Apache-2.0 | In-house synthetic dialogues testing boundaries: validates human emotions while clarifying AI identity without pretending to possess biological life. | **Candidate for training; public model release requires provenance/license review.** | Anthropomorphism Audit: Zero false claims of human feelings, physical body, or personal life. |

---

## 7. Scientific Research Assistance
*Capabilities: Literature comprehension, multi-paper summarization, hypothesis formulation, experimental design critique, and rigorous technical communication.*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **Paper Reading & Evidence Extraction** | QASPER (AllenAI) | CC-BY-4.0 | 5,049 questions over 1,585 full open-access NLP research papers with evidence paragraph grounding. | **Candidate for training; public model release requires provenance/license review.** | F1 Answer Overlap & Evidence Retrieval Precision. |
| **Scientific Extreme Summarization** | SciTLDR (AllenAI) | Apache-2.0 | 5,400 expert-written 1-sentence summaries of scientific papers across multiple domains. | **Candidate for training; public model release requires provenance/license review.** | ROUGE-1/2/L and BERTScore on scientific summaries. |
| **Biomedical Literature QA** | PubMedQA (BioNLP) | MIT | QA pairs derived from PubMed abstracts with research reasoning and categorical answers. | **Candidate for training; public model release requires provenance/license review.** | Accuracy & Macro F1 on PubMedQA test split. |
| **Scientific Claim Verification** | SciFact (AllenAI) | CC-BY-NC 2.0 | 1.4k scientific claims paired with research abstracts, with evidence sentences and labels. | **Evaluation-Only (Non-Commercial)** — CC-BY-NC restriction. | Sentence-level claim verification F1 (Supports / Refutes / Neutral). |

---

## 8. Life Sciences, Genomics & Molecular Biology
*Capabilities: Cellular and molecular biology, genetics, genomics, biochemistry, pathways, neuroscience, therapeutics concepts, and bioinformatics reasoning.*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **Medical & Life Science Knowledge** | MedMCQA (AIIMS/NEET PG Entrance) | Apache-2.0 | 194k multiple-choice questions from Indian medical entrance exams across 21 biomedical subjects. | **Candidate for training; public model release requires provenance/license review.** | Accuracy on MedMCQA dev/test splits. |
| **Biomedical Entity & Pathway Reasoning** | Reactome & Gene Ontology Knowledgebases | CC-BY-4.0 / CC0 | Expert-curated biological pathways, reaction mechanisms, and Gene Ontology annotations. | **Candidate for training; public model release requires provenance/license review.** | Pathway participant identification & biological mechanism explanation accuracy. |
| **Therapeutics & Chemical Biology Concepts** | ChEMBL 34+ / PubChem Open Data | CC-BY-SA 4.0 / CC0 | Bioactivity measurements, drug target mechanisms, SMILES strings, and molecular properties. | **Candidate for training; public model release requires provenance/license review.** | Drug target mechanism accuracy; SMILES/chemical consistency. |
| **Therapeutics Data Commons Open Subsets** | TDC Open Benchmarks (Harvard) | MIT / BSD / CC-BY | Curated machine learning benchmarks for drug discovery (inspired by TxGemma methodology). | **Candidate for training; public model release requires provenance/license review** (Check per-subset terms). | Biochemical property prediction and reasoning. |

---

## 9. General Reasoning, Explanation & Instruction Following
*Capabilities: Multi-step logical deduction, counterfactual reasoning, structured output generation (JSON, Markdown, tables), and strict constraint satisfaction.*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **High-Complexity Competition Math** | MATH Dataset (Hendrycks et al.) | MIT | 12,500 high-school math competition problems with detailed step-by-step LaTeX solutions. | **Candidate for training; public model release requires provenance/license review.** | MATH Benchmark Accuracy across all 7 subject categories. |
| **Instruction Following & Alignment** | UltraFeedback / UltraChat (OpenBMB) | MIT | High-diversity multi-turn instructions with fine-grained aspect ratings and feedback. | **Candidate for training; public model release requires provenance/license review.** | IFEval (Instruction Following Evaluation) & MT-Bench score. |
| **Implicit Step-by-Step Logic** | StrategyQA (Geva et al.) | Apache-2.0 | Multi-step reasoning questions where the required steps are implicit and require commonsense deduction. | **Candidate for training; public model release requires provenance/license review.** | StrategyQA accuracy and step decomposition quality. |

---

## 10. Multimodal Scientific Capabilities (Gemma 4 Native)
*Capabilities: Visual question answering over scientific diagrams, plots, chemical structures, circuit diagrams, and educational charts (supported natively by Gemma 4).*

| Skill Sub-Area | Candidate Resource | Package License | Provenance & Content Origin | Training Suitability | Evaluation Task |
|---|---|---|---|---|---|
| **Scientific Chart & Plot Reasoning** | ChartQA (Masry et al.) | CC-BY-4.0 | 32,886 QA pairs on 20,904 charts requiring visual perception and arithmetic reasoning. | **Candidate for training; public model release requires provenance/license review.** | Relaxed accuracy on ChartQA test split. |
| **Visual Mathematical & Scientific QA** | MathVista (Lu et al.) | CC-BY-SA 4.0 | 6,141 diverse multimodal math and science problems from textbooks and competitions. | **Candidate for training; public model release requires provenance/license review** (Note ShareAlike terms). | Accuracy on MathVista benchmark. |
| **Structural Plot Understanding** | PlotQA (Chaudhry et al.) | MIT | 28M synthetic and web plot Q&A pairs testing structural understanding of scientific plots. | **Candidate for training; public model release requires provenance/license review.** | Plot data extraction accuracy. |
| **Multimodal Science QA** | ScienceQA (Lu et al.) | CC-BY-NC-SA 4.0 | Multimodal science questions with multi-modal lectures and explanations across grades 1–12. | **Evaluation-Only (Non-Commercial)** — Non-commercial ShareAlike restriction. | Multimodal ScienceQA accuracy across grades 1-12. |

---

## Google DeepMind / Gemma Ecosystem Separation

To maintain clear intellectual property and licensing boundaries, resources related to Google DeepMind and Gemma research are categorized into three distinct buckets:

### A. Official Methodology & Inspiration (Techniques to Study)
- **MedGemma**: Methodology for medical multimodal specialization and clinical QA grounding.
- **TxGemma**: Methodology for therapeutics instruction-tuning across small molecules, proteins, and disease targets using instruction-formatted datasets.
- **DataGemma**: Methodology for statistical grounding using Retrieval-Interleaved Generation (RIG) and Retrieval-Augmented Generation (RAG).
- **Gemma 4 Multimodal Architecture**: Unified multimodal processing, `mm_token_type_ids` input structure, and KV-sharing attention.

### B. Reusable Open Resources (Independent Permissive Licenses)
- **PubMedQA** (MIT) — Publicly available biomedical question answering.
- **MedMCQA** (Apache-2.0) — Indian medical entrance examination QA.
- **Therapeutics Data Commons Open Subsets** (MIT / BSD / CC-BY) — Open therapeutic benchmark data.
- **Gemma Open-Weights Ecosystem Recipes** (Apache-2.0) — Open fine-tuning code and cookbooks.

### C. Resources Requiring Separate License Review (Do Not Copy)
- Proprietary hospital/clinical records or electronic health records (EHR) referenced in clinical studies.
- Internal proprietary benchmark sets or non-public training mixtures.
- Commercial or non-permissive datasets that cannot be distributed under open weights.

---

## PAUL Human-Centered Interaction / Anti-Anthropomorphism Guideline

The project adheres to the **PAUL Human-Centered Interaction / Anti-Anthropomorphism Guideline**, an in-house ethical standard for conversational AI:

1. **Empathetic Attunement**: The model must acknowledge and validate user feelings, frustrations, and academic anxiety with warmth, patience, and encouragement ("I can see that this concept feels overwhelming right now; let's take it one step at a time").
2. **Strict Anti-Anthropomorphism (No Deception)**: The model must never claim biological sentience, personal feelings, a physical body, personal life experiences, or human consciousness ("As an AI assistant, I don't experience feelings, but I'm here to help you work through this").
3. **Respect for User Agency**: The model guides through Socratic inquiry rather than dictating solutions, fostering independent critical thinking.
4. **Safety & Boundaries**: Immediate, supportive refusal and referral when encountering self-harm, medical crises, or safety violations.
