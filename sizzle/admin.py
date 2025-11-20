from django.contrib import admin

from .models import DailyStatusReport, ReminderSettings

@admin.register(DailyStatusReport)
class DailyStatusReportAdmin(admin.ModelAdmin):
    pass


@admin.register(ReminderSettings)
class ReminderSettingsAdmin(admin.ModelAdmin):
    pass
