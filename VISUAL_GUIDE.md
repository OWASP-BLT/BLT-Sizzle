# Visual Guide

This guide provides a visual walkthrough of the BLT Sizzle Check-in application.

## Application Screenshots

### Main Check-in Form

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │                   📝 Daily Check-in                      │ │
│  │         Share your progress and plan for today          │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────┐    │ │
│  │  │ What did you do since last check-in?           │    │ │
│  │  │ ┌───────────────────────────────────────────┐  │    │ │
│  │  │ │ Completed API integration                 │  │    │ │
│  │  │ │ Reviewed pull requests                    │  │    │ │
│  │  │ │ Fixed bug in authentication               │  │    │ │
│  │  │ └───────────────────────────────────────────┘  │    │ │
│  │  └─────────────────────────────────────────────────┘    │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────┐    │ │
│  │  │ What do you plan to do today? *               │    │ │
│  │  │ ┌───────────────────────────────────────────┐  │    │ │
│  │  │ │ Work on frontend components               │  │    │ │
│  │  │ │ Implement user settings page              │  │    │ │
│  │  │ │ Write unit tests                          │  │    │ │
│  │  │ └───────────────────────────────────────────┘  │    │ │
│  │  └─────────────────────────────────────────────────┘    │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────┐    │ │
│  │  │ Any blockers or challenges?                   │    │ │
│  │  │ ┌───────────────────────────────────────────┐  │    │ │
│  │  │ │ Waiting for API documentation             │  │    │ │
│  │  │ │                                           │  │    │ │
│  │  │ └───────────────────────────────────────────┘  │    │ │
│  │  └─────────────────────────────────────────────────┘    │ │
│  │                                                           │ │
│  │  How are you feeling today?                            │ │
│  │  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐           │ │
│  │  │😊│ │😐│ │😟│ │😫│ │🤗│ │🤔│ │😴│ │💪│           │ │
│  │  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘           │ │
│  │   ^selected                                            │ │
│  │                                                           │ │
│  │        ┌─────────────────────────────────┐              │ │
│  │        │    Submit Check-in              │              │ │
│  │        └─────────────────────────────────┘              │ │
│  │                                                           │ │
│  │              ⚙️ Notification Settings                   │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Settings Page

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │                    ⚙️ Settings                           │ │
│  │        Configure your notification preferences           │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────┐    │ │
│  │  │ Email Address (optional)                       │    │ │
│  │  │ ┌───────────────────────────────────────────┐  │    │ │
│  │  │ │ your.email@example.com                    │  │    │ │
│  │  │ └───────────────────────────────────────────┘  │    │ │
│  │  └─────────────────────────────────────────────────┘    │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────┐    │ │
│  │  │ Reminder Time                                  │    │ │
│  │  │ ┌───────────────────────────────────────────┐  │    │ │
│  │  │ │ 09:00                                     │  │    │ │
│  │  │ └───────────────────────────────────────────┘  │    │ │
│  │  └─────────────────────────────────────────────────┘    │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────┐    │ │
│  │  │ Timezone                                       │    │ │
│  │  │ ┌───────────────────────────────────────────┐  │    │ │
│  │  │ │ America/New_York ▼                        │  │    │ │
│  │  │ └───────────────────────────────────────────┘  │    │ │
│  │  └─────────────────────────────────────────────────┘    │ │
│  │                                                           │ │
│  │  ☑ Send email reminders                                │ │
│  │                                                           │ │
│  │  ┌───────────────────────────────────────────────────┐  │ │
│  │  │ 🔔 Slack Integration                            │  │ │
│  │  │                                                 │  │ │
│  │  │ To enable Slack notifications, create a        │  │ │
│  │  │ webhook URL and paste it below.                │  │ │
│  │  └───────────────────────────────────────────────────┘  │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────┐    │ │
│  │  │ Slack Webhook URL (optional)                   │    │ │
│  │  │ ┌───────────────────────────────────────────┐  │    │ │
│  │  │ │ https://hooks.slack.com/services/...      │  │    │ │
│  │  │ └───────────────────────────────────────────┘  │    │ │
│  │  └─────────────────────────────────────────────────┘    │ │
│  │                                                           │ │
│  │        ┌─────────────────────────────────┐              │ │
│  │        │    Save Settings                │              │ │
│  │        └─────────────────────────────────┘              │ │
│  │        ┌─────────────────────────────────┐              │ │
│  │        │    Test Notification            │              │ │
│  │        └─────────────────────────────────┘              │ │
│  │                                                           │ │
│  │              ← Back to Check-in                         │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Slack Notification Example

