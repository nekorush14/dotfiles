# React Coding Standards

## Component Structure

All React components should follow this consistent structure:

```typescript
// 1. Imports - React first, then external, then internal, then types
import { useState, useEffect } from 'react'
import { Button } from '@/components/Button'
import { useFetch } from '@/hooks/useFetch'
import type { User } from '@/types/User'

// 2. Types/Interfaces - Define props interface
interface UserCardProps {
  user: User
  onEdit: (id: string) => void
  onDelete: (id: string) => void
}

// 3. Component - Main component definition
export const UserCard: FC<UserCardProps> = ({ user, onEdit, onDelete }) => {
  // 3a. Hooks - Group all hooks at the top
  const [isEditing, setIsEditing] = useState(false)
  const { data, loading } = useFetch(`/api/users/${user.id}`)

  // 3b. Event Handlers - Define handlers
  const handleEdit = () => {
    setIsEditing(true)
    onEdit(user.id)
  }

  const handleDelete = () => {
    if (confirm('Are you sure?')) {
      onDelete(user.id)
    }
  }

  // 3c. Early Returns - Handle loading/error states
  if (loading) return <div>Loading...</div>
  if (!data) return <div>No data</div>

  // 3d. Render - Main render logic
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <Button onClick={handleEdit}>Edit</Button>
      <Button onClick={handleDelete}>Delete</Button>
    </div>
  )
}

// 4. Sub-components (if any) - Define after main component
const UserCardHeader: FC<{ title: string }> = ({ title }) => {
  return <h3>{title}</h3>
}
```

## Props Naming and Types

### Props Interface Naming

```typescript
// Component name + Props suffix
interface ButtonProps {}
interface UserCardProps {}
interface ModalProps {}
```

### Event Handler Props

```typescript
// Always prefix callback props with 'on'
interface CardProps {
  onEdit: (id: string) => void
  onDelete: (id: string) => void
  onSubmit: (data: FormData) => Promise<void>
  onClick?: () => void // Optional callbacks
}
```

### Children Prop

```typescript
// Use React.ReactNode for children
interface CardProps {
  children: React.ReactNode
  title: string
}

// Or use FC type which includes children automatically
export const Card: FC<{ title: string }> = ({ title, children }) => {
  return (
    <div>
      <h2>{title}</h2>
      {children}
    </div>
  )
}
```

### Boolean Props

```typescript
// Prefix boolean props with 'is', 'has', 'should', or 'can'
interface ButtonProps {
  isLoading: boolean
  isDisabled: boolean
  hasIcon?: boolean
}
```

## Hooks Usage Rules

### Hooks Order

Always declare hooks in this order:

```typescript
export const MyComponent: FC = () => {
  // 1. State hooks
  const [count, setCount] = useState(0)
  const [user, setUser] = useState<User | null>(null)

  // 2. Context hooks
  const theme = useTheme()
  const auth = useAuth()

  // 3. Ref hooks
  const inputRef = useRef<HTMLInputElement>(null)

  // 4. Reducer hooks
  const [state, dispatch] = useReducer(reducer, initialState)

  // 5. Custom hooks
  const { data, loading } = useFetch('/api/users')

  // 6. useMemo hooks
  const sortedItems = useMemo(() => items.sort(), [items])

  // 7. useCallback hooks
  const handleClick = useCallback(() => {
    // Handler logic
  }, [])

  // 8. useEffect hooks - Always last
  useEffect(() => {
    // Effect logic
  }, [])

  return <div>...</div>
}
```

### Custom Hook Naming

```typescript
// Always prefix with 'use'
function useFetch<T>(url: string) {}
function useLocalStorage<T>(key: string) {}
function useDebounce<T>(value: T, delay: number) {}
```

### Effect Dependencies

```typescript
// Good: Include all dependencies
useEffect(() => {
  fetchUser(userId)
}, [userId]) // userId is used in effect

// Bad: Missing dependencies
useEffect(() => {
  fetchUser(userId)
}, []) // ESLint will warn

// Good: Empty array for mount-only effects
useEffect(() => {
  // Only run once on mount
  initializeApp()
}, [])

// Good: Cleanup function
useEffect(() => {
  const interval = setInterval(() => {
    console.log('tick')
  }, 1000)

  // WHY: Clear interval on unmount
  return () => clearInterval(interval)
}, [])
```

### Functional setState

```typescript
// Good: Functional update when depending on previous state
const increment = () => {
  setCount(prevCount => prevCount + 1)
}

// Bad: Direct update based on current state
const increment = () => {
  setCount(count + 1) // Can lead to stale state issues
}
```

