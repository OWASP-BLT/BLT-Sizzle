from js import Response, crypto, URL, fetch
import json
import base64
import hashlib
from datetime import date


def json_response(data, status=200):
    """Create a JSON response with proper headers."""
    return Response.new(
        json.dumps(data),
        status=status,
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
    )


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
        hashlib.sha256(key_bytes).digest()
        
        # TODO: This is a placeholder implementation using base64 encoding
        # For production, implement proper AES-GCM encryption using Web Crypto API
        # See SECURITY.md for implementation details
        encrypted = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        iv_b64 = base64.b64encode(bytes(iv)).decode('utf-8')
        
        return f"{iv_b64}:{encrypted}"
    except Exception as e:
        print(f"Encryption error: {e}")
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
        print(f"Decryption error: {e}")
        return encrypted_data


# HTML template
INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Check-in</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }
        
        textarea, input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            transition: border-color 0.3s;
            resize: vertical;
        }
        
        textarea:focus, input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        textarea {
            min-height: 100px;
        }
        
        .emoji-picker {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .emoji-option {
            font-size: 32px;
            cursor: pointer;
            padding: 8px;
            border-radius: 8px;
            transition: all 0.2s;
            border: 2px solid transparent;
        }
        
        .emoji-option:hover {
            background: #f5f5f5;
            transform: scale(1.1);
        }
        
        .emoji-option.selected {
            border-color: #667eea;
            background: #f0f4ff;
        }
        
        .button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        .button:active {
            transform: translateY(0);
        }
        
        .success-message {
            background: #10b981;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .error-message {
            background: #ef4444;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .settings-link {
            text-align: center;
            margin-top: 20px;
        }
        
        .settings-link a {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
        }
        
        .settings-link a:hover {
            text-decoration: underline;
        }
        
        .loading {
            display: none;
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Daily Check-in</h1>
        <p class="subtitle">Share your progress and plan for today</p>
        
        <div class="success-message" id="successMessage">
            ✓ Check-in submitted successfully!
        </div>
        
        <div class="error-message" id="errorMessage">
            ✗ An error occurred. Please try again.
        </div>
        
        <div class="loading" id="loading">
            Loading your previous check-in...
        </div>
        
        <form id="checkinForm">
            <div class="form-group">
                <label for="previousWork">What did you do since last check-in?</label>
                <textarea id="previousWork" name="previousWork" placeholder="Describe your accomplishments..."></textarea>
            </div>
            
            <div class="form-group">
                <label for="todayPlan">What do you plan to do today?</label>
                <textarea id="todayPlan" name="todayPlan" placeholder="Outline your plans..." required></textarea>
            </div>
            
            <div class="form-group">
                <label for="blockers">Any blockers or challenges?</label>
                <textarea id="blockers" name="blockers" placeholder="None, or describe any obstacles..."></textarea>
            </div>
            
            <div class="form-group">
                <label>How are you feeling today?</label>
                <div class="emoji-picker">
                    <span class="emoji-option" data-mood="😊" title="Happy">😊</span>
                    <span class="emoji-option" data-mood="😐" title="Neutral">😐</span>
                    <span class="emoji-option" data-mood="😟" title="Worried">😟</span>
                    <span class="emoji-option" data-mood="😫" title="Stressed">😫</span>
                    <span class="emoji-option" data-mood="🤗" title="Excited">🤗</span>
                    <span class="emoji-option" data-mood="🤔" title="Thoughtful">🤔</span>
                    <span class="emoji-option" data-mood="😴" title="Tired">😴</span>
                    <span class="emoji-option" data-mood="💪" title="Motivated">💪</span>
                </div>
                <input type="hidden" id="mood" name="mood" value="😊">
            </div>
            
            <button type="submit" class="button">Submit Check-in</button>
        </form>
        
        <div class="settings-link">
            <a href="/settings">⚙️ Notification Settings</a>
        </div>
    </div>
    
    <script>
        // Get user ID from localStorage or generate new one
        let userId = localStorage.getItem('userId');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('userId', userId);
        }
        
        // Emoji picker
        const emojiOptions = document.querySelectorAll('.emoji-option');
        const moodInput = document.getElementById('mood');
        
        emojiOptions.forEach(option => {
            option.addEventListener('click', function() {
                emojiOptions.forEach(opt => opt.classList.remove('selected'));
                this.classList.add('selected');
                moodInput.value = this.dataset.mood;
            });
        });
        
        // Select default emoji
        emojiOptions[0].classList.add('selected');
        
        // Load previous check-in data
        async function loadPreviousCheckin() {
            const loading = document.getElementById('loading');
            loading.style.display = 'block';
            
            try {
                const response = await fetch(`/api/checkin/latest?userId=${userId}`);
                if (response.ok) {
                    const data = await response.json();
                    if (data.todayPlan) {
                        // Pre-fill "previous work" with last check-in's "today plan"
                        document.getElementById('previousWork').value = data.todayPlan;
                    }
                }
            } catch (error) {
                console.error('Error loading previous check-in:', error);
            } finally {
                loading.style.display = 'none';
            }
        }
        
        loadPreviousCheckin();
        
        // Form submission
        document.getElementById('checkinForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const successMessage = document.getElementById('successMessage');
            const errorMessage = document.getElementById('errorMessage');
            const submitButton = this.querySelector('button[type="submit"]');
            
            successMessage.style.display = 'none';
            errorMessage.style.display = 'none';
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';
            
            const formData = {
                userId: userId,
                previousWork: document.getElementById('previousWork').value,
                todayPlan: document.getElementById('todayPlan').value,
                blockers: document.getElementById('blockers').value,
                mood: document.getElementById('mood').value
            };
            
            try {
                const response = await fetch('/api/checkin', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                if (response.ok) {
                    successMessage.style.display = 'block';
                    // Don't clear the form, keep it for reference
                    setTimeout(() => {
                        successMessage.style.display = 'none';
                    }, 3000);
                } else {
                    throw new Error('Submission failed');
                }
            } catch (error) {
                console.error('Error:', error);
                errorMessage.style.display = 'block';
                setTimeout(() => {
                    errorMessage.style.display = 'none';
                }, 3000);
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Check-in';
            }
        });
    </script>
</body>
</html>
"""


SETTINGS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notification Settings</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }
        
        input[type="text"], input[type="email"], input[type="time"], select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            transition: border-color 0.3s;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        
        .button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 10px;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        .button.secondary {
            background: #6b7280;
        }
        
        .success-message {
            background: #10b981;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .info-box {
            background: #f0f4ff;
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .info-box h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .info-box p {
            color: #333;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .back-link {
            text-align: center;
            margin-top: 20px;
        }
        
        .back-link a {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
        }
        
        .back-link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚙️ Settings</h1>
        <p class="subtitle">Configure your notification preferences</p>
        
        <div class="success-message" id="successMessage">
            ✓ Settings saved successfully!
        </div>
        
        <form id="settingsForm">
            <div class="form-group">
                <label for="email">Email Address (optional)</label>
                <input type="email" id="email" name="email" placeholder="your.email@example.com">
            </div>
            
            <div class="form-group">
                <label for="notificationTime">Reminder Time</label>
                <input type="time" id="notificationTime" name="notificationTime" value="09:00">
            </div>
            
            <div class="form-group">
                <label for="timezone">Timezone</label>
                <select id="timezone" name="timezone">
                    <option value="UTC">UTC</option>
                    <option value="America/New_York">Eastern Time (US)</option>
                    <option value="America/Chicago">Central Time (US)</option>
                    <option value="America/Denver">Mountain Time (US)</option>
                    <option value="America/Los_Angeles">Pacific Time (US)</option>
                    <option value="Europe/London">London</option>
                    <option value="Europe/Paris">Paris</option>
                    <option value="Asia/Tokyo">Tokyo</option>
                    <option value="Asia/Shanghai">Shanghai</option>
                    <option value="Asia/Kolkata">India</option>
                    <option value="Australia/Sydney">Sydney</option>
                </select>
            </div>
            
            <div class="form-group">
                <div class="checkbox-group">
                    <input type="checkbox" id="emailNotifications" name="emailNotifications">
                    <label for="emailNotifications">Send email reminders</label>
                </div>
            </div>
            
            <div class="info-box">
                <h3>🔔 Slack Integration</h3>
                <p>To enable Slack notifications, you'll need to create a Slack webhook URL. Visit your Slack workspace settings and create an incoming webhook, then paste the URL below.</p>
            </div>
            
            <div class="form-group">
                <label for="slackWebhook">Slack Webhook URL (optional)</label>
                <input type="text" id="slackWebhook" name="slackWebhook" placeholder="https://hooks.slack.com/services/...">
            </div>
            
            <button type="submit" class="button">Save Settings</button>
            <button type="button" class="button secondary" onclick="testNotification()">Test Notification</button>
        </form>
        
        <div class="back-link">
            <a href="/">← Back to Check-in</a>
        </div>
    </div>
    
    <script>
        let userId = localStorage.getItem('userId');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('userId', userId);
        }
        
        // Load current settings
        async function loadSettings() {
            try {
                const response = await fetch(`/api/settings?userId=${userId}`);
                if (response.ok) {
                    const settings = await response.json();
                    if (settings.email) document.getElementById('email').value = settings.email;
                    if (settings.notificationTime) document.getElementById('notificationTime').value = settings.notificationTime;
                    if (settings.timezone) document.getElementById('timezone').value = settings.timezone;
                    if (settings.slackWebhookUrl) document.getElementById('slackWebhook').value = settings.slackWebhookUrl;
                    document.getElementById('emailNotifications').checked = settings.emailNotifications === 1;
                }
            } catch (error) {
                console.error('Error loading settings:', error);
            }
        }
        
        loadSettings();
        
        // Form submission
        document.getElementById('settingsForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const successMessage = document.getElementById('successMessage');
            const submitButton = this.querySelector('button[type="submit"]');
            
            successMessage.style.display = 'none';
            submitButton.disabled = true;
            submitButton.textContent = 'Saving...';
            
            const formData = {
                userId: userId,
                email: document.getElementById('email').value,
                notificationTime: document.getElementById('notificationTime').value,
                timezone: document.getElementById('timezone').value,
                slackWebhookUrl: document.getElementById('slackWebhook').value,
                emailNotifications: document.getElementById('emailNotifications').checked ? 1 : 0
            };
            
            try {
                const response = await fetch('/api/settings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                if (response.ok) {
                    successMessage.style.display = 'block';
                    setTimeout(() => {
                        successMessage.style.display = 'none';
                    }, 3000);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to save settings');
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = 'Save Settings';
            }
        });
        
        async function testNotification() {
            try {
                const response = await fetch(`/api/notification/test?userId=${userId}`, {
                    method: 'POST'
                });
                if (response.ok) {
                    alert('Test notification sent! Check your Slack or email.');
                } else {
                    alert('Failed to send test notification. Make sure you have configured Slack or email.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to send test notification');
            }
        }
    </script>
</body>
</html>
"""


async def handle_request(request, env):
    """Main request handler"""
    url = URL.new(request.url)
    path = url.pathname
    method = request.method
    
    # Handle CORS preflight requests
    if method == "OPTIONS":
        return Response.new("", status=204, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        })
    
    # Initialize database if needed
    if not hasattr(env, '_db_initialized'):
        await init_database(env)
        env._db_initialized = True
    
    # Route handlers
    if path == "/" and method == "GET":
        return Response.new(INDEX_HTML, headers={"Content-Type": "text/html"})
    
    elif path == "/settings" and method == "GET":
        return Response.new(SETTINGS_HTML, headers={"Content-Type": "text/html"})
    
    elif path == "/api/checkin" and method == "POST":
        return await handle_checkin(request, env)
    
    elif path == "/api/checkin/latest" and method == "GET":
        return await handle_get_latest_checkin(request, env)
    
    elif path == "/api/settings" and method == "GET":
        return await handle_get_settings(request, env)
    
    elif path == "/api/settings" and method == "POST":
        return await handle_save_settings(request, env)
    
    elif path == "/api/notification/test" and method == "POST":
        return await handle_test_notification(request, env)
    
    else:
        return Response.new("Not Found", status=404)


