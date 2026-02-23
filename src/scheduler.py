"""
Scheduled notification handler for daily check-in reminders.
This script is triggered by Cloudflare Workers cron triggers.
"""

from js import fetch, Date
import json


async def send_slack_notification(webhook_url, user_email, checkin_url):
    """Send Slack notification to user"""
    message = {
        "text": "🔔 Daily Check-in Reminder",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Good morning! Time for your daily check-in* ✨\n\nTake a moment to reflect on your progress and plan your day."
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*What to include:*\n• What you accomplished previously\n• Your plans for today\n• Any blockers or challenges\n• How you're feeling"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📝 Fill Check-in Form",
                            "emoji": True
                        },
                        "style": "primary",
                        "url": checkin_url,
                        "action_id": "checkin_button"
                    }
                ]
            }
        ]
    }
    
    try:
        response = await fetch(webhook_url, {
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(message)
        })
        return response.ok
    except Exception as e:
        print(f"Error sending Slack notification: {e}")
        return False


async def send_email_notification(email, user_name, checkin_url, env):
    """Send email notification to user"""
    
    # Check if email provider is configured
    if not hasattr(env, 'EMAIL_API_KEY') or not env.EMAIL_API_KEY:
        print("Email notifications not configured")
        return False
    
    email_provider = getattr(env, 'EMAIL_PROVIDER', 'sendgrid')
    
    # Email HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }}
            .content {{
                background: #f9fafb;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 14px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                margin: 20px 0;
            }}
            .checklist {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .checklist-item {{
                padding: 8px 0;
            }}
            .footer {{
                text-align: center;
                color: #666;
                font-size: 12px;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📝 Daily Check-in Reminder</h1>
            <p>Time to reflect and plan your day</p>
        </div>
        <div class="content">
            <p>Good morning!</p>
            <p>It's time for your daily check-in. Take a few minutes to document your progress and set your intentions for today.</p>
            
            <div class="checklist">
                <h3>What to include:</h3>
                <div class="checklist-item">✓ What you accomplished previously</div>
                <div class="checklist-item">✓ Your plans for today</div>
                <div class="checklist-item">✓ Any blockers or challenges</div>
                <div class="checklist-item">✓ How you're feeling</div>
            </div>
            
            <center>
                <a href="{checkin_url}" class="button">Fill Check-in Form</a>
            </center>
            
            <p style="margin-top: 30px; font-size: 14px; color: #666;">
                This reminder was sent to you based on your notification preferences. 
                You can update your settings anytime in the app.
            </p>
        </div>
        <div class="footer">
            <p>BLT Sizzle Check-in App</p>
            <p>You're receiving this because you enabled email notifications</p>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Daily Check-in Reminder
    
    Good morning!
    
    It's time for your daily check-in. Take a few minutes to document your progress and set your intentions for today.
    
    What to include:
    - What you accomplished previously
    - Your plans for today
    - Any blockers or challenges
    - How you're feeling
    
    Click here to fill out your check-in: {checkin_url}
    
    ---
    BLT Sizzle Check-in App
    """
    
    # Send via configured provider
    if email_provider == 'sendgrid':
        return await send_via_sendgrid(email, html_content, text_content, env)
    elif email_provider == 'mailgun':
        return await send_via_mailgun(email, html_content, text_content, env)
    else:
        print(f"Unsupported email provider: {email_provider}")
        return False


async def send_via_sendgrid(to_email, html_content, text_content, env):
    """Send email via SendGrid API"""
    url = "https://api.sendgrid.com/v3/mail/send"
    
    data = {
        "personalizations": [
            {
                "to": [{"email": to_email}]
            }
        ],
        "from": {
            "email": env.EMAIL_FROM if hasattr(env, 'EMAIL_FROM') else "noreply@example.com",
            "name": "BLT Sizzle Check-in"
        },
        "subject": "📝 Daily Check-in Reminder",
        "content": [
            {
                "type": "text/plain",
                "value": text_content
            },
            {
                "type": "text/html",
                "value": html_content
            }
        ]
    }
    
    try:
        response = await fetch(url, {
            "method": "POST",
            "headers": {
                "Authorization": f"Bearer {env.EMAIL_API_KEY}",
                "Content-Type": "application/json"
            },
            "body": json.dumps(data)
        })
        return response.ok
    except Exception as e:
        print(f"Error sending via SendGrid: {e}")
        return False


async def send_via_mailgun(to_email, html_content, text_content, env):
    """Send email via Mailgun API"""
    domain = env.EMAIL_DOMAIN if hasattr(env, 'EMAIL_DOMAIN') else "mg.example.com"
    url = f"https://api.mailgun.net/v3/{domain}/messages"
    
    form_data = {
        "from": f"BLT Sizzle Check-in <{env.EMAIL_FROM if hasattr(env, 'EMAIL_FROM') else 'noreply@example.com'}>",
        "to": to_email,
        "subject": "📝 Daily Check-in Reminder",
        "text": text_content,
        "html": html_content
    }
    
    try:
        # Mailgun uses basic auth
        import base64
        from urllib.parse import urlencode
        auth = base64.b64encode(f"api:{env.EMAIL_API_KEY}".encode()).decode()
        
        # Properly URL-encode form data
        encoded_body = urlencode(form_data)
        
        response = await fetch(url, {
            "method": "POST",
            "headers": {
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "body": encoded_body
        })
        return response.ok
    except Exception as e:
        print(f"Error sending via Mailgun: {e}")
        return False


async def handle_scheduled(event, env):
    """
    Handle scheduled cron trigger.
    This function is called by Cloudflare Workers cron.
    """
    try:
        # Get current time in UTC
        current_time = Date.new().toISOString()
        current_hour = int(current_time.split('T')[1].split(':')[0])
        current_minute = int(current_time.split(':')[1])
        
        print(f"Running scheduled task at {current_hour}:{current_minute:02d} UTC")
        
        # Query users who need notifications at this time
        # We'll check for users with notification_time within the current hour
        results = await env.DB.prepare("""
            SELECT user_id, email, slack_webhook_url, notification_time, 
                   timezone, email_notifications, notification_enabled
            FROM users
            WHERE notification_enabled = 1
        """).all()
        
        if not results or not results['results']:
            print("No users with notifications enabled")
            return
        
        notifications_sent = 0
        checkin_url = f"https://{env.WORKER_HOST}" if hasattr(env, 'WORKER_HOST') else "https://your-worker.workers.dev"
        
        for user in results['results']:
            # Parse notification time
            try:
                notif_hour, notif_minute = map(int, user['notification_time'].split(':'))
                
                # Note: This is a simplified timezone handling
                # In production, use a proper timezone library to convert user's timezone to UTC
                # For now, assuming notification_time is already in UTC or within acceptable window
                # TODO: Add proper timezone conversion using pytz or similar library
                time_diff = abs((current_hour * 60 + current_minute) - (notif_hour * 60 + notif_minute))
                
                if time_diff <= 30:  # Within 30 minutes window
                    # Send Slack notification
                    if user['slack_webhook_url']:
                        success = await send_slack_notification(
                            user['slack_webhook_url'],
                            user['email'] or 'User',
                            checkin_url
                        )
                        if success:
                            notifications_sent += 1
                            print(f"Sent Slack notification to user {user['user_id']}")
                    
                    # Send email notification
                    if user['email'] and user['email_notifications'] == 1:
                        success = await send_email_notification(
                            user['email'],
                            user['user_id'],
                            checkin_url,
                            env
                        )
                        if success:
                            notifications_sent += 1
                            print(f"Sent email notification to {user['email']}")
                            
            except Exception as e:
                print(f"Error processing user {user['user_id']}: {e}")
                continue
        
        print(f"Scheduled task complete. Sent {notifications_sent} notifications.")
        
    except Exception as e:
        print(f"Error in scheduled handler: {e}")


async def on_scheduled(event, env):
    """Entry point for scheduled events"""
    return await handle_scheduled(event, env)
