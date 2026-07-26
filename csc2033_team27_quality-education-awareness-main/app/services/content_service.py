"""Public content and take-action services."""

from datetime import datetime, timezone

import requests
from flask import current_app
from itsdangerous import BadData, URLSafeSerializer

from app.repositories import mail_repository


def get_home_context():
    """Return the home page chart and indicator content."""
    return {
        "labels": ["High-income", "Upper-middle", "Lower-middle", "Low-income"],
        "values": [70, 22, 7, 3],
        "info": {
            "High-income": "Most global education spending comes from wealthy countries.",
            "Upper-middle": "Moderate contribution to global education funding.",
            "Lower-middle": "Limited resources but growing investment.",
            "Low-income": "Severely underfunded education systems.",
        },
    }


def get_stats_context():
    """Return the statistics page content."""
    return {
        "labels": [
            "High Income Countries",
            "Upper Middle Income Countries",
            "Lower middle income countires",
            "Low income countries",
        ],
        "values": [65, 20, 10, 5],
        "info": {
            "High Income Countries": "Test",
            "Upper Middle Income Countries": "This is a PlaceHolder.",
            "Lower middle income countires": "This is a PlaceHolder.",
            "Low income countries": "This is a PlaceHolder.",
        },
    }


def subscribe_email(email):
    """Create a mailing-list subscription and return an unsubscribe token."""
    if mail_repository.get_subscriber(email):
        return {"ok": False, "category": "warning", "message": "Email already signed up to take action"}

    mail_repository.add_subscriber(email)
    serializer = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="unsubscribe")
    return {
        "ok": True,
        "category": "success",
        "message": "Thanks for signing up to take action",
        "token": serializer.dumps(email),
    }


def unsubscribe_email(token):
    """Remove a mailing-list subscription identified by the token."""
    serializer = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="unsubscribe")
    try:
        email = serializer.loads(token)
    except BadData:
        return {"ok": False, "category": "danger", "message": "Invalid or expired token"}

    if mail_repository.delete_subscriber(email):
        return {"ok": True, "category": "success", "message": "You have successfully unsubscribed"}
    return {"ok": False, "category": "danger", "message": "Email is already unsubscribed"}


def build_calendar_events():
    """Fetch calendar events and fall back to an empty list when unavailable."""
    api_key = current_app.config.get("GOOGLE_API_KEY")
    calendar_id = current_app.config.get("GOOGLE_CALENDAR_ID")
    if not api_key or not calendar_id:
        return []

    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
    params = {
        "key": api_key,
        "timeMin": datetime.now(timezone.utc).isoformat(),
        "singleEvents": True,
        "orderBy": "startTime",
        "maxResults": 10,
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return []

    events = []
    for event in data.get("items", []):
        start_data = event.get("start", {})
        end_data = event.get("end", {})
        events.append(
            {
                "title": event.get("summary", "No title"),
                "start": start_data.get("dateTime", start_data.get("date")),
                "end": end_data.get("dateTime", end_data.get("date")),
            }
        )
    return events
