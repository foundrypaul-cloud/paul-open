"""Custom training callbacks.

Includes:
- Structured logging callback
- VRAM monitoring callback
- Early stopping with patience
- Checkpoint management
- W&B conditional logging (only when WANDB_ENABLED=true)
"""
