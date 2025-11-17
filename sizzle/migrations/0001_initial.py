# Generated for blt-sizzle standalone compatibility

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                ("duration", models.DurationField(blank=True, null=True)),
                ("github_issue_url", models.URLField(blank=True, null=True)),
                ("created", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                # Organization integration is now optional via separate fields
                ("organization_id", models.PositiveIntegerField(
                    blank=True, 
                    help_text='Optional organization reference - safe for standalone usage', 
                    null=True
                )),
                ("organization_model", models.CharField(
                    blank=True, 
                    help_text='Model path for organization (e.g., \'myapp.Organization\')', 
                    max_length=255, 
                    null=True
                )),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sizzle_time_logs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReminderSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reminder_time", models.TimeField(help_text="Time to send daily reminders (in user's timezone)")),
                (
                    "reminder_time_utc",
                    models.TimeField(blank=True, help_text="Time to send daily reminders (in UTC)", null=True),
                ),
                ("timezone", models.CharField(default="UTC", max_length=50)),
                ("is_active", models.BooleanField(default=True, help_text="Enable/disable daily reminders")),
                ("last_reminder_sent", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sizzle_reminder_settings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Reminder Settings",
                "verbose_name_plural": "Reminder Settings",
                "indexes": [
                    models.Index(fields=["is_active"], name="sizzle_remi_is_acti_dde965_idx"),
                    models.Index(fields=["reminder_time_utc"], name="sizzle_remi_reminde_8c6dc9_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="DailyStatusReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("previous_work", models.TextField()),
                ("next_plan", models.TextField()),
                ("blockers", models.TextField()),
                ("goal_accomplished", models.BooleanField(default=False)),
                ("current_mood", models.CharField(default="Happy 😊", max_length=50)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sizzle_daily_status_reports",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
                "indexes": [models.Index(fields=["user", "date"], name="sizzle_dail_user_id_667d52_idx")],
                "unique_together": {("user", "date")},
            },
        ),
    ]