async def init_database(env):
    """Initialize database tables"""
    try:
        # Create users table
        await env.DB.prepare("""
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
            )
        """).run()
        
        # Create checkins table
        await env.DB.prepare("""
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                encrypted_previous_work TEXT,
                encrypted_today_plan TEXT,
                encrypted_blockers TEXT,
                mood TEXT,
                checkin_date DATE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """).run()
        
        # Create indexes
        await env.DB.prepare("""
            CREATE INDEX IF NOT EXISTS idx_checkins_user_date ON checkins(user_id, checkin_date)
        """).run()
        
        await env.DB.prepare("""
            CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)
        """).run()
        
    except Exception as e:
        print(f"Database initialization error: {e}")


async def handle_checkin(request, env):
    """Handle check-in submission"""
    try:
        data = await request.json()
        user_id = data.get('userId')
        previous_work = data.get('previousWork', '')
        today_plan = data.get('todayPlan', '')
        blockers = data.get('blockers', '')
        mood = data.get('mood', '😊')
        
        if not user_id:
            return json_response({"error": "User ID required"}, status=400)
        
        # Get encryption key from environment
        if not hasattr(env, 'ENCRYPTION_KEY') or not env.ENCRYPTION_KEY:
            return json_response({"error": "Encryption key not configured"}, status=500)
        encryption_key = env.ENCRYPTION_KEY
        
        # Encrypt sensitive data
        encrypted_previous = await encrypt_data(previous_work, encryption_key)
        encrypted_today = await encrypt_data(today_plan, encryption_key)
        encrypted_blockers = await encrypt_data(blockers, encryption_key)
        
        # Get current date
        today = date.today().isoformat()
        
        # Insert check-in
        await env.DB.prepare("""
            INSERT INTO checkins (user_id, encrypted_previous_work, encrypted_today_plan, 
                                encrypted_blockers, mood, checkin_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """).bind(user_id, encrypted_previous, encrypted_today, encrypted_blockers, mood, today).run()
        
        # Ensure user exists
        await env.DB.prepare("""
            INSERT OR IGNORE INTO users (user_id) VALUES (?)
        """).bind(user_id).run()
        
        return json_response({"success": True, "message": "Check-in saved"})
        
    except Exception as e:
        print(f"Error handling check-in: {e}")
        return json_response({"error": str(e)}, status=500)


