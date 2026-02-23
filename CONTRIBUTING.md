# Contributing to BLT Sizzle Check-in App

Thank you for your interest in contributing to BLT Sizzle! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Feature Requests](#feature-requests)
- [Bug Reports](#bug-reports)

## Code of Conduct

This project follows the OWASP Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/BLT-Sizzle.git
   cd BLT-Sizzle
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/OWASP-BLT/BLT-Sizzle.git
   ```

## Development Setup

### Prerequisites

- Node.js 16.13 or later
- Cloudflare account (free tier works)
- Git

### Setup Steps

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Login to Cloudflare**:
   ```bash
   npx wrangler login
   ```

3. **Create local D1 database**:
   ```bash
   npx wrangler d1 create checkin-db-dev
   npx wrangler d1 execute checkin-db-dev --file=./schema.sql
   ```

4. **Update wrangler.toml** with your database ID

5. **Start development server**:
   ```bash
   npm run dev
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- 🐛 **Bug fixes**
- ✨ **New features**
- 📝 **Documentation improvements**
- 🎨 **UI/UX enhancements**
- 🧪 **Tests**
- 🌐 **Translations** (future)
- ♿ **Accessibility improvements**

### Contribution Workflow

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes** following our coding standards

3. **Test your changes** thoroughly

4. **Commit your changes** with clear messages:
   ```bash
   git add .
   git commit -m "Add feature: description of feature"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## Coding Standards

### Python Code

Follow PEP 8 style guide:

```python
# Good
async def handle_checkin(request, env):
    """Handle check-in submission"""
    data = await request.json()
    user_id = data.get('userId')
    
    if not user_id:
        return error_response("User ID required")
    
    # Process data
    result = await save_checkin(user_id, data)
    return success_response(result)


# Avoid
async def handle_checkin(request,env):
    data=await request.json()
    userId=data.get('userId')
    if not userId:return error_response("User ID required")
    result=await save_checkin(userId,data)
    return success_response(result)
```

### JavaScript Code

Use modern JavaScript (ES6+):

```javascript
// Good
const loadPreviousCheckin = async () => {
    const loading = document.getElementById('loading');
    loading.style.display = 'block';
    
    try {
        const response = await fetch(`/api/checkin/latest?userId=${userId}`);
        if (response.ok) {
            const data = await response.json();
            prefillForm(data);
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        loading.style.display = 'none';
    }
};

// Avoid
function loadPreviousCheckin() {
    var loading = document.getElementById('loading');
    loading.style.display = 'block';
    fetch('/api/checkin/latest?userId=' + userId).then(function(response) {
        return response.json();
    }).then(function(data) {
        prefillForm(data);
        loading.style.display = 'none';
    });
}
```

### HTML/CSS

- Use semantic HTML5 elements
- Keep CSS organized and commented
- Use CSS variables for colors and spacing
- Ensure responsive design
- Follow BEM naming convention for CSS classes

```html
<!-- Good -->
<section class="checkin-form">
    <h1 class="checkin-form__title">Daily Check-in</h1>
    <form class="checkin-form__form">
        <div class="form-group">
            <label for="todayPlan" class="form-group__label">
                What do you plan to do today?
            </label>
            <textarea id="todayPlan" class="form-group__input"></textarea>
        </div>
    </form>
</section>
```

### Documentation

- Use clear, concise language
- Include code examples
- Keep documentation up-to-date with code changes
- Use Markdown formatting

## Testing Guidelines

### Required Tests

All contributions should include tests:

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test API endpoints
3. **Manual Testing**: Test in browser

### Running Tests

```bash
# Start local server
npm run dev

# In another terminal, run tests
python tests/test_api.py
```

### Writing Tests

```python
# Example test
def test_checkin_submission():
    """Test check-in submission endpoint"""
    # Arrange
    data = {
        "userId": "test_user",
        "todayPlan": "Test plan",
        "mood": "😊"
    }
    
    # Act
    response = requests.post(f"{BASE_URL}/api/checkin", json=data)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["success"] == True
    print("✓ Check-in submission test passed")
```

## Pull Request Process

### Before Submitting

- [ ] Code follows our style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up-to-date with main

### PR Template

Use this template for your PR description:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
Describe how you tested your changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
- [ ] All tests pass
```

### Review Process

1. Maintainer reviews code
2. Feedback provided if needed
3. Changes requested or approved
4. Once approved, PR is merged

### After Merge

- Your branch will be deleted
- Update your local repository:
  ```bash
  git checkout main
  git pull upstream main
  ```

## Feature Requests

We love feature ideas! To request a feature:

1. **Check existing issues** to avoid duplicates
2. **Open a new issue** with:
   - Clear title
   - Detailed description
   - Use case/motivation
   - Proposed solution (if any)
   - Examples/mockups (if applicable)

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Problem/Use Case**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Screenshots, examples, etc.
```

## Bug Reports

Found a bug? Help us fix it!

### Before Reporting

1. **Check existing issues** for duplicates
2. **Test in latest version**
3. **Try to reproduce** consistently

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- Browser: [e.g., Chrome 98]
- OS: [e.g., macOS 12.1]
- Device: [e.g., Desktop, iPhone 12]

**Screenshots**
Add screenshots if applicable

**Additional Context**
Logs, error messages, etc.
```

## Areas to Contribute

### High Priority

- 🔒 Enhanced encryption (Web Crypto API implementation)
- 🔐 Authentication system (OAuth integration)
- 📊 Analytics dashboard
- 🌍 Internationalization (i18n)
- ♿ Accessibility improvements

### Good First Issues

Look for issues labeled `good-first-issue`:
- Documentation improvements
- UI tweaks
- Simple bug fixes
- Adding tests

### Ideas for Enhancement

- **Export Data**: Export check-ins as CSV/JSON
- **Analytics**: View check-in history and trends
- **Team View**: See team check-ins
- **Custom Fields**: Add custom check-in fields
- **Integrations**: More platforms (Discord, Teams, etc.)
- **Mobile App**: React Native or Flutter app
- **AI Insights**: Analyze mood trends, suggest improvements
- **Reminders**: More flexible reminder options

## Development Tips

### Useful Commands

```bash
# View logs
npm run tail

# Query database
npx wrangler d1 execute checkin-db-dev --command "SELECT * FROM users"

# Check for updates
npm update

# Format code (if you add a formatter)
npm run format
```

### Debugging

1. **Use console.log** liberally
2. **Check Worker logs**: `npm run tail`
3. **Test locally first**: `npm run dev`
4. **Use browser DevTools**

### Common Issues

**Issue**: Database not found
**Solution**: Recreate database and run schema.sql

**Issue**: Module import errors
**Solution**: Check file paths and ensure proper structure

**Issue**: CORS errors
**Solution**: Check request headers and response headers

## Community

- **GitHub Issues**: For bugs and features
- **Pull Requests**: For code contributions
- **Discussions**: For questions and ideas

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in the README

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (Apache 2.0).

## Questions?

Feel free to:
- Open an issue for questions
- Reach out to maintainers
- Join our community discussions

---

Thank you for contributing to BLT Sizzle! Your efforts help make this project better for everyone. 🎉
