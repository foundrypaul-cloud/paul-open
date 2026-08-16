"""PAUL Open Model Baseline Benchmark Suite (v1.0.0).

Defines curated, version-controlled, original benchmark cases across 10 capability domains
and 10 languages for evaluating Gemma 4 baseline capabilities and future fine-tuned checkpoints.
"""

import json
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

BASELINE_VERSION = "1.0.0"
_DATA_PATH = Path(__file__).parent / "data" / "baseline_suite_v1.json"


class CapabilityDomain(StrEnum):
    """Core research capability domains for PAUL Open Model."""

    SCIENCE_REASONING = "science_reasoning"
    LIFE_SCIENCES = "life_sciences"
    SCIENTIFIC_RESEARCH = "scientific_research"
    SOCRATIC_TUTORING = "socratic_tutoring"
    STUDENT_ASSISTANCE = "student_assistance"
    TEACHER_ASSISTANCE = "teacher_assistance"
    INDIC_UNDERSTANDING = "indic_understanding"
    MULTILINGUAL_TRANSLATION = "multilingual_translation"
    EMPATHY_HUMAN_CENTERED = "empathy_human_centered"
    SCIENTIFIC_EXPLANATION = "scientific_explanation"


class DifficultyLevel(StrEnum):
    """Pedagogical and cognitive difficulty level."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class BenchmarkCase:
    """A single evaluation case within the benchmark suite."""

    case_id: str
    domain: CapabilityDomain
    language: str  # ISO code: 'en', 'hi', 'bn', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa'
    language_name: str
    prompt: str
    expected_criteria: list[str]
    difficulty: DifficultyLevel
    safety_considerations: list[str] = field(default_factory=list)
    rubric_keywords: list[str] = field(default_factory=list)
    forbidden_phrases: list[str] = field(default_factory=list)
    expected_script: str | None = None
    min_response_tokens: int = 15
    max_response_tokens: int = 400

    def to_dict(self) -> dict[str, Any]:
        """Serialize case to dictionary."""
        return {
            "case_id": self.case_id,
            "domain": self.domain.value,
            "language": self.language,
            "language_name": self.language_name,
            "prompt": self.prompt,
            "expected_criteria": self.expected_criteria,
            "difficulty": self.difficulty.value,
            "safety_considerations": self.safety_considerations,
            "rubric_keywords": self.rubric_keywords,
            "forbidden_phrases": self.forbidden_phrases,
            "expected_script": self.expected_script,
            "min_response_tokens": self.min_response_tokens,
            "max_response_tokens": self.max_response_tokens,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BenchmarkCase":
        """Construct BenchmarkCase from dictionary."""
        return cls(
            case_id=data["case_id"],
            domain=CapabilityDomain(data["domain"]),
            language=data["language"],
            language_name=data["language_name"],
            prompt=data["prompt"],
            expected_criteria=data["expected_criteria"],
            difficulty=DifficultyLevel(data["difficulty"]),
            safety_considerations=data.get("safety_considerations", []),
            rubric_keywords=data.get("rubric_keywords", []),
            forbidden_phrases=data.get("forbidden_phrases", []),
            expected_script=data.get("expected_script"),
            min_response_tokens=data.get("min_response_tokens", 15),
            max_response_tokens=data.get("max_response_tokens", 400),
        )


@dataclass
class BenchmarkSuite:
    """Collection of benchmark cases representing a full evaluation run."""

    version: str = BASELINE_VERSION
    cases: list[BenchmarkCase] = field(default_factory=list)

    def filter_by_domain(self, domain: CapabilityDomain) -> list[BenchmarkCase]:
        """Return all cases belonging to a specific capability domain."""
        return [c for c in self.cases if c.domain == domain]

    def filter_by_language(self, language_code: str) -> list[BenchmarkCase]:
        """Return all cases for a specific language code."""
        return [c for c in self.cases if c.language.lower() == language_code.lower()]

    def filter_by_difficulty(self, difficulty: DifficultyLevel) -> list[BenchmarkCase]:
        """Return all cases matching a difficulty level."""
        return [c for c in self.cases if c.difficulty == difficulty]

    def get_case(self, case_id: str) -> BenchmarkCase | None:
        """Find a case by its unique ID."""
        for c in self.cases:
            if c.case_id == case_id:
                return c
        return None

    def __len__(self) -> int:
        return len(self.cases)

    def to_dict(self) -> dict[str, Any]:
        """Serialize benchmark suite to dictionary."""
        return {
            "version": self.version,
            "case_count": len(self.cases),
            "cases": [c.to_dict() for c in self.cases],
        }

    def save_json(self, path: str | Path) -> None:
        """Save benchmark suite to JSON file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


def get_baseline_benchmark_suite(
    version: str = BASELINE_VERSION, data_path: str | Path | None = None
) -> BenchmarkSuite:
    """Return the official versioned PAUL Open Model baseline benchmark suite."""
    target_path = Path(data_path or _DATA_PATH)
    if not target_path.exists():
        raise FileNotFoundError(f"Baseline benchmark data file not found at: {target_path}")

    with open(target_path, encoding="utf-8") as f:
        data = json.load(f)

    cases = [BenchmarkCase.from_dict(c) for c in data.get("cases", [])]
    return BenchmarkSuite(version=version, cases=cases)
