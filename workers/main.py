from js import Response, Request, Headers, crypto, TextEncoder, TextDecoder, URL, fetch
import json
import base64
import hashlib
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Encryption utilities using Web Crypto API
async def encrypt_data(data, key):
    """Encrypt data using AES-GCM"""
    if not data:
        return ""
    
    try:
        # Generate IV
        iv = crypto.getRandomValues(bytearray(12))
        
        # Convert key to bytes
        key_bytes = key.encode('utf-8')
        key_hash = hashlib.sha256(key_bytes).digest()
        
        # TODO: This is a placeholder implementation using base64 encoding
        # For production, implement proper AES-GCM encryption using Web Crypto API
        # See SECURITY.md for implementation details
        encrypted = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        iv_b64 = base64.b64encode(bytes(iv)).decode('utf-8')
        
        return f"{iv_b64}:{encrypted}"
    except Exception as e:
        logger.error("Encryption error: %s", e)
        return data


async def decrypt_data(encrypted_data, key):
    """Decrypt data using AES-GCM"""
    if not encrypted_data:
        return ""
    
    try:
        # Split IV and data
        parts = encrypted_data.split(':')
        if len(parts) != 2:
            return encrypted_data
        
        iv_b64, encrypted = parts
        
        # TODO: This is a placeholder implementation using base64 decoding
        # For production, implement proper AES-GCM decryption using Web Crypto API
        # See SECURITY.md for implementation details
        decrypted = base64.b64decode(encrypted).decode('utf-8')
        
        return decrypted
    except Exception as e:
        logger.error("Decryption error: %s", e)
        return encrypted_data


async def handle_request(request, env):
    """Main request handler"""
    url = URL.new(request.url)
    path = url.pathname
    method = request.method
    
    logger.info("Request: %s %s", method, path)
    # Initialize database if needed
    if not hasattr(env, '_db_initialized'):
        await init_database(env)
        env._db_initialized = True
    # Normalize path: strip trailing slash (except for root)
    original_path = path
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    

    
    # API Routes
    if path.startswith("/api/"):
        # Normalize API path too
        api_path = path
        
        if api_path == "/api/checkins" and method == "GET":
            return await handle_get_all_checkins(request, env)
        
        elif api_path == "/api/checkin" and method == "POST":
            return await handle_checkin(request, env)
        
        elif api_path == "/api/checkin/latest" and method == "GET":
            return await handle_get_latest_checkin(request, env)
        
        elif api_path == "/api/settings" and method == "GET":
            return await handle_get_settings(request, env)
        
        elif api_path == "/api/settings" and method == "POST":
            return await handle_save_settings(request, env)
        
        elif api_path == "/api/notification/test" and method == "POST":
            return await handle_test_notification(request, env)
        
        elif api_path == "/api/timelog/start" and method == "POST":
            return await handle_timelog_start(request, env)
        
        elif api_path == "/api/timelog/stop" and method == "POST":
            return await handle_timelog_stop(request, env)
        
        elif api_path == "/api/timelogs" and method == "GET":
            return await handle_get_timelogs(request, env)
        
        elif api_path == "/api/leaderboard" and method == "GET":
            return await handle_leaderboard(request, env)
            
        elif api_path == "/api/debug/db" and method == "GET":
            return await handle_debug_db(request, env)

        # OAuth routes
        elif api_path == "/api/auth/github" and method == "GET":
            return await handle_auth_github(request, env)

        elif api_path == "/api/auth/github/callback" and method == "GET":
            return await handle_auth_github_callback(request, env)

        elif api_path == "/api/auth/slack" and method == "GET":
            return await handle_auth_slack(request, env)

        elif api_path == "/api/auth/slack/callback" and method == "GET":
            return await handle_auth_slack_callback(request, env)

        elif api_path == "/api/auth/status" and method == "GET":
            return await handle_auth_status(request, env)

        elif api_path == "/api/auth/disconnect" and method == "POST":
            return await handle_auth_disconnect(request, env)

        else:
            return Response.new(json.dumps({"error": "API route not found"}), 
                              {"status": 404, "headers": {"Content-Type": "application/json"}})
    
    # Static Pages & Assets
    if method == "GET":
        if path == "" or path == "/" or path == "/index.html":
            if hasattr(env, 'ASSETS'):
                return await env.ASSETS.fetch(request)
            return Response.new("Assets not found", {"status": 404})
        
        elif path in ["/leaderboard", "/time-logs", "/settings", "/check-ins", "/checkins"]:
            if hasattr(env, 'ASSETS'):
                # Handle both /check-ins and /checkins
                normalized_asset_path = path
                if normalized_asset_path == "/checkins":
                    normalized_asset_path = "/check-ins"
                
                # Fetch from /pages/*.html but keep the response as 200 (no 307 redirect needed)
                url_clone = URL.new(request.url)
                url_clone.pathname = f"/pages{normalized_asset_path}.html"
                request_clone = Request.new(url_clone, request)
                return await env.ASSETS.fetch(request_clone)
            return Response.new("Assets not found", {"status": 404})
        
        # Fallback for all other static assets (favicon.ico, CSS, JS, images)
        elif hasattr(env, 'ASSETS'):
            return await env.ASSETS.fetch(request)
    
    return Response.new("Not Found", {"status": 404})


