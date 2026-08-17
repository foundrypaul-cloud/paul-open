"""Benchmark leakage detection and isolation framework for PAUL Open Model.

Ensures absolute separation between training/eval data and Canonical Benchmark v1.0.0.
Performs read-only inspection against baseline_suite_v1.json using:
1. Exact prompt matching
2. Word-level 3-gram & 4-gram overlap coefficient
3. Numerical parameter matching (e.g. identical velocity/time values)
4. Vector cosine similarity interface with content word filtering
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_BENCHMARK_PATH = Path("src/paul_open_model/evaluation/data/baseline_suite_v1.json")

# Overlap thresholds for flagging potential leakage
EXACT_MATCH_THRESHOLD = 1.0
NGRAM_OVERLAP_THRESHOLD = 0.35
SIMILARITY_SCORE_THRESHOLD = 0.40

# Universal function/stop words to filter from bag-of-words cosine computation
UNIVERSAL_STOP_WORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "in",
    "on",
    "at",
    "to",
    "for",
    "with",
    "by",
    "as",
    "is",
    "are",
    "was",
    "were",
    "it",
    "its",
    "that",
    "this",
    "these",
    "those",
    "how",
    "what",
    "why",
    "which",
    "does",
    "do",
    "from",
    "into",
    "their",
    "your",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "can",
    "will",
    "would",
    "should",
    "could",
    "का",
    "के",
    "की",
    "में",
    "से",
    "को",
    "पर",
    "और",
    "या",
    "है",
    "हैं",
    "था",
    "थी",
    "थे",
    "लिए",
    "एक",
    "यह",
    "वह",
    "इस",
    "उस",
    "जो",
    "तो",
    "ही",
    "भी",
    "एवं",
    "तथा",
    "এই",
    "সেই",
    "এর",
    "এবং",
    "বা",
    "হলো",
    "হয়",
    "আছে",
    "ছিল",
    "থেকে",
    "দ্বারা",
    "জন্য",
}


@dataclass
class LeakageAuditResult:
    """Outcome of checking a single candidate prompt against the benchmark suite."""

    candidate_id: str
    has_leakage: bool
    highest_similarity: float
    matched_benchmark_id: str | None = None
    leakage_type: str | None = None
    details: str = ""
    flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "has_leakage": self.has_leakage,
            "highest_similarity": round(self.highest_similarity, 4),
            "matched_benchmark_id": self.matched_benchmark_id,
            "leakage_type": self.leakage_type,
            "details": self.details,
            "flags": self.flags,
        }


def tokenize_words(text: str) -> list[str]:
    """Tokenize text into full words across Latin, Indic, and general Unicode scripts."""
    raw_tokens = re.findall(r"[^\s\d\.,;:!\?\"\'\(\)\[\]\{\}\<\>\\\/\-\+=_।॥`]+", text.lower())
    return [w.strip() for w in raw_tokens if len(w.strip()) > 0]


def extract_numerical_parameters(text: str) -> set[str]:
    """Extract numeric tokens and numeric+unit compounds from a text string."""
    text_clean = text.lower()
    compounds = re.findall(
        r"\b\d+(?:\.\d+)?\s*(?:m/s\^2|m/s|km/h|°c|k|j|kj|n|kg|g|s|seconds|meters|minutes|hrs|%)?\b",
        text_clean,
    )
    results: set[str] = set()
    for c in compounds:
        c_norm = re.sub(r"\s+", "_", c.strip())
        if c_norm and re.search(r"\d", c_norm):
            results.add(c_norm)
    return results


def get_ngrams(words: list[str], n: int) -> set[tuple[str, ...]]:
    """Generate n-grams from a list of words."""
    if len(words) < n:
        return set()
    return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}


def compute_ngram_overlap(text1: str, text2: str, n: int = 3) -> float:
    """Compute Jaccard overlap coefficient between word n-grams of two texts."""
    words1 = tokenize_words(text1)
    words2 = tokenize_words(text2)

    ngrams1 = get_ngrams(words1, n)
    ngrams2 = get_ngrams(words2, n)

    if not ngrams1 or not ngrams2:
        return 0.0

    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    return intersection / union if union > 0 else 0.0


def compute_tfidf_cosine_similarity(text1: str, text2: str) -> float:
    """Compute word-level cosine similarity over content words (excluding stopwords)."""
    words1 = [w for w in tokenize_words(text1) if len(w) > 1 and w not in UNIVERSAL_STOP_WORDS]
    words2 = [w for w in tokenize_words(text2) if len(w) > 1 and w not in UNIVERSAL_STOP_WORDS]

    if not words1 or not words2:
        return 0.0

    vec1 = Counter(words1)
    vec2 = Counter(words2)

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[x] * vec2[x] for x in intersection)

    sum1 = sum(vec1[x] ** 2 for x in vec1)
    sum2 = sum(vec2[x] ** 2 for x in vec2)
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator / denominator)


class BenchmarkLeakageChecker:
    """Audits candidate training/eval examples against Canonical Benchmark v1.0.0."""

    def __init__(self, benchmark_path: Path | str = DEFAULT_BENCHMARK_PATH) -> None:
        self.benchmark_path = Path(benchmark_path)
        if not self.benchmark_path.exists():
            raise FileNotFoundError(
                f"Canonical benchmark file not found at: {self.benchmark_path}. "
                "Ensure baseline_suite_v1.json exists in read-only location."
            )

        with open(self.benchmark_path, encoding="utf-8") as f:
            self.suite_data = json.load(f)

        self.cases = self.suite_data.get("cases", [])
        self.version = self.suite_data.get("version", "1.0.0")

    def check_text(
        self,
        candidate_text: str,
        candidate_id: str = "CANDIDATE",
        domain: str = "",
        language: str = "",
    ) -> LeakageAuditResult:
        """Check a single candidate prompt against all cases in the benchmark."""
        cand_clean = candidate_text.strip().lower()
        cand_params = extract_numerical_parameters(candidate_text)

        highest_sim = 0.0
        best_match_id: str | None = None
        leakage_type: str | None = None
        flags: list[str] = []

        for b_case in self.cases:
            b_id = b_case["case_id"]
            b_prompt = b_case["prompt"].strip()
            b_clean = b_prompt.lower()

            # 1. Exact Match Check
            if cand_clean == b_clean or (
                len(cand_clean) > 25 and (cand_clean in b_clean or b_clean in cand_clean)
            ):
                return LeakageAuditResult(
                    candidate_id=candidate_id,
                    has_leakage=True,
                    highest_similarity=1.0,
                    matched_benchmark_id=b_id,
                    leakage_type="exact_match",
                    details=f"Exact match or substring containment with benchmark case {b_id}.",
                    flags=[f"CRITICAL: Exact match with {b_id}"],
                )

            # 2. N-Gram Overlap Check (3-grams and 4-grams)
            overlap_3g = compute_ngram_overlap(candidate_text, b_prompt, n=3)
            overlap_4g = compute_ngram_overlap(candidate_text, b_prompt, n=4)
            sim_score = compute_tfidf_cosine_similarity(candidate_text, b_prompt)

            max_overlap = max(overlap_3g, overlap_4g, sim_score)

            if max_overlap > highest_sim:
                highest_sim = max_overlap
                best_match_id = b_id

            if overlap_3g > NGRAM_OVERLAP_THRESHOLD:
                flags.append(f"High 3-gram overlap ({overlap_3g:.1%}) with {b_id}")
                if not leakage_type:
                    leakage_type = "ngram_overlap"

            # 3. Numerical Parameter Check
            if domain and domain == b_case.get("domain"):
                b_params = extract_numerical_parameters(b_prompt)
                param_intersection = cand_params & b_params
                if len(param_intersection) >= 2:
                    params_str = ", ".join(sorted(param_intersection))
                    flags.append(f"Parameter collision with {b_id} (shared: {params_str})")
                    if not leakage_type:
                        leakage_type = "parameter_overlap"

        has_leakage = len(flags) > 0 or highest_sim >= SIMILARITY_SCORE_THRESHOLD

        if has_leakage:
            if not leakage_type:
                leakage_type = "semantic_similarity"
            details = (
                f"Leakage flagged against benchmark case {best_match_id} "
                f"(score: {highest_sim:.2f})."
            )
        else:
            details = (
                f"Clean. Highest similarity with benchmark was {highest_sim:.2f} "
                f"(Case {best_match_id})."
            )

        return LeakageAuditResult(
            candidate_id=candidate_id,
            has_leakage=has_leakage,
            highest_similarity=highest_sim,
            matched_benchmark_id=best_match_id,
            leakage_type=leakage_type,
            details=details,
            flags=flags,
        )

    def audit_dataset_file(self, filepath: Path | str) -> dict[str, Any]:
        """Audit an entire dataset or benchmark suite file for benchmark contamination."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        content = path.read_text(encoding="utf-8")
        items: list[dict[str, Any]] = []

        if path.suffix == ".jsonl":
            for line in content.splitlines():
                if line.strip():
                    items.append(json.loads(line.strip()))
        else:
            loaded = json.loads(content)
            if isinstance(loaded, dict) and "cases" in loaded and isinstance(loaded["cases"], list):
                items = loaded["cases"]
            elif isinstance(loaded, list):
                items = loaded
            else:
                items = [loaded]

        results: list[LeakageAuditResult] = []
        for item in items:
            cid = str(item.get("id", item.get("case_id", "UNKNOWN")))
            domain = str(item.get("domain", ""))
            language = str(item.get("language", ""))

            prompt_text = ""
            if "messages" in item and isinstance(item["messages"], list):
                user_turns = [
                    m.get("content", "") for m in item["messages"] if m.get("role") == "user"
                ]
                prompt_text = "\n".join(user_turns)
            elif "prompt" in item:
                prompt_text = str(item["prompt"])

            res = self.check_text(prompt_text, candidate_id=cid, domain=domain, language=language)
            results.append(res)

        leakage_count = sum(1 for r in results if r.has_leakage)

        return {
            "file": str(path),
            "total_items_audited": len(results),
            "leakage_free_count": len(results) - leakage_count,
            "leakage_detected_count": leakage_count,
            "is_clean": leakage_count == 0,
            "benchmark_version_checked": self.version,
            "results": [r.to_dict() for r in results],
        }
