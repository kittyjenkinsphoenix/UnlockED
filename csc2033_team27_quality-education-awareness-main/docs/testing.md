# Testing Strategy

UnlockED uses pytest for automated testing with a mix of route-level integration tests and smaller unit tests.

## Automated Testing

The current suite covers:

- authentication and password changes
- role-based access control
- quiz page access and scoring flows
- take-action subscriptions and unsubscribe tokens
- calendar endpoint structure
- service-layer helper functions

The tests run against a temporary SQLite database so each run is isolated and repeatable.

## Manual Testing Table

| Area | What to Check | Expected Result |
|---|---|---|
| Home page | Load the home page on desktop and mobile widths | Layout remains readable and responsive |
| Login | Submit valid and invalid credentials | Valid login succeeds, invalid login shows an error |
| Register | Use a strong password and a blacklisted password | Strong password succeeds, weak password is rejected |
| Quiz | Submit quiz answers and review the dashboard | Score updates and recent results appear |
| Admin dashboard | Log in as a non-admin user | Access is denied with HTTP 403 |
| Take action | Subscribe and unsubscribe with the email flow | Subscription is stored and can be removed |

## Edge-Case Rationale

Edge cases are important because they are the most likely places for hidden regressions:

- empty or malformed form input
- duplicate email addresses
- invalid unsubscribe tokens
- unauthorised access to protected routes
- missing external calendar configuration

## Coverage Output

Coverage is generated in CI with `pytest-cov` and published as an HTML artifact. Local developers can generate the same output with:

```bash
pytest --cov=app --cov-report=term-missing --cov-report=html:htmlcov
```
