# Contributing to BLT Sizzle

Thanks for thinking about contributing! BLT Sizzle is a pluggable Django app (not a standalone project) for daily check-ins and time tracking. We welcome contributions from everyone.

## What Is BLT Sizzle?

BLT Sizzle is a Django package that you can install in any Django project. It's not a standalone Django project itself - it's a plugin that adds functionality to existing Django applications.

- **Package name**: `blt-sizzle`
- **Repository**: Part of [OWASP BLT](https://github.com/OWASP-BLT/BLT)
- **Python**: 3.11+
- **Django**: 4.0-5.1

## How You Can Help

- **Fix bugs** - Found something broken? Fix it!
- **Add features** - Have an idea? Build it!
- **Improve docs** - Make things clearer for others
- **Write tests** - Help us catch bugs before they happen
- **Report issues** - Let us know what's not working
- **Answer questions** - Help other users in discussions

## Development Setup

Since Sizzle is a Django plugin, you need a Django project to develop and test it. We recommend two approaches:

### Option 1: Use BLT Project (Recommended)

The easiest way is to develop Sizzle within the BLT project where it's already integrated:

```bash
# 1. Fork the BLT repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/BLT.git
cd BLT

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Sizzle in editable mode
pip install -e sizzle/

# 5. Set up database
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver
```

Now you can:
- Access Sizzle at `http://localhost:8000/sizzle/`
- Make changes to `sizzle/` directory
- See changes immediately (editable install)
- Test within a real Django application

### Option 2: Create Test Django Project

If you prefer working with a minimal setup:

```bash
# 1. Fork and clone BLT repo
git clone https://github.com/YOUR_USERNAME/BLT.git
cd BLT/sizzle

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install Sizzle with development dependencies
pip install -e ".[dev,test]"

# 4. Create a test Django project
django-admin startproject testproject
cd testproject

# 5. Configure settings.py
# Add 'sizzle' to INSTALLED_APPS
# Add Sizzle URLs to urls.py

# 6. Run migrations and test
python manage.py migrate
python manage.py runserver
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b your-feature-name
```

Good branch names:
- `fix-timezone-reminder-bug`
- `add-discord-integration`
- `improve-installation-docs`

### 2. Development Workflow

Since Sizzle is installed in editable mode (`pip install -e`), any changes you make to the code are immediately reflected:

```bash
# Make your changes in sizzle/ directory
# No need to reinstall - changes are live!

# Test your changes
python manage.py runserver
# Visit http://localhost:8000/sizzle/
```

### 3. Writing Code

**Keep it simple:**
- Write code that's easy to read
- Add comments when things are tricky
- Follow Django conventions
- Maintain compatibility with Django 4.0-5.1

**Test your changes:**
```bash
# Run all tests
pytest

# Run specific tests
pytest sizzle/tests.py::TestClassName::test_method_name

# Run with coverage
pytest --cov=sizzle
```

### 4. Code Quality

We use these tools to maintain code quality:

```bash
# Format code (120 character lines)
black sizzle/

# Sort imports
isort sizzle/ --profile black

# Lint code
ruff check sizzle/

# Run all checks at once
black sizzle/ && isort sizzle/ --profile black && ruff check sizzle/
```

Install pre-commit hooks to run these automatically:
```bash
pip install pre-commit
pre-commit install
```

## Testing

### Writing Tests

We use Django's test framework. Place tests in `sizzle/tests.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from sizzle.models import DailyStatusReport

class DailyStatusReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass')
    
    def test_create_report(self):
        """Test creating a daily status report"""
        report = DailyStatusReport.objects.create(
            user=self.user,
            what_i_did="Fixed bugs",
            what_i_will_do="Add features"
        )
        self.assertEqual(report.user, self.user)
        self.assertEqual(report.what_i_did, "Fixed bugs")
```

### Manual Testing

Use the Django admin and web interface to test manually:

1. Create test data through admin: `http://localhost:8000/admin/`
2. Test user flows: `http://localhost:8000/sizzle/`
3. Test management commands:
   ```bash
   python manage.py daily_checkin_reminder
   python manage.py cron_send_reminders
   python manage.py slack_daily_timelogs
   ```

## Submitting Changes

### 1. Commit Your Changes

Write clear commit messages using conventional commits:

```bash
# Good commits
git commit -m "feat: add Discord integration support"
git commit -m "fix: resolve timezone bug in reminder system"
git commit -m "docs: update installation instructions"

# Not so good
git commit -m "fix bug"
git commit -m "update stuff"
```

### 2. Push to Your Fork

```bash
git push origin your-feature-name
```

### 3. Create Pull Request

1. Go to [OWASP BLT repository](https://github.com/OWASP-BLT/BLT)
2. Click "New Pull Request"
3. Choose your branch
4. Fill out the template:
   - What does this change?
   - Why is it needed?
   - How did you test it?
   - Include screenshots for UI changes

### 4. CI and Review

- GitHub Actions will run tests automatically
- A maintainer will review your changes
- They might ask questions or suggest improvements
- Don't worry if changes are requested - it's normal!

## Project Structure

Understanding the Sizzle structure:

```
sizzle/
├── __init__.py          # Package init
├── admin.py             # Django admin config
├── apps.py              # App configuration
├── models.py            # Database models
├── views.py             # View functions
├── urls.py              # URL patterns
├── forms.py             # Django forms
├── management/          # Management commands
├── templates/sizzle/    # HTML templates
├── static/sizzle/       # CSS, JS, images
├── tests.py             # Test cases
└── migrations/          # Database migrations
```

## Types of Contributions

### Bug Fixes

1. Create an issue describing the bug (if one doesn't exist)
2. Reference the issue in your PR: "Fixes #123"
3. Include steps to reproduce
4. Add a test that would have caught the bug

### New Features

1. Open an issue first to discuss the feature
2. Wait for approval before spending time coding
3. Keep the initial implementation simple
4. Write comprehensive tests
5. Update documentation

### Documentation

- Fix typos and unclear sections
- Add code examples
- Improve installation instructions
- Write tutorials

### Tests

- Add tests for uncovered code
- Test edge cases
- Add regression tests for known bugs
- Test new features thoroughly

## Development Tips

### Working with Models

When changing models, create migrations:

```bash
python manage.py makemigrations sizzle
python manage.py migrate
```

### Debugging

Add logging to see what's happening:

```python
import logging
logger = logging.getLogger(__name__)

def my_view(request):
    logger.debug("Processing request for user %s", request.user)
    # Your code here
```

### Testing Different Django Versions

Sizzle supports Django 4.0-5.1. Test compatibility:

```bash
# Install specific Django version
pip install "Django>=4.0,<4.1"
pytest

pip install "Django>=5.0,<5.1"  
pytest
```

## Communication

Need help or have questions?

- **GitHub Issues**: Report bugs, request features
- **GitHub Discussions**: Ask questions, share ideas
- **Pull Request Comments**: Discuss specific changes

## Recognition# Contributing to BLT Sizzle

Thanks for thinking about contributing! BLT Sizzle is a pluggable Django app (not a standalone project) for daily check-ins and time tracking. We welcome contributions from everyone.

## What Is BLT Sizzle?

BLT Sizzle is a Django package that you can install in any Django project. It's not a standalone Django project itself - it's a plugin that adds functionality to existing Django applications.

- **Package name**: `blt-sizzle`
- **Repository**: Part of [OWASP BLT](https://github.com/OWASP-BLT/BLT)
- **Python**: 3.11+
- **Django**: 4.0-5.1

## How You Can Help

- **Fix bugs** - Found something broken? Fix it!
- **Add features** - Have an idea? Build it!
- **Improve docs** - Make things clearer for others
- **Write tests** - Help us catch bugs before they happen
- **Report issues** - Let us know what's not working
- **Answer questions** - Help other users in discussions

## Development Setup

Since Sizzle is a Django plugin, you need a Django project to develop and test it. We recommend two approaches:

### Option 1: Use BLT Project (Recommended)

The easiest way is to develop Sizzle within the BLT project where it's already integrated:

```bash
# 1. Fork the BLT repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/BLT.git
cd BLT

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Sizzle in editable mode
pip install -e sizzle/

# 5. Set up database
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver
```

Now you can:
- Access Sizzle at `http://localhost:8000/sizzle/`
- Make changes to `sizzle/` directory
- See changes immediately (editable install)
- Test within a real Django application

### Option 2: Create Test Django Project

If you prefer working with a minimal setup:

```bash
# 1. Fork and clone BLT repo
git clone https://github.com/YOUR_USERNAME/BLT.git
cd BLT/sizzle

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install Sizzle with development dependencies
pip install -e ".[dev,test]"

# 4. Create a test Django project
django-admin startproject testproject
cd testproject

# 5. Configure settings.py
# Add 'sizzle' to INSTALLED_APPS
# Add Sizzle URLs to urls.py

# 6. Run migrations and test
python manage.py migrate
python manage.py runserver
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b your-feature-name
```

Good branch names:
- `fix-timezone-reminder-bug`
- `add-discord-integration`
- `improve-installation-docs`

### 2. Development Workflow

Since Sizzle is installed in editable mode (`pip install -e`), any changes you make to the code are immediately reflected:

```bash
# Make your changes in sizzle/ directory
# No need to reinstall - changes are live!

# Test your changes
python manage.py runserver
# Visit http://localhost:8000/sizzle/
```

### 3. Writing Code

**Keep it simple:**
- Write code that's easy to read
- Add comments when things are tricky
- Follow Django conventions
- Maintain compatibility with Django 4.0-5.1

**Test your changes:**
```bash
# Run all tests
pytest

# Run specific tests
pytest sizzle/tests.py::TestClassName::test_method_name

# Run with coverage
pytest --cov=sizzle
```

### 4. Code Quality

We use these tools to maintain code quality:

```bash
# Format code (120 character lines)
black sizzle/

# Sort imports
isort sizzle/ --profile black

# Lint code
ruff check sizzle/

# Run all checks at once
black sizzle/ && isort sizzle/ --profile black && ruff check sizzle/
```

Install pre-commit hooks to run these automatically:
```bash
pip install pre-commit
pre-commit install
```

## Testing

### Writing Tests

We use Django's test framework. Place tests in `sizzle/tests.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from sizzle.models import DailyStatusReport

class DailyStatusReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass')
    
    def test_create_report(self):
        """Test creating a daily status report"""
        report = DailyStatusReport.objects.create(
            user=self.user,
            what_i_did="Fixed bugs",
            what_i_will_do="Add features"
        )
        self.assertEqual(report.user, self.user)
        self.assertEqual(report.what_i_did, "Fixed bugs")
```

### Manual Testing

Use the Django admin and web interface to test manually:

1. Create test data through admin: `http://localhost:8000/admin/`
2. Test user flows: `http://localhost:8000/sizzle/`
3. Test management commands:
   ```bash
   python manage.py daily_checkin_reminder
   python manage.py cron_send_reminders
   python manage.py slack_daily_timelogs
   ```

## Submitting Changes

### 1. Commit Your Changes

Write clear commit messages using conventional commits:

```bash
# Good commits
git commit -m "feat: add Discord integration support"
git commit -m "fix: resolve timezone bug in reminder system"
git commit -m "docs: update installation instructions"

# Not so good
git commit -m "fix bug"
git commit -m "update stuff"
```

### 2. Push to Your Fork

```bash
git push origin your-feature-name
```

### 3. Create Pull Request

1. Go to [OWASP BLT repository](https://github.com/OWASP-BLT/BLT)
2. Click "New Pull Request"
3. Choose your branch
4. Fill out the template:
   - What does this change?
   - Why is it needed?
   - How did you test it?
   - Include screenshots for UI changes

### 4. CI and Review

- GitHub Actions will run tests automatically
- A maintainer will review your changes
- They might ask questions or suggest improvements
- Don't worry if changes are requested - it's normal!

## Project Structure

Understanding the Sizzle structure:

```
sizzle/
├── __init__.py          # Package init
├── admin.py             # Django admin config
├── apps.py              # App configuration
├── models.py            # Database models
├── views.py             # View functions
├── urls.py              # URL patterns
├── forms.py             # Django forms
├── management/          # Management commands
├── templates/sizzle/    # HTML templates
├── static/sizzle/       # CSS, JS, images
├── tests.py             # Test cases
└── migrations/          # Database migrations
```

## Types of Contributions

### Bug Fixes

1. Create an issue describing the bug (if one doesn't exist)
2. Reference the issue in your PR: "Fixes #123"
3. Include steps to reproduce
4. Add a test that would have caught the bug

### New Features

1. Open an issue first to discuss the feature
2. Wait for approval before spending time coding
3. Keep the initial implementation simple
4. Write comprehensive tests
5. Update documentation

### Documentation

- Fix typos and unclear sections
- Add code examples
- Improve installation instructions
- Write tutorials

### Tests

- Add tests for uncovered code
- Test edge cases
- Add regression tests for known bugs
- Test new features thoroughly

## Development Tips

### Working with Models

When changing models, create migrations:

```bash
python manage.py makemigrations sizzle
python manage.py migrate
```


## Code of Conduct

- Be respectful and welcoming
- Be patient with newcomers  
- Accept constructive criticism gracefully
- Focus on what's best for the community

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
