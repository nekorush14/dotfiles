# Tailwind CSS Patterns for Angular v21

Sophisticated, minimalist design patterns using Tailwind CSS utility classes in Angular components.

## Table of Contents

- [Layout Patterns](#layout-patterns)
- [Component Patterns](#component-patterns)
- [Form Patterns](#form-patterns)
- [Responsive Patterns](#responsive-patterns)
- [Animation Patterns](#animation-patterns)
- [Dark Mode Patterns](#dark-mode-patterns)

## Layout Patterns

### Container with Max Width

```typescript
@Component({
  template: `
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <!-- Content -->
    </div>
  `,
})
```

### Flexbox Centering

```typescript
@Component({
  template: `
    <div class="flex h-screen items-center justify-center">
      <div class="text-center">
        <h1 class="text-4xl font-bold">Centered Content</h1>
      </div>
    </div>
  `,
})
```

### Grid Layout

```typescript
@Component({
  template: `
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      @for (item of items(); track item.id) {
        <div class="rounded-lg border p-6">
          {{ item.title }}
        </div>
      }
    </div>
  `,
})
```

### Sidebar Layout

```typescript
@Component({
  template: `
    <div class="flex h-screen">
      <!-- Sidebar -->
      <aside class="w-64 border-r bg-gray-50">
        <nav class="space-y-1 p-4">
          <!-- Nav items -->
        </nav>
      </aside>

      <!-- Main content -->
      <main class="flex-1 overflow-auto p-8">
        <!-- Content -->
      </main>
    </div>
  `,
})
```

## Component Patterns

### Card Component

```typescript
@Component({
  selector: 'app-card',
  template: `
    <div class="overflow-hidden rounded-lg bg-white shadow-md transition-shadow hover:shadow-lg">
      @if (imageUrl()) {
        <img
          [ngSrc]="imageUrl()"
          [alt]="title()"
          width="400"
          height="200"
          class="h-48 w-full object-cover"
        />
      }

      <div class="p-6">
        <h3 class="text-xl font-semibold text-gray-900">{{ title() }}</h3>
        <p class="mt-2 text-sm text-gray-600">{{ description() }}</p>

        @if (showActions()) {
          <div class="mt-4 flex gap-2">
            <button class="rounded bg-blue-500 px-4 py-2 text-sm text-white transition-colors hover:bg-blue-600">
              View Details
            </button>
          </div>
        }
      </div>
    </div>
  `,
})
export class CardComponent {
  title = input.required<string>()
  description = input.required<string>()
  imageUrl = input<string>()
  showActions = input(true)
}
```

### Button Variants

```typescript
@Component({
  selector: 'app-button',
  template: `
    <button
      [type]="type()"
      [disabled]="disabled()"
      [class]="buttonClasses()"
      (click)="onClick.emit()"
    >
      @if (isLoading()) {
        <span class="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
      }
      <ng-content />
    </button>
  `,
})
export class ButtonComponent {
  variant = input<'primary' | 'secondary' | 'danger' | 'ghost'>('primary')
  size = input<'sm' | 'md' | 'lg'>('md')
  disabled = input(false)
  isLoading = input(false)
  type = input<'button' | 'submit' | 'reset'>('button')
  onClick = output<void>()

  buttonClasses = computed(() => {
    const base = 'inline-flex items-center justify-center rounded font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'

    const variants = {
      primary: 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-500',
      secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
      danger: 'bg-red-500 text-white hover:bg-red-600 focus:ring-red-500',
      ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
    }

    const sizes = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
    }

    return `${base} ${variants[this.variant()]} ${sizes[this.size()]}`
  })
}
```

### Badge Component

```typescript
@Component({
  selector: 'app-badge',
  template: `
    <span [class]="badgeClasses()">
      <ng-content />
    </span>
  `,
})
export class BadgeComponent {
  variant = input<'default' | 'success' | 'warning' | 'danger'>('default')

  badgeClasses = computed(() => {
    const base = 'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium'

    const variants = {
      default: 'bg-gray-100 text-gray-800',
      success: 'bg-green-100 text-green-800',
      warning: 'bg-yellow-100 text-yellow-800',
      danger: 'bg-red-100 text-red-800',
    }

    return `${base} ${variants[this.variant()]}`
  })
}
```

### Alert Component

```typescript
@Component({
  selector: 'app-alert',
  template: `
    <div [class]="alertClasses()" role="alert">
      <div class="flex">
        <div class="flex-shrink-0">
          @switch (variant()) {
            @case ('success') {
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            }
            @case ('warning') {
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            }
            @case ('danger') {
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            }
            @default {
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
            }
          }
        </div>
        <div class="ml-3">
          @if (title()) {
            <h3 class="text-sm font-medium">{{ title() }}</h3>
          }
          <div class="text-sm">
            <ng-content />
          </div>
        </div>
      </div>
    </div>
  `,
})
export class AlertComponent {
  variant = input<'info' | 'success' | 'warning' | 'danger'>('info')
  title = input<string>()

  alertClasses = computed(() => {
    const base = 'rounded-lg p-4'

    const variants = {
      info: 'bg-blue-50 text-blue-800',
      success: 'bg-green-50 text-green-800',
      warning: 'bg-yellow-50 text-yellow-800',
      danger: 'bg-red-50 text-red-800',
    }

    return `${base} ${variants[this.variant()]}`
  })
}
```

## Form Patterns

### Input with Label and Error

```typescript
@Component({
  selector: 'app-input',
  template: `
    <div class="space-y-1">
      @if (label()) {
        <label [for]="id()" class="block text-sm font-medium text-gray-700">
          {{ label() }}
          @if (required()) {
            <span class="text-red-500">*</span>
          }
        </label>
      }

      <input
        [id]="id()"
        [type]="type()"
        [placeholder]="placeholder()"
        [disabled]="disabled()"
        [class]="inputClasses()"
        (input)="onInput($event)"
        (blur)="onBlur($event)"
      />

      @if (error()) {
        <p class="text-sm text-red-600">{{ error() }}</p>
      }

      @if (hint() && !error()) {
        <p class="text-sm text-gray-500">{{ hint() }}</p>
      }
    </div>
  `,
})
export class InputComponent {
  id = input.required<string>()
  label = input<string>()
  type = input<'text' | 'email' | 'password' | 'number'>('text')
  placeholder = input<string>()
  disabled = input(false)
  required = input(false)
  error = input<string>()
  hint = input<string>()

  inputClasses = computed(() => {
    const base = 'block w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:cursor-not-allowed disabled:bg-gray-50 disabled:text-gray-500'
    const error = this.error() ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'

    return `${base} ${error}`
  })

  onInput = output<Event>()
  onBlur = output<Event>()
}
```

### Select Dropdown

```typescript
@Component({
  selector: 'app-select',
  template: `
    <div class="space-y-1">
      @if (label()) {
        <label [for]="id()" class="block text-sm font-medium text-gray-700">
          {{ label() }}
        </label>
      }

      <select
        [id]="id()"
        [disabled]="disabled()"
        class="block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:cursor-not-allowed disabled:bg-gray-50"
        (change)="onChange.emit($event)"
      >
        @if (placeholder()) {
          <option value="" disabled selected>{{ placeholder() }}</option>
        }
        <ng-content />
      </select>

      @if (error()) {
        <p class="text-sm text-red-600">{{ error() }}</p>
      }
    </div>
  `,
})
export class SelectComponent {
  id = input.required<string>()
  label = input<string>()
  placeholder = input<string>()
  disabled = input(false)
  error = input<string>()
  onChange = output<Event>()
}
```

## Responsive Patterns

### Mobile-First Responsive Grid

```typescript
@Component({
  template: `
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      @for (item of items(); track item.id) {
        <app-card [item]="item" />
      }
    </div>
  `,
})
```

### Responsive Padding and Spacing

```typescript
@Component({
  template: `
    <div class="px-4 py-6 sm:px-6 sm:py-8 lg:px-8 lg:py-12">
      <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold">
        Responsive Title
      </h1>
    </div>
  `,
})
```

### Responsive Visibility

```typescript
@Component({
  template: `
    <!-- Mobile menu button (visible on small screens) -->
    <button class="md:hidden">
      Menu
    </button>

    <!-- Desktop navigation (visible on medium+ screens) -->
    <nav class="hidden md:flex md:gap-4">
      <a href="#">Link 1</a>
      <a href="#">Link 2</a>
    </nav>
  `,
})
```

## Animation Patterns

### Fade In Animation

```typescript
@Component({
  template: `
    <div class="animate-fade-in opacity-0">
      Content
    </div>
  `,
  styles: [`
    @keyframes fade-in {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }

    .animate-fade-in {
      animation: fade-in 0.5s ease-in forwards;
    }
  `],
})
```

### Slide In Animation

```typescript
@Component({
  template: `
    <div class="translate-x-[-100%] animate-slide-in">
      Content
    </div>
  `,
  styles: [`
    @keyframes slide-in {
      from {
        transform: translateX(-100%);
      }
      to {
        transform: translateX(0);
      }
    }

    .animate-slide-in {
      animation: slide-in 0.3s ease-out forwards;
    }
  `],
})
```

### Loading Spinner

```typescript
@Component({
  template: `
    <div class="flex items-center justify-center">
      <div class="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-500"></div>
    </div>
  `,
})
```

## Dark Mode Patterns

### Dark Mode Toggle

```typescript
@Component({
  selector: 'app-theme-toggle',
  template: `
    <button
      (click)="toggleTheme()"
      class="rounded-lg p-2 hover:bg-gray-100 dark:hover:bg-gray-800"
    >
      @if (isDark()) {
        <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
          <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
        </svg>
      } @else {
        <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
        </svg>
      }
    </button>
  `,
})
export class ThemeToggleComponent {
  isDark = signal(false)

  constructor() {
    // WHY: Initialize from localStorage or system preference
    if (typeof window !== 'undefined') {
      this.isDark.set(
        localStorage.getItem('theme') === 'dark' ||
        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)
      )
    }
  }

  toggleTheme(): void {
    this.isDark.update(current => !current)
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', this.isDark() ? 'dark' : 'light')
      document.documentElement.classList.toggle('dark', this.isDark())
    }
  }
}
```

### Dark Mode Styles

```typescript
@Component({
  template: `
    <div class="bg-white text-gray-900 dark:bg-gray-900 dark:text-white">
      <h1 class="text-gray-900 dark:text-white">Title</h1>
      <p class="text-gray-600 dark:text-gray-400">Description</p>

      <div class="border border-gray-200 dark:border-gray-700">
        Content
      </div>

      <button class="bg-blue-500 text-white hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700">
        Action
      </button>
    </div>
  `,
})
```

## Best Practices

1. **Use Computed Classes**: Use `computed()` for dynamic class combinations
2. **Mobile-First**: Always start with mobile styles, then add responsive breakpoints
3. **Consistent Spacing**: Use Tailwind's spacing scale (4px increments)
4. **Semantic Colors**: Use semantic color names (success, warning, danger)
5. **Focus States**: Always include focus states for accessibility
6. **Disabled States**: Style disabled states appropriately
7. **Hover States**: Add hover states for interactive elements
8. **Transitions**: Use `transition-*` utilities for smooth state changes
9. **Dark Mode**: Consider dark mode from the start
10. **Reusable Components**: Extract common patterns into reusable components
