# UnlockED

UnlockED is a Flask web application that raises awareness of global education inequality and Sustainable Development Goal 4. It combines educational content, a quiz, a personal dashboard, a take-action mailing list, and an admin view for project oversight.

## Project Overview

The application is organised as a layered Flask codebase:

- HTTP routes live in [app/routes](app/routes)
- Business logic lives in [app/services](app/services)
- Database access lives in [app/repositories](app/repositories)
- Shared helpers live in [app/utils](app/utils)
- Database models live in [app/models.py](app/models.py)

The main application factory is in [app/__init__.py](app/__init__.py), and environment-specific configuration is in [config.py](config.py).

## Architecture Overview

The request flow is intentionally simple:

1. A route receives the request.
2. The route validates and coordinates the request/response cycle.
3. A service performs the business logic.
4. A repository handles database reads and writes.
5. A template renders the final response.

This keeps each file focused on one responsibility and makes the project easier to test and extend.

See the full write-up in [docs/architecture.md](docs/architecture.md).

## Key Features

- User registration, login, logout, and password changes
- Role-based access control for user, moderator, and admin pages
- SDG 4 homepage content and visualised statistics
- Interactive quiz with saved attempts and score history
- Take-action subscription flow with unsubscribe tokens
- Admin dashboard with user and log-file visibility
- CSRF protection, password hashing, and rate limiting

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/newcastleuniversity-computing/csc2033_team27_quality-education-awareness
cd csc2033_team27_quality-education-awareness
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Configure environment variables

Copy [`.env.example`](.env.example) to `.env` and fill in the values you need for local development.

The application supports PostgreSQL through `DATABASE_URL` and falls back to SQLite when that variable is not set.

### 5. Run the development server

```bash
python run.py
```

or:

```bash
flask --app run run
```

## Docker

The project includes [docker-compose.yml](docker-compose.yml) with a web service and a PostgreSQL service.

```bash
docker compose up --build
```

The web app will be available at `http://localhost:5000`.

## Testing

Automated tests are in [tests](tests) and the strategy is documented in [docs/testing.md](docs/testing.md).

Run the test suite locally with coverage:

```bash
pytest --cov=app --cov-report=term-missing --cov-report=html:htmlcov
```

The HTML coverage report is written to [htmlcov](htmlcov) when generated locally or in CI.

## Demo Accounts

### Admin:

Email: admin1@email.com
Password: Adminpass!23

### User:

Email: user1@email.com
Password: Userpass!23

## CI

GitHub Actions is configured in [.github/workflows/ci.yml](.github/workflows/ci.yml).

The workflow runs:

- `black --check` for formatting
- `isort --check-only` for import ordering
- `flake8` for linting
- `pytest` with coverage and an HTML report

## Screenshots

Updated screenshots are stored in [docs/screenshots](docs/screenshots). The repository includes:

- [Home page](docs/screenshots/home.png)
- [Quiz page](docs/screenshots/quiz.png)
- [Quiz dashboard](docs/screenshots/quiz_dash.png)
- [User dashboard](docs/screenshots/user_dashboard.png)
- [Admin dashboard](docs/screenshots/admin_dashboard.png)
- [Change password](docs/screenshots/change_password.png)

## Contributor Workflow

Recommended workflow:

1. Create a feature branch using the conventions in [docs/branching-strategy.md](docs/branching-strategy.md).
2. Make focused changes and keep commits small.
3. Run the test suite and linters locally.
4. Open a pull request and reference the relevant rubric criteria.

## Marking Criteria Mapping

| Rubric Area | Evidence in the Codebase |
|---|---|
| Architecture and modularity | [app/routes/auth_routes.py](app/routes/auth_routes.py), [app/routes/quiz_routes.py](app/routes/quiz_routes.py), [app/routes/dashboard_routes.py](app/routes/dashboard_routes.py), [app/services/auth_service.py](app/services/auth_service.py), [app/repositories/user_repository.py](app/repositories/user_repository.py) |
| Testing depth and automation | [tests/test_auth.py](tests/test_auth.py), [tests/test_dashboard.py](tests/test_dashboard.py), [tests/test_take_action.py](tests/test_take_action.py), [tests/test_services.py](tests/test_services.py), [docs/testing.md](docs/testing.md) |
| Documentation and professionalism | [docs/architecture.md](docs/architecture.md), [docs/coding-standards.md](docs/coding-standards.md), [docs/branching-strategy.md](docs/branching-strategy.md), [README.md](README.md) |
| Database compliance | [config.py](config.py), [docker-compose.yml](docker-compose.yml), [app/models.py](app/models.py) |
| Deployment and workflow | [Dockerfile](Dockerfile), [docker-compose.yml](docker-compose.yml), [.github/workflows/ci.yml](.github/workflows/ci.yml), [pyproject.toml](pyproject.toml), [.pre-commit-config.yaml](.pre-commit-config.yaml) |
| GUI polish and accessibility | [app/templates/base.html](app/templates/base.html), [app/templates/user_dashboard.html](app/templates/user_dashboard.html), [app/static/css/style.css](app/static/css/style.css), [app/static/css/dashboard.css](app/static/css/dashboard.css) |

## Notes

- `.env` is intentionally ignored by Git; only [`.env.example`](.env.example) is tracked.
- SQLite remains available for local development and testing, while PostgreSQL is supported through environment configuration.
