# Architecture

## Layered Structure

UnlockED uses a lightweight layered architecture.

- Routes live in [app/routes](../app/routes)
- Services live in [app/services](../app/services)
- Repositories live in [app/repositories](../app/repositories)
- Shared helpers live in [app/utils](../app/utils)

## Request Flow

The route layer only coordinates Flask concerns such as request parsing, flash messages, redirects, and template rendering. Any non-trivial business rule is delegated to the service layer.

The service layer coordinates rules such as:

- password policy checks
- quiz scoring
- dashboard metric calculations
- token handling
- calendar fetching

Repositories isolate SQLAlchemy queries and database writes so the services do not need to know query details.

## Data Model

The main models are defined in [app/models.py](../app/models.py):

- `User` stores credentials, role data, quiz scores, and encrypted bios
- `MailList` stores take-action email subscriptions
- `QuizResult` stores historical quiz submissions

## Configuration

Configuration is centralised in [config.py](../config.py).

- PostgreSQL is used when `DATABASE_URL` is present
- SQLite is the fallback for local development and tests
- Production mode validates that required secrets are present

## Operational Notes

- CSRF protection is enabled through Flask-WTF
- Passwords are hashed with a peppered hash strategy
- Login is rate-limited with Flask-Limiter
- Role checks are handled by [app/utils/decorators.py](../app/utils/decorators.py)
