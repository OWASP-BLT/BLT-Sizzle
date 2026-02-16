# Testing Guide

This guide covers how to test the BLT Sizzle Check-in application locally and in production.

## Local Testing

### Prerequisites

1. Install Wrangler CLI: `npm install`
2. Login to Cloudflare: `npx wrangler login`
3. Create a local D1 database for testing

### Setup Local Environment

```bash
# Install dependencies
npm install

# Create local D1 database
npx wrangler d1 create checkin-db-local

# Initialize database schema
npx wrangler d1 execute checkin-db-local --file=./schema.sql
```

### Start Local Development Server

```bash
npm run dev
```

This starts the worker at `http://localhost:8787`

### Manual Testing Workflow

#### 1. Test Check-in Form

1. Open `http://localhost:8787` in your browser
2. Fill out the form:
   - Previous work: "Completed API integration"
   - Today's plan: "Work on frontend components"
   - Blockers: "None"
   - Mood: Select 😊
3. Click "Submit Check-in"
4. Verify success message appears

#### 2. Test Auto Pre-fill

1. Refresh the page
2. Verify "Previous work" is now pre-filled with "Work on frontend components"
3. This confirms data persistence and pre-fill logic

#### 3. Test Settings Page

1. Click "⚙️ Notification Settings"
2. Fill out settings:
   - Email: your.email@example.com
   - Reminder Time: 09:00
   - Timezone: America/New_York
   - Check "Send email reminders"
3. Add a Slack webhook URL (optional - see below)
4. Click "Save Settings"
5. Verify success message

#### 4. Test Slack Integration (Optional)

**Setup test Slack webhook:**

1. Go to https://api.slack.com/messaging/webhooks
2. Create an incoming webhook
3. Copy the webhook URL
4. Paste it in the settings page
5. Click "Test Notification"
6. Check your Slack channel for the notification

#### 5. Test API Endpoints

Using curl or similar:

```bash
# Test check-in submission
curl -X POST http://localhost:8787/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test_user_123",
    "previousWork": "Completed testing",
    "todayPlan": "Write documentation",
    "blockers": "None",
    "mood": "😊"
  }'

# Test get latest check-in
curl "http://localhost:8787/api/checkin/latest?userId=test_user_123"

# Test get settings
curl "http://localhost:8787/api/settings?userId=test_user_123"

# Test save settings
curl -X POST http://localhost:8787/api/settings \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test_user_123",
    "email": "test@example.com",
    "notificationTime": "09:00",
    "timezone": "UTC",
    "slackWebhookUrl": "",
    "emailNotifications": 0
  }'
```

### Database Testing

#### Check Database Contents

```bash
# View all users
npx wrangler d1 execute checkin-db-local --command "SELECT * FROM users"

# View all check-ins
npx wrangler d1 execute checkin-db-local --command "SELECT * FROM checkins"

# Count check-ins per user
npx wrangler d1 execute checkin-db-local --command "
  SELECT user_id, COUNT(*) as count 
  FROM checkins 
  GROUP BY user_id
"

# View recent check-ins with mood
npx wrangler d1 execute checkin-db-local --command "
  SELECT user_id, mood, checkin_date, created_at 
  FROM checkins 
  ORDER BY created_at DESC 
  LIMIT 10
"
```

#### Test Encryption

```bash
# View encrypted data
npx wrangler d1 execute checkin-db-local --command "
  SELECT user_id, 
         encrypted_previous_work, 
         encrypted_today_plan,
         encrypted_blockers
  FROM checkins 
  LIMIT 1
"

# Verify data is encrypted (should see base64 strings, not plain text)
```

### View Logs

```bash
# View real-time logs
npm run tail

# Or with more detail
npx wrangler tail --format pretty
```

## Testing Scheduled Notifications

### Manual Trigger Test

Since cron triggers don't work in local development, you can test the notification logic:

```bash
# Create a test script
cat > test_scheduler.py << 'EOF'
import asyncio
from src.scheduler import handle_scheduled

class MockEnv:
    def __init__(self):
        self.ENCRYPTION_KEY = "test-key"
        self.WORKER_HOST = "localhost:8787"
        # Add mock DB here

class MockEvent:
    pass

async def test():
    env = MockEnv()
    event = MockEvent()
    await handle_scheduled(event, env)

asyncio.run(test())
EOF

# Run test
python test_scheduler.py
```

## Production Testing

### Deploy to Staging

```bash
# Deploy to staging environment
npx wrangler deploy --config wrangler.staging.toml
```

### Production Smoke Tests

After deploying to production:

#### 1. Health Check

```bash
curl https://your-worker.workers.dev/
# Should return HTML with "Daily Check-in" title
```

#### 2. API Endpoint Tests

```bash
# Test with production URL
curl -X POST https://your-worker.workers.dev/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "prod_test_user",
    "previousWork": "Production test",
    "todayPlan": "Verify deployment",
    "blockers": "None",
    "mood": "😊"
  }'
```

#### 3. Monitor Logs

```bash
# View production logs
npx wrangler tail --env production
```

#### 4. Test Scheduled Notifications