async def init_database(env):
    """Initialize database tables"""
    try:
        # Create users table
        await env.sizzle_db.prepare("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                email TEXT,
                display_name TEXT,
                slack_user_id TEXT,
                slack_webhook_url TEXT,
                notification_time TEXT DEFAULT '09:00',
                notification_enabled INTEGER DEFAULT 1,
                email_notifications INTEGER DEFAULT 0,
                timezone TEXT DEFAULT 'UTC',
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_check_in DATE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """).run()
        
        # Create checkins table
        await env.sizzle_db.prepare("""
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                encrypted_previous_work TEXT,
                encrypted_today_plan TEXT,
                encrypted_blockers TEXT,
                mood TEXT,
                goal_accomplished INTEGER DEFAULT 0,
                checkin_date DATE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """).run()
        
        # Create timelogs table
        await env.sizzle_db.prepare("""
            CREATE TABLE IF NOT EXISTS timelogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                start_time DATETIME NOT NULL,
                end_time DATETIME,
                duration_seconds INTEGER,
                github_issue_url TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """).run()
        
        # Create indexes
        await env.sizzle_db.prepare("""
            CREATE INDEX IF NOT EXISTS idx_checkins_user_date ON checkins(user_id, checkin_date)
        """).run()
        
        await env.sizzle_db.prepare("""
            CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)
        """).run()

        # OAuth: add new columns if they don't exist yet (idempotent ALTER TABLE)
        for col_def in [
            "github_id TEXT",
            "github_username TEXT",
            "github_access_token TEXT",
            "slack_access_token TEXT",
            "slack_team_id TEXT",
        ]:
            try:
                await env.sizzle_db.prepare(
                    f"ALTER TABLE users ADD COLUMN {col_def}"
                ).run()
            except Exception:
                pass  # Column already exists

        # OAuth indexes
        try:
            await env.sizzle_db.prepare(
                "CREATE INDEX IF NOT EXISTS idx_users_github_id ON users(github_id)"
            ).run()
        except Exception:
            pass

        try:
            await env.sizzle_db.prepare(
                "CREATE INDEX IF NOT EXISTS idx_users_slack_user_id ON users(slack_user_id)"
            ).run()
        except Exception:
            pass

        # Temporary CSRF state table for OAuth flows
        await env.sizzle_db.prepare("""
            CREATE TABLE IF NOT EXISTS oauth_states (
                state TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """).run()

    except Exception as e:
        logger.error("Database initialization error: %s", e, exc_info=True)


async def handle_checkin(request, env):
    """Handle check-in submission"""
    try:
        raw_json = await request.json()
        data = raw_json.to_py()
        
        user_id = data.get('userId')
        previous_work = data.get('previousWork', '')
        today_plan = data.get('todayPlan', '')
        blockers = data.get('blockers', '')
        mood = data.get('mood', '😊')
        goal_accomplished = 1 if data.get('goalAccomplished') else 0
        
        if not user_id:
            return Response.new(json.dumps({"error": "User ID required"}), 
                              {"status": 400, "headers": {"Content-Type": "application/json"}})
        
        # Ensure user exists (test/pre-upsert)
        await env.sizzle_db.prepare("INSERT OR IGNORE INTO users (user_id) VALUES (?)").bind(user_id).run()
        
        # Get encryption key from environment with fallback
        encryption_key = getattr(env, 'ENCRYPTION_KEY', 'sizzle-dev-key-12345')

        
        # Encrypt sensitive data
        encrypted_previous = await encrypt_data(previous_work, encryption_key)
        encrypted_today = await encrypt_data(today_plan, encryption_key)
        encrypted_blockers = await encrypt_data(blockers, encryption_key)
        
        # Get current date
        today_obj = date.today()
        today = today_obj.isoformat()
        
        # 1. Insert check-in
        checkin_op = await env.sizzle_db.prepare("""
            INSERT INTO checkins (user_id, encrypted_previous_work, encrypted_today_plan, 
                                encrypted_blockers, mood, goal_accomplished, checkin_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """).bind(user_id, encrypted_previous, encrypted_today, encrypted_blockers, mood, goal_accomplished, today).run()
        
        # 2. Update streak and user profile
        user_proxy = await env.sizzle_db.prepare("""
            SELECT current_streak, longest_streak, last_check_in 
            FROM users WHERE user_id = ?
        """).bind(user_id).first()
        
        user = user_proxy.to_py() if user_proxy else None
        
        current_streak = 0
        longest_streak = 0
        last_check_in = None
        
        if user:
            current_streak = user['current_streak'] or 0
            longest_streak = user['longest_streak'] or 0
            last_check_in = user['last_check_in']
        
        # Streak logic
        from datetime import timedelta
        new_streak = 1
        if last_check_in:
            last_date = date.fromisoformat(last_check_in)
            if last_date == today_obj - timedelta(days=1):
                new_streak = current_streak + 1
            elif last_date == today_obj:
                new_streak = current_streak  # Already checked in today
            else:
                new_streak = 1
        
        new_longest = max(new_streak, longest_streak)
        
        display_name = data.get('userName', '')
        
        # Upsert user with new streak
        user_op = await env.sizzle_db.prepare("""
            INSERT INTO users (user_id, current_streak, longest_streak, last_check_in, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                current_streak = excluded.current_streak,
                longest_streak = excluded.longest_streak,
                last_check_in = excluded.last_check_in,
                updated_at = CURRENT_TIMESTAMP
        """).bind(user_id, new_streak, new_longest, today).run()
        
        return Response.new(json.dumps({
            "success": True, 
            "message": "Check-in saved",
            "streak": new_streak
        }), {"headers": {"Content-Type": "application/json"}})
        
    except Exception as e:
        logger.error("Error handling check-in: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_timelog_start(request, env):
    """Start a new time log"""
    try:
        data = (await request.json()).to_py()
        user_id = data.get('userId')
        issue_url = data.get('githubIssueUrl', '')
        
        if not user_id:
            return Response.new(json.dumps({"error": "User ID required"}), {"status": 400, "headers": {"Content-Type": "application/json"}})
            
        # Check if there's already an active log
        active_proxy = await env.sizzle_db.prepare("""
            SELECT id FROM timelogs WHERE user_id = ? AND end_time IS NULL LIMIT 1
        """).bind(user_id).first()
        
        if active_proxy:
            return Response.new(json.dumps({"error": "You already have an active time log"}), {"status": 400, "headers": {"Content-Type": "application/json"}})
            
        now = datetime.now().isoformat()
        await env.sizzle_db.prepare("""
            INSERT INTO timelogs (user_id, start_time, github_issue_url)
            VALUES (?, ?, ?)
        """).bind(user_id, now, issue_url).run()
        
        return Response.new(json.dumps({"success": True, "startTime": now}), 
                          {"headers": {"Content-Type": "application/json"}})
    except Exception as e:
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_timelog_stop(request, env):
    """Stop active time log"""
    try:
        data = (await request.json()).to_py()
        user_id = data.get('userId')
        
        if not user_id:
            return Response.new(json.dumps({"error": "User ID required"}), {"status": 400, "headers": {"Content-Type": "application/json"}})
            
        active_proxy = await env.sizzle_db.prepare("""
            SELECT id, start_time FROM timelogs WHERE user_id = ? AND end_time IS NULL 
            ORDER BY id DESC LIMIT 1
        """).bind(user_id).first()
        
        if not active_proxy:
            return Response.new(json.dumps({"error": "No active time log found"}), {"status": 404, "headers": {"Content-Type": "application/json"}})
        
        active = active_proxy.to_py()
        now_dt = datetime.now()
        start_dt = datetime.fromisoformat(active['start_time'])
        duration = int((now_dt - start_dt).total_seconds())
        
        await env.sizzle_db.prepare("""
            UPDATE timelogs SET end_time = ?, duration_seconds = ? WHERE id = ?
        """).bind(now_dt.isoformat(), duration, active['id']).run()
        
        return Response.new(json.dumps({"success": True, "duration": duration}), 
                          {"headers": {"Content-Type": "application/json"}})
    except Exception as e:
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_get_timelogs(request, env):
    """List time logs for a user"""
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        
        if not user_id:
            return Response.new(json.dumps({"error": "User ID required"}), 
                              {"status": 400, "headers": {"Content-Type": "application/json"}})
            
        result_proxy = await env.sizzle_db.prepare("""
            SELECT id, start_time, end_time, duration_seconds, github_issue_url 
            FROM timelogs WHERE user_id = ? 
            ORDER BY id DESC LIMIT 50
        """).bind(user_id).all()
        
        result = result_proxy.to_py() if hasattr(result_proxy, 'to_py') else result_proxy
        logs = result.get('results', []) if isinstance(result, dict) else []
        
        return Response.new(json.dumps({"logs": logs}), 
                          {"headers": {"Content-Type": "application/json"}})
    except Exception as e:
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_leaderboard(request, env):
    """Get check-in leaderboard based on streaks"""
    try:
        result_proxy = await env.sizzle_db.prepare("""
            SELECT user_id, current_streak, longest_streak 
            FROM users 
            ORDER BY current_streak DESC LIMIT 20
        """).all()
        
        result = result_proxy.to_py() if hasattr(result_proxy, 'to_py') else result_proxy
        
        leaderboard = []
        if isinstance(result, dict):
            leaderboard = result.get('results', [])
        elif isinstance(result, list):
            leaderboard = result
        
        return Response.new(json.dumps({"leaderboard": leaderboard}), 
                          {"headers": {"Content-Type": "application/json"}})
    except Exception as e:
        logger.error("Error in leaderboard handler: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_get_all_checkins(request, env):
    """Get all check-ins for a user"""
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        
        if not user_id:
            return Response.new(json.dumps({"error": "User ID required"}), 
                              {"status": 400, "headers": {"Content-Type": "application/json"}})
        
        # Get encryption key with fallback
        encryption_key = getattr(env, 'ENCRYPTION_KEY', 'sizzle-dev-key-12345')
        
        # Get all check-ins
        result_proxy = await env.sizzle_db.prepare("""
            SELECT id, encrypted_previous_work, encrypted_today_plan, 
                   encrypted_blockers, mood, goal_accomplished, checkin_date
            FROM checkins 
            WHERE user_id = ? 
            ORDER BY id DESC
        """).bind(user_id).all()
        
        result = result_proxy.to_py() if hasattr(result_proxy, 'to_py') else result_proxy
        
        rows = []
        if isinstance(result, dict):
            rows = result.get('results', [])
        elif isinstance(result, list):
            rows = result
        
        checkins = []
        for row in rows:
            previous = await decrypt_data(row['encrypted_previous_work'] if row['encrypted_previous_work'] else '', encryption_key)
            today_plan = await decrypt_data(row['encrypted_today_plan'] if row['encrypted_today_plan'] else '', encryption_key)
            blockers = await decrypt_data(row['encrypted_blockers'] if row['encrypted_blockers'] else '', encryption_key)
            
            checkins.append({
                "id": row['id'],
                "previousWork": previous,
                "todayPlan": today_plan,
                "blockers": blockers,
                "mood": row['mood'],
                "goalAccomplished": row['goal_accomplished'] == 1,
                "date": row['checkin_date']
            })
            
        return Response.new(json.dumps({"checkins": checkins}), 
                          {"headers": {"Content-Type": "application/json"}})
        
    except Exception as e:
        logger.error("Error getting check-ins: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_get_latest_checkin(request, env):
    """Get the latest check-in for pre-filling"""
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        
        if not user_id:
            return Response.new(json.dumps({"error": "User ID required"}), 
                              {"status": 400, "headers": {"Content-Type": "application/json"}})
        
        # Get latest check-in and user streak
        result_proxy = await env.sizzle_db.prepare("""
            SELECT c.encrypted_today_plan, c.mood, c.goal_accomplished, c.checkin_date, u.current_streak
            FROM checkins c
            LEFT JOIN users u ON c.user_id = u.user_id
            WHERE c.user_id = ? 
            ORDER BY c.id DESC 
            LIMIT 1
        """).bind(user_id).first()
        
        if not result_proxy:
            return Response.new(json.dumps({}), 
                              {"headers": {"Content-Type": "application/json"}})
        
        result = result_proxy.to_py()
        
        # Decrypt data
        if not hasattr(env, 'ENCRYPTION_KEY') or not env.ENCRYPTION_KEY:
            return Response.new(json.dumps({"error": "Encryption key not configured"}), 
                              {"status": 500, "headers": {"Content-Type": "application/json"}})
        encryption_key = env.ENCRYPTION_KEY
        today_plan = await decrypt_data(result['encrypted_today_plan'] if result['encrypted_today_plan'] else '', encryption_key)
        
        return Response.new(json.dumps({
            "todayPlan": today_plan,
            "mood": result['mood'],
            "goalAccomplished": result['goal_accomplished'] == 1,
            "date": result['checkin_date'],
            "streak": result['current_streak'] or 0
        }), {"headers": {"Content-Type": "application/json"}})
        
    except Exception as e:
        logger.error("Error getting latest check-in: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_get_settings(request, env):
    """Get user settings"""
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        
        if not user_id:
            return Response.new(json.dumps({"error": "User ID required"}), 
                              {"status": 400, "headers": {"Content-Type": "application/json"}})
        
        result_proxy = await env.sizzle_db.prepare("""
            SELECT email, notification_time, timezone, slack_webhook_url, 
                   email_notifications 
            FROM users 
            WHERE user_id = ?
        """).bind(user_id).first()
        
        if not result_proxy:
            return Response.new(json.dumps({}), 
                              {"headers": {"Content-Type": "application/json"}})
        
        # Standardize result handling
        res_converted = result_proxy.to_py() if hasattr(result_proxy, 'to_py') else result_proxy
        result = res_converted
        
        return Response.new(json.dumps({
            "email": result['email'] if result['email'] else '',
            "notificationTime": result['notification_time'],
            "timezone": result['timezone'],
            "slackWebhookUrl": result['slack_webhook_url'] if result['slack_webhook_url'] else '',
            "emailNotifications": result['email_notifications']
        }), {"headers": {"Content-Type": "application/json"}})
        
    except Exception as e:
        logger.error("Error getting settings: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_save_settings(request, env):
    """Save user settings"""
    try:
        data = (await request.json()).to_py()
        user_id = data.get('userId')
        
        if not user_id:
            return Response.new(json.dumps({"error": "User ID required"}), 
                              {"status": 400, "headers": {"Content-Type": "application/json"}})
        
        email = data.get('email', '')
        notification_time = data.get('notificationTime', '09:00')
        timezone = data.get('timezone', 'UTC')
        slack_webhook_url = data.get('slackWebhookUrl', '')
        email_notifications = data.get('emailNotifications', 0)
        
        # Upsert user settings
        await env.sizzle_db.prepare("""
            INSERT INTO users (user_id, email, notification_time, timezone, 
                             slack_webhook_url, email_notifications, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                email = excluded.email,
                notification_time = excluded.notification_time,
                timezone = excluded.timezone,
                slack_webhook_url = excluded.slack_webhook_url,
                email_notifications = excluded.email_notifications,
                updated_at = CURRENT_TIMESTAMP
        """).bind(user_id, email, notification_time, timezone, slack_webhook_url, email_notifications).run()
        
        return Response.new(json.dumps({"success": True}), {"headers": {"Content-Type": "application/json"}})
        
    except Exception as e:
        logger.error("Error saving settings: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_test_notification(request, env):
    """Send test notification"""
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        
        if not user_id:
            return Response.new(json.dumps({"error": "User ID required"}), 
                              {"status": 400, "headers": {"Content-Type": "application/json"}})
        
        # Get user settings
        result_proxy = await env.sizzle_db.prepare("""
            SELECT slack_webhook_url, email 
            FROM users 
            WHERE user_id = ?
        """).bind(user_id).first()
        
        if not result_proxy:
            return Response.new(json.dumps({"error": "User not found"}), 
                              {"status": 404, "headers": {"Content-Type": "application/json"}})
        
        result = result_proxy.to_py()
        
        # Send Slack notification if webhook is configured
        if result['slack_webhook_url']:
            # ... slack logic ...
            slack_message = {
                "text": "🔔 Test Notification",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Time for your daily check-in!* ✨\n\nClick the link below to fill out your check-in form."
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "📝 Fill Check-in Form"
                                },
                                "url": url.origin
                            }
                        ]
                    }
                ]
            }
            
            try:
                await fetch(result['slack_webhook_url'], {
                    "method": "POST",
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(slack_message)
                })
            except Exception as e:
                logger.error("Error sending Slack notification: %s", e)
        
        return Response.new(json.dumps({"success": True, "message": "Test notification sent"}),
                          {"headers": {"Content-Type": "application/json"}})
    except Exception as e:
        logger.error("Error sending test notification: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_debug_db(request, env):
    """Debug endpoint to check database counts"""
    try:
        users_count_proxy = await env.sizzle_db.prepare("SELECT COUNT(*) as count FROM users").first()
        checkins_count_proxy = await env.sizzle_db.prepare("SELECT COUNT(*) as count FROM checkins").first()
        
        users_res = users_count_proxy.to_py() if users_count_proxy else {"count": 0}
        checkins_res = checkins_count_proxy.to_py() if checkins_count_proxy else {"count": 0}
        
        return Response.new(json.dumps({
            "users": users_res.get('count', 0),
            "checkins": checkins_res.get('count', 0),
            "db_initialized": getattr(env, '_db_initialized', False)
        }), {"headers": {"Content-Type": "application/json"}})
    except Exception as e:
        return Response.new(json.dumps({"error": str(e)}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


# ---------------------------------------------------------------------------
# OAuth helpers
# ---------------------------------------------------------------------------

def _generate_state():
    """Generate a cryptographically random state token."""
    random_bytes = crypto.getRandomValues(bytearray(32))
    return base64.urlsafe_b64encode(bytes(random_bytes)).decode('utf-8').rstrip('=')


def _get_worker_base_url(env, request):
    """Return the base URL of this worker (e.g. https://blt-sizzle.workers.dev)."""
    worker_host = getattr(env, 'WORKER_HOST', None)
    if worker_host:
        return f"https://{worker_host}"
    # Fall back to the request's own origin
    req_url = URL.new(request.url)
    return req_url.origin


async def _store_oauth_state(env, state, user_id, provider):
    """Persist an OAuth state token so we can validate it on callback."""
    await env.sizzle_db.prepare("""
        INSERT INTO oauth_states (state, user_id, provider) VALUES (?, ?, ?)
    """).bind(state, user_id, provider).run()
    # Prune states older than 15 minutes to keep the table small
    try:
        await env.sizzle_db.prepare("""
            DELETE FROM oauth_states
            WHERE created_at < datetime('now', '-15 minutes')
        """).run()
    except Exception:
        pass


async def _validate_oauth_state(env, state, provider):
    """Validate and consume a state token.  Returns user_id or None."""
    if not state:
        return None
    row_proxy = await env.sizzle_db.prepare("""
        SELECT user_id FROM oauth_states
        WHERE state = ? AND provider = ?
          AND created_at >= datetime('now', '-15 minutes')
        LIMIT 1
    """).bind(state, provider).first()
    if not row_proxy:
        return None
    row = row_proxy.to_py()
    # Consume the state (one-time use)
    await env.sizzle_db.prepare(
        "DELETE FROM oauth_states WHERE state = ?"
    ).bind(state).run()
    return row['user_id']


# ---------------------------------------------------------------------------
# GitHub OAuth
# ---------------------------------------------------------------------------

async def handle_auth_github(request, env):
    """Initiate GitHub OAuth flow.

    Query params:
      userId (required) – the caller's current user_id so we can link the
                          GitHub account to their existing data after the flow.
    """
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        if not user_id:
            return Response.new(json.dumps({"error": "userId is required"}),
                                {"status": 400, "headers": {"Content-Type": "application/json"}})

        client_id = getattr(env, 'GITHUB_CLIENT_ID', None)
        if not client_id:
            return Response.new(json.dumps({"error": "GitHub OAuth is not configured on this server"}),
                                {"status": 503, "headers": {"Content-Type": "application/json"}})

        state = _generate_state()
        await _store_oauth_state(env, state, user_id, 'github')

        base_url = _get_worker_base_url(env, request)
        redirect_uri = f"{base_url}/api/auth/github/callback"

        github_url = (
            f"https://github.com/login/oauth/authorize"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope=read:user,user:email"
            f"&state={state}"
        )

        return Response.new("", {
            "status": 302,
            "headers": {"Location": github_url}
        })
    except Exception as e:
        logger.error("Error initiating GitHub OAuth: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}),
                            {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_auth_github_callback(request, env):
    """Handle GitHub OAuth callback."""
    try:
        url = URL.new(request.url)
        code = url.searchParams.get('code')
        state = url.searchParams.get('state')
        error = url.searchParams.get('error')

        base_url = _get_worker_base_url(env, request)

        if error:
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=github_denied"}
            })

        if not code or not state:
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=github_invalid"}
            })

        user_id = await _validate_oauth_state(env, state, 'github')
        if not user_id:
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=github_state_invalid"}
            })

        client_id = getattr(env, 'GITHUB_CLIENT_ID', '')
        client_secret = getattr(env, 'GITHUB_CLIENT_SECRET', '')
        redirect_uri = f"{base_url}/api/auth/github/callback"

        # Exchange code for access token
        token_resp = await fetch("https://github.com/login/oauth/access_token", {
            "method": "POST",
            "headers": {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            }),
        })

        if not token_resp.ok:
            logger.error("GitHub token exchange failed: status %s", token_resp.status)
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=github_token"}
            })

        token_data_raw = await token_resp.json()
        token_data = token_data_raw.to_py() if hasattr(token_data_raw, 'to_py') else token_data_raw

        access_token = token_data.get('access_token')
        if not access_token:
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=github_token"}
            })

        # Fetch GitHub user profile
        user_resp = await fetch("https://api.github.com/user", {
            "headers": {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "BLT-Sizzle/1.0",
            }
        })

        if not user_resp.ok:
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=github_profile"}
            })

        gh_user_raw = await user_resp.json()
        gh_user = gh_user_raw.to_py() if hasattr(gh_user_raw, 'to_py') else gh_user_raw

        github_id = str(gh_user.get('id', ''))
        github_username = gh_user.get('login', '')
        display_name = gh_user.get('name') or github_username
        email = gh_user.get('email') or ''

        # Ensure the user row exists, then link GitHub credentials
        await env.sizzle_db.prepare(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)"
        ).bind(user_id).run()

        await env.sizzle_db.prepare("""
            UPDATE users
            SET github_id = ?,
                github_username = ?,
                github_access_token = ?,
                display_name = COALESCE(NULLIF(display_name, ''), ?),
                email = COALESCE(NULLIF(email, ''), ?),
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """).bind(github_id, github_username, access_token, display_name, email, user_id).run()

        return Response.new("", {
            "status": 302,
            "headers": {"Location": f"{base_url}/?connected=github&userId={user_id}"}
        })

    except Exception as e:
        logger.error("Error in GitHub OAuth callback: %s", e, exc_info=True)
        base_url = _get_worker_base_url(env, request)
        return Response.new("", {
            "status": 302,
            "headers": {"Location": f"{base_url}/?auth_error=github_error"}
        })


