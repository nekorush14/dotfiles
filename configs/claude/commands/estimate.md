---
name: estimate
description: Estimate software development tasks, features, or project with intelligent analysis
---

# Estimate

## Triggers

- Development planning requiring time, effort, or complexity estimates
- Project scoping and resource allocation decisions
- Feature breakdown needing systematic estimation methodology
- Risk assessment and confidence interval analysis requirements

## Usage

```
/estimate [target] [--type time|effort|complexity] [--unit hours|days|weeks] [--breakdown]
```

## Behavioral Flow

1. **Analyze**: Examine scope, complexity factors, dependencies, and framework patterns
2. **Calculate**: Apply estimation methodology with historical benchmarks and complexity scoring
3. **Validate**: Cross-reference estimates with project patterns and domain expertise
4. **Present**: Provide detailed breakdown with confidence intervals and risk assessment
5. **Track**: Document estimation accuracy for continuous methodology improvement

### Key behaviors

- Multi-persona coordination (architect, performance, project-manager) based on estimation scope
- Intelligent breakdown analysis with confidence intervals and risk factors

## Tool Coordination

- **Read/Grep/Glob**: Codebase analysis for complexity assessment and scope evaluation
- **TodoWrite**: Estimation breakdown and progress tracking for complex estimation workflows
- **Task**: Advanced delegation for multi-domain estimation requiring systematic coordination
- **Bash**: Project analysis and dependency evaluation for accurate complexity scoring

## Key Patterns

- **Scope Analysis**: Project requirements → complexity factors → framework patterns → risk assessment
- **Estimation Methodology**: Time-based → Effort-based → Complexity-based → Cost-based approaches
- **Multi-Domain Assessment**: Architecture complexity → Performance requirements → Project timeline
- **Validation Framework**: Historical benchmarks → cross-validation → confidence intervals → accuracy tracking

## Boundaries

### **Will**

- Provide systematic development estimates with confidence intervals and risk assessment
- Apply multi-persona coordination for comprehensive complexity analysis
- Generate detailed breakdown analysis with historical benchmark comparisons
- The result of your task must written by Japanese

### **Will Not**

- Guarantee estimate accuracy without proper scope analysis and validation
- Provide estimates without appropriate domain expertise and complexity assessment
- Override historical benchmarks without clear justification and analysis
