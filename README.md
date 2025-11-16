# BLT Sizzle 🔥

A simple Django app that helps teams stay in sync with daily check-ins, time tracking, and progress monitoring. Think of it as your team's daily standup tool, but better.

## What Can You Do With Sizzle?

- **📝 Daily Check-ins**: Your team shares what they did, what's next, and any blockers
- **⏱️ Time Tracking**: Log hours spent on tasks and projects  
- **🏆 Stay Motivated**: Streaks and leaderboards keep things fun
- **🔔 Get Reminders**: Never forget to check in with email or Slack notifications
- **📊 See Progress**: View reports for yourself or your whole team
- **💬 Slack Integration**: Share updates directly in your Slack channels (optional)
- **Analytics**: View individual and team reports
- **Slack Integration**: Post check-ins directly to Slack (optional)

## Architecture & Design
## Why Use Sizzle?

### Built to Play Nice

Sizzle is designed to work with your existing Django project without getting in the way:

- **Drop it in**: Works out of the box with just a few lines of configuration
- **Use what you need**: Turn features on/off with simple settings
- **Bring your own models**: Plug into your existing User, Organization, or Team models
- **Looks like your app**: Uses your project's templates and styles automatically

### Smart Defaults

You don't need to configure everything upfront:

```python
# This is literally all you need to get started
INSTALLED_APPS = ['sizzle']
```

Want more? Add what you need:

```python
# Connect to your existing models
SIZZLE_ORGANIZATION_MODEL = 'your_app.Organization'

# Turn features on/off
SIZZLE_SLACK_ENABLED = False          # No Slack? No problem
SIZZLE_EMAIL_REMINDERS_ENABLED = True # Just use email

# Match your design
SIZZLE_PARENT_BASE = 'base.html'      # Extends your base template
```
## Requirements
## What You'll Need

- Python 3.11 or newer
- Django 4.0 or newer
- That's it for the basics!

Optional stuff:
- Slack workspace (if you want Slack notifications)
- Email server (if you want email reminders)

## Installation

### The Easy Way

```bash
pip install blt-sizzle
```

### From Source (for developers)

```bash
### Set It Up

**Step 1:** Add to your `settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'myapp',  # Your existing apps
    'sizzle', # Add this line
]
```

**Step 2:** Add URLs to your main `urls.py`

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sizzle/', include('sizzle.urls')),  # Add this
    # ... your other URLs
]
```m django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Add Sizzle URLs
    path('sizzle/', include('sizzle.urls')),
    
    # Your other URLs
]
**Step 3:** Make Sizzle match your design (optional but recommended)

```python
# In settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sizzle.context_processors.sizzle_context',  # Add this line
            ],
        },
    },
]

# Optional: Tell Sizzle to use your base template
SIZZLE_PARENT_BASE = 'base.html'  # Your project's main template
SIZZLE_SHOW_SIDENAV = True        # Show your navigation
```

**Step 4:** Set up the database

```bash
python manage.py migrate sizzle
python manage.py collectstatic --noinput
```

This creates three simple tables:
- Daily check-in reports
- Time log entries  
- Reminder settings for each user
python manage.py createsuperuser
```

## Quick Start

### Access Sizzle

Start your development server:
```
python manage.py runserver
```

Visit these URLs:
- Main dashboard: `http://localhost:8000/sizzle/`
- Submit check-in: `http://localhost:8000/sizzle/check-in/`
- View time logs: `http://localhost:8000/sizzle/time-logs/`
- Admin panel: `http://localhost:8000/admin/`

### Submit Your First Check-in

1. Log in to your Django app
2. Navigate to `/sizzle/check-in/`
3. Fill out the daily status form
## Your First Check-in

Start Django:
```bash
python manage.py runserver
```

Go to http://localhost:8000/sizzle/ and you'll see:

- **Main Dashboard**: See everyone's recent activity
- **Check-in Page**: Submit your daily update
- **Time Logs**: View and track hours worked
- **Your Profile**: See your streak and stats

Try submitting a check-in:

1. Go to `/sizzle/check-in/`
2. Fill in what you worked on today
3. Add what you're planning tomorrow
4. Mention any blockers
5. Submit!

## Making It Yours

### The Basics

Sizzle works like Django's `AUTH_USER_MODEL` - it has smart defaults but lets you customize everything.

