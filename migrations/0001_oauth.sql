-- Migration number: 0001 	 2026-03-07T19:00:00.000Z

-- Add OAuth provider columns to users table
ALTER TABLE users ADD COLUMN github_id TEXT;
ALTER TABLE users ADD COLUMN github_username TEXT;
ALTER TABLE users ADD COLUMN github_access_token TEXT;
ALTER TABLE users ADD COLUMN slack_access_token TEXT;
ALTER TABLE users ADD COLUMN slack_team_id TEXT;
-- Note: slack_user_id already exists from migration 0000_init.sql

-- Create indexes for OAuth lookups
CREATE INDEX IF NOT EXISTS idx_users_github_id ON users(github_id);
-- Note: idx_users_slack_user_id references the slack_user_id column added in 0000_init.sql
CREATE INDEX IF NOT EXISTS idx_users_slack_user_id ON users(slack_user_id);

-- Create oauth_states table for CSRF protection during OAuth flows
CREATE TABLE IF NOT EXISTS oauth_states (
    state TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    provider TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
