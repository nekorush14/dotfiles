# TypeScript Coding Standards

## Indentation

- 2 spaces (JavaScript/TypeScript)

## Linter & Formatter

### ESLint + Prettier

- **ESLint**: Linting and code quality rules
- **Prettier**: Code formatting
- **TypeScript ESLint**: TypeScript-specific linting rules

### Configuration

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint", "react", "react-hooks"],
  "rules": {
    "@typescript-eslint/explicit-function-return-type": "off",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
```

### Usage

```bash
# Linting
eslint src/ --ext .ts,.tsx

# Auto-fix
eslint src/ --ext .ts,.tsx --fix

# Formatting
prettier --write "src/**/*.{ts,tsx}"

# Type checking
tsc --noEmit
```

## Type Annotations

- **Always use type annotations** for function parameters and return types
- Let TypeScript infer types for simple variables when obvious
- Use explicit types for complex structures

### Good Example

```typescript
// Explicit function types
function calculateTotal(prices: number[], taxRate: number): number {
  const subtotal = prices.reduce((sum, price) => sum + price, 0)
  return subtotal * (1 + taxRate)
}

// Type inference for simple variables
const count = 5 // number (inferred)
const name = 'John' // string (inferred)

// Explicit types for complex structures
const user: User = {
  id: '1',
  name: 'John',
  email: 'john@example.com',
}
```

### Bad Example

```typescript
// Missing type annotations
function calculateTotal(prices, taxRate) {
  const subtotal = prices.reduce((sum, price) => sum + price, 0)
  return subtotal * (1 + taxRate)
}

// Unnecessary explicit type for simple variable
const count: number = 5
```

## Naming Conventions

### File Naming

- Components: `PascalCase.tsx` (e.g., `UserCard.tsx`)
- Hooks: `useCamelCase.ts` (e.g., `useFetch.ts`)
- Utilities: `camelCase.ts` (e.g., `formatDate.ts`)
- Types: `PascalCase.ts` or `types.ts` (e.g., `User.ts` or `types.ts`)
- Constants: `UPPER_SNAKE_CASE.ts` or `constants.ts`

### Code Naming

- **PascalCase**: Components, Types, Interfaces, Classes
  ```typescript
  interface User {}
  type OrderStatus = 'pending' | 'completed'
  class UserService {}
  const UserCard: FC = () => {}
  ```

- **camelCase**: Variables, functions, methods, hooks
  ```typescript
  const userName = 'John'
  function fetchUser() {}
  const useFetch = () => {}
  ```

- **UPPER_SNAKE_CASE**: Constants
  ```typescript
  const API_URL = 'https://api.example.com'
  const MAX_RETRIES = 3
  ```

## Import Order

Following ESLint `import/order` conventions:

1. React imports
2. External library imports
3. Internal imports (components, hooks, utils)
4. Type imports
5. Blank line between each group

### Example

```typescript
// React
import { useState, useEffect } from 'react'

// External libraries
import axios from 'axios'
import { z } from 'zod'

// Internal - Components
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'

// Internal - Hooks
import { useFetch } from '@/hooks/useFetch'
import { useAuth } from '@/hooks/useAuth'

// Internal - Utils
import { formatDate } from '@/utils/formatDate'
import { cn } from '@/utils/cn'

// Types
import type { User } from '@/types/User'
import type { Order } from '@/types/Order'
```

## Comments

- Language: English
- Style: Explain **WHY**, not WHAT or HOW
- Use JSDoc for public APIs

### Good Example

```typescript
// WHY: Debounce to avoid excessive API calls during typing
const debouncedSearch = useMemo(
  () => debounce(handleSearch, 300),
  [handleSearch]
)

// WHY: Clean up event listener to prevent memory leaks
useEffect(() => {
  window.addEventListener('resize', handleResize)
  return () => window.removeEventListener('resize', handleResize)
}, [])

/**
 * Fetch user data with automatic retry on failure.
 *
 * WHY: Network requests can fail, retry improves reliability
 */
async function fetchUser(id: string): Promise<User> {
  // Implementation
}
```

### Bad Example

```typescript
// Set loading to true (obvious from code)
setLoading(true)

// Call the API (obvious from code)
const response = await api.getUser(id)
```

## Directory Structure

```
src/
├── components/          # React components
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   └── Card/
│       ├── Card.tsx
│       └── index.ts
├── hooks/              # Custom React hooks
│   ├── useFetch.ts
│   └── useLocalStorage.ts
├── utils/              # Utility functions
│   ├── formatDate.ts
│   └── cn.ts
├── types/              # TypeScript types/interfaces
│   ├── User.ts
│   └── Order.ts
├── lib/                # Third-party library configs
│   └── api.ts
├── pages/              # Next.js pages (if using Next.js)
│   └── index.tsx
└── app/                # Next.js app directory (if using App Router)
    └── page.tsx
```

## Type Safety Best Practices

### Prefer Interfaces for Objects

```typescript
// Good: Interface for object shapes
interface User {
  id: string
  name: string
  email: string
}

// Good: Type for unions/intersections
type Status = 'pending' | 'completed' | 'cancelled'
type UserWithStatus = User & { status: Status }
```

### Use const assertions

```typescript
// Without const assertion
const colors = ['red', 'green', 'blue'] // string[]

// With const assertion
const colors = ['red', 'green', 'blue'] as const // readonly ['red', 'green', 'blue']
```

### Use unknown over any

```typescript
// Bad
function processValue(value: any) {
  return value.toString()
}

// Good
function processValue(value: unknown) {
  if (typeof value === 'string' || typeof value === 'number') {
    return value.toString()
  }
  throw new Error('Unsupported type')
}
```

## React-Specific Standards

### Props Interface Naming

```typescript
// Component name + Props
interface ButtonProps {
  label: string
  onClick: () => void
}

export const Button: FC<ButtonProps> = ({ label, onClick }) => {
  return <button onClick={onClick}>{label}</button>
}
```

### Event Handler Naming

```typescript
// Prefix with 'handle' for internal handlers
const handleClick = () => {
  console.log('Clicked')
}

// Prefix with 'on' for prop callbacks
interface CardProps {
  onDelete: (id: string) => void
  onEdit: (id: string) => void
}
```

### Hook Naming

```typescript
// Always prefix custom hooks with 'use'
function useFetch<T>(url: string) {
  // Implementation
}

function useLocalStorage<T>(key: string, initialValue: T) {
  // Implementation
}
```

## Code Organization Principles

- **Single Responsibility**: One file/function = one responsibility
- **DRY (Don't Repeat Yourself)**: Extract common logic
- **Explicit is Better Than Implicit**: Clear over clever
- **Type Safety First**: Use TypeScript's type system fully
- **Immutability**: Prefer `const` and readonly
- **Composition Over Inheritance**: Use composition patterns
