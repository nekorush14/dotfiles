# Vitest Testing Patterns for Angular v21

Testing patterns and best practices for Angular v21 applications using Vitest, following Test-Driven Development (TDD) approach.

## Table of Contents

- [Setup and Configuration](#setup-and-configuration)
- [Component Testing](#component-testing)
- [Service Testing](#service-testing)
- [Form Testing](#form-testing)
- [Async Testing](#async-testing)
- [Mocking Patterns](#mocking-patterns)
- [TDD Workflow](#tdd-workflow)

## Setup and Configuration

### Basic Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import angular from '@analogjs/vite-plugin-angular'

export default defineConfig({
  plugins: [angular()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['src/test-setup.ts'],
    include: ['**/*.spec.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.ts'],
      exclude: [
        'src/**/*.spec.ts',
        'src/test-setup.ts',
        'src/main.ts',
      ],
    },
  },
})
```

### Test Setup File

```typescript
// src/test-setup.ts
import 'zone.js'
import 'zone.js/testing'
import { getTestBed } from '@angular/core/testing'
import {
  BrowserDynamicTestingModule,
  platformBrowserDynamicTesting,
} from '@angular/platform-browser-dynamic/testing'

// WHY: Initialize Angular testing environment
getTestBed().initTestEnvironment(
  BrowserDynamicTestingModule,
  platformBrowserDynamicTesting()
)
```

## Component Testing

### Basic Component Test

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { ButtonComponent } from './button.component'

describe('ButtonComponent', () => {
  let component: ButtonComponent
  let fixture: ComponentFixture<ButtonComponent>

  beforeEach(async () => {
    // WHY: Configure testing module with component imports
    await TestBed.configureTestingModule({
      imports: [ButtonComponent],
    }).compileComponents()

    fixture = TestBed.createComponent(ButtonComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })

  it('should render button text', () => {
    const compiled = fixture.nativeElement as HTMLElement
    const button = compiled.querySelector('button')
    expect(button?.textContent?.trim()).toBe('Click me')
  })
})
```

### Testing Signal Inputs

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { UserCardComponent } from './user-card.component'

describe('UserCardComponent', () => {
  let fixture: ComponentFixture<UserCardComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent],
    }).compileComponents()

    fixture = TestBed.createComponent(UserCardComponent)
  })

  it('should display user name', () => {
    // WHY: Use fixture.componentRef.setInput for signal inputs
    fixture.componentRef.setInput('user', {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    })
    fixture.detectChanges()

    const compiled = fixture.nativeElement as HTMLElement
    expect(compiled.textContent).toContain('John Doe')
  })

  it('should hide actions when showActions is false', () => {
    fixture.componentRef.setInput('user', {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    })
    fixture.componentRef.setInput('showActions', false)
    fixture.detectChanges()

    const compiled = fixture.nativeElement as HTMLElement
    const actions = compiled.querySelector('.actions')
    expect(actions).toBeNull()
  })
})
```

### Testing Signal Outputs

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { UserCardComponent } from './user-card.component'

describe('UserCardComponent - Outputs', () => {
  let fixture: ComponentFixture<UserCardComponent>
  let component: UserCardComponent

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent],
    }).compileComponents()

    fixture = TestBed.createComponent(UserCardComponent)
    component = fixture.componentInstance

    fixture.componentRef.setInput('user', {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    })
    fixture.detectChanges()
  })

  it('should emit onEdit when edit button is clicked', () => {
    let emittedId: string | undefined

    // WHY: Subscribe to output events
    component.onEdit.subscribe((id: string) => {
      emittedId = id
    })

    const editButton = fixture.nativeElement.querySelector('button.edit')
    editButton?.click()

    expect(emittedId).toBe('1')
  })

  it('should emit onDelete when delete button is clicked', () => {
    const deleteSpy = vi.fn()
    component.onDelete.subscribe(deleteSpy)

    const deleteButton = fixture.nativeElement.querySelector('button.delete')
    deleteButton?.click()

    expect(deleteSpy).toHaveBeenCalledWith('1')
    expect(deleteSpy).toHaveBeenCalledTimes(1)
  })
})
```

### Testing Computed Signals

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { TodoListComponent } from './todo-list.component'

describe('TodoListComponent - Computed Signals', () => {
  let fixture: ComponentFixture<TodoListComponent>
  let component: TodoListComponent

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TodoListComponent],
    }).compileComponents()

    fixture = TestBed.createComponent(TodoListComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should compute remaining count correctly', () => {
    // WHY: Test computed signals by setting dependencies
    component.todos.set([
      { id: '1', title: 'Task 1', completed: false },
      { id: '2', title: 'Task 2', completed: true },
      { id: '3', title: 'Task 3', completed: false },
    ])

    expect(component.remainingCount()).toBe(2)
  })

  it('should update computed signal when todos change', () => {
    component.todos.set([
      { id: '1', title: 'Task 1', completed: false },
    ])
    expect(component.remainingCount()).toBe(1)

    component.todos.update(current => [
      ...current,
      { id: '2', title: 'Task 2', completed: false },
    ])
    expect(component.remainingCount()).toBe(2)
  })
})
```

### Testing Control Flow (@if, @for, @switch)

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { ProductListComponent } from './product-list.component'

describe('ProductListComponent - Control Flow', () => {
  let fixture: ComponentFixture<ProductListComponent>
  let component: ProductListComponent

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProductListComponent],
    }).compileComponents()

    fixture = TestBed.createComponent(ProductListComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  // WHY: Test @if directive behavior
  it('should show loading state', () => {
    component.isLoading.set(true)
    fixture.detectChanges()

    const compiled = fixture.nativeElement as HTMLElement
    expect(compiled.textContent).toContain('Loading products...')
  })

  it('should show error message', () => {
    component.isLoading.set(false)
    component.error.set('Failed to load products')
    fixture.detectChanges()

    const compiled = fixture.nativeElement as HTMLElement
    expect(compiled.textContent).toContain('Error: Failed to load products')
  })

  // WHY: Test @for directive behavior
  it('should render all products', () => {
    component.isLoading.set(false)
    component.products.set([
      { id: '1', name: 'Product 1', price: 100, inStock: true },
      { id: '2', name: 'Product 2', price: 200, inStock: true },
    ])
    fixture.detectChanges()

    const productElements = fixture.nativeElement.querySelectorAll('.product')
    expect(productElements.length).toBe(2)
  })

  it('should show empty message when no products', () => {
    component.isLoading.set(false)
    component.products.set([])
    fixture.detectChanges()

    const compiled = fixture.nativeElement as HTMLElement
    expect(compiled.textContent).toContain('No products found')
  })

  // WHY: Test @switch directive behavior
  it('should render list view', () => {
    component.viewMode.set('list')
    component.products.set([
      { id: '1', name: 'Product 1', price: 100, inStock: true },
    ])
    fixture.detectChanges()

    const listView = fixture.nativeElement.querySelector('.space-y-2')
    expect(listView).not.toBeNull()
  })

  it('should render grid view', () => {
    component.viewMode.set('grid')
    component.products.set([
      { id: '1', name: 'Product 1', price: 100, inStock: true },
    ])
    fixture.detectChanges()

    const gridView = fixture.nativeElement.querySelector('.grid')
    expect(gridView).not.toBeNull()
  })
})
```

