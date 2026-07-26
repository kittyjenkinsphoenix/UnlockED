# Branching Strategy

## Branch Naming

Use short, lower-case branch names with a prefix that describes the work:

- `feature/...` for new functionality
- `fix/...` for bug fixes
- `docs/...` for documentation-only changes
- `refactor/...` for internal structure changes

## Commit Conventions

Keep commits small and meaningful.

- Start commit messages with an action verb
- Mention the scope when possible
- Avoid vague messages such as `update` or `changes`

Examples:

- `Refactor quiz scoring service`
- `Add PostgreSQL configuration`
- `Improve dashboard accessibility`

## Pull Request Workflow

1. Create a feature branch from `main`.
2. Make a focused change set.
3. Run `pytest`, `black`, `isort`, and `flake8` locally.
4. Open a PR with a short summary, screenshots if relevant, and test evidence.
5. Request review before merging.