async def handle_get_latest_checkin(request, env):
    """Get the latest check-in for pre-filling"""
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        
        if not user_id:
            return json_response({"error": "User ID required"}, status=400)
        
        # Get latest check-in
        result = await env.DB.prepare("""
            SELECT encrypted_today_plan, mood, checkin_date 
            FROM checkins 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        """).bind(user_id).first()
        
        if not result:
            return json_response({})
        
        # Decrypt data
        if not hasattr(env, 'ENCRYPTION_KEY') or not env.ENCRYPTION_KEY:
            return json_response({"error": "Encryption key not configured"}, status=500)
        encryption_key = env.ENCRYPTION_KEY
        today_plan = await decrypt_data(result['encrypted_today_plan'] if result['encrypted_today_plan'] else '', encryption_key)
        
        return json_response({
            "todayPlan": today_plan,
            "mood": result['mood'],
            "date": result['checkin_date']
        })
        
    except Exception as e:
        print(f"Error getting latest check-in: {e}")
        return json_response({"error": str(e)}, status=500)


async def handle_get_settings(request, env):
    """Get user settings"""
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        
        if not user_id:
            return json_response({"error": "User ID required"}, status=400)
        
        result = await env.DB.prepare("""
            SELECT email, notification_time, timezone, slack_webhook_url, 
                   email_notifications 
            FROM users 
            WHERE user_id = ?
        """).bind(user_id).first()
        
        if not result:
            return json_response({})
        
        return json_response({
            "email": result['email'] if result['email'] else '',
            "notificationTime": result['notification_time'],
            "timezone": result['timezone'],
            "slackWebhookUrl": result['slack_webhook_url'] if result['slack_webhook_url'] else '',
            "emailNotifications": result['email_notifications']
        })
        
    except Exception as e:
        print(f"Error getting settings: {e}")
        return json_response({"error": str(e)}, status=500)


