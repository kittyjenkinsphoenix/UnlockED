# Coding Standards

## General Rules

- Prefer small, focused functions and modules
- Keep route handlers thin and move logic into services
- Use repositories for database access
- Write docstrings for public functions, classes, routes, and services

## Python Conventions

- Follow PEP 8
- Use snake_case for functions and variables
- Use PascalCase for classes
- Keep imports sorted with `isort`
- Format code with `black`

## Branching and Commits

- Branch names should be short and descriptive, such as `feature/quiz-refactor` or `fix/login-validation`
- Commit messages should be imperative and specific, such as `Refactor quiz scoring service`
- Pull requests should describe the change, include testing evidence, and mention any user-facing impact

## Security Practices

- Never commit `.env`
- Keep secrets in environment variables only
- Hash passwords and validate inputs before persistence
- Use role checks for sensitive routes