## Component Naming and Files

### File Naming

```
components/
├── Button.tsx              # Single component export
├── UserCard/               # Multiple related components
│   ├── UserCard.tsx        # Main component
│   ├── UserCardHeader.tsx  # Sub-component
│   ├── UserCard.test.tsx   # Tests
│   └── index.ts            # Re-export
└── index.ts                # Barrel export (optional)
```

### Export Patterns

```typescript
// Named export (preferred)
export const Button: FC<ButtonProps> = ({ label }) => {
  return <button>{label}</button>
}

// With barrel export in index.ts
export { Button } from './Button'

// Usage
import { Button } from '@/components/Button'
```

## State Management Guidelines

### Local vs Global State

```typescript
// Local state - Component-specific data
const [isOpen, setIsOpen] = useState(false)

// Global state - Shared across components
const user = useAuth() // From context
const cart = useCart() // From context/store
```

### When to Lift State Up

```typescript
// Bad: Duplicated state in multiple components
const ComponentA = () => {
  const [user, setUser] = useState(null)
  // ...
}

const ComponentB = () => {
  const [user, setUser] = useState(null)
  // ...
}

// Good: Lift state to common parent
const Parent = () => {
  const [user, setUser] = useState(null)
  return (
    <>
      <ComponentA user={user} />
      <ComponentB user={user} />
    </>
  )
}
```

## Performance Best Practices

### Use memo for Expensive Components

```typescript
// Only re-render when props change
export const ExpensiveComponent = memo<Props>(({ data }) => {
  // Expensive rendering logic
  return <div>...</div>
})
```

### Use useMemo for Expensive Calculations

```typescript
// Only recalculate when dependencies change
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name))
}, [items])
```

### Use useCallback for Event Handlers

```typescript
// Prevent function recreation on every render
const handleClick = useCallback((id: string) => {
  console.log('Clicked:', id)
}, [])

// Pass to memoized child components
<MemoizedChild onClick={handleClick} />
```

### Avoid Inline Functions in Props

```typescript
// Bad: Creates new function on every render
<Button onClick={() => handleClick(id)} />

// Good: Use useCallback or stable reference
const onClick = useCallback(() => handleClick(id), [id])
<Button onClick={onClick} />
```

## Conditional Rendering

```typescript
// Early return pattern
if (loading) return <Loader />
if (error) return <Error message={error} />
if (!data) return <Empty />

// Ternary for simple conditions
{isLoggedIn ? <Dashboard /> : <Login />}

// Logical && for optional rendering
{error && <ErrorMessage error={error} />}

// Switch/case for multiple conditions
const renderContent = () => {
  switch (status) {
    case 'loading':
      return <Loader />
    case 'error':
      return <Error />
    case 'success':
      return <Content />
    default:
      return null
  }
}
```

## List Rendering

```typescript
// Always use key prop
{items.map(item => (
  <Item key={item.id} data={item} />
))}

// Don't use index as key if list can be reordered
// Bad
{items.map((item, index) => (
  <Item key={index} data={item} />
))}

// Good: Use stable ID
{items.map(item => (
  <Item key={item.id} data={item} />
))}
```

## Component Composition

```typescript
// Prefer composition over complex props
// Good
<Card>
  <CardHeader>
    <h2>Title</h2>
  </CardHeader>
  <CardBody>
    <p>Content</p>
  </CardBody>
</Card>

// Less flexible
<Card
  title="Title"
  content="Content"
/>
```

## Testing Considerations

```typescript
// Export components for testing
export const Button: FC<ButtonProps> = ({ label, onClick }) => {
  return <button onClick={onClick}>{label}</button>
}

// Use data-testid for test selectors
<button data-testid="submit-button" onClick={onClick}>
  Submit
</button>

// Avoid test IDs in production (optional)
{process.env.NODE_ENV === 'test' && (
  <div data-testid="test-only-element" />
)}
```

## Key Reminders

- Follow consistent component structure (imports → types → hooks → handlers → render)
- Group hooks by type and always place useEffect last
- Use functional setState updates when depending on previous state
- Prefix event handler props with 'on', internal handlers with 'handle'
- Always include cleanup functions in useEffect when needed
- Use memo, useMemo, useCallback for performance but don't over-optimize
- Prefer composition over complex prop configurations
- Always use stable keys in list rendering
- Keep components focused on single responsibility
- Extract reusable logic into custom hooks