## Service Testing

### Basic Service Test

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { TestBed } from '@angular/core/testing'
import { UserService } from './user.service'

describe('UserService', () => {
  let service: UserService

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [UserService],
    })
    service = TestBed.inject(UserService)
  })

  it('should be created', () => {
    expect(service).toBeTruthy()
  })
})
```

### Testing HTTP Requests

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { TestBed } from '@angular/core/testing'
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing'
import { UserService } from './user.service'

describe('UserService - HTTP', () => {
  let service: UserService
  let httpMock: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService],
    })

    service = TestBed.inject(UserService)
    httpMock = TestBed.inject(HttpTestingController)
  })

  afterEach(() => {
    // WHY: Verify that no unmatched requests are outstanding
    httpMock.verify()
  })

  it('should fetch users', () => {
    const mockUsers = [
      { id: '1', name: 'John Doe', email: 'john@example.com' },
      { id: '2', name: 'Jane Smith', email: 'jane@example.com' },
    ]

    service.getUsers().subscribe(users => {
      expect(users).toEqual(mockUsers)
      expect(users.length).toBe(2)
    })

    const req = httpMock.expectOne('/api/users')
    expect(req.request.method).toBe('GET')
    req.flush(mockUsers)
  })

  it('should create user', () => {
    const newUser = { name: 'New User', email: 'new@example.com' }
    const createdUser = { id: '3', ...newUser }

    service.createUser(newUser).subscribe(user => {
      expect(user).toEqual(createdUser)
    })

    const req = httpMock.expectOne('/api/users')
    expect(req.request.method).toBe('POST')
    expect(req.request.body).toEqual(newUser)
    req.flush(createdUser)
  })

  it('should handle error', () => {
    service.getUsers().subscribe({
      next: () => fail('should have failed with 500 error'),
      error: (error) => {
        expect(error.status).toBe(500)
      },
    })

    const req = httpMock.expectOne('/api/users')
    req.flush('Server error', { status: 500, statusText: 'Internal Server Error' })
  })
})
```

