# Deployment Guide

## Step-by-Step Deployment to Cloudflare Workers

### 1. Prerequisites Check

Ensure you have:
- ✅ Cloudflare account (free tier works!)
- ✅ Node.js installed (v16.13+)
- ✅ Git installed

### 2. Install Dependencies

```bash
npm install
```

This installs Wrangler CLI locally.

### 3. Authenticate with Cloudflare

```bash
npx wrangler login
```

This opens your browser for authentication.

### 4. Create and Configure D1 Database

```bash
npm run db:create
```

**Important**: Copy the database ID from the output and update `wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "checkin-db"
database_id = "PASTE_YOUR_DATABASE_ID_HERE"
```

### 5. Initialize Database Schema

```bash
npm run db:init
```

This creates the necessary tables.

### 6. Set Encryption Key

Generate a random key:
```bash
# On Linux/Mac
openssl rand -base64 32

# On Windows PowerShell
[Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
```

Set it as a secret:
```bash
npx wrangler secret put ENCRYPTION_KEY
# Paste your generated key when prompted
```

Or add to `wrangler.toml` for development:
```toml
[vars]
ENCRYPTION_KEY = "your-generated-key"
```

### 7. (Optional) Create KV Namespace

For session storage:
```bash
npx wrangler kv:namespace create "KV"
```

Update the ID in `wrangler.toml`.

### 8. Deploy!

```bash
npm run deploy
```

Your app is now live! 🎉

The deployment will output a URL like:
```
https://blt-sizzle-checkin.your-subdomain.workers.dev
```

### 9. Configure Slack Integration

1. Visit your deployed app URL
2. Click on "⚙️ Notification Settings"
3. Create a Slack webhook:
   - Go to https://api.slack.com/messaging/webhooks
   - Create a new webhook for your workspace
   - Copy the webhook URL
4. Paste the webhook URL in the settings
5. Set your notification time and timezone
6. Click "Test Notification" to verify it works!

## Development Workflow

### Local Development

```bash
npm run dev
```

Visit http://localhost:8787

### View Logs

```bash
npm run tail
```

### Query Database

```bash
npm run db:query "SELECT * FROM users LIMIT 5"
```

## Troubleshooting

### Error: Database not found
- Make sure you ran `npm run db:create`
- Verify the database ID in `wrangler.toml` is correct

### Error: Worker exceeded CPU time limit
- This shouldn't happen with normal usage
- Check for infinite loops in custom modifications

### Slack webhook not working
- Test the URL directly with curl:
  ```bash
  curl -X POST -H 'Content-Type: application/json' \
    -d '{"text":"Test"}' \
    YOUR_WEBHOOK_URL
  ```

### Database table not found
- Ensure you ran `npm run db:init`
- Check if schema.sql was applied: `npm run db:query "SELECT name FROM sqlite_master WHERE type='table'"`

## Environment Variables

Production secrets should be set using:
```bash
npx wrangler secret put SECRET_NAME
```

Available secrets:
- `ENCRYPTION_KEY` - For encrypting user data
- `EMAIL_API_KEY` - For email notifications (optional)
- `EMAIL_FROM` - Sender email address (optional)

## Custom Domain

To use a custom domain:

1. Add to `wrangler.toml`:
```toml
routes = [
  { pattern = "checkin.yourdomain.com", custom_domain = true }
]
```

2. Deploy:
```bash
npm run deploy
```

3. Cloudflare will automatically configure DNS!

## Cost Estimation

With Cloudflare's free tier:
- 100,000 requests/day
- 10 GB D1 database storage
- Unlimited bandwidth

For most teams, this is **completely free**! 🎉

For larger teams, costs are minimal:
- $5/month for 10M requests
- $0.75/month for 1GB D1 storage

## Next Steps

1. Invite your team members
2. Set up scheduled notifications (see README)
3. Customize the UI colors in `src/index.py`
4. Add custom emoji options
5. Export check-in data for analytics

---

Need help? Open an issue on GitHub!
