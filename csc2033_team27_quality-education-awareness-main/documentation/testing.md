# Testing Documentation

## General Strategy

Testing is conducted using **PyTest** with a mix of unit and integration tests.
Every test runs against an in-memory SQLite database (`tests/conftest.py`)
so tests cannot interfere with each other or with production data.

The CI/CD pipeline (`.github/workflows/ci.yml`) runs the full suite automatically
on every push and pull request to `main`, and generates an HTML coverage report
saved as a build artefact under `documentation/coverage_report/`.

To run locally:

```
pip install -r requirements-dev.txt
python -m pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Test Types

| Type | Description | Files |
|---|---|---|
| Unit | Test individual model methods and form validation in isolation | `test_auth.py`, `test_home.py` |
| Integration | Test full request/response cycle through Flask routes and database | All test files |
| Security | Verify access control, CSRF enforcement, and input validation | `test_auth.py`, `test_dashboard.py` |
| API | Verify external API endpoint format and structure | `test_take_action.py` |

---

## Test Cases

### Authentication — `tests/test_auth.py`

| Test ID | Test Name | What It Tests | Requirement | Expected Result | Status |
|---|---|---|---|---|---|
| T01 | `test_registered_user_can_login` | A seeded user can log in with correct credentials and a valid CSRF token | User authentication | HTTP 200, redirected to dashboard | Pass |
| T02 | `test_login_fails_with_wrong_password` | Login is rejected when the password is incorrect | Access control / security | HTTP 200, error message shown | Pass |
| T03 | `test_login_fails_with_unregistered_user` | Login is rejected for an email address not in the database | Access control | HTTP 200, error message shown | Pass |
| T04 | `test_logout` | A logged-in user is redirected to the login page after logging out | Session management | HTTP 200, login page shown | Pass |
| T05 | `test_login_with_empty_fields` | Login is rejected when username and password fields are empty | Input validation | HTTP 200, error message shown | Pass |
| T06 | `test_register_with_incorrect_email_format` | Registration is rejected for a malformed email address | Input validation | HTTP 200/400/500, registration fails | Pass |
| T07 | `test_register_with_incorrect_password_format` | Registration is rejected for a password that does not meet complexity rules | Security / password policy | HTTP 200, login attempt with empty fields fails | Pass |
| T08 | `test_change_password_requires_login` | Unauthenticated users are redirected away from the change-password page | Access control | HTTP 302 redirect to login | Pass |
| T09 | `test_change_password` | A logged-in user can change their password and immediately log in with the new one | Password management | HTTP 200, dashboard accessible with new password | Pass |
| T10 | `test_change_password_with_wrong_current_password` | Password change is rejected when the supplied current password is wrong | Security | HTTP 200, error message shown | Pass |

---

### Dashboard & Access Control — `tests/test_dashboard.py`

| Test ID | Test Name | What It Tests | Requirement | Expected Result | Status |
|---|---|---|---|---|---|
| T11 | `test_user_dashboard_logged_in` | A logged-in user with the `user` role can access their dashboard | Role-based access / dashboard | HTTP 200 | Pass |
| T12 | `test_user_cant_access_admin_dashboard` | A `user`-role account is forbidden from accessing the admin dashboard | Role-based access control | HTTP 403 | Pass |
| T13 | `test_user_dashboard_requires_login` | The user dashboard redirects unauthenticated visitors | Access control | HTTP 302 redirect | Pass |
| T14 | `test_admin_dashboard_requires_login` | The admin dashboard redirects unauthenticated visitors | Access control | HTTP 302 redirect | Pass |

---

### Home Page — `tests/test_home.py`

| Test ID | Test Name | What It Tests | Requirement | Expected Result | Status |
|---|---|---|---|---|---|
| T15 | `test_home_page` | The home page loads successfully for any visitor | Educational content / public access | HTTP 200 | Pass |

---

### Data Visualisation — `tests/test_piechart.py`

| Test ID | Test Name | What It Tests | Requirement | Expected Result | Status |
|---|---|---|---|---|---|
| T16 | `test_chart_data_present` | The home page response contains the expected pie chart labels | Data visualisation (SDG indicators) | Response body contains `High-income` and `Low-income` | Pass |

---

### Quiz — `tests/test_quiz.py`

| Test ID | Test Name | What It Tests | Requirement | Expected Result | Status |
|---|---|---|---|---|---|
| T17 | `test_quiz_requires_login` | Unauthenticated users cannot access the quiz | Access control | HTTP 302 redirect to login | Pass |
| T18 | `test_quiz_access_logged_in` | A logged-in user can access the quiz page | User interaction / quiz feature | HTTP 200 | Pass |

---

### Take Action & Email — `tests/test_take_action.py`

| Test ID | Test Name | What It Tests | Requirement | Expected Result | Status |
|---|---|---|---|---|---|
| T19 | `test_take_action_loads` | The Take Action page loads for any visitor | Public access / user engagement | HTTP 200 | Pass |
| T20 | `test_take_action_signup` | A new email address can be submitted via the Take Action form | Email notification / mailing list | HTTP 200, submission accepted | Pass |
| T21 | `test_take_action_duplicate` | Submitting an already-registered email shows an appropriate message | Input validation / duplicate prevention | HTTP 200, `already signed up` in response | Pass |
| T22 | `test_unsubscribe_valid` | A correctly signed unsubscribe token processes without error | Email management / token security | HTTP 200 | Pass |
| T23 | `test_unsubscribe_invalid` | A malformed unsubscribe token is rejected with an error message | Security / token validation | HTTP 200, `Invalid or expired token` in response | Pass |
| T24 | `test_calendar_api_json` | The `/api/calendar` endpoint returns a valid JSON response | External API integration | HTTP 200, `Content-Type: application/json` | Pass |
| T25 | `test_calendar_api_structure` | The calendar API JSON contains the required `title`, `start`, and `end` fields | External API data format | Response is a list; each item has expected keys | Pass |

---

## Coverage

Coverage is measured automatically in CI using `pytest-cov`. The HTML report is
uploaded as a build artefact after each run and can be downloaded from the
GitHub Actions summary page. The report covers all files under `app/`.
