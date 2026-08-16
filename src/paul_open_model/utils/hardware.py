"""Hardware detection, VRAM budgeting, and environment verification.

Supports dynamic GPU detection (Tesla T4, L4, A100, H100, RTX 3090/4090, CPU)
and matches the optimal Gemma 4 model variant to available memory constraints.
"""

import os
import platform
import sys
from dataclasses import dataclass


@dataclass
class GPUInfo:
    """Detailed hardware metadata for an available GPU."""

    index: int
    name: str
    total_memory_gb: float
    usable_memory_gb: float
    compute_capability: str
    cuda_version: str | None = None


@dataclass
class EnvironmentReport:
    """Full system and package environment verification report."""

    python_version: str
    os_platform: str
    is_colab: bool
    cuda_available: bool
    device_count: int
    gpus: list[GPUInfo]
    recommended_model: str
    recommended_role: str
    vram_assessment: str
    package_versions: dict[str, str]


def is_colab_environment() -> bool:
    """Detect if running inside Google Colab."""
    return "google.colab" in sys.modules or os.environ.get("COLAB_GPU") is not None


def get_gpu_info() -> list[GPUInfo]:
    """Retrieve detailed GPU metadata using PyTorch CUDA if available."""
    gpus: list[GPUInfo] = []
    try:
        import torch

        if torch.cuda.is_available():
            cuda_ver = torch.version.cuda
            for i in range(torch.cuda.device_count()):
                prop = torch.cuda.get_device_properties(i)
                total_gb = prop.total_memory / (1024**3)
                usable_gb = total_gb * 0.95
                cc = f"{prop.major}.{prop.minor}"
                gpus.append(
                    GPUInfo(
                        index=i,
                        name=prop.name,
                        total_memory_gb=round(total_gb, 2),
                        usable_memory_gb=round(usable_gb, 2),
                        compute_capability=cc,
                        cuda_version=cuda_ver,
                    )
                )
    except Exception:
        pass
    return gpus


def recommend_model_for_vram(usable_vram_gb: float) -> dict[str, str]:
    """Determine the safest and most capable Gemma 4 model variant for available VRAM.

    VRAM Thresholds (QLoRA 4-bit SFT fine-tuning with gradient checkpointing):
    - < 8 GB: Gemma 4 E2B IT (On-device ultralight)
    - 8 GB - 15.5 GB (e.g. Tesla T4 14.56 GiB): Gemma 4 E4B IT (Safe Development Model on T4)
    - 16 GB - 23.5 GB (e.g. L4 24GB, RTX 4090 24GB): Gemma 4 12B IT (Unified)
    - 24 GB - 47.5 GB: Gemma 4 26B A4B IT (Primary Target MoE)
    - >= 48 GB (e.g. A100 80GB, H100): Gemma 4 31B IT (Maximum Capability)
    """
    if usable_vram_gb < 8.0:
        return {
            "model_id": "google/gemma-4-E2B-it",
            "role": "edge_ultralight",
            "assessment": (
                f"Available VRAM ({usable_vram_gb:.2f} GB) is highly constrained. "
                "Recommend Gemma 4 E2B IT (~3.5 GB QLoRA training footprint)."
            ),
        }
    elif usable_vram_gb <= 15.5:
        # Standard Tesla T4 runtime (~14.56 GiB usable)
        return {
            "model_id": "google/gemma-4-E4B-it",
            "role": "edge_lightweight (Safe T4 Development Target)",
            "assessment": (
                f"Tesla T4 tier detected ({usable_vram_gb:.2f} GB usable VRAM). "
                "Gemma 4 E4B IT is the SAFE development target (~6 GB QLoRA training footprint). "
                "Gemma 4 12B IT is an EXPERIMENTAL target (requires seq_len <= 2048, batch size 1, "
                "gradient accumulation 8+, and may encounter OOM under heavy activations)."
            ),
        }
    elif usable_vram_gb < 24.0:
        return {
            "model_id": "google/gemma-4-12B-it",
            "role": "development_fallback",
            "assessment": (
                f"Mid-range GPU detected ({usable_vram_gb:.2f} GB usable VRAM). "
                "Gemma 4 12B IT (Unified) is recommended (~14 GB QLoRA training footprint)."
            ),
        }
    elif usable_vram_gb < 48.0:
        return {
            "model_id": "google/gemma-4-26B-A4B-it",
            "role": "primary_target",
            "assessment": (
                f"High-end 24-48 GB GPU detected ({usable_vram_gb:.2f} GB usable VRAM). "
                "Gemma 4 26B A4B IT (MoE Primary Target) is recommended (~22 GB QLoRA footprint)."
            ),
        }
    else:
        return {
            "model_id": "google/gemma-4-31B-it",
            "role": "maximum_capability",
            "assessment": (
                f"Enterprise GPU tier detected ({usable_vram_gb:.2f} GB usable VRAM). "
                "Gemma 4 31B IT (Maximum Capability) or full fine-tuning of 26B MoE is supported."
            ),
        }


