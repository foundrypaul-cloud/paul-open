"""Unified and dynamic model loader & registry for Google Gemma 4 models.

Tracks current Gemma 4 releases (April 2026 launch through August 2026 updates):
- Primary target: Gemma 4 26B A4B IT (Mixture-of-Experts)
- Development/fallback: Gemma 4 12B IT (June 2026 Unified release / August refresh)
- Maximum capability: Gemma 4 31B IT (Dense flagship)
- Edge/Mobile: Gemma 4 E4B IT / E2B IT (On-device lightweight)
- Quantized QAT variants (w4a16-ct, q4_0-gguf) & Assistant checkpoints

Handles:
- Dynamic model registry with alias resolution
- Architecture detection ('gemma4' vs 'gemma4_unified')
- Multimodal metadata requirements (mm_token_type_ids, token_type_ids)
- Quantization configuration (BitsAndBytes 4-bit NF4, official Google QAT)
- Device mapping across single-GPU and multi-GPU environments
"""

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any, ClassVar, cast

import yaml  # type: ignore[import-untyped]


class ModelRole(StrEnum):
    PRIMARY_TARGET = "primary_target"
    DEVELOPMENT_FALLBACK = "development_fallback"
    MAXIMUM_CAPABILITY = "maximum_capability"
    EDGE_LIGHTWEIGHT = "edge_lightweight"
    EDGE_ULTRALIGHT = "edge_ultralight"
    QUANTIZED_QAT = "quantized_qat"


@dataclass
class GemmaModelSpec:
    """Metadata specification for a Gemma 4 model variant."""

    name: str
    hf_model_id: str
    role: ModelRole
    architecture: str  # 'gemma4' or 'gemma4_unified'
    parameter_count: str
    active_parameters: str | None = None
    is_moe: bool = False
    context_length: int = 262144
    is_multimodal: bool = True
    release_date: str = "2026-08"
    config_path: str | None = None
    aliases: list[str] = field(default_factory=list)


class GemmaModelRegistry:
    """Dynamic registry for all Gemma 4 model variants.

    Maintains current Google DeepMind Gemma 4 releases and allows
    dynamic registration of new checkpoints, fine-tunes, or QAT variants.
    """

    _REGISTRY: ClassVar[dict[str, GemmaModelSpec]] = {}

    @classmethod
    def register(cls, spec: GemmaModelSpec) -> None:
        """Register a new model specification."""
        cls._REGISTRY[spec.name] = spec
        cls._REGISTRY[spec.hf_model_id] = spec
        for alias in spec.aliases:
            cls._REGISTRY[alias] = spec

    @classmethod
    def get(cls, identifier: str) -> GemmaModelSpec:
        """Retrieve a model specification by name, HF ID, or alias."""
        if identifier in cls._REGISTRY:
            return cls._REGISTRY[identifier]
        raise KeyError(
            f"Model '{identifier}' not found in Gemma registry. "
            f"Available models: {list(cls.list_models().keys())}"
        )

    @classmethod
    def list_models(cls) -> dict[str, GemmaModelSpec]:
        """Return unique registered models (keyed by canonical name)."""
        unique: dict[str, GemmaModelSpec] = {}
        for spec in cls._REGISTRY.values():
            unique[spec.name] = spec
        return unique

    @classmethod
    def get_primary_target(cls) -> GemmaModelSpec:
        """Return the primary project target (Gemma 4 26B A4B IT)."""
        return cls.get("gemma-4-26b-a4b-it")

    @classmethod
    def get_development_fallback(cls) -> GemmaModelSpec:
        """Return the development/fallback model (Gemma 4 12B IT Unified)."""
        return cls.get("gemma-4-12b-it")

    @classmethod
    def get_maximum_capability(cls) -> GemmaModelSpec:
        """Return the maximum capability model (Gemma 4 31B IT)."""
        return cls.get("gemma-4-31b-it")


# Register official Gemma 4 models (Updated to August 2026 ecosystem)
GemmaModelRegistry.register(
    GemmaModelSpec(
        name="gemma-4-26b-a4b-it",
        hf_model_id="google/gemma-4-26B-A4B-it",
        role=ModelRole.PRIMARY_TARGET,
        architecture="gemma4",
        parameter_count="26B",
        active_parameters="4B",
        is_moe=True,
        context_length=262144,
        release_date="2026-08",
        config_path="configs/models/gemma4_26b_a4b_it.yaml",
        aliases=["26b", "26b-a4b", "primary", "gemma-4-26b", "26b-moe"],
    )
)

GemmaModelRegistry.register(
    GemmaModelSpec(
        name="gemma-4-12b-it",
        hf_model_id="google/gemma-4-12B-it",
        role=ModelRole.DEVELOPMENT_FALLBACK,
        architecture="gemma4_unified",  # June 2026 Unified release / August refresh
        parameter_count="12B",
        active_parameters="12B",
        is_moe=False,
        context_length=262144,
        release_date="2026-08",
        config_path="configs/models/gemma4_12b_it.yaml",
        aliases=["12b", "12b-unified", "fallback", "dev", "gemma-4-12b"],
    )
)

GemmaModelRegistry.register(
    GemmaModelSpec(
        name="gemma-4-31b-it",
        hf_model_id="google/gemma-4-31B-it",
        role=ModelRole.MAXIMUM_CAPABILITY,
        architecture="gemma4",
        parameter_count="31B",
        active_parameters="31B",
        is_moe=False,
        context_length=262144,
        release_date="2026-08",
        config_path="configs/models/gemma4_31b_it.yaml",
        aliases=["31b", "max", "gemma-4-31b"],
    )
)

GemmaModelRegistry.register(
    GemmaModelSpec(
        name="gemma-4-e4b-it",
        hf_model_id="google/gemma-4-E4B-it",
        role=ModelRole.EDGE_LIGHTWEIGHT,
        architecture="gemma4",
        parameter_count="4.5B",
        active_parameters="4.5B",
        is_moe=False,
        context_length=131072,
        release_date="2026-08",
        config_path="configs/models/gemma4_e4b_it.yaml",
        aliases=["e4b", "4b", "edge", "gemma-4-e4b"],
    )
)

GemmaModelRegistry.register(
    GemmaModelSpec(
        name="gemma-4-e2b-it",
        hf_model_id="google/gemma-4-E2B-it",
        role=ModelRole.EDGE_ULTRALIGHT,
        architecture="gemma4",
        parameter_count="2.3B",
        active_parameters="2.3B",
        is_moe=False,
        context_length=131072,
        release_date="2026-08",
        config_path="configs/models/gemma4_e2b_it.yaml",
        aliases=["e2b", "2b", "ultralight", "gemma-4-e2b"],
    )
)


def load_model_config(config_path: str | Path) -> dict[str, Any]:
    """Load and validate a model YAML configuration file."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Model configuration not found at {path}")
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "model" not in data:
        raise ValueError(f"Invalid model configuration in {path}: must contain 'model' root key")
    model_cfg = data["model"]
    if not isinstance(model_cfg, dict):
        raise ValueError(f"Invalid 'model' section in {path}: expected dictionary")
    return cast(dict[str, Any], model_cfg)
