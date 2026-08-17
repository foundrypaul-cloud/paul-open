# PAUL Open Model — Phase 3 Data Validation & Quality Guide

This guide documents the data infrastructure, schemas, validation tools, and leakage prevention systems for Phase 3 dataset curation.

---

## 1. The Tri-Tier Validation Architecture

To ensure high data quality without brittle or overly rigid heuristic rejections, dataset validation is organized into three operational tiers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TRI-TIER VALIDATION TAXONOMY                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [TIER 1: HARD VALIDITY CONSTRAINTS] ──► AUTO-REJECT (Exit Code 1)          │
│  • JSON / JSONL syntax and UTF-8 encoding integrity                         │
│  • Required schema fields (id, track, domain, language, messages, metadata) │
│  • Non-empty prompt and response strings                                    │
│  • Token length budget adherence (< 350 tokens per single turn)             │
│                                                                             │
│  [TIER 2: HEURISTIC SCREENING SIGNALS] ──► WARNING FLAGS (Non-Blocking)     │
│  • Socratic structural question parser (verifies trailing guided probe)     │
│  • Clean translation parser with math/scientific acronym whitelist          │
│  • STEM numerical preamble density (< 25 words before calculation)          │
│  • Highlighted / boxed final answer with SI units                           │
│                                                                             │
│  [TIER 3: HUMAN-EXPERT REVIEW WORKFLOW] ──► MANDATORY SIGN-OFF              │
│  • Reviewer identity, review notes, timestamp, approval boolean             │
│  • Pedagogical plausibility and classroom register validation               │
│  • Mathematical, dimensional, and formula correctness verification          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. CLI Validation Tooling

The repository provides two dedicated CLI tools under [`scripts/`](file:///home/paul-foundry/Projects/Open%20Source/PAUL%20Open/paul-open/scripts):

### A. Dataset Validator (`scripts/validate_dataset.py`)

Validates an entire dataset file (JSON or JSONL) against the official schemas and tri-tier quality checks:

```bash
# Validate SFT dataset (JSON or JSONL) with default 350-token limit
uv run python scripts/validate_dataset.py data/pilot/sft/socratic_tutoring.jsonl --type sft

# Validate DPO preference pairs
uv run python scripts/validate_dataset.py data/pilot/dpo/socratic_dpo.jsonl --type dpo

# Custom token limit override (e.g. 500 tokens for long-context tasks)
uv run python scripts/validate_dataset.py data/pilot/sft/stem_calc.jsonl --max-tokens 500

# Verbose output with per-record findings and JSON report export
uv run python scripts/validate_dataset.py data/pilot/sft/stem_calc.jsonl --verbose --json-output report.json
```

**Exit Codes**:
- `0`: All Tier 1 hard constraints passed (file is structurally sound).
- `1`: One or more Tier 1 hard errors encountered (file rejected).

---

### B. Benchmark Leakage Checker (`scripts/check_leakage.py`)

Audits candidate training examples against the **Canonical Benchmark v1.0.0** ([`src/paul_open_model/evaluation/data/baseline_suite_v1.json`](file:///home/paul-foundry/Projects/Open%20Source/PAUL%20Open/paul-open/src/paul_open_model/evaluation/data/baseline_suite_v1.json)) in strictly read-only mode:

```bash
# Audit a complete dataset file for benchmark leakage
uv run python scripts/check_leakage.py data/pilot/sft/socratic_tutoring.jsonl

# Audit a single candidate prompt string
uv run python scripts/check_leakage.py "A block of ice at 0°C is placed with water at 0°C..."

# Export detailed leakage audit to JSON
uv run python scripts/check_leakage.py data/pilot/sft/all_pilot.jsonl --json-output leakage_report.json
```

**Leakage Detection Modes**:
1. **Exact Match**: Flags identical prompts or direct substring containment.
2. **N-Gram Overlap**: Computes 3-gram and 4-gram Jaccard overlap (flags $> 35\%$ overlap).
3. **Parameter Collision**: Extracts numeric+unit pairs (e.g. $20\text{ m/s}, 5\text{ s}$) and detects domain collisions.
4. **Cosine Similarity**: Vector-space similarity interface with zero external dependency fallback.

---

## 3. JSON Schemas

Official schemas are located in [`data/schemas/`](file:///home/paul-foundry/Projects/Open%20Source/PAUL%20Open/paul-open/data/schemas):

### SFT Schema ([`data/schemas/sft_schema.json`](file:///home/paul-foundry/Projects/Open%20Source/PAUL%20Open/paul-open/data/schemas/sft_schema.json))
```json
{
  "id": "paul_sft_physics_optics_001",
  "track": "socratic_tutoring",
  "domain": "physics",
  "subdomain": "optics",
  "language": "en",
  "messages": [
    {
      "role": "user",
      "content": "Why does a pencil look bent in water?"
    },
    {
      "role": "assistant",
      "content": "When light passes from air into water, its speed changes. Think about running on a road and stepping into shallow water—what happens to your direction when one foot slows down first?"
    }
  ],
  "metadata": {
    "target_grade": "middle_school",
    "difficulty": "basic",
    "misconception_tag": "refraction_optical_density",
    "human_verified": true,
    "benchmark_leakage_checked": true,
    "reviewer_id": "reviewer_stem_01",
    "review_status": "approved",
    "review_notes": "Clean thought experiment, single trailing probe.",
    "review_timestamp": "2026-08-16T12:00:00Z",
    "approved": true
  }
}
```

### DPO Schema ([`data/schemas/dpo_schema.json`](file:///home/paul-foundry/Projects/Open%20Source/PAUL%20Open/paul-open/data/schemas/dpo_schema.json))
```json
{
  "id": "paul_dpo_physics_calc_001",
  "track": "concise_stem_calc",
  "domain": "physics",
  "language": "en",
  "prompt": "Calculate the kinetic energy of a 2 kg cart moving at 3 m/s.",
  "chosen": "### Given: $m = 2\\text{ kg}, v = 3\\text{ m/s}$\n$$KE = \\frac{1}{2}mv^2 = \\frac{1}{2}(2)(3)^2 = \\mathbf{9\\text{ J}}$$\n**Final Answer:** $\\mathbf{9\\text{ J}}$",
  "rejected": "Kinetic energy is the energy possessed by an object due to its motion. In classical mechanics, whenever a particle moves with speed v, it possesses energy proportional to the square of velocity. The answer is 9 J.",
  "rejection_reason": "preamble_verbosity_truncation",
  "metadata": {
    "difficulty": "basic",
    "human_verified": true,
    "benchmark_leakage_checked": true,
    "reviewer_id": "reviewer_stem_01",
    "review_status": "approved",
    "approved": true
  }
}
```

---

## 4. Human Review (Tier 3) Metadata Workflow

Every candidate example in the pilot dataset includes a machine-readable `metadata` block to track human verification:

| Field | Type | Description |
|---|---|---|
| `reviewer_id` | `string` | Unique identifier of the human reviewer (e.g. `reviewer_hindi_02`). |
| `review_status` | `enum` | `pending` $\to$ `in_review` $\to$ `approved` / `rejected` / `needs_revision`. |
| `review_notes` | `string` | Notes explaining why an example was approved, edited, or rejected. |
| `review_timestamp` | `string (ISO-8601)` | Timestamp when the human review was completed. |
| `approved` | `boolean` | Hard gate: `true` indicates readiness for training inclusion. |
