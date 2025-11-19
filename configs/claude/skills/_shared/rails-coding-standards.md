# Rails Coding Standards

## Indentation

- 4 spaces (Ruby/Rails)

## Linter & Formatter

- Rubocop

## Ruby & Rails Commands

- Ruby: `$HOME/.rbenv/shims/ruby`
- Rails: `bundle exec rails`

## Comments

- Language: English or Japanese (match codebase conventions)
- Style: Explain WHY, not WHAT or HOW

### Good Example

```ruby
# WHY: Use transaction to ensure atomicity between balance update and log creation
ActiveRecord::Base.transaction do
    account.update!(balance: new_balance)
    TransactionLog.create!(account: account, amount: amount)
end
```

### Bad Example

```ruby
# Update account balance (obvious from code)
account.update!(balance: new_balance)
```

## File Naming Conventions

- Models: `app/models/user.rb` (singular)
- Controllers: `app/controllers/users_controller.rb` (plural)
- Services: `app/services/order_processing_service.rb` (descriptive)
- Form Objects: `app/forms/user_registration_form.rb`
- Jobs: `app/jobs/report_generation_job.rb`

## Code Organization

- Fat Model, Skinny Controller
- Single Responsibility Principle
- RESTful Design
- Convention over Configuration
