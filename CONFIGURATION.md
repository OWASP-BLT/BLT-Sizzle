# Example Wrangler Configurations

This file contains example configurations for different deployment scenarios.

## Development Configuration (wrangler.dev.toml)

```toml
name = "blt-sizzle-checkin-dev"
main = "src/index.py"
compatibility_date = "2024-01-01"
compatibility_flags = ["python_workers"]

# Development triggers (every 5 minutes for testing)
[triggers]
crons = ["*/5 * * * *"]

# Development D1 Database
[[d1_databases]]
binding = "DB"
database_name = "checkin-db-dev"
database_id = "your-dev-database-id"

# Development KV namespace
[[kv_namespaces]]
binding = "KV"
id = "your-dev-kv-id"

# Development environment variables (not secrets)
[vars]
ENCRYPTION_KEY = "dev-encryption-key-not-for-production"
WORKER_HOST = "blt-sizzle-checkin-dev.your-subdomain.workers.dev"
DEBUG = "true"
```

## Production Configuration (wrangler.toml)

```toml
name = "blt-sizzle-checkin"
main = "src/index.py"
compatibility_date = "2024-01-01"
compatibility_flags = ["python_workers"]

# Production triggers (every hour)
[triggers]
crons = ["0 * * * *"]

# Production D1 Database
[[d1_databases]]
binding = "DB"
database_name = "checkin-db"
database_id = "your-prod-database-id"

# Production KV namespace
[[kv_namespaces]]
binding = "KV"
id = "your-prod-kv-id"

# Production environment variables
[vars]
WORKER_HOST = "checkin.yourdomain.com"
DEBUG = "false"

# Note: Use secrets for sensitive values in production
# wrangler secret put ENCRYPTION_KEY
# wrangler secret put EMAIL_API_KEY
```

## Staging Configuration (wrangler.staging.toml)

```toml
name = "blt-sizzle-checkin-staging"
main = "src/index.py"
compatibility_date = "2024-01-01"
compatibility_flags = ["python_workers"]

# Staging triggers (every 15 minutes)
[triggers]
crons = ["*/15 * * * *"]

# Staging D1 Database
[[d1_databases]]
binding = "DB"
database_name = "checkin-db-staging"
database_id = "your-staging-database-id"

# Staging KV namespace
[[kv_namespaces]]
binding = "KV"
id = "your-staging-kv-id"

# Staging environment variables
[vars]
WORKER_HOST = "blt-sizzle-checkin-staging.your-subdomain.workers.dev"
DEBUG = "true"
```

## Custom Domain Configuration

Add routes to your wrangler.toml:

```toml
# For custom domain
routes = [
  { pattern = "checkin.yourdomain.com", custom_domain = true }
]

# Or for zone/route based routing
route = "checkin.yourdomain.com/*"
zone_id = "your-cloudflare-zone-id"
```

## Email Provider Configurations

### SendGrid

```toml
[vars]
EMAIL_PROVIDER = "sendgrid"
EMAIL_FROM = "noreply@yourdomain.com"

# Set as secret:
# wrangler secret put EMAIL_API_KEY
```

### Mailgun

```toml
[vars]
EMAIL_PROVIDER = "mailgun"
EMAIL_DOMAIN = "mg.yourdomain.com"
EMAIL_FROM = "noreply@yourdomain.com"

# Set as secret:
# wrangler secret put EMAIL_API_KEY
```

## Multiple Environments Management

Deploy to different environments:

```bash
# Deploy to development
wrangler deploy --config wrangler.dev.toml

# Deploy to staging
wrangler deploy --config wrangler.staging.toml

# Deploy to production
wrangler deploy
```

## Environment-Specific Commands

```bash
# Development
wrangler dev --config wrangler.dev.toml

# View logs for specific environment
wrangler tail --env production

# Execute D1 queries
wrangler d1 execute checkin-db-dev --command "SELECT COUNT(*) FROM users"
wrangler d1 execute checkin-db --command "SELECT COUNT(*) FROM users"
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Cloudflare Workers

on:
  push:
    branches: [main, develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: npx wrangler deploy --config wrangler.staging.toml
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
      
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: npx wrangler deploy
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

## Resource Limits

Configure resource limits (optional):

```toml
[limits]
cpu_ms = 50  # CPU time limit in milliseconds
```

## Observability

Enable logging and monitoring:

```toml
[observability]
enabled = true

# Optional: Logpush configuration
[logpush]
enabled = true
```

## Notes

1. **Never commit secrets**: Use `wrangler secret put` for sensitive values
2. **Database IDs**: Create separate databases for each environment
3. **Testing**: Use development environment for testing before production
4. **Cron triggers**: Adjust frequency based on your needs and Cloudflare limits
5. **Custom domains**: Requires domain to be on Cloudflare (can use free plan)
