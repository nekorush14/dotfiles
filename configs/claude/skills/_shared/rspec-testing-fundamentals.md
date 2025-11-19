# RSpec Testing Fundamentals

Common RSpec concepts, structure, matchers, and best practices used across all testing skills.

## Core TDD Principles

**Always** write tests BEFORE implementation:

1. Write failing test first (Red)
2. Run test to confirm it fails correctly
3. Commit test when verified
4. Implementation happens separately
5. Run tests to confirm they pass (Green)
6. Refactor if needed

## RSpec Structure

### Basic Structure

```ruby
RSpec.describe ClassName do
    describe '#method_name' do
        context 'when condition is met' do
            it 'does expected behavior' do
                # Arrange
                # Act
                # Assert
            end
        end

        context 'when condition is not met' do
            it 'handles error appropriately' do
                # Test error case
            end
        end
    end
end
```

### Test Organization

- `describe`: Group tests by class or method
- `context`: Group tests by specific conditions
- `it`: Individual test case
- `let`/`let!`: Define test data lazily/eagerly
- `before`/`after`: Setup and teardown

## RSpec Matchers

### Equality

```ruby
expect(actual).to eq(expected)
expect(actual).not_to eq(unexpected)
```

### Truthiness

```ruby
expect(actual).to be_truthy
expect(actual).to be_falsey
expect(actual).to be_nil
```

### Comparisons

```ruby
expect(actual).to be > expected
expect(actual).to be_between(min, max)
```

### Collections

```ruby
expect(array).to include(item)
expect(array).to contain_exactly(item1, item2)
expect(hash).to have_key(:key)
```

### Changes

```ruby
expect { action }.to change(Model, :count).by(1)
expect { action }.to change { object.attribute }.from(old).to(new)
```

### Errors

```ruby
expect { action }.to raise_error(ErrorClass)
expect { action }.not_to raise_error
```

### Jobs

```ruby
expect { action }.to have_enqueued_job(JobClass)
expect { action }.to have_enqueued_job(JobClass).with(arg1, arg2)
```

## Mocking and Stubbing

### Basic Stubbing

```ruby
# Stubbing methods
allow(object).to receive(:method).and_return(value)
allow(object).to receive(:method).and_raise(ErrorClass)

# Expecting method calls
expect(object).to receive(:method).with(arg1, arg2)
expect(object).not_to receive(:method)

# Stubbing class methods
allow(Class).to receive(:method).and_return(value)
```

### Partial Doubles (Spy)

```ruby
user = create(:user)
allow(user).to receive(:send_email)
user.send_email
expect(user).to have_received(:send_email)
```

### Time Manipulation

```ruby
travel_to Time.zone.local(2024, 1, 1) do
    # Test time-dependent code
end
```

## Mocking Best Practices

**IMPORTANT**: Never put logic inside mocks. Mocks should return simple values.

```ruby
# Bad: Logic in mock
allow(service).to receive(:calculate) do |x|
    if x > 100
        x * 0.9
    else
        x * 0.8
    end
end

# Good: Simple return value
allow(service).to receive(:calculate).and_return(90)

# Good: Test different scenarios separately
context 'with valid payment' do
    before do
        allow(PaymentGateway).to receive(:charge).and_return(
            { status: 'success', transaction_id: '123' }
        )
    end

    it 'processes payment successfully' do
        # Test logic here
    end
end

context 'when payment fails' do
    before do
        allow(PaymentGateway).to receive(:charge).and_raise(
            PaymentError, 'Payment failed'
        )
    end

    it 'handles payment error' do
        # Test error handling here
    end
end
```

**WHY**: Logic in mocks makes tests fragile and defeats the purpose of testing the actual implementation.

## Shared Examples

Reuse test logic with shared examples:

```ruby
# spec/support/shared_examples/api_authentication.rb
RSpec.shared_examples 'requires authentication' do
    context 'when not authenticated' do
        it 'returns unauthorized status' do
            make_request

            expect(response).to have_http_status(:unauthorized)
        end
    end
end

# Usage in specs
RSpec.describe 'API::V1::Users', type: :request do
    describe 'GET /api/v1/users' do
        def make_request
            get '/api/v1/users'
        end

        it_behaves_like 'requires authentication'
    end
end
```

## RSpec Configuration

Basic RSpec configuration:

```ruby
# spec/rails_helper.rb
RSpec.configure do |config|
    config.use_transactional_fixtures = true
    config.include FactoryBot::Syntax::Methods

    config.before(:suite) do
        DatabaseCleaner.clean_with(:truncation)
    end

    config.before(:each) do
        DatabaseCleaner.strategy = :transaction
    end

    config.before(:each, :js) do
        DatabaseCleaner.strategy = :truncation
    end
end
```

## Test Quality Principles

- **Descriptive**: Test names clearly describe what is being tested
- **Independent**: Tests don't depend on each other
- **Focused**: Each test validates one specific behavior
- **Fast**: Tests run quickly; use mocks/stubs for external dependencies
- **Maintainable**: Easy to understand and update

## Best Practices

- Write tests before implementation (TDD)
- One assertion per test when possible
- Use descriptive test names
- Test edge cases and error conditions
- Keep tests independent and isolated
- Mock external dependencies
- Avoid testing implementation details
- Test behavior, not methods
- Keep tests fast and focused
- Maintain high test coverage (aim for 90%+)

## Running Tests

```bash
# Run all tests
bundle exec rspec

# Run specific test file
bundle exec rspec spec/path/to/spec.rb

# Run specific test by line number
bundle exec rspec spec/path/to/spec.rb:42

# Run with documentation format
bundle exec rspec --format documentation
```

## Coding Standards

- **Indentation**: 4 spaces (Ruby/RSpec)
- **Comments**: English only, explain WHY not WHAT
- **Test Names**: Use descriptive, behavior-focused names
