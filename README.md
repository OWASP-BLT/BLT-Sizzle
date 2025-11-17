# BLT Sizzle

A pluggable Django app that helps teams stay in sync with daily check-ins, time tracking, and progress monitoring. Think of it as your team's daily standup tool, but better.

Originally built for the OWASP Bug Logging Tool (BLT), now available as a standalone package that works with any Django project.

## What Can You Do With Sizzle?

- **Daily Check-ins**: Your team shares what they did, what's next, and any blockers
- **Time Tracking**: Log hours spent on tasks and projects  
- **Stay Motivated**: Streaks and leaderboards keep things fun
- **Get Reminders**: Never forget to check in with email or Slack notifications
- **See Progress**: View reports for yourself or your whole team
- **Slack Integration**: Share updates directly in your Slack channels (optional)
- **Analytics**: View individual and team reports

## Architecture & Design

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
git clone https://github.com/OWASP-BLT/BLT.git
cd BLT
pip install -e sizzle/
```

## Quick Start

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
```

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

```bash
python manage.py createsuperuser
python manage.py runserver
```

Now visit `http://localhost:8000/sizzle/` to get started!

## Basic Configuration

Sizzle works out of the box, but you can customize it:

```python
# settings.py

# Feature toggles
SIZZLE_SLACK_ENABLED = True              # Enable Slack integration
SIZZLE_EMAIL_REMINDERS_ENABLED = True    # Enable email reminders

# Template integration
SIZZLE_PARENT_BASE = 'base.html'         # Use your base template
SIZZLE_SHOW_SIDENAV = True               # Show navigation

# Model integration (optional)
SIZZLE_ORGANIZATION_MODEL = 'myapp.Organization'
SIZZLE_USERPROFILE_MODEL = 'myapp.UserProfile'
```

## Optional External Integrations

Sizzle can integrate with your existing models to add extra functionality. All integrations are completely optional - Sizzle works perfectly fine without them.

### Organization Support

If you have an Organization/Company model, you can link time logs to organizations:

```python
# settings.py
SIZZLE_ORGANIZATION_MODEL = 'myapp.Organization'
```

**Requirements for your Organization model:**
- Must have an `id` field (standard Django)
- Should have a `name` field for display
- Optional: `url` field for organization links

**Example Organization model:**
```python
# myapp/models.py
class Organization(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
```

### User Profile Support  

Connect to your existing user profile system:

```python
# settings.py
SIZZLE_USERPROFILE_MODEL = 'myapp.UserProfile'
```

**Requirements for your UserProfile model:**
- Must be linked to Django's User model
- Used for enhanced user information in reports

### Notification System Integration

If you have a notification system, Sizzle can use it:

```python
# settings.py
SIZZLE_NOTIFICATION_MODEL = 'myapp.Notification'
```

### Slack Integration

For Slack notifications, you'll need:

1. **Install Slack dependencies:**
```bash
pip install slack-bolt
```

2. **Configure Slack settings:**
```python
# settings.py
SIZZLE_SLACK_ENABLED = True
SIZZLE_SLACK_INTEGRATION_MODEL = 'myapp.SlackIntegration'

# Slack API settings
SLACK_BOT_TOKEN = 'xoxb-your-bot-token'
SLACK_SIGNING_SECRET = 'your-signing-secret'
```

**Example SlackIntegration model:**
```python
# myapp/models.py
class SlackIntegration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slack_user_id = models.CharField(max_length=50)
    slack_channel = models.CharField(max_length=50, blank=True)
    enabled = models.BooleanField(default=True)
```

## Testing With Optional Features

Here's how to test Sizzle with organization support in a new Django project:

### Step 1: Create Test Project
```bash
mkdir test_sizzle_project
cd test_sizzle_project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install django blt-sizzle
django-admin startproject testproject .
cd testproject
python manage.py startapp myapp
```

### Step 2: Create Organization Model
```python
# myapp/models.py
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

### Step 3: Configure Settings
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'myapp',     # Your app with Organization model
    'sizzle',    # Sizzle app
]

# Optional: Connect Sizzle to your Organization model
SIZZLE_ORGANIZATION_MODEL = 'myapp.Organization'

# Optional: Customize templates
SIZZLE_PARENT_BASE = 'base.html'
SIZZLE_SHOW_SIDENAV = True

# Add URLs
# In your main urls.py, add:
# path('sizzle/', include('sizzle.urls')),
```

### Step 4: Set Up Database
```bash
python manage.py makemigrations myapp
python manage.py makemigrations sizzle
python manage.py migrate
python manage.py createsuperuser
```

### Step 5: Test Integration
```bash
python manage.py runserver
```

Visit `/admin/` and create some organizations, then go to `/sizzle/` to see them available in time tracking.

## What Features Work With/Without Integrations

| Feature | Without Integrations | With Organization Model | With User Profile | With Slack |
|---------|---------------------|------------------------|------------------|------------|
| Time Logging | ✅ Full functionality | ✅ + Organization linking | ✅ Enhanced user info | ✅ + Notifications |
| Daily Check-ins | ✅ Full functionality | ✅ Team organization | ✅ Rich profiles | ✅ + Auto-posting |
| Leaderboards | ✅ Username-based | ✅ Organization groups | ✅ Profile pictures | ✅ + Slack sharing |
| Reports | ✅ Basic reports | ✅ Org-level reporting | ✅ Detailed profiles | ✅ + Auto-summaries |
| Reminders | ✅ Email only | ✅ Team notifications | ✅ Personalized | ✅ + Slack DMs |

## Contributing

We'd love your help! Check out our [Contributing Guide](CONTRIBUTING.md) for detailed instructions on:

- Setting up your development environment
- Testing Sizzle within a Django project
- Code standards and testing
- Submitting pull requests

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

## What's New?

BLT Sizzle was built by the [OWASP Bug Logging Tool (BLT)](https://github.com/OWASP-BLT/BLT) team and community contributors. We needed a way to keep our distributed team connected, so we built this.

Now we're sharing it so other teams can use it too!

## Community & Support

- **Main Project**: [OWASP BLT Repository](https://github.com/OWASP-BLT/BLT)
- **Found a bug?** [Open an issue](https://github.com/OWASP-BLT/BLT/issues)
- **Have a question?** [Start a discussion](https://github.com/OWASP-BLT/BLT/discussions)
- **Slack Community**: [Join OWASP Slack](https://owasp.org/slack/invite)
- **BLT Channel**: [#project-blt](https://owasp.slack.com/archives/C2FF0UVHU)

## What's New?

### Version 0.1.0 (November 2024)
Initial release of BLT Sizzle as a standalone Django package.

Features included:
- Daily check-ins with streak tracking
- Time logging for tasks
- Email and Slack reminders
- Team leaderboards
- REST API
- Compatible with any Django project

### Roadmap
- Mobile-friendly interface
- Additional integrations (Discord, Teams)
- Enhanced analytics dashboard
- Recurring task support
- Team goal setting

Suggestions welcome! [Submit a feature request](https://github.com/OWASP-BLT/BLT/issues/new)

---

**Quick Links:**
- [OWASP BLT Project](https://github.com/OWASP-BLT/BLT)
- [Contributing Guide](CONTRIBUTING.md)
- [Join OWASP Slack](https://owasp.org/slack/invite)
- [BLT Community Channel](https://owasp.slack.com/archives/C2FF0UVHU)

## License

MIT License - see [LICENSE](LICENSE) for details.

Developed by the OWASP BLT community