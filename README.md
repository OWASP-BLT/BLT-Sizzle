# 🔥 BLT Sizzle — Async Daily Check-in App

<div align="center">

[![Deploy to Cloudflare Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/OWASP-BLT/BLT-Sizzle)
[![License](https://img.shields.io/badge/license-OWASP%20BLT-blue.svg)](#-license)
[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-orange.svg)](https://workers.cloudflare.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

**A lightweight, secure, async-first daily check-in app built on Cloudflare Workers.**  
Track progress, surface blockers, and keep your team aligned — without another meeting.

</div>

---

## 📑 Table of Contents

- [Features](#-features)
- [Quick Deploy](#-quick-deploy)
- [Prerequisites](#-prerequisites)
- [Manual Setup](#-manual-setup)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Architecture](#-architecture)
- [Database Schema](#-database-schema)
- [Scheduled Notifications](#-scheduled-notifications)
- [Development](#-development)
- [Roadmap](#-roadmap)
- [Security](#-security)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 **Daily Check-ins** | Document previous work, today's plan, and any blockers |
| 😊 **Mood Tracking** | Express how you're feeling with emoji selections |
| 🔁 **Auto Pre-fill** | Yesterday's plans automatically populate as today's accomplished work |
| 💬 **Slack Integration** | Daily reminders via Slack with a direct link to your check-in form |
| 📧 **Email Reminders** | Optional email notifications for check-in reminders |
| 🔒 **Encrypted Storage** | All sensitive data encrypted before being stored in Cloudflare D1 |
| ⏰ **Customizable Notifications** | Set your preferred reminder time and timezone |
| 🎨 **Beautiful UI** | Clean, modern interface with gradient design |

> **⚠️ Security Note:** The current implementation uses base64 encoding as a placeholder for encryption.
> For production use with sensitive data, implement proper AES-GCM encryption via the Web Crypto API.
> See [SECURITY.md](SECURITY.md) for details.

---

## 🚀 Quick Deploy

[![Deploy to Cloudflare Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/OWASP-BLT/BLT-Sizzle)

---

## 📋 Prerequisites

- [Cloudflare Account](https://dash.cloudflare.com/sign-up)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/) installed
- Node.js 16.13 or later

---

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

### 5. Create KV Namespace *(Optional)*

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

---

## 🔧 Configuration

### Slack Integration

1. Go to your Slack workspace settings
2. Create an [Incoming Webhook](https://api.slack.com/messaging/webhooks)
3. Copy the webhook URL
4. In the app, go to **Settings** and paste the webhook URL
5. Set your preferred notification time and timezone
6. Click **Test** to confirm it works!

### Email Notifications

Email notifications require an email service provider. Configure these environment variables:

| Variable | Description |
|---|---|
| `EMAIL_API_KEY` | Your email service API key |
| `EMAIL_FROM` | Sender email address |

**Supported providers:** SendGrid · Mailgun · AWS SES · Postmark

---

## 📱 Usage

### Daily Check-in

1. Visit your deployed app URL
2. Fill out the form:
   - **Previous Work** — What you accomplished (auto-filled from last check-in)
   - **Today's Plan** — What you plan to do today
   - **Blockers** — Any obstacles or challenges
   - **Mood** — Select an emoji that represents how you feel
3. Submit and you're done! ✅

### Notifications

The app sends a reminder at your configured time with a direct link to the check-in form.

---

## 🛣️ API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Main check-in form |
| `GET` | `/settings` | Notification settings page |
| `POST` | `/api/checkin` | Submit a check-in |
| `GET` | `/api/checkin/latest` | Get latest check-in for pre-filling |
| `GET` | `/api/settings` | Get user settings |
| `POST` | `/api/settings` | Save user settings |
| `POST` | `/api/notification/test` | Send a test notification |

---

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

---

## 📊 Database Schema

### Users Table

| Column | Description |
|---|---|
| `user_id` | Unique user identifier |
| `email` | Optional email for notifications |
| `slack_webhook_url` | Slack webhook URL |
| `notification_time` | Preferred reminder time |
| `timezone` | User's timezone |
| `email_notifications` | Email notification preference |

### Check-ins Table

| Column | Description |
|---|---|
| `user_id` | Reference to user |
| `encrypted_previous_work` | Encrypted previous accomplishments |
| `encrypted_today_plan` | Encrypted today's plans |
| `encrypted_blockers` | Encrypted blockers/challenges |
| `mood` | Emoji representing mood |
| `checkin_date` | Date of check-in |

---

## 🔄 Scheduled Notifications

To enable automatic daily notifications, add a cron trigger to your `wrangler.toml`:

```toml
[triggers]
crons = ["0 9 * * *"]  # Run at 9 AM UTC daily
```

Then implement the scheduled handler in your worker to check user notification times and send reminders.

---

## 🧪 Development

### Local Development

```bash
wrangler dev
```

This starts a local development server at `http://localhost:8787`.

### Testing

1. Visit `http://localhost:8787` in your browser
2. Fill out a check-in form
3. Check the settings page
4. Test Slack notifications (requires a valid webhook URL)

---

## 🗺️ Roadmap

Everything that still needs to be built — contributions welcome!

- [ ] 🔄 **Async Check-ins** — Allow team members to post updates whenever it suits them instead of synchronizing schedules. Removes awkward silences, late apologies, and calendar clutter while respecting deep work and timezones.
- [ ] 🤖 **AI-generated Summaries** — Automatically summarize updates daily, weekly, or on custom intervals. Highlight key wins, blockers, and focus areas for managers.
- [ ] 👥 **Per-group Summaries** — Support different summaries for different teams or roles (e.g., engineering vs design) to ensure context-specific insights.
- [ ] 🏠 **Persistent Check-in Rooms** — Keep daily rooms open so team members can post updates without creating new meetings. Make historical updates easy to browse and comment on.
- [ ] 🖼️ **Rich Media Support** — Enable uploads of images, GIFs, and short videos alongside text updates for more engaging check-ins.
- [ ] 🎨 **Customizable Questions & Prompts** — Allow admins to define prompts for check-ins with color coding or emoji prefixes to guide consistent updates.
- [ ] 💬 **Comments & Reactions** — Enable team members to react to updates or add comments asynchronously to encourage discussion and recognition.
- [ ] 📦 **Bulk Export Options** — Allow exporting check-ins to CSV, JSON, or PDF formats for reporting or archiving purposes.
- [ ] 🎥 **Video and Voice Updates** — Support optional short video or audio clips for check-ins while keeping text-only as an alternative.
- [ ] 🔗 **Integration with Project Tools** — Connect with GitHub, Jira, Trello, or similar platforms to link updates with tasks and tickets.
- [ ] 🌟 **Team Mood Tracking & Kudos** — Optional mood tracking and peer recognition features. Include icebreakers or wellness prompts to boost engagement.
- [ ] 🌍 **Timezone-aware Scheduling** — Ensure prompts and reminders respect each team member's local time in a distributed setup.
- [ ] 🏃 **Agile Workflow Support** — Provide templates for Scrum, Kanban, or other agile methodologies. Include retrospective tools if needed.
- [ ] 🔐 **Private vs Public Check-ins** — Allow check-ins to be visible to the whole team or restricted to managers for sensitive updates.
- [ ] 📈 **Participation Analytics** — Track who submits updates and optionally provide statistics for engagement or follow-ups.
- [ ] 🆓 **Free-tier Friendly Limits** — Set limitations on team size or features for a free/open-source plan to reduce server costs and encourage adoption.

---

## 🔒 Security

- All user data (previous work, plans, blockers) is encrypted using AES-GCM before storage
- Database uses Cloudflare D1 with built-in security
- No personally identifiable information is stored without encryption
- User IDs are randomly generated and stored in browser localStorage
- HTTPS enforced by default on Cloudflare Workers

See [SECURITY.md](SECURITY.md) for full details.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and feel free to open a Pull Request.

---

## 🐛 Troubleshooting

<details>
<summary><strong>Database not initializing</strong></summary>

- Ensure the D1 database is created and the ID is correct in `wrangler.toml`
- Re-run the schema manually: `wrangler d1 execute checkin-db --file=./schema.sql`

</details>

<details>
<summary><strong>Slack notifications not working</strong></summary>

- Verify the webhook URL is correct
- Test the webhook URL directly with curl
- Check Cloudflare Worker logs: `wrangler tail`

</details>

<details>
<summary><strong>Data not persisting</strong></summary>

- Check the D1 database binding in `wrangler.toml`
- Verify database initialization ran successfully
- Check Worker logs for errors

</details>

---

## 📄 License

This project is part of [OWASP BLT](https://github.com/OWASP-BLT) and follows the same license terms.

---

<div align="center">Made with ❤️ by <a href="https://github.com/OWASP-BLT">OWASP BLT</a></div>
