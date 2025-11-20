import logging
from collections import defaultdict
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from rest_framework import status

# Safe import for Token model - handle standalone mode
try:
    from rest_framework.authtoken.models import Token
    AUTHTOKEN_AVAILABLE = True
except ImportError:
    AUTHTOKEN_AVAILABLE = False

from sizzle.utils.model_loader import get_daily_status_report_model, get_organization_model

logger = logging.getLogger(__name__)


def sizzle_docs(request):
    return render(request, "sizzle_docs.html")


def sizzle(request):
    # Get models dynamically
    DailyStatusReport = get_daily_status_report_model()

    # Get recent daily status reports for display
    recent_reports = []
    if request.user.is_authenticated:
        recent_reports = (
            DailyStatusReport.objects.filter(user=request.user)
            .order_by("-date")
            .select_related("user")
            [:5]  # Show last 5 reports
        )

    # Get all users who have submitted reports (for community visibility)
    active_users = (
        DailyStatusReport.objects.values("user__username")
        .distinct()
        .order_by("user__username")
    )

    return render(
        request,
        "sizzle.html",
        {
            "recent_reports": recent_reports,
            "active_users": active_users,
        },
    )


def checkIN(request):
    from datetime import date

    # Get models dynamically
    DailyStatusReport = get_daily_status_report_model()

    # Find the most recent date that has data
    last_report = DailyStatusReport.objects.order_by("-date").first()
    if last_report:
        default_start_date = last_report.date
        default_end_date = last_report.date
    else:
        # If no data at all, fallback to today
        default_start_date = date.today()
        default_end_date = date.today()

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            start_date = default_start_date
            end_date = default_end_date
    else:
        # No date range provided, use the default (most recent date with data)
        start_date = default_start_date
        end_date = default_end_date

    reports = (
        DailyStatusReport.objects.filter(date__range=(start_date, end_date))
        .select_related("user")
        .order_by("date", "created")
    )

    data = []
    for r in reports:
        data.append(
            {
                "id": r.id,
                "username": r.user.username,
                "previous_work": truncate_text(r.previous_work),
                "next_plan": truncate_text(r.next_plan),
                "blockers": truncate_text(r.blockers),
                "goal_accomplished": r.goal_accomplished,  # Add this line
                "current_mood": r.current_mood,  # Add this line
                "date": r.date.strftime("%d %B %Y"),
            }
        )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(data, safe=False)

    # Render template with initial data if needed
    return render(
        request,
        "checkin.html",
        {
            "data": data,
            "default_start_date": default_start_date.isoformat(),
            "default_end_date": default_end_date.isoformat(),
        },
    )


def truncate_text(text, length=15):
    return text if len(text) <= length else text[:length] + "..."


@login_required
def add_sizzle_checkIN(request):
    # Get models dynamically
    DailyStatusReport = get_daily_status_report_model()

    # Check if user already has a report for today
    today = now().date()
    today_report = DailyStatusReport.objects.filter(user=request.user, date=today).first()

    # Fetch yesterday's report
    yesterday = now().date() - timedelta(days=1)
    yesterday_report = DailyStatusReport.objects.filter(user=request.user, date=yesterday).first()

    # Fetch all check-ins for the user, ordered by date
    all_checkins = DailyStatusReport.objects.filter(user=request.user).order_by("-date")

    return render(
        request,
        "add_sizzle_checkin.html",
        {
            "today_report": today_report,
            "yesterday_report": yesterday_report, 
            "all_checkins": all_checkins
        },
    )


@login_required
def checkIN_detail(request, report_id):
    DailyStatusReport = get_daily_status_report_model()
    report = get_object_or_404(DailyStatusReport, pk=report_id)

    # Restrict to own reports or authorized users
    if report.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to view this report.")

    context = {
        "username": report.user.username,
        "date": report.date.strftime("%d %B %Y"),
        "previous_work": report.previous_work,
        "next_plan": report.next_plan,
        "blockers": report.blockers,
    }
    return render(request, "checkin_detail.html", context)

@login_required
def sizzle_daily_log(request):
    # Get models dynamically
    DailyStatusReport = get_daily_status_report_model()

    try:
        if request.method == "GET":
            reports = DailyStatusReport.objects.filter(user=request.user).order_by("-date")
            return render(request, "sizzle_daily_status.html", {"reports": reports})

        if request.method == "POST":
            previous_work = request.POST.get("previous_work")
            next_plan = request.POST.get("next_plan")
            blockers = request.POST.get("blockers")
            goal_accomplished = request.POST.get("goal_accomplished") == "on"
            current_mood = request.POST.get("feeling")
            print(previous_work, next_plan, blockers, goal_accomplished, current_mood)

            DailyStatusReport.objects.create(
                user=request.user,
                date=now().date(),
                previous_work=previous_work,
                next_plan=next_plan,
                blockers=blockers,
                goal_accomplished=goal_accomplished,
                current_mood=current_mood,
            )

            messages.success(request, "Daily status report submitted successfully.")
            return redirect("add_sizzle_checkin")

    except (ValidationError, IntegrityError) as e:
        logger.exception("Error creating daily status report")
        # Check if this is a unique constraint violation for user+date
        if "UNIQUE constraint failed" in str(e) and "user_id" in str(e) and "date" in str(e):
            messages.error(request, "You have already submitted a daily check-in for today. You can only submit one report per day.")
        else:
            messages.error(request, "An error occurred while submitting your report. Please try again.")
        return redirect("add_sizzle_checkin")

    return HttpResponseBadRequest("Invalid request method.")


@login_required
def user_sizzle_report(request, username):
    # Get models dynamically
    DailyStatusReport = get_daily_status_report_model()

    user_model = get_user_model()
    user = get_object_or_404(user_model, username=username)
    
    # Get daily status reports for the user
    reports = (
        DailyStatusReport.objects.filter(user=user)
        .order_by("-date")
        .select_related("user")
    )

    response_data = []
    for report in reports:
        response_data.append({
            "date": report.date.strftime("%d %B %Y"),
            "previous_work": report.previous_work,
            "next_plan": report.next_plan,
            "blockers": report.blockers,
            "goal_accomplished": "Yes" if report.goal_accomplished else "No",
            "current_mood": report.current_mood,
            "created": report.created.strftime("%I:%M %p"),
        })

    return render(
        request,
        "user_sizzle_report.html",
        {"response_data": response_data, "user": user},
    )
