# Python Coding Standards

## Indentation

- 4 spaces (Python)

## Linter & Formatter

### Modern Tooling (Recommended)

- **ruff**: All-in-one linter + formatter + import sorter (replaces flake8, isort, and partially black)
  - `ruff check .` (linting)
  - `ruff format .` (formatting)

### Traditional Tooling

- **black**: Opinionated code formatter
- **isort**: Import statement sorter
- **flake8**: Style guide enforcement (PEP8)
- **mypy**: Static type checker

### Usage

```bash
# Modern approach (ruff only)
ruff check --fix .
ruff format .

# Traditional approach
black .
isort .
flake8 .
mypy .
```

## Type Hints

- **Always use type hints** for function signatures and class attributes
- Use `from typing import` for complex types
- Use `from collections.abc import` for abstract types (Python 3.9+)

### Good Example

```python
from collections.abc import Sequence
from typing import Optional

def process_items(
    items: Sequence[str],
    max_count: Optional[int] = None
) -> list[str]:
    """Process items with optional max count limit."""
    if max_count is not None:
        items = items[:max_count]
    return [item.upper() for item in items]
```

### Bad Example

```python
def process_items(items, max_count=None):  # No type hints
    if max_count is not None:
        items = items[:max_count]
    return [item.upper() for item in items]
```

## Docstrings

- Use Google-style docstrings
- Include Args, Returns, Raises sections when applicable

### Example

```python
def calculate_total(
    prices: list[float],
    tax_rate: float = 0.1
) -> float:
    """Calculate total price including tax.

    Args:
        prices: List of item prices
        tax_rate: Tax rate as decimal (default: 0.1 for 10%)

    Returns:
        Total price including tax

    Raises:
        ValueError: If tax_rate is negative
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)
```

## Comments

- Language: English or Japanese (match codebase conventions)
- Style: Explain WHY, not WHAT or HOW

### Good Example

```python
# WHY: Use async context manager to ensure connection cleanup even on error
async with database.connection() as conn:
    await conn.execute(query)
```

### Bad Example

```python
# Execute the query (obvious from code)
await conn.execute(query)
```

## Import Order

Following PEP8 and isort conventions:

1. Standard library imports
2. Related third-party imports
3. Local application imports
4. Blank line between each group

### Example

```python
# Standard library
import os
from pathlib import Path
from typing import Optional

# Third-party
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

# Local
from app.core.config import settings
from app.models.user import User
```

## File Naming Conventions

- Modules: `snake_case.py`
- Classes: `PascalCase` in snake_case file
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

### Examples

```
app/
├── models/
│   ├── user.py           # class User
│   └── order.py          # class Order
├── services/
│   ├── order_service.py  # class OrderService
│   └── email_service.py  # class EmailService
├── api/
│   ├── users.py          # router endpoints
│   └── orders.py         # router endpoints
└── core/
    ├── config.py         # class Settings
    └── database.py       # database connection
```

## Code Organization

- **Single Responsibility Principle**: One class/function = one responsibility
- **Explicit is Better Than Implicit**: Clear over clever
- **Flat is Better Than Nested**: Avoid deep nesting
- **DRY (Don't Repeat Yourself)**: Extract common logic
- **Type Safety First**: Use type hints everywhere