Wait for the next cron trigger (every hour) and verify:
- Check Cloudflare dashboard for cron execution logs
- Verify Slack notifications are sent
- Check email delivery (if configured)

## Automated Testing

### Create Test Suite

```bash
# Create tests directory
mkdir -p tests

# Create test file
cat > tests/test_api.py << 'EOF'
import requests
import json

BASE_URL = "http://localhost:8787"

def test_checkin_submission():
    """Test check-in submission"""
    data = {
        "userId": "test_user",
        "previousWork": "Test work",
        "todayPlan": "Test plan",
        "blockers": "None",
        "mood": "😊"
    }
    response = requests.post(f"{BASE_URL}/api/checkin", json=data)
    assert response.status_code == 200
    assert response.json()["success"] == True
    print("✓ Check-in submission test passed")

def test_get_latest_checkin():
    """Test getting latest check-in"""
    response = requests.get(f"{BASE_URL}/api/checkin/latest?userId=test_user")
    assert response.status_code == 200
    data = response.json()
    assert "todayPlan" in data
    print("✓ Get latest check-in test passed")

def test_settings():
    """Test settings save and retrieve"""
    settings = {
        "userId": "test_user",
        "email": "test@example.com",
        "notificationTime": "09:00",
        "timezone": "UTC",
        "slackWebhookUrl": "",
        "emailNotifications": 0
    }
    response = requests.post(f"{BASE_URL}/api/settings", json=settings)
    assert response.status_code == 200
    
    # Retrieve settings
    response = requests.get(f"{BASE_URL}/api/settings?userId=test_user")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    print("✓ Settings test passed")

if __name__ == "__main__":
    test_checkin_submission()
    test_get_latest_checkin()
    test_settings()
    print("\n✓ All tests passed!")
EOF
```

### Run Tests

```bash
# Install requests library
pip install requests

# Start local server in one terminal
npm run dev

# Run tests in another terminal
python tests/test_api.py
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Install Apache Bench
# Ubuntu: sudo apt-get install apache2-utils
# Mac: brew install httpd

# Test check-in endpoint (100 requests, 10 concurrent)
ab -n 100 -c 10 -p checkin.json -T application/json \
  http://localhost:8787/api/checkin

# Create checkin.json
cat > checkin.json << 'EOF'
{
  "userId": "load_test_user",
  "previousWork": "Load testing",
  "todayPlan": "More testing",
  "blockers": "None",
  "mood": "😊"
}
EOF
```

### Load Testing with k6

```bash
# Install k6: https://k6.io/docs/getting-started/installation/

# Create load test script
cat > loadtest.js << 'EOF'
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 10,
  duration: '30s',
};

export default function() {
  let payload = JSON.stringify({
    userId: `user_${__VU}_${__ITER}`,
    previousWork: 'Load test',
    todayPlan: 'More testing',
    blockers: 'None',
    mood: '😊'
  });

  let params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  let res = http.post('http://localhost:8787/api/checkin', payload, params);
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response has success': (r) => r.json('success') === true,
  });
}
EOF

# Run load test
k6 run loadtest.js
```

## Security Testing

### Test Encryption

```bash
# Submit data and verify it's encrypted in database
curl -X POST http://localhost:8787/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "security_test",
    "previousWork": "SENSITIVE_DATA_TEST",
    "todayPlan": "SECRET_PLAN",
    "blockers": "CONFIDENTIAL",
    "mood": "😊"
  }'

# Check database - data should NOT be in plain text
npx wrangler d1 execute checkin-db-local --command "
  SELECT * FROM checkins WHERE user_id = 'security_test'
"
```

### Test SQL Injection Protection

```bash
# Try SQL injection
curl -X POST http://localhost:8787/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test'; DROP TABLE users; --",
    "previousWork": "Test",
    "todayPlan": "Test",
    "blockers": "None",
    "mood": "😊"
  }'

# Verify tables still exist
npx wrangler d1 execute checkin-db-local --command "
  SELECT name FROM sqlite_master WHERE type='table'
"
```

## Troubleshooting Tests

### Common Issues

**1. Database not found**
```bash
# Recreate database
npx wrangler d1 create checkin-db-local
npx wrangler d1 execute checkin-db-local --file=./schema.sql
```

**2. Port already in use**
```bash
# Kill process on port 8787
lsof -ti:8787 | xargs kill -9

# Or use different port
npx wrangler dev --port 8788
```

**3. Module import errors**
```bash
# Ensure you're in the correct directory
cd /path/to/BLT-Sizzle
```

## Test Checklist

Before deploying to production:

- [ ] Local development server starts without errors
- [ ] Check-in form submits successfully
- [ ] Data persists and pre-fills correctly
- [ ] Settings save and load correctly
- [ ] Slack test notification works
- [ ] Database encryption is working
- [ ] API endpoints return correct responses
- [ ] Error handling works properly
- [ ] Logs don't contain sensitive data
- [ ] Load testing shows acceptable performance
- [ ] Security tests pass

## Continuous Testing

Set up automated testing in CI/CD:

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm run test  # Add test script to package.json
```

---

Happy testing! 🧪
