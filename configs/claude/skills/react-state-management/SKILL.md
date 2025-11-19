---
name: react-state-management
description: Implement state management with Context API and TanStack Query. Use when managing global client state, handling server state, implementing optimistic updates, or coordinating state across components.
---

# React State Management Specialist

Specialized in managing application state using React Context API for client state and TanStack Query for server state.

## When to Use This Skill

- Managing global client state (user preferences, UI state, etc.)
- Implementing server state management with caching and revalidation
- Coordinating state across multiple components
- Implementing optimistic updates for better UX
- Choosing between local, global, client, and server state
- Normalizing state for efficient updates

## Core Principles

- **Local First**: Prefer local state when possible
- **Lift State Up**: Move state to common ancestor when needed
- **Separate Client/Server State**: Use Context for client, TanStack Query for server
- **Single Source of Truth**: Avoid state duplication
- **Optimistic UI**: Update UI immediately, sync with server later
- **Data Normalization**: Structure state for efficient access and updates

## Implementation Guidelines

### State Selection Guidelines

```typescript
// Local state - Component-specific, doesn't need to be shared
const [isOpen, setIsOpen] = useState(false)
const [searchQuery, setSearchQuery] = useState('')

// Lifted state - Shared among child components
const Parent = () => {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  return (
    <>
      <List onSelect={setSelectedId} />
      <Detail id={selectedId} />
    </>
  )
}

// Global client state - App-wide UI state, user preferences
// Use Context API
const theme = useTheme() // 'light' | 'dark'
const locale = useLocale() // 'en' | 'ja'

// Server state - Data from API, needs caching and revalidation
// Use TanStack Query
const { data: users } = useQuery({ queryKey: ['users'], queryFn: fetchUsers })
```

### Context API for Global Client State

```typescript
import { createContext, useContext, useState, ReactNode } from 'react'

// 1. Define context value type
interface ThemeContextValue {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

// 2. Create context with undefined default
const ThemeContext = createContext<ThemeContextValue | undefined>(undefined)

// 3. Create provider component
export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    // WHY: Initialize from localStorage for persistence
    const saved = localStorage.getItem('theme')
    return (saved === 'dark' ? 'dark' : 'light')
  })

  const toggleTheme = () => {
    setTheme(prev => {
      const newTheme = prev === 'light' ? 'dark' : 'light'
      localStorage.setItem('theme', newTheme)
      return newTheme
    })
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// 4. Create custom hook for consuming context
export const useTheme = (): ThemeContextValue => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}

// 5. Usage in app
const App = () => {
  return (
    <ThemeProvider>
      <Dashboard />
    </ThemeProvider>
  )
}

// 6. Usage in components
const Dashboard = () => {
  const { theme, toggleTheme } = useTheme()

  return (
    <div className={theme === 'light' ? 'light-mode' : 'dark-mode'}>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  )
}
```

### Complex Context with useReducer

```typescript
// State and actions
type State = {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
}

type Action =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_FAILURE' }
  | { type: 'LOGOUT' }

// Reducer
function authReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, loading: true }
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        loading: false,
      }
    case 'LOGIN_FAILURE':
      return { ...state, loading: false }
    case 'LOGOUT':
      return { user: null, isAuthenticated: false, loading: false }
    default:
      return state
  }
}

// Context value
interface AuthContextValue {
  state: State
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

// Provider
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    isAuthenticated: false,
    loading: false,
  })

  const login = async (email: string, password: string) => {
    dispatch({ type: 'LOGIN_START' })
    try {
      const user = await api.login(email, password)
      dispatch({ type: 'LOGIN_SUCCESS', payload: user })
    } catch {
      dispatch({ type: 'LOGIN_FAILURE' })
    }
  }

  const logout = () => {
    api.logout()
    dispatch({ type: 'LOGOUT' })
  }

  return (
    <AuthContext.Provider value={{ state, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

### TanStack Query for Server State

```typescript
// Setup QueryClient
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
    },
  },
})

export const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  )
}

// Basic query
import { useQuery } from '@tanstack/react-query'

