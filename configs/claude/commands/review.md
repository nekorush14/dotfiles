---
description: Review code for performance, efficiency, and best practices
argument-hint: [file or directory path]
---
# Code Review

Perform a comprehensive code review focusing on performance, efficiency, and best practices.

## Review Target

Review the code specified by $ARGUMENTS.
If no argument is provided, review staged changes (`git diff --cached`) or recent changes.

## Flow

### 1. Gather Context

First, identify:
- Programming language(s) and frameworks used
- Purpose and responsibilities of the code

### 2. Analysis Aspects

Analyze the code from the following perspectives:

#### Database Query Issues

- N+1 query problems
- Missing indexes (based on query patterns)
- Inefficient JOINs or subqueries
- Unnecessary data fetching (SELECT *)
- Missing query optimization (pagination, lazy loading)
- Connection pooling issues
- Transaction scope problems

#### Algorithm Efficiency

- Time complexity analysis (identify O(n^2) or worse)
- Space complexity concerns
- Unnecessary iterations or nested loops
- Opportunities for early termination
- Data structure selection (array vs set vs map)
- Sorting and searching efficiency

#### Memory Management

- Memory leaks (unclosed resources, event listeners)
- Large object allocations
- Circular references
- Buffer/stream handling
- Garbage collection pressure
- Object pooling opportunities

#### Caching Opportunities

- Repeated expensive computations
- Frequently accessed data without caching
- Missing memoization
- HTTP caching headers
- Database query result caching
- CDN utilization for static assets

#### Language Best Practices

Evaluate based on the detected language:

- **JavaScript/TypeScript**: async/await patterns, null safety, type usage
- **Python**: PEP 8 compliance, pythonic idioms, type hints
- **Go**: Error handling, goroutine leaks, defer usage
- **Rust**: Ownership patterns, lifetime issues, unsafe usage
- **Ruby**: Rails conventions, Ruby idioms
- **Java/Kotlin**: Null safety, Stream API usage, concurrency
- **General**: SOLID principles, DRY, error handling, logging

### 3. Generate Report

Output the analysis results in the following format.

## Output Format

YOU MUST WRITE THE REVIEW REPORT IN JAPANESE.

```markdown
# Code Review Report

## Summary

<Overview of findings with severity indicators>

## Findings

### Critical

<Issues that must be fixed>

### Warning

<Issues that should be addressed>

### Suggestion

<Improvements that would enhance code quality>

## Recommended Actions

<Prioritized list of recommended actions>
```

## Severity Levels

- **Critical**: Performance degradation, memory leaks, security risks
- **Warning**: Suboptimal patterns, potential issues under load
- **Suggestion**: Best practice improvements, code clarity enhancements

## Constraints

- DO NOT modify any code directly
- DO NOT create or delete files
- Only provide review feedback and recommendations
- YOU MUST OUTPUT THE REVIEW RESULT IN JAPANESE