# ---------------------------------------------------------------------------
# Slack OAuth
# ---------------------------------------------------------------------------

async def handle_auth_slack(request, env):
    """Initiate Slack OAuth flow.

    Query params:
      userId (required) – the caller's current user_id.
    """
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        if not user_id:
            return Response.new(json.dumps({"error": "userId is required"}),
                                {"status": 400, "headers": {"Content-Type": "application/json"}})

        client_id = getattr(env, 'SLACK_CLIENT_ID', None)
        if not client_id:
            return Response.new(json.dumps({"error": "Slack OAuth is not configured on this server"}),
                                {"status": 503, "headers": {"Content-Type": "application/json"}})

        state = _generate_state()
        await _store_oauth_state(env, state, user_id, 'slack')

        base_url = _get_worker_base_url(env, request)
        redirect_uri = f"{base_url}/api/auth/slack/callback"

        slack_url = (
            f"https://slack.com/oauth/v2/authorize"
            f"?client_id={client_id}"
            f"&user_scope=identity.basic,identity.email,identity.team"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
        )

        return Response.new("", {
            "status": 302,
            "headers": {"Location": slack_url}
        })
    except Exception as e:
        logger.error("Error initiating Slack OAuth: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}),
                            {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_auth_slack_callback(request, env):
    """Handle Slack OAuth callback."""
    try:
        url = URL.new(request.url)
        code = url.searchParams.get('code')
        state = url.searchParams.get('state')
        error = url.searchParams.get('error')

        base_url = _get_worker_base_url(env, request)

        if error:
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=slack_denied"}
            })

        if not code or not state:
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=slack_invalid"}
            })

        user_id = await _validate_oauth_state(env, state, 'slack')
        if not user_id:
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=slack_state_invalid"}
            })

        client_id = getattr(env, 'SLACK_CLIENT_ID', '')
        client_secret = getattr(env, 'SLACK_CLIENT_SECRET', '')
        redirect_uri = f"{base_url}/api/auth/slack/callback"

        # Exchange code for access token via oauth.v2.access
        token_resp = await fetch(
            f"https://slack.com/api/oauth.v2.access"
            f"?client_id={client_id}"
            f"&client_secret={client_secret}"
            f"&code={code}"
            f"&redirect_uri={redirect_uri}",
            {"method": "GET"}
        )

        if not token_resp.ok:
            logger.error("Slack token exchange failed: status %s", token_resp.status)
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=slack_token"}
            })

        token_data_raw = await token_resp.json()
        token_data = token_data_raw.to_py() if hasattr(token_data_raw, 'to_py') else token_data_raw

        if not token_data.get('ok'):
            slack_err = token_data.get('error', 'unknown')
            logger.error("Slack OAuth error: %s", slack_err)
            return Response.new("", {
                "status": 302,
                "headers": {"Location": f"{base_url}/?auth_error=slack_token"}
            })

        # User-level token lives under authed_user
        authed_user = token_data.get('authed_user', {})
        user_access_token = authed_user.get('access_token', '')
        slack_user_id = authed_user.get('id', '')
        team = token_data.get('team', {})
        slack_team_id = team.get('id', '') if isinstance(team, dict) else ''

        # Fetch user identity
        identity_resp = await fetch("https://slack.com/api/users.identity", {
            "headers": {"Authorization": f"Bearer {user_access_token}"}
        })

        display_name = ''
        email = ''
        if identity_resp.ok:
            identity_raw = await identity_resp.json()
            identity = identity_raw.to_py() if hasattr(identity_raw, 'to_py') else identity_raw
            if identity.get('ok'):
                slack_profile = identity.get('user', {})
                display_name = slack_profile.get('name', '')
                email = slack_profile.get('email', '')

        # Ensure user row exists, then link Slack credentials
        await env.sizzle_db.prepare(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)"
        ).bind(user_id).run()

        await env.sizzle_db.prepare("""
            UPDATE users
            SET slack_user_id = ?,
                slack_access_token = ?,
                slack_team_id = ?,
                display_name = COALESCE(NULLIF(display_name, ''), ?),
                email = COALESCE(NULLIF(email, ''), ?),
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """).bind(slack_user_id, user_access_token, slack_team_id, display_name, email, user_id).run()

        return Response.new("", {
            "status": 302,
            "headers": {"Location": f"{base_url}/?connected=slack&userId={user_id}"}
        })

    except Exception as e:
        logger.error("Error in Slack OAuth callback: %s", e, exc_info=True)
        base_url = _get_worker_base_url(env, request)
        return Response.new("", {
            "status": 302,
            "headers": {"Location": f"{base_url}/?auth_error=slack_error"}
        })