def get_installed_package_versions() -> dict[str, str]:
    """Inspect installed versions of core ML dependencies."""
    package_map = {
        "torch": "torch",
        "transformers": "transformers",
        "peft": "peft",
        "trl": "trl",
        "bitsandbytes": "bitsandbytes",
        "accelerate": "accelerate",
        "datasets": "datasets",
        "huggingface_hub": "huggingface_hub",
        "tensorboard": "tensorboard",
        "yaml": "pyyaml",
        "rich": "rich",
        "sentencepiece": "sentencepiece",
        "tokenizers": "tokenizers",
    }
    versions: dict[str, str] = {}
    for import_name, display_name in package_map.items():
        try:
            mod = __import__(import_name)
            ver = getattr(mod, "__version__", "installed")
            versions[display_name] = str(ver)
        except ImportError:
            versions[display_name] = "not installed"
    return versions


def verify_environment() -> EnvironmentReport:
    """Generate a complete environment verification report."""
    gpus = get_gpu_info()
    cuda_avail = len(gpus) > 0
    total_usable_vram = sum(g.usable_memory_gb for g in gpus) if gpus else 0.0

    if cuda_avail:
        rec = recommend_model_for_vram(total_usable_vram)
    else:
        rec = {
            "model_id": "google/gemma-4-E2B-it",
            "role": "cpu_development_only",
            "assessment": (
                "No CUDA GPU detected. System is suitable for code development, "
                "config validation, and testing only. Remote GPU required for training."
            ),
        }

    return EnvironmentReport(
        python_version=platform.python_version(),
        os_platform=platform.platform(),
        is_colab=is_colab_environment(),
        cuda_available=cuda_avail,
        device_count=len(gpus),
        gpus=gpus,
        recommended_model=rec["model_id"],
        recommended_role=rec["role"],
        vram_assessment=rec["assessment"],
        package_versions=get_installed_package_versions(),
    )


def print_environment_report(report: EnvironmentReport | None = None) -> None:
    """Print formatted environment report to console."""
    if report is None:
        report = verify_environment()

    print("=" * 70)
    print(" PAUL OPEN MODEL — ENVIRONMENT & HARDWARE VERIFICATION")
    print("=" * 70)
    print(f" Python Version : {report.python_version} (Target: >=3.12,<3.13)")
    print(f" OS / Platform  : {report.os_platform}")
    print(f" Colab Runtime  : {'Yes' if report.is_colab else 'No (Local / Dedicated Host)'}")
    print(f" CUDA Available : {'Yes' if report.cuda_available else 'No'}")
    print(f" GPU Devices    : {report.device_count}")

    if report.gpus:
        for gpu in report.gpus:
            print(
                f"   [GPU {gpu.index}] {gpu.name} | Compute {gpu.compute_capability} | "
                f"Total VRAM: {gpu.total_memory_gb:.2f} GB | "
                f"Usable: {gpu.usable_memory_gb:.2f} GB | "
                f"CUDA: {gpu.cuda_version}"
            )
    print("-" * 70)
    print(f" Recommended Model : {report.recommended_model}")
    print(f" Target Role       : {report.recommended_role}")
    print(f" Memory Assessment : {report.vram_assessment}")
    print("-" * 70)
    print(" Installed Key Packages:")
    for pkg, ver in sorted(report.package_versions.items()):
        print(f"   - {pkg:<18}: {ver}")
    print("=" * 70)
