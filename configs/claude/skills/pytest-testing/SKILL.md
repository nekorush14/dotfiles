---
name: pytest-testing
description: Write pytest tests for Python code including unit tests, integration tests, fixtures, mocking, and parametrize. Use when writing tests for functions, classes, or complex business logic.
---

# Pytest Testing Specialist

Specialized in writing comprehensive pytest tests with fixtures, mocking, and parametrize.

## When to Use This Skill

- Writing unit tests for functions and classes
- Creating integration tests
- Setting up test fixtures
- Mocking external dependencies
- Parametrizing tests for multiple scenarios
- Testing async code

## Core Principles

- **Test First (TDD)**: Write tests before implementation
- **Independent Tests**: Each test should run independently
- **Clear Test Names**: Test names describe expected behavior
- **Fixture Reusability**: Share setup code via fixtures
- **Mock External Dependencies**: Isolate unit tests from external systems
- **One Assertion Focus**: Prefer focused tests over complex multi-assertion tests

## Implementation Guidelines

### Basic Test Structure

```python
# tests/test_user_service.py
import pytest
from app.services.user_service import UserService
from app.models.user import User

class TestUserService:
    """Test suite for UserService."""

    def test_create_user_success(self):
        """Should create user with valid data."""
        # Arrange
        service = UserService()
        user_data = {
            "email": "john@example.com",
            "name": "John Doe"
        }

        # Act
        user = service.create_user(user_data)

        # Assert
        assert user.email == "john@example.com"
        assert user.name == "John Doe"
        assert user.id is not None

    def test_create_user_invalid_email(self):
        """Should raise ValidationError for invalid email."""
        # Arrange
        service = UserService()
        user_data = {
            "email": "invalid",
            "name": "John Doe"
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid email"):
            service.create_user(user_data)

    def test_create_user_missing_name(self):
        """Should raise ValidationError when name is missing."""
        service = UserService()
        user_data = {"email": "john@example.com"}

        with pytest.raises(ValueError, match="Name is required"):
            service.create_user(user_data)
```

### Using Fixtures

```python
# tests/conftest.py
import pytest
from app.database import Database
from app.services.user_service import UserService

@pytest.fixture
def database():
    """Provide test database connection."""
    db = Database(":memory:")
    db.setup()
    yield db
    db.close()

@pytest.fixture
def user_service(database):
    """Provide UserService with test database."""
    return UserService(database=database)

@pytest.fixture
def sample_user_data():
    """Provide sample user data for tests."""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "age": 30
    }

# tests/test_user_service.py
def test_create_user_with_fixtures(user_service, sample_user_data):
    """Test user creation using fixtures."""
    user = user_service.create_user(sample_user_data)

    assert user.email == sample_user_data["email"]
    assert user.name == sample_user_data["name"]
```

### Fixture Scopes

```python
# conftest.py
import pytest

@pytest.fixture(scope="function")  # Default: new instance per test
def function_scoped_db():
    """New database for each test."""
    db = create_test_db()
    yield db
    db.cleanup()

@pytest.fixture(scope="class")  # Shared within test class
def class_scoped_cache():
    """Cache shared across test class."""
    cache = Cache()
    yield cache
    cache.clear()

@pytest.fixture(scope="module")  # Once per module
def module_scoped_config():
    """Config loaded once per test module."""
    return load_test_config()

@pytest.fixture(scope="session")  # Once per test session
def session_scoped_app():
    """Application instance for entire test session."""
    app = create_app()
    yield app
    app.shutdown()
```

### Parametrize Tests

```python
import pytest

@pytest.mark.parametrize("input_email,expected_valid", [
    ("user@example.com", True),
    ("admin@company.co.uk", True),
    ("invalid", False),
    ("@example.com", False),
    ("user@", False),
])
def test_email_validation(input_email, expected_valid):
    """Test email validation with various inputs."""
    result = validate_email(input_email)
    assert result == expected_valid

@pytest.mark.parametrize("age,expected_category", [
    (5, "child"),
    (15, "teenager"),
    (25, "adult"),
    (70, "senior"),
])
def test_age_category(age, expected_category):
    """Test age categorization."""
    category = categorize_age(age)
    assert category == expected_category

# Parametrize with IDs for better test output
@pytest.mark.parametrize("amount,discount,expected", [
    (100, 0.1, 90),
    (200, 0.2, 160),
    (50, 0, 50),
], ids=["10% discount", "20% discount", "no discount"])
def test_calculate_discounted_price(amount, discount, expected):
    """Test price calculation with different discounts."""
    result = calculate_price(amount, discount)
    assert result == pytest.approx(expected)
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch, MagicMock
import pytest

def test_send_email_success():
    """Test email sending with mocked SMTP client."""
    # WHY: Mock SMTP to avoid actual email sending in tests
    mock_smtp = Mock()
    mock_smtp.send.return_value = True

    service = NotificationService(smtp_client=mock_smtp)
    result = service.send_welcome_email("user@example.com")

    assert result is True
    mock_smtp.send.assert_called_once_with(
        to="user@example.com",
        subject="Welcome",
        body=pytest.mock.ANY  # Match any body content
    )

@patch('app.services.payment_service.PaymentGateway')
def test_process_payment(mock_payment_gateway):
    """Test payment processing with patched gateway."""
    # Configure mock
    mock_instance = mock_payment_gateway.return_value
    mock_instance.charge.return_value = {
        "status": "success",
        "transaction_id": "txn_123"
    }

    # Test
    service = PaymentService()
    result = service.process_payment(100, "card_token")

    # Verify
    assert result["status"] == "success"
    assert result["transaction_id"] == "txn_123"
    mock_instance.charge.assert_called_once_with(100, "card_token")

def test_api_call_with_context_manager():
    """Test API call using patch as context manager."""
    with patch('app.api.requests.get') as mock_get:
        # WHY: Mock HTTP request to avoid external API dependency
        mock_get.return_value.json.return_value = {"id": 1, "name": "Test"}
        mock_get.return_value.status_code = 200

        client = ApiClient()
        result = client.fetch_user(1)

        assert result["name"] == "Test"
        mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### Testing Exceptions

```python
import pytest

