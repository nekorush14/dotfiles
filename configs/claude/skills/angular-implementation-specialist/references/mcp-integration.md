# Angular CLI MCP Server Integration Guide

Guide for leveraging Angular CLI MCP server tools to get version-specific best practices, search documentation, and find modern code examples.

## Table of Contents

- [Available MCP Tools](#available-mcp-tools)
- [Workflow Integration](#workflow-integration)
- [Usage Patterns](#usage-patterns)
- [Example Scenarios](#example-scenarios)
- [Best Practices](#best-practices)

## Available MCP Tools

### mcp__angular-cli__list_projects

Lists all Angular projects in the workspace.

**Purpose**: Get workspace path required for other MCP tools.

**Parameters**: None

**Returns**:
```json
{
  "projects": [
    {
      "name": "my-angular-app",
      "workspacePath": "/Users/username/project",
      "angularVersion": "21.0.0"
    }
  ]
}
```

**Usage**:
```typescript
// ALWAYS call this FIRST before other MCP tools
const projectsResult = await mcp__angular-cli__list_projects()
const workspacePath = projectsResult.projects[0].workspacePath
```

### mcp__angular-cli__get_best_practices

Get Angular version-specific best practices and recommendations.

**Purpose**: Get guidelines tailored to the specific Angular version in use.

**Parameters**:
- `workspacePath` (required): Path to Angular workspace (from list_projects)
- `topic` (optional): Specific topic to focus on

**Returns**: Markdown-formatted best practices document

**Usage**:
```typescript
// Get general best practices
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath: '/Users/username/project'
})

// Get topic-specific practices
const componentPractices = await mcp__angular-cli__get_best_practices({
  workspacePath: '/Users/username/project',
  topic: 'components'
})
```

**Available Topics**:
- `components`: Component design patterns
- `services`: Service implementation patterns
- `routing`: Routing best practices
- `forms`: Form handling patterns
- `testing`: Testing strategies
- `performance`: Performance optimization
- `state-management`: State management patterns

### mcp__angular-cli__search_documentation

Search Angular official documentation with version alignment.

**Purpose**: Find relevant documentation sections for specific topics.

**Parameters**:
- `query` (required): Search query string
- `version` (optional): Angular version to target

**Returns**: Array of documentation search results with URLs and snippets

**Usage**:
```typescript
// Search for signals documentation
const docsResults = await mcp__angular-cli__search_documentation({
  query: 'signals input output'
})

// Search version-specific docs
const v21Docs = await mcp__angular-cli__search_documentation({
  query: 'control flow syntax',
  version: '21'
})
```

### mcp__angular-cli__find_examples

Find modern Angular code examples from the Angular repository.

**Purpose**: Get real-world code examples following current best practices.

**Parameters**:
- `pattern` (required): Code pattern or feature to search for
- `fileType` (optional): File type filter (ts, html, css, etc.)

**Returns**: Array of code examples with file paths and content

**Usage**:
```typescript
// Find component examples
const componentExamples = await mcp__angular-cli__find_examples({
  pattern: 'standalone component with signals'
})

// Find specific file types
const templateExamples = await mcp__angular-cli__find_examples({
  pattern: 'control flow @if @for',
  fileType: 'html'
})
```

### mcp__angular-cli__onpush_zoneless_migration

Analyze code for OnPush change detection and zoneless migration opportunities.

**Purpose**: Identify optimization opportunities in existing code.

**Parameters**:
- `filePath` (required): Path to Angular component/service file
- `workspacePath` (required): Path to Angular workspace

**Returns**: Migration analysis report with recommendations

**Usage**:
```typescript
const analysis = await mcp__angular-cli__onpush_zoneless_migration({
  filePath: 'src/app/components/user-card/user-card.component.ts',
  workspacePath: '/Users/username/project'
})
```

## Workflow Integration

### Standard Development Workflow

```
1. list_projects
   ↓
2. get_best_practices (with workspacePath)
   ↓
3. find_examples (for reference)
   ↓
4. Write tests (TDD)
   ↓
5. Implement code
   ↓
6. onpush_zoneless_migration (optimization check)
   ↓
7. Run tests
```

### Documentation Lookup Workflow

```
1. User asks about feature
   ↓
2. search_documentation (query feature)
   ↓
3. find_examples (pattern match)
   ↓
4. Provide answer with references
```

### Optimization Workflow

```
1. list_projects
   ↓
2. onpush_zoneless_migration (analyze component)
   ↓
3. get_best_practices (topic: 'performance')
   ↓
4. Apply recommendations
   ↓
5. Run tests
```

## Usage Patterns

### Pattern 1: Starting New Component

```typescript
// Step 1: Get workspace info
const projects = await mcp__angular-cli__list_projects()
const workspacePath = projects.projects[0].workspacePath

// Step 2: Get best practices for components
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath,
  topic: 'components'
})

// Step 3: Find examples
const examples = await mcp__angular-cli__find_examples({
  pattern: 'standalone component signals OnPush'
})

// Step 4: Write tests following TDD
// ... create test file ...

// Step 5: Implement component following practices and examples
// ... create component file ...
```

### Pattern 2: Implementing New Feature

```typescript
// Step 1: Get workspace info
const projects = await mcp__angular-cli__list_projects()
const workspacePath = projects.projects[0].workspacePath

// Step 2: Search documentation for feature
const docs = await mcp__angular-cli__search_documentation({
  query: 'reactive forms validators'
})

// Step 3: Get best practices
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath,
  topic: 'forms'
})

// Step 4: Find code examples
const examples = await mcp__angular-cli__find_examples({
  pattern: 'reactive form custom validator'
})

// Step 5: Implement feature
// ... write tests and code ...
```

### Pattern 3: Optimizing Existing Code

```typescript
// Step 1: Get workspace info
const projects = await mcp__angular-cli__list_projects()
const workspacePath = projects.projects[0].workspacePath

// Step 2: Analyze component
const analysis = await mcp__angular-cli__onpush_zoneless_migration({
  filePath: 'src/app/components/slow-component/slow-component.component.ts',
  workspacePath
})

// Step 3: Get performance best practices
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath,
  topic: 'performance'
})

// Step 4: Apply recommendations from analysis and practices
// ... refactor code ...

// Step 5: Verify with tests
// ... run tests ...
```

## Example Scenarios

### Scenario 1: User Asks "How do I use signals in Angular?"

```typescript
// Step 1: Search documentation
const docs = await mcp__angular-cli__search_documentation({
  query: 'signals input output computed'
})

// Step 2: Get best practices
const projects = await mcp__angular-cli__list_projects()
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath: projects.projects[0].workspacePath,
  topic: 'components'
})

// Step 3: Find examples
const examples = await mcp__angular-cli__find_examples({
  pattern: 'signal input output computed'
})

// Step 4: Provide comprehensive answer with:
// - Explanation from docs
// - Best practices from practices
// - Code examples from examples
// - Custom code example following patterns
```

### Scenario 2: User Asks "Create a form component"

```typescript
// Step 1: Get workspace info
const projects = await mcp__angular-cli__list_projects()
const workspacePath = projects.projects[0].workspacePath

// Step 2: Get form best practices
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath,
  topic: 'forms'
})

// Step 3: Find form examples
const examples = await mcp__angular-cli__find_examples({
  pattern: 'reactive form validators FormBuilder'
})

// Step 4: Write test first (TDD)
// ... create test file ...

// Step 5: Implement form component
// - Follow practices
// - Reference examples
// - Use signals for state
// - Apply OnPush strategy
// - Style with Tailwind
```

### Scenario 3: User Asks "Optimize this component"

```typescript
// Step 1: Get workspace info
const projects = await mcp__angular-cli__list_projects()
const workspacePath = projects.projects[0].workspacePath

// Step 2: Analyze component
const analysis = await mcp__angular-cli__onpush_zoneless_migration({
  filePath: 'src/app/components/target/target.component.ts',
  workspacePath
})

// Step 3: Get performance practices
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath,
  topic: 'performance'
})

// Step 4: Apply optimizations:
// - Add OnPush if not present
// - Convert to signals
// - Use computed() for derived state
// - Apply recommendations from analysis
// - Optimize template with new control flow

// Step 5: Run tests to ensure no regressions
```

### Scenario 4: User Asks About Control Flow Syntax

```typescript
// Step 1: Search documentation
const docs = await mcp__angular-cli__search_documentation({
  query: '@if @for @switch control flow'
})

// Step 2: Find examples
const examples = await mcp__angular-cli__find_examples({
  pattern: '@if @for @switch',
  fileType: 'html'
})

// Step 3: Get component practices
const projects = await mcp__angular-cli__list_projects()
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath: projects.projects[0].workspacePath,
  topic: 'components'
})

// Step 4: Provide answer with:
// - Syntax explanation from docs
// - Real examples from examples
// - Migration tips from practices
// - Custom examples showing all three directives
```

## Best Practices

### 1. Always Call list_projects First

```typescript
// ✅ CORRECT
const projects = await mcp__angular-cli__list_projects()
const workspacePath = projects.projects[0].workspacePath

const practices = await mcp__angular-cli__get_best_practices({
  workspacePath
})

// ❌ WRONG - Missing workspacePath
const practices = await mcp__angular-cli__get_best_practices({
  topic: 'components'
})
```

### 2. Use Specific Topics for get_best_practices

```typescript
// ✅ CORRECT - Specific topic
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath: '/path/to/project',
  topic: 'components'
})

// ⚠️ LESS OPTIMAL - Generic (may be too broad)
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath: '/path/to/project'
})
```

### 3. Use Descriptive Search Queries

```typescript
// ✅ CORRECT - Specific and descriptive
const docs = await mcp__angular-cli__search_documentation({
  query: 'reactive forms custom validators FormBuilder'
})

// ❌ WRONG - Too vague
const docs = await mcp__angular-cli__search_documentation({
  query: 'forms'
})
```

### 4. Combine Multiple MCP Tools

```typescript
// ✅ CORRECT - Comprehensive approach
const projects = await mcp__angular-cli__list_projects()
const workspacePath = projects.projects[0].workspacePath

const [docs, practices, examples] = await Promise.all([
  mcp__angular-cli__search_documentation({ query: 'signals' }),
  mcp__angular-cli__get_best_practices({ workspacePath, topic: 'components' }),
  mcp__angular-cli__find_examples({ pattern: 'signal input output' })
])

// ❌ WRONG - Missing context
const examples = await mcp__angular-cli__find_examples({
  pattern: 'component'
})
// Now implement without checking docs or practices
```

### 5. Use onpush_zoneless_migration for Optimization

```typescript
// ✅ CORRECT - Analyze before optimizing
const analysis = await mcp__angular-cli__onpush_zoneless_migration({
  filePath: 'src/app/components/user-list/user-list.component.ts',
  workspacePath: '/path/to/project'
})

// Apply specific recommendations from analysis
// - Add OnPush if suggested
// - Convert to signals if suggested
// - etc.

// ❌ WRONG - Blind optimization without analysis
// Just add OnPush and hope it works
```

### 6. Handle Multiple Projects

```typescript
// ✅ CORRECT - Handle multiple projects
const projects = await mcp__angular-cli__list_projects()

if (projects.projects.length > 1) {
  // Ask user which project or use the first one
  const targetProject = projects.projects.find(p => p.name === 'my-app')
  const workspacePath = targetProject.workspacePath
} else {
  const workspacePath = projects.projects[0].workspacePath
}

// ❌ WRONG - Assume single project
const projects = await mcp__angular-cli__list_projects()
const workspacePath = projects.projects[0].workspacePath
// Crashes if projects array is empty
```

### 7. Cache Workspace Path

```typescript
// ✅ CORRECT - Cache workspace path for session
let cachedWorkspacePath: string | null = null

async function getWorkspacePath(): Promise<string> {
  if (!cachedWorkspacePath) {
    const projects = await mcp__angular-cli__list_projects()
    cachedWorkspacePath = projects.projects[0].workspacePath
  }
  return cachedWorkspacePath
}

// Use it
const workspacePath = await getWorkspacePath()

// ❌ WRONG - Call list_projects every time
// Wastes time and API calls
const projects1 = await mcp__angular-cli__list_projects()
const practices = await mcp__angular-cli__get_best_practices({
  workspacePath: projects1.projects[0].workspacePath
})

const projects2 = await mcp__angular-cli__list_projects() // Unnecessary
const docs = await mcp__angular-cli__search_documentation({...})
```

## Error Handling

```typescript
try {
  const projects = await mcp__angular-cli__list_projects()

  if (!projects.projects || projects.projects.length === 0) {
    throw new Error('No Angular projects found in workspace')
  }

  const workspacePath = projects.projects[0].workspacePath

  const practices = await mcp__angular-cli__get_best_practices({
    workspacePath,
    topic: 'components'
  })

  // Use practices...
} catch (error) {
  console.error('Failed to get Angular best practices:', error)
  // Fall back to built-in knowledge
}
```

## Integration with TDD Workflow

```typescript
// Complete TDD workflow with MCP integration
async function createComponentWithTDD(componentName: string) {
  // Step 1: Get workspace and best practices
  const projects = await mcp__angular-cli__list_projects()
  const workspacePath = projects.projects[0].workspacePath

  const practices = await mcp__angular-cli__get_best_practices({
    workspacePath,
    topic: 'components'
  })

  const examples = await mcp__angular-cli__find_examples({
    pattern: 'standalone component signals OnPush'
  })

  // Step 2: Write test first (RED)
  const testContent = generateTestFromPractices(componentName, practices)
  await writeFile(`${componentName}.spec.ts`, testContent)

  // Step 3: Run test (should fail)
  await runCommand('npm run test')

  // Step 4: Implement component (GREEN)
  const componentContent = generateComponentFromExamples(componentName, examples, practices)
  await writeFile(`${componentName}.component.ts`, componentContent)

  // Step 5: Run test (should pass)
  await runCommand('npm run test')

  // Step 6: Optimize (REFACTOR)
  const analysis = await mcp__angular-cli__onpush_zoneless_migration({
    filePath: `${componentName}.component.ts`,
    workspacePath
  })

  // Apply optimizations based on analysis
  // Re-run tests to ensure no regressions
}
```

## Key Reminders

1. **Always call list_projects first** to get workspacePath
2. **Use specific topics** in get_best_practices for targeted guidance
3. **Combine multiple MCP tools** for comprehensive context
4. **Cache workspace path** to avoid repeated API calls
5. **Use search_documentation** when user asks about specific features
6. **Use find_examples** to see real-world code patterns
7. **Use onpush_zoneless_migration** before and after optimization
8. **Handle errors gracefully** and fall back to built-in knowledge
9. **Integrate MCP tools with TDD workflow** for best results
10. **Provide source references** when using MCP tool results
