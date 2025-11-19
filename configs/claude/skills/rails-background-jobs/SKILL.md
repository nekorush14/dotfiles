---
name: rails-background-jobs
description: Implement background jobs using ActiveJob for asynchronous task processing. Use when tasks are time-consuming, can be processed asynchronously, or should not block user requests (emails, reports, data processing).
---

# Rails Background Jobs Specialist

Specialized in implementing background jobs with ActiveJob and Sidekiq.

## When to Use This Skill

- Sending emails asynchronously
- Generating large reports
- Processing uploaded files
- API calls to external services
- Data import/export operations
- Scheduled recurring tasks

## Core Principles

- **Asynchronous Execution**: Don't block user requests
- **Idempotency**: Jobs can be safely retried
- **Error Handling**: Graceful failure and retry logic
- **Queue Management**: Organize jobs by priority
- **Monitoring**: Track job execution and failures

## Implementation Guidelines

### Basic Job Structure

```ruby
# app/jobs/report_generation_job.rb
class ReportGenerationJob < ApplicationJob
    queue_as :default
    retry_on StandardError, wait: 5.seconds, attempts: 3

    def perform(report_id)
        report = Report.find(report_id)

        # WHY: Use transaction to ensure atomicity
        ActiveRecord::Base.transaction do
            generator = ReportGenerator.new(report)
            data = generator.generate!

            report.update!(
                status: 'completed',
                data: data,
                completed_at: Time.current
            )
        end

        # WHY: Notify user when report is ready
        ReportMailer.report_ready(report).deliver_now
    rescue ActiveRecord::RecordNotFound => e
        # WHY: Don't retry if record doesn't exist
        Rails.logger.error("Report #{report_id} not found: #{e.message}")
    end
end
```

### Enqueuing Jobs

```ruby
# Immediate execution
ReportGenerationJob.perform_now(report.id)

# Enqueue for background processing
ReportGenerationJob.perform_later(report.id)

# Schedule for later
ReportGenerationJob.set(wait: 1.hour).perform_later(report.id)

# Schedule for specific time
ReportGenerationJob.set(wait_until: Date.tomorrow.noon).perform_later(report.id)
```

### Email Delivery Jobs

```ruby
# app/mailers/user_mailer.rb
class UserMailer < ApplicationMailer
    def welcome_email(user)
        @user = user
        mail(to: @user.email, subject: 'Welcome!')
    end
end

# Enqueue email job
UserMailer.welcome_email(user).deliver_later

# With delay
UserMailer.welcome_email(user).deliver_later(wait: 1.hour)

# Immediate delivery (not recommended in controllers)
UserMailer.welcome_email(user).deliver_now
```

### Custom Queues

```ruby
class ReportGenerationJob < ApplicationJob
    # WHY: Use low priority queue for resource-intensive reports
    queue_as :low_priority

    def perform(report_id)
        # ...
    end
end

class NotificationJob < ApplicationJob
    # WHY: High priority for user-facing notifications
    queue_as :high_priority

    def perform(user_id, message)
        # ...
    end
end
```

### Retry Configuration

```ruby
class DataImportJob < ApplicationJob
    # Exponential backoff retry
    retry_on StandardError, wait: :exponentially_longer, attempts: 5

    # Fixed wait time
    retry_on NetworkError, wait: 10.seconds, attempts: 3

    # Custom retry logic
    retry_on CustomError, attempts: 5 do |job, exception|
        Rails.logger.warn("Job #{job.job_id} failed: #{exception.message}")
        # Custom handling
    end

    # Don't retry for certain errors
    discard_on ActiveRecord::RecordNotFound

    def perform(file_path)
        # Import logic
    end
end
```

### Job Callbacks

```ruby
class DataProcessingJob < ApplicationJob
    before_perform :log_start
    after_perform :log_completion
    around_perform :measure_time

    def perform(data_id)
        # Processing logic
    end

    private

    def log_start
        Rails.logger.info("Starting job #{job_id}")
    end

    def log_completion
        Rails.logger.info("Completed job #{job_id}")
    end

    def measure_time
        start_time = Time.current
        yield
        duration = Time.current - start_time
        Rails.logger.info("Job took #{duration} seconds")
    end
end
```

