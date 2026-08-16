"""Tests for Gemma model loader and dynamic registry."""

from paul_open_model.models.loader import (
    GemmaModelRegistry,
    GemmaModelSpec,
    ModelRole,
    load_model_config,
)


def test_registry_primary_target():
    """Verify primary target is set to Gemma 4 26B A4B IT."""
    primary = GemmaModelRegistry.get_primary_target()
    assert primary.name == "gemma-4-26b-a4b-it"
    assert primary.hf_model_id == "google/gemma-4-26B-A4B-it"
    assert primary.role == ModelRole.PRIMARY_TARGET
    assert primary.is_moe is True
    assert primary.parameter_count == "26B"
    assert primary.active_parameters == "4B"


def test_registry_development_fallback():
    """Verify development/fallback is set to Gemma 4 12B IT (Unified)."""
    dev = GemmaModelRegistry.get_development_fallback()
    assert dev.name == "gemma-4-12b-it"
    assert dev.hf_model_id == "google/gemma-4-12B-it"
    assert dev.role == ModelRole.DEVELOPMENT_FALLBACK
    assert dev.architecture == "gemma4_unified"


def test_registry_maximum_capability():
    """Verify maximum capability is set to Gemma 4 31B IT."""
    maximum = GemmaModelRegistry.get_maximum_capability()
    assert maximum.name == "gemma-4-31b-it"
    assert maximum.hf_model_id == "google/gemma-4-31B-it"
    assert maximum.role == ModelRole.MAXIMUM_CAPABILITY
    assert maximum.parameter_count == "31B"


def test_registry_edge_variants():
    """Verify edge variants (E4B, E2B) are present in the registry."""
    e4b = GemmaModelRegistry.get("gemma-4-e4b-it")
    assert e4b.role == ModelRole.EDGE_LIGHTWEIGHT
    assert e4b.parameter_count == "4.5B"

    e2b = GemmaModelRegistry.get("gemma-4-e2b-it")
    assert e2b.role == ModelRole.EDGE_ULTRALIGHT
    assert e2b.parameter_count == "2.3B"


def test_registry_aliases():
    """Verify aliases resolve correctly to canonical specs."""
    assert GemmaModelRegistry.get("primary").hf_model_id == "google/gemma-4-26B-A4B-it"
    assert GemmaModelRegistry.get("26b-moe").hf_model_id == "google/gemma-4-26B-A4B-it"
    assert GemmaModelRegistry.get("fallback").hf_model_id == "google/gemma-4-12B-it"
    assert GemmaModelRegistry.get("12b-unified").hf_model_id == "google/gemma-4-12B-it"
    assert GemmaModelRegistry.get("max").hf_model_id == "google/gemma-4-31B-it"


def test_registry_custom_registration():
    """Verify registry is dynamic and supports registering new fine-tunes or variants."""
    custom_spec = GemmaModelSpec(
        name="paul-gemma4-26b-indic-v1",
        hf_model_id="foundrypaul/paul-gemma4-26b-indic-v1",
        role=ModelRole.PRIMARY_TARGET,
        architecture="gemma4",
        parameter_count="26B",
        active_parameters="4B",
        is_moe=True,
        aliases=["paul-26b-v1"],
    )
    GemmaModelRegistry.register(custom_spec)
    assert GemmaModelRegistry.get("paul-26b-v1").name == "paul-gemma4-26b-indic-v1"


def test_load_model_configs_from_disk():
    """Verify all model YAML configs on disk load and validate."""
    models = GemmaModelRegistry.list_models()
    for spec in models.values():
        if spec.config_path:
            cfg = load_model_config(spec.config_path)
            assert cfg["hf_model_id"] == spec.hf_model_id
            assert cfg["architecture"] == spec.architecture
