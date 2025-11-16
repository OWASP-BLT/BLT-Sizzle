# Contributing to BLT Sizzle

Thanks for thinking about contributing! We're happy to have you here. This is a community project, and we welcome contributions from everyone.

## How You Can Help

There are lots of ways to contribute:

- **Fix bugs** - Found something broken? Fix it!
- **Add features** - Have an idea? Build it!
- **Improve docs** - Make things clearer for others
- **Write tests** - Help us catch bugs before they happen
- **Report issues** - Let us know what's not working
- **Answer questions** - Help other users in discussions

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/BLT.git
cd BLT/sizzle
```

### 2. Set Up Your Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install for development
pip install -e .[dev,test]

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

### 3. Create a Branch

```bash
git checkout -b your-feature-name
```

Good branch names:
- `fix-reminder-timezone-bug`
- `add-discord-integration`
- `improve-installation-docs`

## Making Changes

### Writing Code

**Keep it simple:**
- Write code that's easy to read
- Add comments when things are tricky
- Follow the existing style

**Test your changes:**
```bash
# Run all tests
pytest

# Run specific tests
pytest sizzle/tests.py::TestClassName::test_method_name

# Check coverage
pytest --cov=sizzle
```

**Format your code:**
```bash
# Format everything
black sizzle/
isort sizzle/

# Check for issues
ruff check sizzle/
```

If you installed pre-commit, this happens automatically when you commit!

### Writing Tests

We use Django's test framework. Here's a quick example:

```python
from django.test import TestCase
from sizzle.models import DailyStatusReport

class MyNewFeatureTest(TestCase):
    def test_something_works(self):
        """Test that my feature does what it should"""
        # Your test here
        self.assertTrue(True)
```

Put tests in `sizzle/tests.py` or create a new test file.

### Updating Documentation

Changed how something works? Update the docs:

- **README.md** - User-facing documentation
- **Docstrings** - Explain what your code does
- **Comments** - Clarify tricky bits

## Submitting Your Changes

### 1. Commit Your Changes

Write clear commit messages:

```bash
# Good commits
git commit -m "Fix timezone bug in reminder system"
git commit -m "Add Discord integration support"
git commit -m "Update installation docs for Windows"

# Not so good
git commit -m "fix bug"
git commit -m "update stuff"
```

### 2. Push to Your Fork

```bash
git push origin your-feature-name
```

### 3. Create a Pull Request

1. Go to the [BLT repository](https://github.com/OWASP-BLT/BLT)
2. Click "New Pull Request"
3. Choose your branch
4. Fill in the template:
   - What does this change?
   - Why is it needed?
   - How did you test it?
   - Any screenshots? (for UI changes)

### 4. Wait for Review

Someone from the team will review your PR. They might:
- Approve it immediately (awesome!)
- Ask questions
- Suggest changes

Don't worry if changes are requested - it's totally normal!

## Development Tips

### Running a Test Server

```bash
# In the BLT main directory
python manage.py runserver
```

Then visit `http://localhost:8000/sizzle/`

### Testing Management Commands

```bash
# Test individual commands
python manage.py daily_checkin_reminder
python manage.py cron_send_reminders
python manage.py slack_daily_timelogs

# Run all daily tasks
python manage.py run_sizzle_daily
```

### Debugging

Add this to see detailed logs:

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'sizzle': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Working with Migrations

Made model changes?

```bash
# Create migrations
python manage.py makemigrations sizzle

# Apply them
python manage.py migrate sizzle

# Check migration status
python manage.py showmigrations sizzle
```

## Code Style

We use these tools to keep code consistent:

- **Black** - Code formatting (120 char lines)
- **isort** - Import sorting  
- **Ruff** - Fast linting

Run them before committing:

```bash
black sizzle/
isort sizzle/
ruff check sizzle/
```

Or just install pre-commit and it happens automatically!

## What Makes a Good PR?

✅ **Do:**
- Keep changes focused (one feature/fix per PR)
- Write tests for new features
- Update docs when needed
- Format your code
- Write clear commit messages
- Respond to review feedback

❌ **Don't:**
- Mix multiple unrelated changes
- Break existing functionality
- Skip writing tests
- Ignore code style

## Types of Contributions

### Bug Fixes

1. Create an issue describing the bug (if one doesn't exist)
2. Reference the issue in your PR: "Fixes #123"
3. Include steps to reproduce
4. Add a test that would have caught the bug

### New Features

1. Open a discussion or issue first - let's talk about it!
2. Wait for approval before spending lots of time
3. Keep it simple at first
4. Write comprehensive tests
5. Document how to use it

### Documentation

- Fix typos and unclear wording
- Add examples
- Improve installation instructions
- Write tutorials

All documentation improvements are welcome, no matter how small!

### Tests

More tests = fewer bugs. Add tests for:
- Uncovered code paths
- Edge cases
- Known bugs (regression tests)
- New features

## Getting Help

Stuck? Have questions? We're here to help:

- **GitHub Discussions** - Ask questions, share ideas
- **GitHub Issues** - Report bugs, request features
- **Pull Request Comments** - Ask questions in your PR

Don't be shy! We were all beginners once.

## Code of Conduct

Be nice. That's it.

More specifically:
- Be respectful and welcoming
- Be patient with newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the community

## Recognition

Contributors are awesome! We recognize contributions by:
- Listing you in our contributors
- Thanking you in release notes
- Celebrating your PRs on social media (with your permission)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Not sure about something? Just ask! Open an issue with your question or start a discussion.

---

Thanks for contributing to BLT Sizzle! 🎉