## Form Testing

### Reactive Form Testing

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { ReactiveFormsModule } from '@angular/forms'
import { LoginFormComponent } from './login-form.component'

describe('LoginFormComponent', () => {
  let fixture: ComponentFixture<LoginFormComponent>
  let component: LoginFormComponent

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginFormComponent, ReactiveFormsModule],
    }).compileComponents()

    fixture = TestBed.createComponent(LoginFormComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create form with default values', () => {
    expect(component.form.value).toEqual({
      email: '',
      password: '',
      rememberMe: false,
    })
  })

  it('should validate email field', () => {
    const emailControl = component.form.controls.email

    expect(emailControl.valid).toBe(false)

    emailControl.setValue('invalid-email')
    expect(emailControl.valid).toBe(false)
    expect(emailControl.errors?.['email']).toBeTruthy()

    emailControl.setValue('valid@example.com')
    expect(emailControl.valid).toBe(true)
  })

  it('should validate password field', () => {
    const passwordControl = component.form.controls.password

    expect(passwordControl.valid).toBe(false)

    passwordControl.setValue('short')
    expect(passwordControl.valid).toBe(false)
    expect(passwordControl.errors?.['minlength']).toBeTruthy()

    passwordControl.setValue('long-enough-password')
    expect(passwordControl.valid).toBe(true)
  })

  it('should disable submit button when form is invalid', () => {
    const submitButton = fixture.nativeElement.querySelector('button[type="submit"]')
    expect(submitButton.disabled).toBe(true)

    component.form.controls.email.setValue('test@example.com')
    component.form.controls.password.setValue('password123')
    fixture.detectChanges()

    expect(submitButton.disabled).toBe(false)
  })

  it('should call onSubmit when form is submitted', () => {
    component.form.controls.email.setValue('test@example.com')
    component.form.controls.password.setValue('password123')

    const form = fixture.nativeElement.querySelector('form')
    form.dispatchEvent(new Event('submit'))

    expect(component.isSubmitting()).toBe(true)
  })
})
```

## Async Testing

### Testing Observables

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { TestBed } from '@angular/core/testing'
import { of, delay } from 'rxjs'
import { DataService } from './data.service'

describe('DataService - Async', () => {
  let service: DataService

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DataService],
    })
    service = TestBed.inject(DataService)
  })

  it('should fetch data asynchronously', async () => {
    const mockData = { id: '1', name: 'Test' }

    // WHY: Use toPromise() to convert Observable to Promise for async/await
    const data = await service.getData().toPromise()
    expect(data).toBeDefined()
  })

  it('should handle delayed observables', async () => {
    const mockData = of({ id: '1', name: 'Test' }).pipe(delay(100))

    // WHY: Use fakeAsync and tick for time-based testing
    const data = await mockData.toPromise()
    expect(data).toEqual({ id: '1', name: 'Test' })
  })
})
```

### Testing Promises

```typescript
import { describe, it, expect } from 'vitest'
import { AuthService } from './auth.service'

describe('AuthService - Promises', () => {
  it('should resolve promise on successful login', async () => {
    const service = new AuthService()
    const result = await service.login('user', 'password')

    expect(result).toBeTruthy()
    expect(result.token).toBeDefined()
  })

  it('should reject promise on failed login', async () => {
    const service = new AuthService()

    await expect(
      service.login('user', 'wrong-password')
    ).rejects.toThrow('Invalid credentials')
  })
})
```

## Mocking Patterns

### Mocking Services

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { TestBed } from '@angular/core/testing'
import { UserService } from './user.service'
import { UserListComponent } from './user-list.component'
import { of } from 'rxjs'