#### Minimum Config (it really is this simple)
# Template Context Processor (for template integration)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # Add Sizzle context processor
                'sizzle.context_processors.sizzle_context',
            ],
        },
    },
]
```

### Model Integration (Optional)

If your project has existing models that Sizzle should integrate with, configure them:

```python
# settings.py

# Model Configuration (all optional)
SIZZLE_SLACK_INTEGRATION_MODEL = 'your_app.SlackIntegration'  # For Slack notifications
SIZZLE_ORGANIZATION_MODEL = 'your_app.Organization'           # For organization features
SIZZLE_USERPROFILE_MODEL = 'your_app.UserProfile'            # For user profiles
SIZZLE_NOTIFICATION_MODEL = 'your_app.Notification'          # For in-app notifications

# Feature Flags
SIZZLE_SLACK_ENABLED = True              # Enable Slack integration
SIZZLE_EMAIL_REMINDERS_ENABLED = True    # Enable email reminders
SIZZLE_DAILY_CHECKINS_ENABLED = True     # Enable check-in reminders
### Connecting to Your Existing Models

Got a User model? Organization? Team? Sizzle can use them:
SIZZLE_SHOW_SIDENAV = True               # Show your project's navigation
```

### Slack Integration (Optional)

To enable Slack notifications:

1. **Install Slack dependencies:**
```bash
pip install slack-bolt
```

2. **Create SlackIntegration model in your project:**
```python
# your_app/models.py
class SlackIntegration(models.Model):
    integration = models.ForeignKey('Integration', on_delete=models.CASCADE)
    bot_access_token = models.CharField(max_length=255)
    default_channel_id = models.CharField(max_length=255)
    daily_updates = models.BooleanField(default=False)
### Want Slack Updates?

If you use Slack, Sizzle can post there too:

**1. Install the Slack stuff:**
```bash
pip install blt-sizzle[slack]
```