export const UserList = () => {
  const {
    data: users,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users')
      if (!response.ok) throw new Error('Failed to fetch')
      return response.json()
    },
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

// Query with parameters
export const UserDetail = ({ userId }: { userId: string }) => {
  const { data: user } = useQuery({
    queryKey: ['users', userId],
    queryFn: () => fetchUser(userId),
    // WHY: Don't fetch if userId is null
    enabled: !!userId,
  })

  return <div>{user?.name}</div>
}

// Dependent queries
export const UserOrders = ({ userId }: { userId: string }) => {
  const { data: user } = useQuery({
    queryKey: ['users', userId],
    queryFn: () => fetchUser(userId),
  })

  // WHY: Only fetch orders after user is loaded
  const { data: orders } = useQuery({
    queryKey: ['orders', userId],
    queryFn: () => fetchOrders(userId),
    enabled: !!user,
  })

  return <div>...</div>
}
```

### Mutations with TanStack Query

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

export const CreateUserForm = () => {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (newUser: NewUser) => {
      return fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(newUser),
      }).then(res => res.json())
    },
    onSuccess: () => {
      // WHY: Invalidate and refetch users list after creation
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate({ name: 'John', email: 'john@example.com' })
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <button disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create User'}
      </button>
      {mutation.isError && <div>Error: {mutation.error.message}</div>}
    </form>
  )
}
```

### Optimistic Updates

```typescript
export const TodoList = () => {
  const queryClient = useQueryClient()

  const toggleMutation = useMutation({
    mutationFn: async (todoId: string) => {
      return fetch(`/api/todos/${todoId}/toggle`, { method: 'POST' })
    },
    // WHY: Update UI immediately for better UX
    onMutate: async (todoId) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['todos'] })

      // Snapshot previous value
      const previousTodos = queryClient.getQueryData(['todos'])

      // Optimistically update
      queryClient.setQueryData(['todos'], (old: Todo[]) =>
        old.map(todo =>
          todo.id === todoId
            ? { ...todo, completed: !todo.completed }
            : todo
        )
      )

      // Return context for rollback
      return { previousTodos }
    },
    onError: (err, todoId, context) => {
      // WHY: Rollback on error
      queryClient.setQueryData(['todos'], context?.previousTodos)
    },
    onSettled: () => {
      // WHY: Refetch to ensure consistency
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  return <div>...</div>
}
```

### State Normalization

```typescript
// Bad: Nested structure makes updates difficult
type State = {
  posts: Array<{
    id: string
    title: string
    author: {
      id: string
      name: string
    }
    comments: Array<{
      id: string
      text: string
      author: {
        id: string
        name: string
      }
    }>
  }>
}

// Good: Normalized structure
type NormalizedState = {
  users: Record<string, User>
  posts: Record<string, Post>
  comments: Record<string, Comment>
}

// Selector to get post with relations
function selectPostWithRelations(state: NormalizedState, postId: string) {
  const post = state.posts[postId]
  return {
    ...post,
    author: state.users[post.authorId],
    comments: post.commentIds.map(id => ({
      ...state.comments[id],
      author: state.users[state.comments[id].authorId],
    })),
  }
}

// Update is simpler
function updateUser(state: NormalizedState, userId: string, updates: Partial<User>) {
  return {
    ...state,
    users: {
      ...state.users,
      [userId]: { ...state.users[userId], ...updates },
    },
  }
}
```

### Combining Context and TanStack Query

```typescript
// Use Context for derived UI state
interface UIContextValue {
  selectedUserId: string | null
  setSelectedUserId: (id: string | null) => void
}

const UIContext = createContext<UIContextValue | undefined>(undefined)

export const UIProvider = ({ children }: { children: ReactNode }) => {
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null)

  return (
    <UIContext.Provider value={{ selectedUserId, setSelectedUserId }}>
      {children}
    </UIContext.Provider>
  )
}

// Use TanStack Query for server data
export const UserDashboard = () => {
  const { selectedUserId } = useUI()
  const { data: users } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  })

  const { data: selectedUser } = useQuery({
    queryKey: ['users', selectedUserId],
    queryFn: () => fetchUser(selectedUserId!),
    enabled: !!selectedUserId,
  })

  return (
    <div>
      <UserList users={users} />
      {selectedUser && <UserDetail user={selectedUser} />}
    </div>
  )
}
```

## Tools to Use

- `Read`: Read existing context providers and queries
- `Write`: Create new state management code
- `Edit`: Update state management logic
- `Bash`: Run tests and type checker

### Bash Commands

```bash
# Type checking
tsc --noEmit

# Run tests
vitest

# Run development server
vite
```

## Workflow

1. **Identify State Type**: Determine if state is local, global client, or server
2. **Choose Solution**: Use local state, Context API, or TanStack Query
3. **Write Tests First**: Test state management logic with TDD
4. **Implement State**: Create context providers or queries
5. **Test Integration**: Ensure components work with state
6. **Optimize**: Add memoization if needed
7. **Commit**: Create atomic commit

## Related Skills

- `react-component-development`: For component integration
- `vitest-react-testing`: For testing state logic
- `typescript-core-development`: For type-safe state

## Coding Standards

See [React Coding Standards](../_shared/react-coding-standards.md)

## TDD Workflow

Follow [Frontend TDD Workflow](../_shared/frontend-tdd-workflow.md)

## Key Reminders

- Prefer local state when possible, lift state up when needed
- Use Context API for global client state (theme, locale, UI state)
- Use TanStack Query for server state (API data, caching)
- Implement optimistic updates for better UX
- Normalize state for efficient updates
- Always provide custom hooks for consuming context
- Throw error if context is used outside provider
- Use useReducer for complex state logic
- Invalidate queries after mutations
- Set staleTime and cacheTime appropriately
- Enable queries conditionally when needed
- Test state management logic thoroughly
- Write comments explaining WHY, not WHAT