describe('UserListComponent - with mocked service', () => {
  let fixture: ComponentFixture<UserListComponent>
  let component: UserListComponent
  let mockUserService: Partial<UserService>

  beforeEach(async () => {
    // WHY: Create mock service with spy functions
    mockUserService = {
      getUsers: vi.fn().mockReturnValue(of([
        { id: '1', name: 'John Doe' },
        { id: '2', name: 'Jane Smith' },
      ])),
      deleteUser: vi.fn().mockReturnValue(of(void 0)),
    }

    await TestBed.configureTestingModule({
      imports: [UserListComponent],
      providers: [
        { provide: UserService, useValue: mockUserService },
      ],
    }).compileComponents()

    fixture = TestBed.createComponent(UserListComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should load users on init', () => {
    expect(mockUserService.getUsers).toHaveBeenCalled()
    expect(component.users().length).toBe(2)
  })

  it('should delete user', () => {
    component.deleteUser('1')

    expect(mockUserService.deleteUser).toHaveBeenCalledWith('1')
  })
})
```

### Mocking inject() Dependencies

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { TestBed } from '@angular/core/testing'
import { Router } from '@angular/router'
import { UserContainerComponent } from './user-container.component'

describe('UserContainerComponent - inject() mocking', () => {
  let fixture: ComponentFixture<UserContainerComponent>
  let component: UserContainerComponent
  let mockRouter: Partial<Router>

  beforeEach(async () => {
    mockRouter = {
      navigate: vi.fn(),
    }

    await TestBed.configureTestingModule({
      imports: [UserContainerComponent],
      providers: [
        { provide: Router, useValue: mockRouter },
      ],
    }).compileComponents()

    fixture = TestBed.createComponent(UserContainerComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should navigate to edit page', () => {
    component.editUser('1')

    expect(mockRouter.navigate).toHaveBeenCalledWith(['/users', '1', 'edit'])
  })
})
```

## TDD Workflow

### Step 1: Write Failing Test

```typescript
// user-card.component.spec.ts
import { describe, it, expect } from 'vitest'
import { TestBed } from '@angular/core/testing'
import { UserCardComponent } from './user-card.component'

describe('UserCardComponent', () => {
  it('should display user name', () => {
    const fixture = TestBed.createComponent(UserCardComponent)

    fixture.componentRef.setInput('user', {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    })
    fixture.detectChanges()

    const compiled = fixture.nativeElement as HTMLElement
    expect(compiled.textContent).toContain('John Doe')
  })
})

// Run test: npm run test
// Expected: Test fails because component doesn't exist yet
```

### Step 2: Implement Minimum Code to Pass

```typescript
// user-card.component.ts
import { Component, input } from '@angular/core'

interface User {
  id: string
  name: string
  email: string
}

@Component({
  selector: 'app-user-card',
  template: `<div>{{ user().name }}</div>`,
})
export class UserCardComponent {
  user = input.required<User>()
}

// Run test: npm run test
// Expected: Test passes
```

### Step 3: Refactor While Keeping Tests Green

```typescript
// user-card.component.ts
import { Component, ChangeDetectionStrategy, input } from '@angular/core'

interface User {
  id: string
  name: string
  email: string
}

@Component({
  selector: 'app-user-card',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="rounded-lg bg-white p-6 shadow-md">
      <h3 class="text-xl font-semibold text-gray-900">{{ user().name }}</h3>
      <p class="mt-2 text-sm text-gray-600">{{ user().email }}</p>
    </div>
  `,
})
export class UserCardComponent {
  user = input.required<User>()
}

// Run test: npm run test
// Expected: Test still passes
```

### Step 4: Add More Tests

```typescript
// user-card.component.spec.ts
describe('UserCardComponent', () => {
  // ... existing test ...

  it('should display user email', () => {
    const fixture = TestBed.createComponent(UserCardComponent)

    fixture.componentRef.setInput('user', {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    })
    fixture.detectChanges()

    const compiled = fixture.nativeElement as HTMLElement
    expect(compiled.textContent).toContain('john@example.com')
  })
})

// Run test: npm run test
// Expected: New test passes without code changes
```

## Best Practices

1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **One Assertion Per Test**: Test one thing at a time
3. **Descriptive Test Names**: Use "should" pattern
4. **Test User Behavior**: Focus on what users see and do
5. **Mock Dependencies**: Isolate component under test
6. **Avoid Implementation Details**: Test public API only
7. **Use beforeEach**: Setup common test state
8. **Clean Up**: Verify mocks and subscriptions
9. **Test Edge Cases**: Empty states, errors, boundaries
10. **Keep Tests Fast**: Mock slow operations
11. **TDD Cycle**: Red → Green → Refactor
12. **Test Coverage**: Aim for 80%+ coverage
