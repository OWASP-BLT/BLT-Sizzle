"""
Configuration for Sizzle app with safe defaults for standalone usage.
Follows Django's AUTH_USER_MODEL pattern for swappable models.

Key principle: All external model integrations are OPTIONAL and default to None.
This ensures Sizzle works as a standalone plugin without breaking.
"""
from django.conf import settings

# Sizzle configuration - makes the plugin flexible for different Django projects
SIZZLE_SETTINGS = {
    # Default base template for standalone projects
    "BASE_TEMPLATE": getattr(settings, "SIZZLE_BASE_TEMPLATE", "base.html"),
    # Parent base template - set this in your main project for integration
    "PARENT_BASE": getattr(settings, "SIZZLE_PARENT_BASE", None),
    # Whether to integrate with the parent project's layout
    "USE_PROJECT_BASE": getattr(settings, "SIZZLE_USE_PROJECT_BASE", True),
    # Show sidenav if available (for BLT integration)
    "SHOW_SIDENAV": getattr(settings, "SIZZLE_SHOW_SIDENAV", True),
}

# ===============================
# Model Configuration (Optional External Integrations)
# ===============================
# 
# IMPORTANT: All external model integrations default to None to ensure
# Sizzle works standalone. Host projects can optionally enable integrations
# by setting these in their Django settings.

# Slack Integration Model (optional)
# Example: SIZZLE_SLACK_INTEGRATION_MODEL = "myapp.SlackIntegration"
SIZZLE_SLACK_INTEGRATION_MODEL = getattr(
    settings,
    "SIZZLE_SLACK_INTEGRATION_MODEL", 
    None  # Default: disabled, no external dependency
)

# Organization Model (optional)
# Example: SIZZLE_ORGANIZATION_MODEL = "myapp.Organization"
SIZZLE_ORGANIZATION_MODEL = getattr(
    settings,
    "SIZZLE_ORGANIZATION_MODEL",
    None  # Default: disabled, no external dependency
)

# UserProfile Model (optional)
# Example: SIZZLE_USERPROFILE_MODEL = "myapp.UserProfile"
SIZZLE_USERPROFILE_MODEL = getattr(
    settings,
    "SIZZLE_USERPROFILE_MODEL",
    None  # Default: disabled, no external dependency
)

# Notification Model (optional)
# Example: SIZZLE_NOTIFICATION_MODEL = "myapp.Notification"
SIZZLE_NOTIFICATION_MODEL = getattr(
    settings,
    "SIZZLE_NOTIFICATION_MODEL",
    None  # Default: disabled, no external dependency
)

# ===============================
# Feature Flags
# ===============================

# Enable/disable features
SIZZLE_SLACK_ENABLED = getattr(
    settings,
    "SIZZLE_SLACK_ENABLED",
    True,  # Enabled by default for BLT
)

SIZZLE_EMAIL_REMINDERS_ENABLED = getattr(settings, "SIZZLE_EMAIL_REMINDERS_ENABLED", True)

SIZZLE_DAILY_CHECKINS_ENABLED = getattr(settings, "SIZZLE_DAILY_CHECKINS_ENABLED", True)


def get_base_template():
    """Get the appropriate base template for sizzle templates"""
    if SIZZLE_SETTINGS["PARENT_BASE"]:
        return SIZZLE_SETTINGS["PARENT_BASE"]
    return SIZZLE_SETTINGS["BASE_TEMPLATE"]
