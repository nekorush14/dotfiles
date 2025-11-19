# Vitest Fundamentals

## Test Structure

```typescript
import { describe, it, expect } from 'vitest'

// Test suite
describe('Calculator', () => {
  // Individual test
  it('should add two numbers', () => {
    const result = add(2, 3)
    expect(result).toBe(5)
  })

  // Nested describe for grouping
  describe('multiplication', () => {
    it('should multiply two numbers', () => {
      expect(multiply(2, 3)).toBe(6)
    })

    it('should handle zero', () => {
      expect(multiply(5, 0)).toBe(0)
    })
  })
})

// Alternative: test() is alias for it()
test('should subtract numbers', () => {
  expect(subtract(5, 3)).toBe(2)
})
```

## Matchers

### Equality

```typescript
// Exact equality (===)
expect(value).toBe(5)
expect(value).toBe('hello')
expect(value).toBe(true)

// Deep equality (objects, arrays)
expect(user).toEqual({ id: '1', name: 'John' })
expect(array).toEqual([1, 2, 3])

// Partial object matching
expect(user).toMatchObject({ name: 'John' })
```

### Truthiness

```typescript
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(value).toBeNull()
expect(value).toBeUndefined()
expect(value).toBeDefined()
```

### Numbers

```typescript
expect(value).toBeGreaterThan(5)
expect(value).toBeGreaterThanOrEqual(5)
expect(value).toBeLessThan(10)
expect(value).toBeLessThanOrEqual(10)
expect(value).toBeCloseTo(0.3) // For floating point
```

### Strings

```typescript
expect(string).toMatch(/pattern/)
expect(string).toContain('substring')
```

### Arrays and Iterables

```typescript
expect(array).toContain(item)
expect(array).toHaveLength(3)
expect(array).toContainEqual({ id: '1' })
```

### Exceptions

```typescript
expect(() => {
  throw new Error('error')
}).toThrow()

expect(() => {
  throw new Error('specific error')
}).toThrow('specific error')

expect(() => {
  throw new Error('error')
}).toThrow(Error)
```

### Negation

```typescript
expect(value).not.toBe(5)
expect(value).not.toBeNull()
```

## Setup and Teardown

```typescript
import { describe, it, beforeEach, afterEach, beforeAll, afterAll } from 'vitest'

describe('Database', () => {
  // Run once before all tests in this suite
  beforeAll(() => {
    console.log('Connect to database')
  })

  // Run before each test
  beforeEach(() => {
    console.log('Clear database')
  })

  // Run after each test
  afterEach(() => {
    console.log('Cleanup')
  })

  // Run once after all tests in this suite
  afterAll(() => {
    console.log('Disconnect from database')
  })

  it('should insert user', () => {
    // Test logic
  })

  it('should delete user', () => {
    // Test logic
  })
})
```

## Mocking

### Mock Functions

```typescript
import { vi } from 'vitest'

// Create mock function
const mockFn = vi.fn()

// Mock with return value
const mockFn = vi.fn().mockReturnValue(42)

// Mock with implementation
const mockFn = vi.fn((x: number) => x * 2)

// Assertions
expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledTimes(2)
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2')
expect(mockFn).toHaveBeenLastCalledWith('last-arg')
```

### Spy on Functions

```typescript
import * as utils from './utils'

// Spy on existing function
const spy = vi.spyOn(utils, 'formatDate')

// Use the function
utils.formatDate(new Date())

// Assert
expect(spy).toHaveBeenCalled()

// Restore original implementation
spy.mockRestore()
```

### Mock Modules

```typescript
// Mock entire module
vi.mock('./api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: '1', name: 'John' }),
  deleteUser: vi.fn().mockResolvedValue(undefined),
}))

// Partial mock
vi.mock('./api', async () => {
  const actual = await vi.importActual('./api')
  return {
    ...actual,
    fetchUser: vi.fn(),
  }
})
```

## React Testing Library

### Rendering

```typescript
import { render, screen } from '@testing-library/react'

const { container, rerender, unmount } = render(<Component />)

// Get root element
const rootElement = container.firstChild

// Re-render with new props
rerender(<Component prop="new value" />)

// Unmount component
unmount()
```

### Queries

#### Priority Order

1. **getByRole** (most accessible)
2. **getByLabelText** (forms)
3. **getByPlaceholderText** (forms)
4. **getByText** (text content)
5. **getByDisplayValue** (form values)
6. **getByAltText** (images)
7. **getByTitle** (less accessible)
8. **getByTestId** (last resort)

#### Query Variants

