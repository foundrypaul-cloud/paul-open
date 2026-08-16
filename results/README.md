# Results Directory

Training outputs, checkpoints, and evaluation results are saved here.

This directory is gitignored except for this README and .gitkeep.

## Convention

Each experiment creates a subdirectory:
```
results/
├── experiment_name_YYYYMMDD_HHMMSS/
│   ├── checkpoints/
│   ├── logs/
│   ├── eval/
│   └── config_snapshot.yaml
```
