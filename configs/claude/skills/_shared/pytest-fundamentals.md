# Pytest Testing Fundamentals

Common pytest concepts, structure, assertions, fixtures, and best practices used across all testing skills.

## Core TDD Principles

**Always** write tests BEFORE implementation:

1. Write failing test first (Red)
2. Run test to confirm it fails correctly
3. Commit test when verified
4. Implementation happens separately
5. Run tests to confirm they pass (Green)
6. Refactor if needed

## Pytest Structure

### Basic Structure

```python
# tests/test_user_service.py
import pytest
from app.services.user_service import UserService

class TestUserService:
    """Tests for UserService."""

    def test_create_user_success(self):
        """Should create user with valid data."""
        # Arrange
        user_data = {"name": "John", "email": "john@example.com"}
        service = UserService()

        # Act
        user = service.create_user(user_data)

        # Assert
        assert user.name == "John"
        assert user.email == "john@example.com"

    def test_create_user_invalid_email(self):
        """Should raise error for invalid email."""
        # Arrange
        user_data = {"name": "John", "email": "invalid"}
        service = UserService()

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid email"):
            service.create_user(user_data)
```

### Test Organization

- **Class**: Group related tests (optional, can use standalone functions)
- **Function**: Individual test case (must start with `test_`)
- **Fixtures**: Define reusable test data and setup
- **Markers**: Tag tests with custom metadata
- **conftest.py**: Share fixtures across multiple test files

## Pytest Assertions

### Equality

```python
assert actual == expected
assert actual != unexpected
```

### Truthiness

```python
assert value  # Truthy
assert not value  # Falsey
assert value is None
assert value is not None
```

### Comparisons

```python
assert actual > expected
assert actual >= expected
assert actual < expected
assert actual <= expected
```

### Collections

```python
assert item in collection
assert item not in collection
assert len(collection) == 5
assert set(actual) == set(expected)  # Order-independent comparison
```

### Exceptions

```python
# Basic exception check
with pytest.raises(ValueError):
    raise ValueError("Error message")

# Check exception message
with pytest.raises(ValueError, match="Invalid"):
    raise ValueError("Invalid input")

# Capture exception for further inspection
with pytest.raises(ValueError) as exc_info:
    raise ValueError("Error message")
assert "Error" in str(exc_info.value)
```

### Approximate Comparisons

```python
import pytest

# Floating point comparison
assert 0.1 + 0.2 == pytest.approx(0.3)
assert value == pytest.approx(expected, rel=1e-3)  # 0.1% tolerance
```

## Fixtures

### Basic Fixtures

```python
# conftest.py
import pytest

@pytest.fixture
def user_data():
    """Provide sample user data."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }

@pytest.fixture
def user_service():
    """Provide UserService instance."""
    return UserService()

# tests/test_user_service.py
def test_create_user(user_service, user_data):
    """Fixtures are injected as function parameters."""
    user = user_service.create_user(user_data)
    assert user.name == user_data["name"]
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: runs for each test
def function_fixture():
    return "new instance per test"

@pytest.fixture(scope="class")  # Runs once per test class
def class_fixture():
    return "shared within class"

@pytest.fixture(scope="module")  # Runs once per module
def module_fixture():
    return "shared within module"

@pytest.fixture(scope="session")  # Runs once per test session
def session_fixture():
    return "shared across all tests"
```

### Fixture Cleanup (Teardown)

```python
@pytest.fixture
def database_connection():
    """Provide database connection with cleanup."""
    # Setup
    conn = Database.connect()

    yield conn  # Provide to test

    # Teardown (runs after test completes)
    conn.close()
```

## Parametrize

### Basic Parametrize

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input_value, expected):
    """Test doubling function with multiple inputs."""
    assert double(input_value) == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (5, 5, 10),
    (-1, 1, 0),
])
def test_addition(a, b, expected):
    assert add(a, b) == expected
