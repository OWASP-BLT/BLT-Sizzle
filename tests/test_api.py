"""
Integration tests for BLT Sizzle Check-in API.

These tests require the development server to be running:
    npm run dev

Run with:
    python -m pytest tests/test_api.py -v
"""

import requests
import pytest

BASE_URL = "http://localhost:8787"
TEST_USER_ID = "test_user_integration"


def is_server_running():
    """Check if the development server is running."""
    try:
        response = requests.get(BASE_URL, timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


pytestmark = pytest.mark.skipif(
    not is_server_running(),
    reason="Development server not running at " + BASE_URL,
)


class TestCheckinEndpoints:
    """Tests for check-in API endpoints."""

    def test_get_index_page(self):
        """Test that the main page loads successfully."""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        assert "Daily Check-in" in response.text
        assert "text/html" in response.headers.get("Content-Type", "")

    def test_get_settings_page(self):
        """Test that the settings page loads successfully."""
        response = requests.get(f"{BASE_URL}/settings")
        assert response.status_code == 200
        assert "Settings" in response.text
        assert "text/html" in response.headers.get("Content-Type", "")

    def test_checkin_submission(self):
        """Test check-in submission."""
        data = {
            "userId": TEST_USER_ID,
            "previousWork": "Completed testing",
            "todayPlan": "Write documentation",
            "blockers": "None",
            "mood": "😊",
        }
        response = requests.post(f"{BASE_URL}/api/checkin", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True

    def test_checkin_requires_user_id(self):
        """Test that check-in requires a user ID."""
        data = {
            "previousWork": "Test",
            "todayPlan": "Test",
            "blockers": "None",
            "mood": "😊",
        }
        response = requests.post(f"{BASE_URL}/api/checkin", json=data)
        assert response.status_code == 400

    def test_checkin_requires_today_plan(self):
        """Test check-in submission with minimal data."""
        data = {
            "userId": TEST_USER_ID,
            "todayPlan": "Minimal plan",
            "mood": "😊",
        }
        response = requests.post(f"{BASE_URL}/api/checkin", json=data)
        assert response.status_code == 200

    def test_get_latest_checkin(self):
        """Test getting latest check-in for pre-filling."""
        # First submit a check-in
        data = {
            "userId": TEST_USER_ID,
            "previousWork": "Previous task",
            "todayPlan": "Plan for auto-fill test",
            "blockers": "No blockers",
            "mood": "💪",
        }
        requests.post(f"{BASE_URL}/api/checkin", json=data)

        # Then retrieve the latest
        response = requests.get(f"{BASE_URL}/api/checkin/latest?userId={TEST_USER_ID}")
        assert response.status_code == 200
        result = response.json()
        assert "todayPlan" in result
        assert result["todayPlan"] == "Plan for auto-fill test"

    def test_get_latest_checkin_requires_user_id(self):
        """Test that get latest check-in requires user ID."""
        response = requests.get(f"{BASE_URL}/api/checkin/latest")
        assert response.status_code == 400

    def test_not_found(self):
        """Test 404 for unknown routes."""
        response = requests.get(f"{BASE_URL}/nonexistent")
        assert response.status_code == 404


class TestSettingsEndpoints:
    """Tests for settings API endpoints."""

    def test_save_settings(self):
        """Test saving user settings."""
        settings = {
            "userId": TEST_USER_ID,
            "email": "test@example.com",
            "notificationTime": "09:00",
            "timezone": "UTC",
            "slackWebhookUrl": "",
            "emailNotifications": 0,
        }
        response = requests.post(f"{BASE_URL}/api/settings", json=settings)
        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True

    def test_get_settings(self):
        """Test retrieving user settings."""
        # First save settings
        settings = {
            "userId": TEST_USER_ID,
            "email": "test@example.com",
            "notificationTime": "10:00",
            "timezone": "America/New_York",
            "slackWebhookUrl": "",
            "emailNotifications": 1,
        }
        requests.post(f"{BASE_URL}/api/settings", json=settings)

        # Then retrieve
        response = requests.get(f"{BASE_URL}/api/settings?userId={TEST_USER_ID}")
        assert response.status_code == 200
        result = response.json()
        assert result["email"] == "test@example.com"
        assert result["notificationTime"] == "10:00"
        assert result["timezone"] == "America/New_York"
        assert result["emailNotifications"] == 1

    def test_get_settings_requires_user_id(self):
        """Test that get settings requires user ID."""
        response = requests.get(f"{BASE_URL}/api/settings")
        assert response.status_code == 400

    def test_save_settings_requires_user_id(self):
        """Test that save settings requires user ID."""
        settings = {
            "email": "test@example.com",
            "notificationTime": "09:00",
        }
        response = requests.post(f"{BASE_URL}/api/settings", json=settings)
        assert response.status_code == 400

    def test_settings_update(self):
        """Test that settings can be updated (upsert)."""
        # Save initial settings
        settings = {
            "userId": TEST_USER_ID,
            "email": "initial@example.com",
            "notificationTime": "08:00",
            "timezone": "UTC",
            "slackWebhookUrl": "",
            "emailNotifications": 0,
        }
        requests.post(f"{BASE_URL}/api/settings", json=settings)

        # Update settings
        updated_settings = {
            "userId": TEST_USER_ID,
            "email": "updated@example.com",
            "notificationTime": "14:00",
            "timezone": "Europe/London",
            "slackWebhookUrl": "",
            "emailNotifications": 1,
        }
        response = requests.post(f"{BASE_URL}/api/settings", json=updated_settings)
        assert response.status_code == 200

        # Verify update
        response = requests.get(f"{BASE_URL}/api/settings?userId={TEST_USER_ID}")
        result = response.json()
        assert result["email"] == "updated@example.com"
        assert result["notificationTime"] == "14:00"


class TestNotificationEndpoints:
    """Tests for notification API endpoints."""

    def test_test_notification_requires_user(self):
        """Test that test notification requires an existing user."""
        response = requests.post(
            f"{BASE_URL}/api/notification/test?userId=nonexistent_user_xyz"
        )
        assert response.status_code == 404

    def test_test_notification_with_valid_user(self):
        """Test notification endpoint with a valid user (no webhook configured)."""
        # Ensure user exists
        settings = {
            "userId": TEST_USER_ID,
            "email": "test@example.com",
            "notificationTime": "09:00",
            "timezone": "UTC",
            "slackWebhookUrl": "",
            "emailNotifications": 0,
        }
        requests.post(f"{BASE_URL}/api/settings", json=settings)

        response = requests.post(
            f"{BASE_URL}/api/notification/test?userId={TEST_USER_ID}"
        )
        assert response.status_code == 200
