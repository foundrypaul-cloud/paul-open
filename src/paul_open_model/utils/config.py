"""YAML configuration loading and validation.

Loads model, training, data, and evaluation configs from configs/ directory.
Validates against Pydantic schemas to catch misconfigurations early.
Supports environment variable overrides via python-dotenv.
"""