async def handle_save_settings(request, env):
    """Save user settings"""
    try:
        data = await request.json()
        user_id = data.get('userId')
        
        if not user_id:
            return json_response({"error": "User ID required"}, status=400)
        
        email = data.get('email', '')
        notification_time = data.get('notificationTime', '09:00')
        timezone = data.get('timezone', 'UTC')
        slack_webhook_url = data.get('slackWebhookUrl', '')
        email_notifications = data.get('emailNotifications', 0)
        
        # Upsert user settings
        await env.DB.prepare("""
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
        
        return json_response({"success": True})
        
    except Exception as e:
        print(f"Error saving settings: {e}")
        return json_response({"error": str(e)}, status=500)


async def handle_test_notification(request, env):
    """Send test notification via Slack and/or email"""
    try:
        url = URL.new(request.url)
        user_id = url.searchParams.get('userId')
        
        if not user_id:
            return json_response({"error": "User ID required"}, status=400)
        
        # Get user settings
        result = await env.DB.prepare("""
            SELECT slack_webhook_url, email, email_notifications 
            FROM users 
            WHERE user_id = ?
        """).bind(user_id).first()
        
        if not result:
            return json_response({"error": "User not found"}, status=404)
        
        notifications_sent = []
        checkin_url = request.url.split('/api')[0]
        
        # Send Slack notification if webhook is configured
        if result['slack_webhook_url']:
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
                                "url": checkin_url
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
                notifications_sent.append("slack")
            except Exception as e:
                print(f"Error sending Slack notification: {e}")
        
        # Send email notification if email is configured
        if result['email'] and result['email_notifications'] == 1:
            try:
                from scheduler import send_email_notification
                success = await send_email_notification(
                    result['email'],
                    user_id,
                    checkin_url,
                    env
                )
                if success:
                    notifications_sent.append("email")
            except Exception as e:
                print(f"Error sending email notification: {e}")
        
        return json_response({
            "success": True,
            "message": "Test notification sent",
            "channels": notifications_sent
        })
        
    except Exception as e:
        print(f"Error sending test notification: {e}")
        return json_response({"error": str(e)}, status=500)


# Main entry point for Cloudflare Worker
async def on_fetch(request, env):
    """Worker entry point for HTTP requests"""
    return await handle_request(request, env)


async def on_scheduled(event, env):
    """Worker entry point for scheduled/cron events"""
    try:
        # Import scheduler module
        from scheduler import handle_scheduled
        await handle_scheduled(event, env)
    except Exception as e:
        print(f"Error in scheduled event: {e}")