```
┌─────────────────────────────────────────────────────┐
│  BLT Sizzle Check-in                         4:09 PM │
├─────────────────────────────────────────────────────┤
│  🔔 Daily Check-in Reminder                         │
│                                                      │
│  Good morning! Time for your daily check-in ✨      │
│                                                      │
│  Take a moment to reflect on your progress and      │
│  plan your day.                                      │
│                                                      │
│  ────────────────────────────────────────────       │
│                                                      │
│  What to include:                                    │
│  • What you accomplished previously                  │
│  • Your plans for today                             │
│  • Any blockers or challenges                       │
│  • How you're feeling                               │
│                                                      │
│  ┌────────────────────────────┐                     │
│  │  📝 Fill Check-in Form      │                     │
│  └────────────────────────────┘                     │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Email Notification Example

```
┌────────────────────────────────────────────────────────────┐
│ From: BLT Sizzle Check-in <noreply@example.com>          │
│ Subject: 📝 Daily Check-in Reminder                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  📝 Daily Check-in Reminder                        │   │
│  │  Time to reflect and plan your day                 │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  Good morning!                                             │
│                                                            │
│  It's time for your daily check-in. Take a few minutes    │
│  to document your progress and set your intentions for    │
│  today.                                                    │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  What to include:                                  │   │
│  │  ✓ What you accomplished previously                │   │
│  │  ✓ Your plans for today                           │   │
│  │  ✓ Any blockers or challenges                     │   │
│  │  ✓ How you're feeling                             │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│              ┌──────────────────────────┐                 │
│              │  Fill Check-in Form      │                 │
│              └──────────────────────────┘                 │
│                                                            │
│  This reminder was sent to you based on your notification │
│  preferences. You can update your settings anytime in the │
│  app.                                                      │
│                                                            │
│  ────────────────────────────────────────────────────     │
│  BLT Sizzle Check-in App                                  │
│  You're receiving this because you enabled email          │
│  notifications                                             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Color Scheme

The application uses a beautiful gradient color scheme:

- **Primary Gradient**: `#667eea` to `#764ba2` (Purple gradient)
- **Success**: `#10b981` (Green)
- **Error**: `#ef4444` (Red)
- **Text**: `#333` (Dark gray)
- **Muted**: `#666` (Medium gray)
- **Background**: `#f9fafb` (Light gray)
- **Border**: `#e1e8ed` (Light border)

## Typography

- **Font Family**: System fonts (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto)
- **Heading**: 32px, bold
- **Body**: 14-16px, regular
- **Labels**: 14px, semi-bold

## UI Components

### Buttons

Primary buttons feature:
- Gradient background (purple to violet)
- White text
- Rounded corners (8px border-radius)
- Hover effects (slight lift and shadow)
- Full width on mobile

### Form Fields

All input fields have:
- 2px border
- 8px border-radius
- 12px padding
- Focus state with primary color border
- Smooth transitions

### Emoji Picker

- Large emoji display (32px)
- Hover state with background
- Selected state with border
- Touch-friendly spacing

## Responsive Design

The application is fully responsive:

### Desktop (>768px)
- Fixed width container (600px max)
- Centered on screen
- Full gradient background

### Mobile (<768px)
- Full width with padding
- Stack all elements vertically
- Touch-friendly button sizes
- Optimized emoji picker layout

## Accessibility Features

- Semantic HTML elements
- Proper labels for all form fields
- Keyboard navigation support
- Focus indicators
- Color contrast compliance
- Screen reader friendly

## Animation & Transitions

Smooth transitions on:
- Button hover/press states
- Form field focus
- Emoji picker selection
- Message appearances
- Page transitions

## User Flow Diagram

```
┌─────────────┐
│   Landing   │
│    Page     │
└──────┬──────┘
       │
       ▼
┌─────────────┐        ┌──────────────┐
│  Check-in   │◄───────┤  Pre-fill    │
│    Form     │        │  From Last   │
└──────┬──────┘        └──────────────┘
       │
       │ Submit
       ▼
┌─────────────┐
│   Encrypt   │
│    Data     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Store in   │
│     D1      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Success   │
│   Message   │
└─────────────┘

    Parallel Flow:
    
┌─────────────┐
│   Settings  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Configure   │
│ Slack/Email │
└──────┬──────┘
       │
       ▼
┌─────────────┐        ┌──────────────┐
│   Cron      │───────►│   Send       │
│  Trigger    │        │ Notification │
└─────────────┘        └──────────────┘
```

## Database Schema Visualization

```
┌─────────────────────────────┐
│          USERS              │
├─────────────────────────────┤
│ • id (PK)                   │
│ • user_id (UNIQUE)          │
│ • email                     │
│ • slack_user_id             │
│ • slack_webhook_url         │
│ • notification_time         │
│ • notification_enabled      │
│ • email_notifications       │
│ • timezone                  │
│ • created_at                │
│ • updated_at                │
└──────────┬──────────────────┘
           │
           │ 1:N
           ▼
┌─────────────────────────────┐
│        CHECKINS             │
├─────────────────────────────┤
│ • id (PK)                   │
│ • user_id (FK)              │
│ • encrypted_previous_work   │
│ • encrypted_today_plan      │
│ • encrypted_blockers        │
│ • mood                      │
│ • checkin_date              │
│ • created_at                │
└─────────────────────────────┘
```

## Technology Stack Visualization

```
┌─────────────────────────────────────────┐
│            FRONTEND                     │
│  HTML5 + CSS3 + Vanilla JavaScript      │
│  • Responsive Design                    │
│  • Modern UI/UX                         │
│  • Client-side Encryption               │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│       CLOUDFLARE WORKER                 │
│         Python Runtime                  │
│  • Request Routing                      │
│  • API Endpoints                        │
│  • Data Encryption                      │
│  • Scheduled Tasks                      │
└────────┬───────────────┬────────────────┘
         │               │
         ▼               ▼
┌────────────────┐  ┌──────────────────┐
│  D1 DATABASE   │  │  INTEGRATIONS    │
│  • SQLite      │  │  • Slack API     │
│  • Encrypted   │  │  • Email API     │
│  • Indexed     │  │  • Webhooks      │
└────────────────┘  └──────────────────┘
```

---

This visual guide provides a comprehensive overview of the application's design and architecture.
