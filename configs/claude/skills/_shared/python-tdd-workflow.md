# Python Test-Driven Development (TDD) Workflow

## TDD Workflow Steps

1. **Write Tests First**: Use appropriate pytest testing skill (`pytest-testing` or `pytest-api-testing`)
2. **Confirm Tests Fail (Red)**: Run tests and verify they fail correctly
3. **Implement Code (Green)**: Write minimal implementation to pass tests
4. **Do NOT Modify Tests**: Keep tests unchanged during implementation
5. **Iterate**: Repeat until all tests pass
6. **Refactor**: Improve code quality while keeping tests green
7. **Run Linter/Formatter**: Validate code style (ruff, mypy, black, isort, flake8)
8. **Check Coverage**: Ensure adequate test coverage
9. **Commit**: Create atomic commits with clear messages

## Test Running Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_order_service.py

# Run specific test function
pytest tests/test_order_service.py::test_process_order

# Run with verbose output
pytest -v

# Run with output capture disabled (see print statements)
pytest -s

# Run tests matching pattern
pytest -k "test_create"
```

## Coverage Check

```bash
# Run tests with coverage
pytest --cov=app tests/

# Generate HTML coverage report
pytest --cov=app --cov-report=html tests/

# Check coverage with minimum threshold
pytest --cov=app --cov-fail-under=80 tests/

# Show missing lines
pytest --cov=app --cov-report=term-missing tests/
```

## Code Quality Commands

```bash
# Modern approach (ruff + mypy)
ruff check --fix .
ruff format .
mypy .

# Traditional approach
black .
isort .
flake8 .
mypy .
```

## Commit Guidelines

- One commit per feature/fix
- Clear commit messages
- Ensure tests pass before committing
- Ensure linters pass before committing
- Do NOT revert past commits using git command
- If you need to revert changes, create new REVERTING COMMIT

## Related Skills

- `pytest-testing`: For writing unit and integration tests
- `pytest-api-testing`: For writing API endpoint tests
- `python-core-development`: For implementing core Python code
- `python-api-development`: For implementing API endpoints