```typescript
// getBy - throws if not found or multiple matches
const button = screen.getByRole('button')

// queryBy - returns null if not found
const button = screen.queryByRole('button')
if (button) {
  // Element exists
}

// findBy - returns Promise, waits for element
const button = await screen.findByRole('button')

// getAllBy - returns array (throws if none found)
const buttons = screen.getAllByRole('button')

// queryAllBy - returns array (empty if none found)
const buttons = screen.queryAllByRole('button')

// findAllBy - returns Promise<array>
const buttons = await screen.findAllByRole('button')
```

#### Common Queries

```typescript
// By role (preferred)
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })
screen.getByRole('heading', { level: 1 })

// By label text (forms)
screen.getByLabelText(/email address/i)

// By placeholder
screen.getByPlaceholderText(/enter email/i)

// By text
screen.getByText(/hello world/i)
screen.getByText('Exact text')
screen.getByText((content, element) => content.startsWith('Hello'))

// By test ID (last resort)
screen.getByTestId('submit-button')
```

### User Interaction (userEvent)

```typescript
import { userEvent } from '@testing-library/user-event'

const user = userEvent.setup()

// Click
await user.click(button)
await user.dblClick(button)

// Type
await user.type(input, 'Hello')
await user.clear(input)

// Select
await user.selectOptions(select, 'option-value')
await user.selectOptions(select, ['value1', 'value2'])

// Check
await user.click(checkbox) // Toggle
```

### Async Testing

```typescript
import { waitFor, waitForElementToBeRemoved } from '@testing-library/react'

// Wait for condition
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument()
})

// Wait for element to be removed
await waitForElementToBeRemoved(() => screen.queryByText('Loading'))

// findBy - combines getBy + waitFor
const element = await screen.findByText('Loaded')

// Wait with timeout
await waitFor(
  () => {
    expect(screen.getByText('Loaded')).toBeInTheDocument()
  },
  { timeout: 3000 }
)
```

## jest-dom Matchers

```typescript
// Document presence
expect(element).toBeInTheDocument()
expect(element).not.toBeInTheDocument()

// Visibility
expect(element).toBeVisible()
expect(element).not.toBeVisible()

// Disabled state
expect(button).toBeDisabled()
expect(button).toBeEnabled()

// Form elements
expect(input).toHaveValue('text')
expect(checkbox).toBeChecked()
expect(select).toHaveDisplayValue('Option 1')

// Attributes
expect(element).toHaveAttribute('href', '/path')
expect(element).toHaveClass('btn-primary')

// Text content
expect(element).toHaveTextContent('Hello')
expect(element).toContainHTML('<span>Hello</span>')

// Focus
expect(input).toHaveFocus()
```

## Common Patterns

### Testing Loading States

```typescript
it('should show loading state', async () => {
  render(<AsyncComponent />)

  // Initially loading
  expect(screen.getByText(/loading/i)).toBeInTheDocument()

  // Wait for loaded state
  await waitFor(() => {
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
  })

  expect(screen.getByText('Data loaded')).toBeInTheDocument()
})
```

### Testing Forms

```typescript
it('should submit form', async () => {
  const user = userEvent.setup()
  const handleSubmit = vi.fn()
  render(<Form onSubmit={handleSubmit} />)

  await user.type(screen.getByLabelText(/email/i), 'user@example.com')
  await user.type(screen.getByLabelText(/password/i), 'password')
  await user.click(screen.getByRole('button', { name: /submit/i }))

  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'password',
  })
})
```

### Testing Error States

```typescript
it('should display error message', async () => {
  server.use(
    http.get('/api/data', () => {
      return new HttpResponse(null, { status: 500 })
    })
  )

  render(<DataFetcher />)

  expect(await screen.findByText(/error/i)).toBeInTheDocument()
})
```

### Testing Conditional Rendering

```typescript
it('should not render when condition is false', () => {
  render(<ConditionalComponent show={false} />)

  expect(screen.queryByText('Content')).not.toBeInTheDocument()
})

it('should render when condition is true', () => {
  render(<ConditionalComponent show={true} />)

  expect(screen.getByText('Content')).toBeInTheDocument()
})
```

## Best Practices

- Use `getByRole` with accessible names whenever possible
- Prefer `userEvent` over `fireEvent` for interactions
- Use `findBy` for elements that appear asynchronously
- Use `queryBy` to assert element does not exist
- Clean up after each test with `afterEach(() => cleanup())`
- Avoid testing implementation details
- Test what users see and do
- Use `waitFor` for async assertions
- Mock at the network layer (MSW) not the component layer
- Write descriptive test names
- Follow Arrange-Act-Assert pattern
