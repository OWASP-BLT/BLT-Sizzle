# BLT Sizzle - Daily Check-in App 📝

A simple, secure daily check-in application built as a Cloudflare Python Worker. Track your progress, plan your day, and share your mood with your team via Slack or email notifications.

## ✨ Features

- **Daily Check-ins**: Document what you did previously, plan for today, and note any blockers
- **Mood Tracking**: Express how you're feeling with emoji selections
- **Auto Pre-fill**: Your previous day's plans automatically populate as today's accomplished work
- **Slack Integration**: Get daily reminders via Slack with a direct link to your check-in form
- **Email Reminders**: Optional email notifications for check-in reminders
- **Encrypted Storage**: All sensitive data is encrypted before being stored in Cloudflare D1 database
- **Customizable Notifications**: Set your preferred reminder time and timezone
- **Beautiful UI**: Clean, modern interface with gradient design

## 🚀 Quick Deploy to Cloudflare Workers

[![Deploy to Cloudflare Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/OWASP-BLT/BLT-Sizzle)

## 📋 Prerequisites

- [Cloudflare Account](https://dash.cloudflare.com/sign-up)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/) installed
- Node.js 16.13 or later

## 🛠️ Manual Setup

### 1. Install Wrangler

```bash
npm install -g wrangler
```

### 2. Login to Cloudflare

```bash
wrangler login
```

### 3. Create D1 Database

```bash
wrangler d1 create checkin-db
```

Note the database ID from the output and update it in `wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "checkin-db"
database_id = "your-database-id-here"
```

### 4. Initialize Database Schema

```bash
wrangler d1 execute checkin-db --file=./schema.sql
```

### 5. Create KV Namespace (Optional)

```bash
wrangler kv:namespace create "KV"
```

Update the KV namespace ID in `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "KV"
id = "your-kv-id-here"
```

### 6. Set Encryption Key

Generate a secure encryption key and add it to your `wrangler.toml`:

```toml
[vars]
ENCRYPTION_KEY = "your-secure-random-key-here"
```

Or use secrets for production:

```bash
wrangler secret put ENCRYPTION_KEY
```

### 7. Deploy

```bash
wrangler deploy
```

Your app will be live at: `https://blt-sizzle-checkin.your-subdomain.workers.dev`

## 🔧 Configuration

### Slack Integration

1. Go to your Slack workspace settings
2. Create an [Incoming Webhook](https://api.slack.com/messaging/webhooks)
3. Copy the webhook URL
4. In the app, go to Settings and paste the webhook URL
5. Set your preferred notification time and timezone
6. Test the notification to ensure it works!

### Email Notifications

Email notifications require additional setup with an email service provider. Configure your email service settings in the worker environment variables:

- `EMAIL_API_KEY`: Your email service API key
- `EMAIL_FROM`: Sender email address

Supported providers:
- SendGrid
- Mailgun
- AWS SES
- Postmark

## 📱 Usage

### Daily Check-in

1. Visit your deployed app URL
2. Fill out the form:
   - **Previous Work**: What you accomplished (auto-filled from last check-in)
   - **Today's Plan**: What you plan to do today
   - **Blockers**: Any obstacles or challenges
   - **Mood**: Select an emoji that represents how you feel
3. Submit and you're done!

### Notifications

The app will send you a reminder at your configured time with a link directly to the check-in form. Simply click the link and fill out your check-in!

## 🔒 Security

- All user data (previous work, plans, blockers) is encrypted using AES-GCM before storage
- Database uses Cloudflare D1 with built-in security
- No personally identifiable information is stored without encryption
- User IDs are randomly generated and stored in browser localStorage
- HTTPS enforced by default on Cloudflare Workers

## 🏗️ Architecture

```
┌─────────────────┐
│  Browser Client │
│  (HTML/JS/CSS)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Python Worker  │
│  (index.py)     │
└────────┬────────┘
         │
         ├──────────────┐
         ▼              ▼
┌──────────────┐  ┌──────────────┐
│ D1 Database  │  │ Slack/Email  │
│  (Encrypted) │  │ Notifications│
└──────────────┘  └──────────────┘
```

## 📊 Database Schema

### Users Table
- `user_id`: Unique user identifier
- `email`: Optional email for notifications
- `slack_webhook_url`: Slack webhook URL
- `notification_time`: Preferred reminder time
- `timezone`: User's timezone
- `email_notifications`: Email notification preference

### Check-ins Table
- `user_id`: Reference to user
- `encrypted_previous_work`: Encrypted previous accomplishments
- `encrypted_today_plan`: Encrypted today's plans
- `encrypted_blockers`: Encrypted blockers/challenges
- `mood`: Emoji representing mood
- `checkin_date`: Date of check-in

## 🛣️ API Endpoints

- `GET /` - Main check-in form
- `GET /settings` - Notification settings page
- `POST /api/checkin` - Submit a check-in
- `GET /api/checkin/latest` - Get latest check-in for pre-filling
- `GET /api/settings` - Get user settings
- `POST /api/settings` - Save user settings
- `POST /api/notification/test` - Send a test notification

## 🔄 Scheduled Notifications

To enable automatic daily notifications, add a cron trigger to your `wrangler.toml`:

```toml
[triggers]
crons = ["0 9 * * *"]  # Run at 9 AM UTC daily
```

Then implement the scheduled handler in your worker to check user notification times and send reminders.

## 🧪 Development

### Local Development

```bash
wrangler dev
```

This starts a local development server at `http://localhost:8787`

### Testing

1. Visit `http://localhost:8787` in your browser
2. Fill out a check-in form
3. Check the settings page
4. Test Slack notifications (requires valid webhook URL)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is part of OWASP BLT and follows the same license terms.

## 🐛 Troubleshooting

### Database not initializing
- Ensure D1 database is created and ID is correct in `wrangler.toml`
- Run the schema.sql manually: `wrangler d1 execute checkin-db --file=./schema.sql`

### Slack notifications not working
- Verify webhook URL is correct
- Test the webhook URL directly with curl
- Check Cloudflare Worker logs: `wrangler tail`

### Data not persisting
- Check D1 database binding in `wrangler.toml`
- Verify database initialization ran successfully
- Check Worker logs for errors

## 📞 Support

For issues and questions, please open an issue on GitHub or contact the OWASP BLT team.

---

Made with ❤️ by OWASP BLT
