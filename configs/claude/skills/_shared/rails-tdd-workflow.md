# Rails Test-Driven Development (TDD) Workflow

## TDD Workflow Steps

1. **Write Tests First**: Use appropriate RSpec testing skill (`rspec-model-testing`, `rspec-request-testing`, `rspec-service-testing`, or `rspec-job-testing`)
2. **Confirm Tests Fail**: Run tests and verify they fail correctly
3. **Implement Code**: Write implementation to pass tests
4. **Do NOT Modify Tests**: Keep tests unchanged during implementation
5. **Iterate**: Repeat until all tests pass
6. **Refactor**: Improve code quality while keeping tests green
7. **Run Rubocop**: Validate code style
8. **Commit**: Create atomic commits with clear messages

## Test Running Commands

```bash
# Run all tests
bundle exec rspec

# Run specific test file
bundle exec rspec spec/services/order_processing_service_spec.rb

# Run specific test by line number
bundle exec rspec spec/services/order_processing_service_spec.rb:15

# Run with documentation format
bundle exec rspec --format documentation
```

## Commit Guidelines

- One commit per feature/fix
- Clear commit messages
- Ensure tests pass before committing
- Do NOT revert past commits using git command
- If you need to revert changes, create new REVERTING COMMIT

## Related Skills

- `rspec-model-testing`: For writing model specs
- `rspec-request-testing`: For writing API/request specs
- `rspec-service-testing`: For writing service object specs
- `rspec-job-testing`: For writing background job specs