### Batch Processing Jobs

```ruby
class UserNotificationJob < ApplicationJob
    queue_as :notifications

    def perform(user_ids)
        User.where(id: user_ids).find_each do |user|
            NotificationService.notify(user)
        rescue => e
            # WHY: Log error but continue processing other users
            Rails.logger.error("Failed to notify user #{user.id}: #{e.message}")
        end
    end
end

# Enqueue in batches
User.active.in_batches(of: 1000) do |users|
    UserNotificationJob.perform_later(users.pluck(:id))
end
```

### Scheduled Jobs (with Sidekiq-Cron)

```ruby
# config/schedule.yml
daily_cleanup:
    cron: "0 2 * * *"  # 2 AM daily
    class: "DailyCleanupJob"

weekly_report:
    cron: "0 9 * * 1"  # 9 AM every Monday
    class: "WeeklyReportJob"
```

```ruby
# app/jobs/daily_cleanup_job.rb
class DailyCleanupJob < ApplicationJob
    queue_as :maintenance

    def perform
        # WHY: Clean up old records to maintain database performance
        OldRecord.where('created_at < ?', 90.days.ago).delete_all
        TempFile.where('created_at < ?', 7.days.ago).delete_all

        Rails.logger.info("Daily cleanup completed")
    end
end
```

## Sidekiq Configuration

```ruby
# config/sidekiq.yml
:concurrency: 5
:queues:
    - [high_priority, 2]
    - [default, 1]
    - [low_priority, 1]
    - [mailers, 1]
```

```ruby
# config/initializers/sidekiq.rb
Sidekiq.configure_server do |config|
    config.redis = { url: ENV['REDIS_URL'] }

    # WHY: Ensure database connections are properly managed
    config.on(:startup) do
        Rails.logger.info("Sidekiq server started")
    end
end

Sidekiq.configure_client do |config|
    config.redis = { url: ENV['REDIS_URL'] }
end
```

## Testing Background Jobs

```ruby
# spec/jobs/report_generation_job_spec.rb
RSpec.describe ReportGenerationJob, type: :job do
    let(:report) { create(:report) }

    describe '#perform' do
        it 'generates report' do
            expect {
                described_class.perform_now(report.id)
            }.to change { report.reload.status }.to('completed')
        end

        it 'sends notification email' do
            expect(ReportMailer).to receive(:report_ready).with(report)
            described_class.perform_now(report.id)
        end

        context 'when report not found' do
            it 'logs error without raising' do
                expect(Rails.logger).to receive(:error)
                described_class.perform_now(99999)
            end
        end
    end

    describe 'job enqueuing' do
        it 'enqueues job' do
            expect {
                described_class.perform_later(report.id)
            }.to have_enqueued_job(described_class).with(report.id)
        end
    end
end
```

## Tools to Use

- `Read`: Read existing job files
- `Write`: Create new job files
- `Edit`: Modify job logic
- `Bash`: Generate jobs, run Sidekiq

### Bash Commands

```bash
# Generate job
bundle exec rails generate job ReportGeneration

# Run Sidekiq
bundle exec sidekiq

# Monitor jobs (Sidekiq Web UI)
# Add to config/routes.rb: mount Sidekiq::Web => '/sidekiq'

# Clear jobs
bundle exec rails runner "Sidekiq::Queue.new.clear"
```

## Workflow

1. **Identify Async Task**: Determine what should run in background
2. **Write Tests**: Test job execution and retry logic
3. **Generate Job**: Use Rails generator
4. **Implement Logic**: Write job perform method
5. **Add Error Handling**: Configure retry and discard
6. **Configure Queue**: Set appropriate queue and priority
7. **Test**: Verify job executes correctly
8. **Monitor**: Track job execution in production

## Related Skills

- `rails-service-objects`: Complex job logic
- `rails-error-handling`: Error handling in jobs
- `rails-rspec-testing`: Testing jobs

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Keep jobs idempotent (safe to retry)
- Pass IDs, not objects
- Configure appropriate retry logic
- Use specific error handling
- Set queue priorities appropriately
- Monitor job execution and failures
- Test both success and failure scenarios
- Use transactions for data consistency
- Log important events
- Don't perform long-running operations synchronously