```

### Parametrize with IDs

```python
@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
], ids=["one", "two", "three"])
def test_double_with_ids(input_value, expected):
    assert double(input_value) == expected
```

## Mocking and Patching

### Basic Mocking (unittest.mock)

```python
from unittest.mock import Mock, patch

def test_external_api_call():
    """Mock external API call."""
    # Create mock
    mock_api = Mock()
    mock_api.get_user.return_value = {"id": 1, "name": "John"}

    # Use mock
    service = UserService(api=mock_api)
    user = service.fetch_user(1)

    # Verify
    assert user["name"] == "John"
    mock_api.get_user.assert_called_once_with(1)
```

### Patching

```python
from unittest.mock import patch

@patch('app.services.user_service.EmailClient')
def test_send_email(mock_email_client):
    """Patch EmailClient class."""
    # Configure mock
    mock_instance = mock_email_client.return_value
    mock_instance.send.return_value = True

    # Test
    service = UserService()
    result = service.notify_user(1)

    # Verify
    assert result is True
    mock_instance.send.assert_called_once()
```

### Patch as Context Manager

```python
def test_database_query():
    """Patch database connection."""
    with patch('app.database.get_connection') as mock_conn:
        mock_conn.return_value.execute.return_value = [{"id": 1}]

        result = query_users()

        assert len(result) == 1
        mock_conn.return_value.execute.assert_called_once()
```

## Mocking Best Practices

**IMPORTANT**: Never put logic inside mocks. Mocks should return simple values.

```python
# Bad: Logic in mock
mock_service.calculate = lambda x: x * 0.9 if x > 100 else x * 0.8

# Good: Simple return value
mock_service.calculate.return_value = 90

# Good: Test different scenarios separately
def test_large_amount():
    """Test with amount over 100."""
    mock_service.calculate.return_value = 90
    # Test logic here

def test_small_amount():
    """Test with amount under 100."""
    mock_service.calculate.return_value = 80
    # Test logic here
```

**WHY**: Logic in mocks makes tests fragile and defeats the purpose of testing the actual implementation.

## Pytest Markers

### Built-in Markers

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires Python 3.9+")
def test_new_syntax():
    pass

@pytest.mark.xfail(reason="Known bug")
def test_buggy_feature():
    pass
```

### Custom Markers

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

# tests/test_api.py
@pytest.mark.slow
def test_heavy_computation():
    pass

@pytest.mark.integration
def test_database_integration():
    pass

# Run only marked tests
# pytest -m "not slow"
# pytest -m integration
```

## Pytest Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=app
    --cov-report=term-missing
```

### conftest.py

```python
# tests/conftest.py
import pytest

@pytest.fixture(autouse=True)
def reset_database():
    """Automatically reset database for each test."""
    database.reset()
    yield
    database.cleanup()

@pytest.fixture
def client():
    """Provide test client."""
    return TestClient(app)
```

## Test Quality Principles

- **Descriptive**: Test names clearly describe what is being tested
- **Independent**: Tests don't depend on each other
- **Focused**: Each test validates one specific behavior
- **Fast**: Tests run quickly; use mocks for external dependencies
- **Maintainable**: Easy to understand and update

## Best Practices

- Write tests before implementation (TDD)
- One assertion per test when possible
- Use descriptive test names (verb + expected outcome)
- Test edge cases and error conditions
- Keep tests independent and isolated
- Mock external dependencies (APIs, databases, file I/O)
- Avoid testing implementation details
- Test behavior, not methods
- Keep tests fast and focused
- Maintain high test coverage (aim for 90%+)

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_user_service.py

# Run specific test function
pytest tests/test_user_service.py::test_create_user

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app tests/

# Run tests matching pattern
pytest -k "test_create"

# Run marked tests
pytest -m integration
```

## Coding Standards

- **Indentation**: 4 spaces (Python)
- **Comments**: English only, explain WHY not WHAT
- **Test Names**: Use descriptive, behavior-focused names
- **Type Hints**: Use type hints in test fixtures and helpers