**2. Set up a Slack bot** (through Slack's admin panel)

**3. Create a simple model in your app:**
```python
# your_app/models.py
class SlackIntegration(models.Model):
    bot_access_token = models.CharField(max_length=255)
    default_channel_id = models.CharField(max_length=255)
    daily_updates = models.BooleanField(default=False)
    daily_update_time = models.IntegerField()  # Hour in UTC (0-23)
```

**4. Tell Sizzle about it:**
```python
# settings.py
SIZZLE_SLACK_ENABLED = True
SIZZLE_SLACK_INTEGRATION_MODEL = 'your_app.SlackIntegration'
```

**5. Test it:**
```bash
python manage.py slack_daily_timelogs
### What Sizzle Expects (If You're Integrating)

Sizzle works fine on its own, but if you want to connect it to your existing models, here's what it looks for:
- `user` (ForeignKey to User): Target user
- `message` (TextField): Notification message
- `notification_type` (CharField): Type of notification
- `link` (URLField): Link to action

**Organization Model:**
- Any model that represents teams/organizations
- Referenced by TimeLog for organization-specific time tracking

## Configuration Examples

### Standalone Project (Minimal)

```python
# settings.py
INSTALLED_APPS = ['sizzle']

# All features disabled except core functionality
SIZZLE_SLACK_ENABLED = False
SIZZLE_EMAIL_REMINDERS_ENABLED = True
SIZZLE_DAILY_CHECKINS_ENABLED = False
```

### BLT Integration (Full Features)
## Real-World Examples

### Just Getting Started?
INSTALLED_APPS = ['website', 'sizzle']

# Model Configuration
SIZZLE_SLACK_INTEGRATION_MODEL = 'website.SlackIntegration'
SIZZLE_ORGANIZATION_MODEL = 'website.Organization'
SIZZLE_USERPROFILE_MODEL = 'website.UserProfile'
SIZZLE_NOTIFICATION_MODEL = 'website.Notification'

# All features enabled
SIZZLE_SLACK_ENABLED = True
SIZZLE_EMAIL_REMINDERS_ENABLED = True
### Using Everything (Like in BLT)e

# Template Integration
SIZZLE_PARENT_BASE = 'base.html'
SIZZLE_SHOW_SIDENAV = True
```

### Custom Project

```python
# settings.py
# Use your own models
SIZZLE_ORGANIZATION_MODEL = 'companies.Company'
SIZZLE_USERPROFILE_MODEL = 'accounts.Profile'

# Disable unused features
SIZZLE_SLACK_ENABLED = False
SIZZLE_DAILY_CHECKINS_ENABLED = False

# Keep email reminders
SIZZLE_EMAIL_REMINDERS_ENABLED = True
```
### Pick and Choose
## Quick Start

### Basic Settings

Add these to your `settings.py` to customize Sizzle:

```
# Optional: Customize the base template (see Template Customization below)
SIZZLE_BASE_TEMPLATE = 'sizzle/base.html'  # Default

# Optional: Sizzle-specific settings
SIZZLE_SETTINGS = {
    'ENABLE_SLACK_INTEGRATION': False,  # Set to True if using Slack
    'ENABLE_EMAIL_REMINDERS': True,     # Send email reminders
    'DEFAULT_REMINDER_TIME': '09:00',   # Daily reminder time (24-hour format)
## All the Settings (Reference)

Here's everything you can configure:
### Slack Integration (Optional)

If you want Slack notifications:

1. Install Slack dependencies:
```
pip install django-sizzle[slack]
```

2. Add Slack configuration to `settings.py`:
```
SIZZLE_SETTINGS = {
    'ENABLE_SLACK_INTEGRATION': True,
}

# You'll need these from your Slack app
SLACK_BOT_TOKEN = 'xoxb-your-bot-token'
SLACK_SIGNING_SECRET = 'your-signing-secret'
```

3. Run the Slack time log command:
```
python manage.py slack_daily_timelogs
```

### Email Reminders

To enable email reminders for check-ins:

1. Configure Django email settings in `settings.py`:
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

2. Set up a cron job to send daily reminders:
```
# Add to crontab (example: 9 AM daily)
### Setting Up Email Reminders

Want to remind people to check in? Set up email:

**1. Configure email in `settings.py`:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use an app password, not your real one!
```

**2. Set up a daily cron job:**
```bash
# Runs every day at 9 AM
0 9 * * * cd /path/to/your/project && python manage.py cron_send_reminders
```endblock %}

## Making Sizzle Look Like Your App

Sizzle comes with basic templates, but you'll probably want it to match your site's design.

### Easy Way: Tell Sizzle to Use Your Template

Just add this to `settings.py`:
```python
SIZZLE_PARENT_BASE = 'base.html'  # Your project's base template
```

### Custom Way: Override the Whole Thing

Create your own `templates/sizzle/base.html`:
```
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Your project templates
        'APP_DIRS': True,  # Important: Finds sizzle/templates/
        ...
    },
]
```

### Option 2: Use Settings to Specify Base Template

In `settings.py`:
```
SIZZLE_BASE_TEMPLATE = 'my_site/base.html'
```

Then create `my_site/base.html` with these required blocks:
```
{% block title %}{% endblock %}
### What Sizzle Needs in Your Template

Your base template just needs these blocks:

```django
{% block title %}{% endblock %}         {# Page titles #}
{% block content %}{% endblock %}       {# Main content #}
{% block extra_head %}{% endblock %}    {# Extra CSS (optional) #}
{% block extra_js %}{% endblock %}      {# Extra JavaScript (optional) #}
```

That's it! Sizzle will fill them in.
- `created_at` (DateTimeField): Submission timestamp
- `streak_count` (IntegerField): Current streak days

**Example usage**:
```
from sizzle.models import DailyStatusReport

# Get today's check-ins
today_reports = DailyStatusReport.objects.filter(
    created_at__date=timezone.now().date()
## The Data Models

### DailyStatusReport

What people submit for their daily check-ins.

```python
from sizzle.models import DailyStatusReport

# See what everyone did today
today = DailyStatusReport.objects.filter(
    created_at__date=timezone.now().date()
)
```

**What it stores:**
- Who submitted it
- What they worked on yesterday
- What they're doing today
- Any blockers
- Their current mood
- Streak count

### TimeLog

Time tracking for tasks and projects.

```python
from sizzle.models import TimeLog

# Log some work
TimeLog.objects.create(
    user=request.user,
    start_time=timezone.now(),
    end_time=timezone.now() + timedelta(hours=2),
    github_issue_url="https://github.com/org/repo/issues/123"
)
```

**What it tracks:**
- Who worked
- Start and end time
- Which organization (optional)
- Link to GitHub issue (optional)
- Duration (calculated automatically)

### ReminderSettings

Personal reminder preferences for each user.

**What you can customize:**
- What time to get reminded
- Which days of the week
- Timezone
- Enable/disable reminders
- Notification model (website app)
## Automation Commands

Sizzle comes with commands you can run manually or schedule with cron:

### Remind People to Check In
Sends a notification to everyone who hasn't checked in yet.

### Email Reminder System
Send email reminders to users based on their personal ReminderSettings.

```bash
**How it works:**
- Checks which teams have check-ins enabled
- Finds users who haven't checked in today
- Sends them a friendly reminder

