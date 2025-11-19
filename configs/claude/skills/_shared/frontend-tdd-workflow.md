# Frontend TDD Workflow

## Test-Driven Development Cycle

### 1. Red - Write Failing Test

Write a test for the functionality you want to implement. The test should fail because the code doesn't exist yet.

```typescript
// Button.test.tsx
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import { Button } from './Button'

describe('Button', () => {
  it('should call onClick when clicked', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()

    render(<Button onClick={handleClick}>Click me</Button>)

    await user.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

Run the test:
```bash
vitest Button.test.tsx
```

**Expected**: Test fails (button component doesn't exist)

### 2. Green - Write Minimal Code

Write the minimum code required to make the test pass.

```typescript
// Button.tsx
interface ButtonProps {
  onClick: () => void
  children: React.ReactNode
}

export const Button: FC<ButtonProps> = ({ onClick, children }) => {
  return <button onClick={onClick}>{children}</button>
}
```

Run the test again:
```bash
vitest Button.test.tsx
```

**Expected**: Test passes

### 3. Refactor - Improve Code

Improve the code while keeping tests green.

```typescript
// Button.tsx
interface ButtonProps {
  onClick: () => void
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
  disabled?: boolean
}

export const Button: FC<ButtonProps> = ({
  onClick,
  children,
  variant = 'primary',
  disabled = false,
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  )
}
```

Run tests to ensure refactoring didn't break anything:
```bash
vitest Button.test.tsx
```

**Expected**: All tests still pass

### 4. Repeat

Continue the cycle for each new feature or requirement.

## Test Execution Commands

### Vitest

```bash
# Run all tests
vitest

# Run in watch mode (recommended during development)
vitest --watch

# Run specific test file
vitest src/components/Button.test.tsx

# Run tests matching pattern
vitest --grep "Button"

# Run tests with coverage
vitest --coverage

# Run tests in UI mode
vitest --ui

# Run only changed tests
vitest --changed
```

## Coverage Checking

```bash
# Generate coverage report
vitest --coverage

# View coverage in browser
open coverage/index.html

# Set minimum coverage thresholds in vite.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    },
  },
})
```

## Type Checking

```bash
# Check types (no output if successful)
tsc --noEmit

# Watch mode
tsc --noEmit --watch

# Check specific file
tsc --noEmit src/components/Button.tsx
```

## Linting and Formatting

```bash
# ESLint - Lint code
eslint src/ --ext .ts,.tsx

# ESLint - Auto-fix issues
eslint src/ --ext .ts,.tsx --fix

# Prettier - Check formatting
prettier --check "src/**/*.{ts,tsx}"

# Prettier - Format files
prettier --write "src/**/*.{ts,tsx}"

# Run both in sequence
prettier --write "src/**/*.{ts,tsx}" && eslint src/ --ext .ts,.tsx --fix
```

## Complete Workflow Example

```bash
# 1. Write test (Red)
vitest Button.test.tsx
# Test fails ✗

# 2. Write minimal code (Green)
vitest Button.test.tsx
# Test passes ✓

# 3. Refactor
vitest Button.test.tsx
# Test still passes ✓

# 4. Run full test suite
vitest

# 5. Check types
tsc --noEmit

# 6. Check coverage
vitest --coverage

# 7. Lint and format
prettier --write "src/**/*.{ts,tsx}"
eslint src/ --ext .ts,.tsx --fix

# 8. Commit changes
git add .
git commit -m "feat: add Button component with click handler"
```

## Commit Guidelines

- **One feature per commit**: Keep commits focused
- **All tests passing**: Never commit failing tests
- **Clean code**: Run linter and formatter before commit
- **Type safe**: Ensure `tsc --noEmit` passes
- **Meaningful messages**: Use conventional commits format

### Conventional Commits Format

```
feat: add user authentication
fix: correct email validation logic
refactor: extract validation into custom hook
test: add tests for login form
docs: update README with setup instructions
style: format code with prettier
chore: update dependencies
```

## Best Practices

- **Write test first**: Always write the test before implementation
- **Run tests frequently**: Use watch mode during development
- **Keep tests simple**: One assertion per test when possible
- **Test behavior**: Focus on what users see and do, not implementation
- **Maintain coverage**: Aim for 80%+ coverage on critical code
- **Fast feedback**: Run subset of tests during development, full suite before commit
- **Type safety**: Catch errors at compile time with TypeScript
- **Clean code**: Use linter and formatter consistently
- **Small commits**: Commit frequently with clear messages
