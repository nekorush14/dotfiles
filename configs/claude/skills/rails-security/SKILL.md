---
name: rails-security
description: Implement security best practices including authentication, authorization, and protection against common vulnerabilities. Use when implementing user authentication, access control, or securing application endpoints.
---

# Rails Security Specialist

Specialized in implementing security best practices for Rails applications.

## When to Use This Skill

- Implementing user authentication
- Adding authorization and access control
- Protecting against common vulnerabilities (XSS, CSRF, SQL injection)
- Securing API endpoints
- Implementing strong parameters

## Core Principles

- **Defense in Depth**: Multiple layers of security
- **Least Privilege**: Grant minimum necessary permissions
- **Secure by Default**: Safe defaults, explicit opt-in for risky operations
- **Validate Input**: Never trust user input
- **Protect Sensitive Data**: Encrypt passwords and sensitive information

## Implementation Guidelines

### Strong Parameters

```ruby
class UsersController < ApplicationController
    def create
        @user = User.new(user_params)
        if @user.save
            redirect_to @user
        else
            render :new
        end
    end

    private

    def user_params
        # WHY: Whitelist permitted attributes to prevent mass assignment
        params.require(:user).permit(:name, :email, :password, :password_confirmation)
    end
end
```

### Authentication with Devise

```ruby
class ApplicationController < ActionController::Base
    before_action :authenticate_user!

    # WHY: Allow public access to specific actions
    skip_before_action :authenticate_user!, only: [:index, :show]
end
```

### Authorization

```ruby
class ArticlesController < ApplicationController
    before_action :authenticate_user!
    before_action :set_article, only: [:edit, :update, :destroy]
    before_action :authorize_owner!, only: [:edit, :update, :destroy]

    private

    def set_article
        @article = Article.find(params[:id])
    end

    def authorize_owner!
        unless current_user.admin? || @article.user == current_user
            redirect_to root_path, alert: 'Not authorized'
        end
    end
end
```

### Using Pundit for Authorization

```ruby
# app/policies/article_policy.rb
class ArticlePolicy < ApplicationPolicy
    def update?
        user.admin? || record.user == user
    end

    def destroy?
        user.admin? || record.user == user
    end
end

# In controller
class ArticlesController < ApplicationController
    def update
        @article = Article.find(params[:id])
        authorize @article

        if @article.update(article_params)
            redirect_to @article
        else
            render :edit
        end
    end
end
```

### SQL Injection Prevention

```ruby
# Bad: SQL injection vulnerable
User.where("email = '#{params[:email]}'")

# Good: Parameterized query
User.where('email = ?', params[:email])

# Good: Hash conditions
User.where(email: params[:email])

# Good: Named parameters
User.where('email = :email', email: params[:email])
```

### Cross-Site Scripting (XSS) Prevention

```ruby
# In views: Rails escapes by default
<%= @user.name %>  # Automatically escaped

# Explicitly escape
<%= h @user.name %>

# Mark as HTML safe only for trusted content
<%= sanitize @article.content %>

# Raw (dangerous, avoid unless necessary)
<%= raw @trusted_html %>  # Use sparingly
```

### CSRF Protection

```ruby
class ApplicationController < ActionController::Base
    # WHY: Enabled by default, protects against CSRF attacks
    protect_from_forgery with: :exception

    # For API endpoints
    protect_from_forgery with: :null_session
end
```

### Password Security

```ruby
class User < ApplicationRecord
    # Use bcrypt for password hashing
    has_secure_password

    validates :password, length: { minimum: 8 }, on: :create
    validates :password, format: {
        with: /\A(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
        message: 'must include uppercase, lowercase, and number'
    }, on: :create
end
```

### Secure Token Generation

```ruby
class User < ApplicationRecord
    has_secure_token :auth_token

    # Custom token generation
    before_create :generate_reset_token

    private

    def generate_reset_token
        # WHY: Use SecureRandom for cryptographically secure tokens
        self.reset_token = SecureRandom.urlsafe_base64(32)
    end
end
```

### API Authentication

```ruby
class Api::BaseController < ActionController::API
    before_action :authenticate_api_user!

    private

    def authenticate_api_user!
        token = request.headers['Authorization']&.split(' ')&.last
        @current_user = User.find_by(auth_token: token)

        # WHY: Return 401 if token invalid
        render json: { error: 'Unauthorized' }, status: :unauthorized unless @current_user
    end
end
```

### Rate Limiting

```ruby
# Using Rack::Attack
class Application < Rails::Application
    config.middleware.use Rack::Attack
end

# config/initializers/rack_attack.rb
Rack::Attack.throttle('api/ip', limit: 100, period: 1.hour) do |req|
    req.ip if req.path.start_with?('/api')
end
```

### Content Security Policy

```ruby
# config/initializers/content_security_policy.rb
Rails.application.config.content_security_policy do |policy|
    policy.default_src :self
    policy.script_src :self, :https
    policy.style_src :self, :https
    policy.img_src :self, :https, :data
end
```

## Common Vulnerabilities to Prevent

### Mass Assignment

```ruby
# Bad: Allows users to set any attribute
User.create(params[:user])

# Good: Use strong parameters
User.create(user_params)
```

### Insecure Direct Object Reference

```ruby
# Bad: Users can access any article by ID
@article = Article.find(params[:id])

# Good: Scope to current user
@article = current_user.articles.find(params[:id])
```

### Session Fixation

```ruby
# After login, reset session
def create
    user = User.authenticate(params[:email], params[:password])
    if user
        reset_session  # WHY: Prevent session fixation
        session[:user_id] = user.id
        redirect_to dashboard_path
    end
end
```

## Tools to Use

- `Read`: Review existing security code
- `Edit`: Modify security implementations
- `Bash`: Run security audit tools
- `mcp__serena__find_symbol`: Find security patterns

### Bash Commands

```bash
# Run Brakeman security scanner
gem install brakeman
brakeman

# Run Bundler audit
gem install bundler-audit
bundle audit

# Check for vulnerable gems
bundle exec bundle-audit check --update
```

## Workflow

1. **Identify Security Requirements**: Authentication, authorization needs
2. **Write Security Tests**: Test unauthorized access
3. **Implement Protection**: Add authentication/authorization
4. **Use Strong Parameters**: Whitelist attributes
5. **Test Security**: Verify protection works
6. **Run Security Audit**: Use Brakeman
7. **Review Dependencies**: Check for vulnerable gems

## Related Skills

- `rails-model-design`: Secure model validations
- `rails-rspec-testing`: Testing security features

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Always use strong parameters
- Parameterize SQL queries (never string interpolation)
- Enable CSRF protection
- Use `has_secure_password` for passwords
- Authenticate before authorization
- Validate and sanitize user input
- Use HTTPS in production
- Keep dependencies updated
- Run security audits regularly
- Implement proper error handling (don't leak sensitive info)