**Run it daily:**
```bash
# Every day at 9 AM
0 9 * * * cd /path/to/project && python manage.py daily_checkin_reminder
```

### Send Email Reminders
Emails people based on their personal preferences.

**Cron setup (runs every hour):**
```bash
0 * * * * cd /path/to/project && python manage.py cron_send_reminders
```

### Slack Daily Timelogs
Post daily timelog summaries to Slack channels.

**Smart about it:**
- Only emails people who want reminders
- Respects their timezone
- Skips people who already checked in
- Logs everything

**Run it every hour:**
```bash
0 * * * * cd /path/to/project && python manage.py cron_send_reminders
```

### Post to Slack
Shares daily time log summaries in Slack.
- Valid Slack bot tokens

**Example output:**
```
### Time Log Summary ###

Task: Bug fix - Issue #123
Start: 2024-11-08 09:00:00
End: 2024-11-08 11:30:00
Issue URL: https://github.com/org/repo/issues/123

Task: Feature development - Issue #456
Start: 2024-11-08 13:00:00
End: 2024-11-08 16:00:00
**What gets posted:**zed logging and error handling

**Cron setup (once daily):**
```bash
0 9 * * * cd /path/to/project && python manage.py run_sizzle_daily
```

## URLs Reference

| URL Pattern | View | Description |
|-------------|------|-------------|
| `/sizzle/` | `sizzle` | Main dashboard |
| `/sizzle/check-in/` | `checkIN` | Check-in list |
| `/sizzle/add-sizzle-checkin/` | `add_sizzle_checkIN` | Submit new check-in |
| `/sizzle/check-in/<id>/` | `checkIN_detail` | View specific check-in |
| `/sizzle/time-logs/` | `TimeLogListView` | View time logs |
| `/sizzle/api/timelogsreport/` | `TimeLogListAPIView` | Time log API |
| `/sizzle/sizzle-daily-log/` | `sizzle_daily_log` | Daily log view |
| `/sizzle/user-sizzle-report/<username>/` | `user_sizzle_report` | User report |

## Dependencies

### Required (Core)

These are installed automatically with `pip install django-sizzle`:

- **Django** (>= 4.0): Web framework
- **pytz** (>= 2023.3): Timezone handling

### Optional Dependencies

Install with extras for additional features:

**Slack Integration**:
```
pip install django-sizzle[slack]
```
**Set it up:**
```bash
# Every hour
0 * * * * cd /path/to/project && python manage.py slack_daily_timelogs
```

### Run Everything at Once
One command to rule them all.

## External Dependencies

Sizzle relies on these Django built-in models (you must have them):
```bash
python manage.py run_sizzle_daily
```

This runs all the commands above in one go. Perfect for a single daily cron job:

```bash
# Every day at 9 AM
0 9 * * * cd /path/to/project && python manage.py run_sizzle_daily
```
## All the URLs

Here's where everything lives:

| URL | What's There |
|-----|--------------|
| `/sizzle/` | Main dashboard with everyone's activity |
| `/sizzle/check-in/` | List of all check-ins |
| `/sizzle/add-sizzle-checkin/` | Form to submit a new check-in |
| `/sizzle/check-in/<id>/` | View a specific check-in |
| `/sizzle/time-logs/` | Browse time logs |
| `/sizzle/api/timelogsreport/` | API for time log data (JSON) |
| `/sizzle/sizzle-daily-log/` | Your daily activity log |
| `/sizzle/user-sizzle-report/<username>/` | See someone's full report |

status = validate_model_configuration()
print(json.dumps(status, indent=2))
```

This will show you which models are available:
```json
{
  "slack_integration": true,
  "organization": true,
## What Gets Installed

### The Basics (Always Installed)

```bash
pip install blt-sizzle
```

Gets you:
- Django 4.0+ support
- pytz for timezone handling
- python-dateutil for date stuff

### Extra Features

Want more? Add these:

```bash
# Slack notifications
pip install blt-sizzle[slack]

