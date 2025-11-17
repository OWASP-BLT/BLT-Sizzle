import logging
from datetime import datetime

import pytz
from django.conf import settings
from django.db import models
from django.utils import timezone

from .utils.model_loader import get_organization_model

logger = logging.getLogger(__name__)


class TimeLog(models.Model):
    """
    Time tracking model for sizzle functionality.
    
    Uses optional organization integration - if no organization model
    is configured, the organization field will remain None and the
    TimeLog will work perfectly fine as a standalone time tracker.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="sizzle_time_logs"
    )
    
    # Organization integration is completely optional
    # This field will remain None if no organization model is configured
    organization_id = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Optional organization reference - safe for standalone usage"
    )
    organization_model = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Model path for organization (e.g., 'myapp.Organization')"
    )
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    github_issue_url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, editable=False)

    @property
    def organization(self):
        """
        Safely get the organization object if available.
        Returns None if no organization model is configured or object doesn't exist.
        """
        if not self.organization_id or not self.organization_model:
            return None
            
        OrganizationModel = get_organization_model()
        if not OrganizationModel:
            return None
            
        try:
            return OrganizationModel.objects.get(id=self.organization_id)
        except (OrganizationModel.DoesNotExist, AttributeError):
            return None

    def set_organization(self, org_obj):
        """
        Safely set the organization if available.
        Does nothing if no organization model is configured.
        """
        if not org_obj:
            self.organization_id = None
            self.organization_model = None
            return
            
        OrganizationModel = get_organization_model()
        if not OrganizationModel or not isinstance(org_obj, OrganizationModel):
            return
            
        self.organization_id = org_obj.id
        self.organization_model = f"{org_obj._meta.app_label}.{org_obj._meta.object_name}"

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time <= self.end_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        org_name = ""
        if self.organization:
            org_name = f" ({getattr(self.organization, 'name', 'Unknown Org')})"
        return f"TimeLog by {self.user.username}{org_name} from {self.start_time} to {self.end_time}"


class DailyStatusReport(models.Model):
    """Daily status report for team check-ins"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sizzle_daily_status_reports"
    )
    date = models.DateField()
    previous_work = models.TextField()
    next_plan = models.TextField()
    blockers = models.TextField()
    goal_accomplished = models.BooleanField(default=False)
    current_mood = models.CharField(max_length=50, default="Happy 😊")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]

    def __str__(self):
        return f"Daily Status Report by {self.user.username} on {self.date}"


class ReminderSettings(models.Model):
    """User settings for daily reminder notifications"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sizzle_reminder_settings"
    )
    reminder_time = models.TimeField(help_text="Time to send daily reminders (in user's timezone)")
    reminder_time_utc = models.TimeField(help_text="Time to send daily reminders (in UTC)", null=True, blank=True)
    timezone = models.CharField(max_length=50, default="UTC")
    is_active = models.BooleanField(default=True, help_text="Enable/disable daily reminders")
    last_reminder_sent = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reminder Settings"
        verbose_name_plural = "Reminder Settings"
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["reminder_time_utc"]),
        ]

    def __str__(self):
        return f"Reminder Settings for {self.user.username}"

    def save(self, *args, **kwargs):
        if self.reminder_time and self.timezone:
            user_tz = pytz.timezone(self.timezone)
            # Create a datetime with today's date and the reminder time
            today = timezone.now().date()
            local_dt = user_tz.localize(datetime.combine(today, self.reminder_time))
            # Convert to UTC
            utc_dt = local_dt.astimezone(pytz.UTC)
            # Extract just the time part
            self.reminder_time_utc = utc_dt.time()
        super().save(*args, **kwargs)

    @classmethod
    def get_timezone_choices(cls):
        if not hasattr(cls, "_timezone_choices"):
            cls._timezone_choices = [(tz, tz) for tz in pytz.common_timezones]
        return cls._timezone_choices
