---
name: playwright-testing
description: Write E2E tests with Playwright including Page Object Model, visual regression testing, and CI/CD integration. Use when testing user flows, integration testing, or visual regression testing.
---

# Playwright Testing Specialist

Specialized in writing end-to-end tests using Playwright for web applications.

## When to Use This Skill

- Writing E2E tests for user flows
- Testing cross-browser compatibility
- Implementing Page Object Model pattern
- Visual regression testing
- Testing authentication flows
- Integration testing
- CI/CD test automation

## Core Principles

- **User-Centric**: Test from user's perspective
- **Reliable**: Tests should be deterministic and stable
- **Maintainable**: Use Page Object Model for reusability
- **Fast**: Parallelize tests and use efficient selectors
- **Isolated**: Each test should be independent
- **Comprehensive**: Cover critical user journeys

## Playwright Setup

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

## Basic E2E Tests

```typescript
import { test, expect } from '@playwright/test'

test('homepage loads successfully', async ({ page }) => {
  await page.goto('/')

  await expect(page).toHaveTitle(/My App/)
  await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible()
})

test('navigation works', async ({ page }) => {
  await page.goto('/')

  // Click navigation link
  await page.getByRole('link', { name: 'About' }).click()

  // Verify URL
  await expect(page).toHaveURL('/about')

  // Verify content
  await expect(page.getByRole('heading', { name: 'About Us' })).toBeVisible()
})

test('form submission', async ({ page }) => {
  await page.goto('/contact')

  // Fill form
  await page.getByLabel('Name').fill('John Doe')
  await page.getByLabel('Email').fill('john@example.com')
  await page.getByLabel('Message').fill('Hello, this is a test message')

  // Submit
  await page.getByRole('button', { name: 'Submit' }).click()

  // Verify success
  await expect(page.getByText('Thank you for your message')).toBeVisible()
})
```

## Page Object Model

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Log in' })
    this.errorMessage = page.getByRole('alert')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }

  async loginWithValidCredentials() {
    await this.login('user@example.com', 'password123')
  }

  async expectErrorMessage(message: string) {
    await expect(this.errorMessage).toContainText(message)
  }
}

// Usage in tests
import { test, expect } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'

test('successful login', async ({ page }) => {
  const loginPage = new LoginPage(page)

  await loginPage.goto()
  await loginPage.loginWithValidCredentials()

  // Verify redirect
  await expect(page).toHaveURL('/dashboard')
})

test('login with invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page)

  await loginPage.goto()
  await loginPage.login('invalid@example.com', 'wrongpassword')

  await loginPage.expectErrorMessage('Invalid credentials')
})
```

## Fixtures for Reusability

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'

type Fixtures = {
  loginPage: LoginPage
  dashboardPage: DashboardPage
  authenticatedPage: Page
}

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page)
    await use(loginPage)
  },

  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page)
    await use(dashboardPage)
  },

  // WHY: Reuse authenticated state across tests
  authenticatedPage: async ({ page }, use) => {
    // Perform login
    const loginPage = new LoginPage(page)
    await loginPage.goto()
    await loginPage.loginWithValidCredentials()

    // Use authenticated page
    await use(page)

    // Cleanup: logout
    await page.getByRole('button', { name: 'Logout' }).click()
  },
})

export { expect } from '@playwright/test'

// Usage
import { test, expect } from './fixtures'

test('dashboard displays user info', async ({ authenticatedPage, dashboardPage }) => {
  await dashboardPage.goto()
  await expect(dashboardPage.userName).toContainText('John Doe')
})
```

## Authentication State

```typescript
// e2e/auth.setup.ts
import { test as setup } from '@playwright/test'

const authFile = 'playwright/.auth/user.json'

setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('Email').fill('user@example.com')
  await page.getByLabel('Password').fill('password123')
  await page.getByRole('button', { name: 'Log in' }).click()

  await page.waitForURL('/dashboard')

  // WHY: Save authenticated state for reuse
  await page.context().storageState({ path: authFile })
})

// playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: authFile,
      },
      dependencies: ['setup'],
    },
  ],
})
```

## API Testing

