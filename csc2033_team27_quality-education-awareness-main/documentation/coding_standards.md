# Coding Standards – UnlockED

## General Principles

* Code should prioritise readability over complexity
* Use clear and descriptive names for variables and functions
* Follow single responsibility principle (each function does one thing)
* Avoid duplicated code where possible
* Remove unused code

---

## Python & Flask Conventions

* Follow PEP 8 style guidelines
* Use snake_case for variables and functions
* Use PascalCase for classes
* Keep routes, models, and logic separated

Example:

```python
def calculate_quiz_score(answers):
    return sum(answers)
```

---

## Project Structure

* `/routes` → handles HTTP requests
* `/models` → database models
* `/templates` → HTML files
* `/static` → CSS and JavaScript

Each file should have a single clear responsibility

---

## Comments and Documentation

* Use comments to explain why, not what
* All functions should include a short description

Example:

```python
# Calculates average quiz score for dashboard display
def get_average_score(scores):
    return sum(scores) / len(scores)
```

---

## Error Handling

* Validate user input before processing
* Use try/except blocks where necessary
* Return meaningful error messages

Example:

```python
try:
    user = User.query.get(user_id)
except Exception:
    return "Error retrieving user"
```

---

## Security Practices

* Passwords must be hashed (never stored in plain text)
* Validate all form inputs to prevent injection attacks
* Restrict access using role-based permissions
* Never commit `.env` or secret keys to GitHub

---

## Version Control Workflow

Our team used branches during development.

### Branching Strategy

Each major feature was developed in its own branch before being merged into the main branch.

Examples:

* `admin` – admin functionality and role management
* `take-action` – “Take Action” feature implementation
* `userdashboard` – dashboard development
* `errorhandling` – error handling improvements
* `documentation` – project documentation updates

Some earlier branches (e.g. `omer-css`, `addedfeatures`) reflect individual contributions or early-stage development before conventions were fully standardised.

### Naming Conventions (Refined During Development)

As the project progressed, we aimed to follow clearer naming conventions.

### Commit Practices

* Commits were made regularly to track progress
* Messages describe the change clearly (e.g. “Added login system”, “Fixed dashboard bug”)
* Work was merged into `main` after feature completion

This allowed multiple team members to work at the same time while maintaining a structured way of working.

---

## Code Review Guidelines

Before merging:

* Code compiles and runs without errors
* No unused code or debug prints
* Naming is consistent
* Logic is clear and readable

---

## Testing Standards

* Unit tests should be placed in `/tests`
* Test important functionality:

  * Authentication
  * Quiz logic
  * Database interactions

---

## Naming Conventions

| Item | Convention | Example |
| --------- | ---------- | --------------- |
| Variables | snake_case | user_score |
| Functions | snake_case | calculate_score |
| Classes | PascalCase | User |
| Files | snake_case | quiz_routes.py |
| Constants | UPPER_CASE | MAX_SCORE |

---

## Performance Guidelines

* Avoid unnecessary database queries
* Use efficient loops and logic
* Keep functions small and focused

---


