# Contributing to PAUL Open Model

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/foundrypaul-cloud/paul-open.git
cd paul-open
uv sync --extra all
```

## Code Standards

- **Formatting**: `uv run ruff format .`
- **Linting**: `uv run ruff check .`
- **Type checking**: `uv run mypy src/`
- **Testing**: `uv run pytest`

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all checks pass
4. Submit a PR with a clear description

## Code of Conduct

Be respectful, inclusive, and constructive.