def test_divide_by_zero():
    """Should raise ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_validation_error_message():
    """Should raise ValidationError with specific message."""
    with pytest.raises(ValueError, match="Email is required"):
        validate_user({"name": "John"})

def test_exception_details():
    """Should raise exception with correct details."""
    with pytest.raises(NotFoundError) as exc_info:
        get_user(999)

    # Verify exception details
    assert exc_info.value.resource == "User"
    assert exc_info.value.id == 999
```

### Testing Async Code

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_fetch_user():
    """Test async user fetch."""
    service = AsyncUserService()
    user = await service.fetch_user(1)

    assert user["id"] == 1
    assert user["name"] is not None

@pytest.mark.asyncio
async def test_concurrent_operations():
    """Test concurrent async operations."""
    service = AsyncOrderService()

    # WHY: Test that concurrent operations work correctly
    orders = await asyncio.gather(
        service.fetch_order(1),
        service.fetch_order(2),
        service.fetch_order(3)
    )

    assert len(orders) == 3
    assert all(order["id"] for order in orders)

@pytest.fixture
async def async_database():
    """Async fixture for database."""
    db = await create_async_db()
    yield db
    await db.close()

@pytest.mark.asyncio
async def test_with_async_fixture(async_database):
    """Test using async fixture."""
    result = await async_database.query("SELECT 1")
    assert result is not None
```

### Integration Tests

```python
import pytest

@pytest.mark.integration
def test_user_registration_flow(database, email_service):
    """Test complete user registration flow.

    WHY: Integration test verifying multiple components work together.
    """
    # Arrange
    registration_service = RegistrationService(
        database=database,
        email_service=email_service
    )
    user_data = {
        "email": "newuser@example.com",
        "name": "New User",
        "password": "securepass123"
    }

    # Act
    result = registration_service.register(user_data)

    # Assert
    assert result["success"] is True
    assert result["user"]["id"] is not None

    # Verify user exists in database
    user = database.get_user_by_email("newuser@example.com")
    assert user is not None
    assert user.name == "New User"

    # Verify welcome email was sent
    email_service.send_welcome_email.assert_called_once_with(
        "newuser@example.com"
    )

@pytest.mark.integration
def test_order_processing_transaction(database):
    """Test order processing with database transaction."""
    service = OrderService(database=database)

    # Create order
    order = service.create_order(
        user_id=1,
        items=[{"id": 1, "quantity": 2}],
        total=200
    )

    # Verify order in database
    stored_order = database.get_order(order.id)
    assert stored_order.status == "pending"
    assert stored_order.total == 200
```

## Tools to Use

- `Write`: Create new test files
- `Edit`: Modify existing tests
- `Bash`: Run pytest commands

### Bash Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_user_service.py

# Run specific test function
pytest tests/test_user_service.py::test_create_user_success

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app tests/

# Run only marked tests
pytest -m integration
pytest -m "not slow"

# Run with output
pytest -s  # Show print statements
```

## Workflow

1. **Understand Requirements**: Clarify what needs to be tested
2. **Write Test First**: Write failing test (Red)
3. **Verify Test Fails**: Confirm test fails correctly
4. **Commit Test**: Commit the failing test
5. **Implementation**: Write code to pass test (Green)
6. **Run Tests**: Verify tests pass
7. **Refactor**: Improve code quality
8. **Run Coverage**: Check test coverage
9. **Commit**: Create atomic commit

## Related Skills

- `python-core-development`: For implementing code being tested
- `pytest-api-testing`: For testing API endpoints
- `python-api-development`: For FastAPI/Flask code being tested

## Testing Fundamentals

See [Pytest Fundamentals](../_shared/pytest-fundamentals.md)

## Coding Standards

See [Python Coding Standards](../_shared/python-coding-standards.md)

## TDD Workflow

Follow [Python TDD Workflow](../_shared/python-tdd-workflow.md)

## Key Reminders

- Write tests BEFORE implementation (TDD)
- Use descriptive test names that explain expected behavior
- Keep tests independent and isolated
- Use fixtures for reusable test setup
- Mock external dependencies (APIs, databases, file I/O)
- Parametrize tests to cover multiple scenarios
- Test both success and error cases
- Use appropriate fixture scopes for performance
- Run coverage checks to ensure adequate testing
- Commit tests separately from implementation