# Email sending
pip install blt-sizzle[email]

# Everything
pip install blt-sizzle[full]

# Development tools
pip install blt-sizzle[dev]

# Testing tools  
pip install blt-sizzle[test]
```

### Playing Nice with Your Models
## Common Issues (And How to Fix Them)

### "Can't find sizzle"

Did you add it to `INSTALLED_APPS`? 

```python
### Check What's Working

Run this to see which features are set up:
    # ...
    'sizzle',  # This line!
]
```
All optional! Sizzle will work fine either way.

### Template Issues

#### "TemplateDoesNotExist: sizzle/base.html"
Run `python manage.py collectstatic` and ensure `APP_DIRS: True` in `TEMPLATES` settings.

#### Templates look unstyled
1. Run `python manage.py collectstatic`
2. Make sure `STATIC_URL` is configured in `settings.py`
3. Check browser console for 404 errors on CSS files

### Database Issues

#### Migrations not applying
```bash
# Check pending migrations
python manage.py showmigrations sizzle
### Slack Not Working?

Two common fixes:

**Don't need Slack?**
```python
SIZZLE_SLACK_ENABLED = False
```

**Want Slack?**
```bash
pip install blt-sizzle[slack]
```

### Commands Failing?

Test them one at a time:

```bash
python manage.py daily_checkin_reminder  # Notifications working?
python manage.py cron_send_reminders     # Emails working?
python manage.py slack_daily_timelogs    # Slack working?
```

### Templates Look Broken?

Try this:
```bash
python manage.py collectstatic
```

Then check:
1. Is `STATIC_URL` in your settings?
2. Any errors in browser console?
3. Is `APP_DIRS = True` in TEMPLATES?

### Database Problems?

```bash
# See what's pending
python manage.py showmigrations sizzle

# Run migrations
python manage.py migrate sizzle
```

### Turn On Debug Mode

Want to see what's happening?

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `pytest`
5. Format code: `black sizzle/ && isort sizzle/`
6. Submit a pull request

## License

This project is licensed under the AGPL-3.0 License - see LICENSE file for details.

## Credits

Developed as part of the OWASP Bug Logging Tool (BLT) project.

## Support

- GitHub Issues: https://github.com/OWASP-BLT/BLT/issues
- OWASP BLT: https://owasp.org/www-project-bug-logging-tool/

## Changelog

### Version 0.1.0 (2025-11-08)
- Initial release
- Daily check-in functionality
- Time logging
- Streak tracking
- Email reminders
- Slack integration (optional)
- REST API endpoints
    ## For Developers

Want to contribute or modify Sizzle? Here's how:

### Get Set Up

```bash
# Clone it
git clone https://github.com/OWASP-BLT/BLT.git
cd BLT/sizzle

# Install for development
pip install -e .[dev,test]
```

### Run Tests

```bash
# All tests
pytest

# Just Sizzle tests
python manage.py test sizzle

# With coverage
pytest --cov=sizzle
```

### Keep Code Clean

We use these tools:

```bash
# Format everything
black sizzle/
isort sizzle/

# Check for issues
ruff check sizzle/
```

All of this runs automatically with pre-commit hooks if you set it up:

```bash
pre-commit install
```

## Contributing

We'd love your help! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Who Made This?

BLT Sizzle was built by the OWASP Bug Logging Tool (BLT) team and community contributors. We needed a way to keep our distributed team connected, so we built this.

Now we're sharing it so other teams can use it too!

## Get Help

- **Found a bug?** [Open an issue](https://github.com/OWASP-BLT/BLT/issues)
- **Have a question?** [Start a discussion](https://github.com/OWASP-BLT/BLT/discussions)
- **Want to chat?** Join our community (link in BLT repo)

## License

MIT License - use it however you want! See [LICENSE](LICENSE) for the legal stuff.

## What's New?

### Version 0.1.0 (November 2024)
First release! 🎉

What's included:
- Daily check-ins with streak tracking
- Time logging for tasks
- Email and Slack reminders
- Team leaderboards
- REST API
- Works with any Django project

### Coming Soon
- Mobile-friendly interface
- More integrations (Discord, Teams)
- Analytics dashboard
- Recurring tasks
- Team goals

Have ideas? [Let us know!](https://github.com/OWASP-BLT/BLT/issues/new)

---

Made with ❤️ by the OWASP BLT community