# ---------------------------------------------------------------------------
# Auth status & disconnect
# ---------------------------------------------------------------------------

async def handle_auth_status(request, env):
    """Return which OAuth providers are connected for a user."""
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        if not user_id:
            return Response.new(json.dumps({"error": "userId is required"}),
                                {"status": 400, "headers": {"Content-Type": "application/json"}})

        row_proxy = await env.sizzle_db.prepare("""
            SELECT github_id, github_username, slack_user_id, slack_team_id, display_name, email
            FROM users WHERE user_id = ?
        """).bind(user_id).first()

        if not row_proxy:
            return Response.new(json.dumps({
                "github": {"connected": False},
                "slack": {"connected": False}
            }), {"headers": {"Content-Type": "application/json"}})

        row = row_proxy.to_py()

        return Response.new(json.dumps({
            "github": {
                "connected": bool(row.get('github_id')),
                "username": row.get('github_username') or '',
            },
            "slack": {
                "connected": bool(row.get('slack_user_id')),
                "userId": row.get('slack_user_id') or '',
                "teamId": row.get('slack_team_id') or '',
            },
            "displayName": row.get('display_name') or '',
            "email": row.get('email') or '',
        }), {"headers": {"Content-Type": "application/json"}})

    except Exception as e:
        logger.error("Error getting auth status: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}),
                            {"status": 500, "headers": {"Content-Type": "application/json"}})


