# FactoryBot Guide

Guide for defining and using FactoryBot factories for test data.

## Basic Factory Definition

```ruby
# spec/factories/users.rb
FactoryBot.define do
    factory :user do
        sequence(:email) { |n| "user#{n}@example.com" }
        password { 'password123' }
        name { 'Test User' }
        active { true }
    end
end
```

## Using Factories

```ruby
# Build (not saved to database)
user = build(:user)

# Create (saved to database)
user = create(:user)

# Build stubbed (fake record, not saved)
user = build_stubbed(:user)

# Attributes hash
attrs = attributes_for(:user)

# Override attributes
user = create(:user, name: 'Custom Name', email: 'custom@example.com')
```

## Traits

Define variations of factories:

```ruby
FactoryBot.define do
    factory :user do
        sequence(:email) { |n| "user#{n}@example.com" }
        password { 'password123' }
        name { 'Test User' }
        active { true }

        trait :inactive do
            active { false }
        end

        trait :admin do
            role { 'admin' }
        end

        trait :with_profile do
            after(:create) do |user|
                create(:profile, user: user)
            end
        end
    end
end

# Usage
inactive_user = create(:user, :inactive)
admin = create(:user, :admin)
user_with_profile = create(:user, :with_profile)

# Multiple traits
inactive_admin = create(:user, :inactive, :admin)
```

## Associations

```ruby
FactoryBot.define do
    factory :post do
        title { 'Test Post' }
        content { 'Test content' }
        association :user  # Creates associated user
    end

    factory :comment do
        content { 'Test comment' }
        association :post
        association :user
    end
end

# Usage
post = create(:post)  # Also creates a user
comment = create(:comment)  # Creates post and user

# Custom association
post = create(:post, user: existing_user)
```

## Nested Factories

```ruby
FactoryBot.define do
    factory :user do
        name { 'User' }

        factory :admin do
            role { 'admin' }
        end

        factory :guest do
            role { 'guest' }
        end
    end
end

# Usage
admin = create(:admin)
guest = create(:guest)
```

## After Callbacks

```ruby
FactoryBot.define do
    factory :user do
        sequence(:email) { |n| "user#{n}@example.com" }

        trait :with_posts do
            after(:create) do |user|
                create_list(:post, 3, user: user)
            end
        end

        trait :with_profile_and_settings do
            after(:create) do |user|
                create(:profile, user: user)
                create(:settings, user: user)
            end
        end
    end
end
```

## Creating Multiple Records

```ruby
# Create list
users = create_list(:user, 3)

# Create list with traits
admins = create_list(:user, 2, :admin)

# Create list with overrides
users = create_list(:user, 3, active: true)
```

## Sequences

```ruby
FactoryBot.define do
    sequence :email do |n|
        "user#{n}@example.com"
    end

    sequence :username do |n|
        "user_#{n}"
    end

    factory :user do
        email
        username
    end
end
```

## Transient Attributes

```ruby
FactoryBot.define do
    factory :user do
        name { 'Test User' }

        transient do
            posts_count { 0 }
        end

        after(:create) do |user, evaluator|
            create_list(:post, evaluator.posts_count, user: user) if evaluator.posts_count > 0
        end
    end
end

# Usage
user_with_posts = create(:user, posts_count: 5)
```

## Dynamic Attributes

```ruby
FactoryBot.define do
    factory :order do
        status { 'pending' }
        total_amount { rand(100..1000) }
        created_at { rand(30.days.ago..Time.current) }

        trait :old do
            created_at { rand(1.year.ago..6.months.ago) }
        end
    end
end
```

## Best Practices

- Use sequences for unique fields (email, username)
- Keep factories simple and minimal
- Use traits for variations
- Use `build` when you don't need database persistence
- Use `build_stubbed` for unit tests (fastest)
- Use `create` only when you need database persistence
- Define associations but allow overrides
- Use after callbacks for complex setups
- Keep factory definitions DRY
- Name factories clearly

## Common Patterns

### Order with Items

```ruby
FactoryBot.define do
    factory :order do
        association :user
        status { 'pending' }
        total_amount { 1000 }

        trait :with_items do
            after(:create) do |order|
                create_list(:order_item, 2, order: order)
            end
        end

        trait :empty do
            after(:create) do |order|
                order.order_items.destroy_all
            end
        end
    end

    factory :order_item do
        association :order
        association :product
        quantity { 1 }
        price { 100 }
    end
end

# Usage
order = create(:order, :with_items)
empty_order = create(:order, :empty)
```

### Polymorphic Associations

```ruby
FactoryBot.define do
    factory :comment do
        content { 'Test comment' }
        association :user

        trait :on_post do
            association :commentable, factory: :post
        end

        trait :on_article do
            association :commentable, factory: :article
        end
    end
end

# Usage
comment_on_post = create(:comment, :on_post)
comment_on_article = create(:comment, :on_article)
```

## Usage in Specs

```ruby
RSpec.describe User, type: :model do
    describe 'validations' do
        it 'is valid with valid attributes' do
            user = build(:user)
            expect(user).to be_valid
        end

        it 'is invalid without email' do
            user = build(:user, email: nil)
            expect(user).not_to be_valid
        end
    end

    describe 'associations' do
        it 'can have multiple posts' do
            user = create(:user, :with_posts)
            expect(user.posts.count).to eq(3)
        end
    end
end
```
