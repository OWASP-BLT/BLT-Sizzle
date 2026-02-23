-- D1 Database Schema for Check-in App

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE NOT NULL,
    email TEXT,
    slack_user_id TEXT,
    slack_webhook_url TEXT,
    notification_time TEXT DEFAULT '09:00',
    notification_enabled INTEGER DEFAULT 1,
    email_notifications INTEGER DEFAULT 0,
    timezone TEXT DEFAULT 'UTC',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Check-ins table (encrypted data)
CREATE TABLE IF NOT EXISTS checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    encrypted_previous_work TEXT,
    encrypted_today_plan TEXT,
    encrypted_blockers TEXT,
    mood TEXT,
    checkin_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_checkins_user_date ON checkins(user_id, checkin_date);
CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);