async def handle_auth_disconnect(request, env):
    """Disconnect a provider (github or slack) from a user account."""
    try:
        data = (await request.json()).to_py()
        user_id = data.get('userId')
        provider = data.get('provider')

        if not user_id or provider not in ('github', 'slack'):
            return Response.new(json.dumps({"error": "userId and provider (github|slack) are required"}),
                                {"status": 400, "headers": {"Content-Type": "application/json"}})

        if provider == 'github':
            await env.sizzle_db.prepare("""
                UPDATE users
                SET github_id = NULL, github_username = NULL, github_access_token = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """).bind(user_id).run()
        else:
            await env.sizzle_db.prepare("""
                UPDATE users
                SET slack_user_id = NULL, slack_access_token = NULL, slack_team_id = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """).bind(user_id).run()

        return Response.new(json.dumps({"success": True}),
                            {"headers": {"Content-Type": "application/json"}})

    except Exception as e:
        logger.error("Error disconnecting provider: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e)}),
                            {"status": 500, "headers": {"Content-Type": "application/json"}})


# Main entry point for Cloudflare Worker
async def on_fetch(request, env):
    """Worker entry point for HTTP requests"""
    try:
        return await handle_request(request, env)
    except Exception as e:
        logger.critical("Unhandled worker error: %s", e, exc_info=True)
        return Response.new(json.dumps({"error": str(e), "stack": "See worker logs"}), 
                          {"status": 500, "headers": {"Content-Type": "application/json"}})


async def on_scheduled(event, env):
    """Worker entry point for scheduled/cron events"""
    try:
        # Import scheduler module
        from scheduler import handle_scheduled
        await handle_scheduled(event, env)
    except Exception as e:
        logger.error("Error in scheduled event: %s", e, exc_info=True)