```typescript
test('API endpoint returns user data', async ({ request }) => {
  const response = await request.get('/api/users/1')

  expect(response.ok()).toBeTruthy()
  expect(response.status()).toBe(200)

  const user = await response.json()
  expect(user).toMatchObject({
    id: '1',
    name: expect.any(String),
    email: expect.stringContaining('@'),
  })
})

test('API POST creates user', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: {
      name: 'John Doe',
      email: 'john@example.com',
    },
  })

  expect(response.status()).toBe(201)

  const user = await response.json()
  expect(user).toHaveProperty('id')
  expect(user.name).toBe('John Doe')
})
```

## Visual Regression Testing

```typescript
test('homepage visual regression', async ({ page }) => {
  await page.goto('/')

  // Compare full page
  await expect(page).toHaveScreenshot('homepage.png')
})

test('button visual regression', async ({ page }) => {
  await page.goto('/components')

  const button = page.getByRole('button', { name: 'Primary' })

  // Compare specific element
  await expect(button).toHaveScreenshot('primary-button.png')
})

// With options
test('responsive visual regression', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 })
  await page.goto('/')

  await expect(page).toHaveScreenshot('homepage-mobile.png', {
    fullPage: true,
    maxDiffPixels: 100, // Allow small differences
  })
})
```

## Waiting Strategies

```typescript
test('wait for element', async ({ page }) => {
  await page.goto('/dashboard')

  // Wait for element to be visible
  await page.getByRole('heading', { name: 'Dashboard' }).waitFor()

  // Wait for specific state
  await page.getByRole('button', { name: 'Submit' }).waitFor({ state: 'visible' })

  // Wait for network idle
  await page.waitForLoadState('networkidle')

  // Wait for specific response
  await page.waitForResponse(response =>
    response.url().includes('/api/users') && response.status() === 200
  )

  // Custom wait condition
  await page.waitForFunction(() => {
    return document.querySelectorAll('.item').length > 5
  })
})
```

## Mocking Network Requests

```typescript
test('mock API response', async ({ page }) => {
  // Mock API call
  await page.route('/api/users', route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: '1', name: 'Mocked User 1' },
        { id: '2', name: 'Mocked User 2' },
      ]),
    })
  })

  await page.goto('/users')

  await expect(page.getByText('Mocked User 1')).toBeVisible()
})

test('mock network failure', async ({ page }) => {
  await page.route('/api/users', route => {
    route.abort('failed')
  })

  await page.goto('/users')

  await expect(page.getByText('Failed to load users')).toBeVisible()
})
```

## Debugging

```typescript
test('debug test', async ({ page }) => {
  await page.goto('/')

  // Pause for debugging
  await page.pause()

  // Step through with playwright inspector
  await page.getByRole('button', { name: 'Submit' }).click()

  // Take screenshot for debugging
  await page.screenshot({ path: 'debug-screenshot.png' })

  // Log page content
  console.log(await page.content())
})
```

## CI/CD Integration

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps
      - name: Run Playwright tests
        run: npx playwright test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Tools to Use

- `Read`: Read existing tests and page objects
- `Write`: Create new tests
- `Edit`: Update tests and page objects
- `Bash`: Run Playwright tests

### Bash Commands

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test e2e/login.spec.ts

# Run tests in UI mode
npx playwright test --ui

# Debug mode
npx playwright test --debug

# Run with specific browser
npx playwright test --project=chromium

# Generate tests (codegen)
npx playwright codegen http://localhost:3000

# Show report
npx playwright show-report

# Update screenshots
npx playwright test --update-snapshots
```

## Workflow

1. **Identify User Flow**: Determine critical path to test
2. **Write Test First**: Follow TDD approach
3. **Create Page Objects**: Extract reusable page interactions
4. **Run Test**: Ensure test passes
5. **Add Visual Regression**: Capture screenshots
6. **Parallelize**: Run tests in parallel for speed
7. **Integrate CI/CD**: Automate test execution
8. **Monitor**: Track test reliability

## Related Skills

- `vitest-react-testing`: For unit tests
- `nextjs-app-development`: For application structure
- `react-component-development`: For component understanding

## Key Reminders

- Use accessible selectors (getByRole, getByLabel) over CSS selectors
- Implement Page Object Model for maintainable tests
- Use fixtures to share setup code
- Save authentication state to speed up tests
- Run tests in parallel for faster feedback
- Mock network requests for reliability
- Use visual regression testing for UI consistency
- Configure retries for flaky tests
- Integrate with CI/CD pipeline
- Debug with `page.pause()` and Playwright Inspector
- Keep tests isolated and independent
- Test critical user journeys, not every feature
- Write comments explaining WHY for complex test logic
