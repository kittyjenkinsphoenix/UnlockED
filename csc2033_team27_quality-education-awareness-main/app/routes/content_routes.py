"""Public content routes and shared response handlers."""

from flask import current_app, flash, jsonify, redirect, render_template, url_for
from flask_mail import Message

from app import mail
from app.forms import TakeActionForm
from app.services.content_service import (
    build_calendar_events,
    get_home_context,
    get_stats_context,
    subscribe_email,
    unsubscribe_email,
)

from . import main


@main.after_request
def add_security_headers(response):
    """Attach a small set of security headers to every response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net"
    )
    return response


@main.route("/")
def home():
    """Render the public home page."""
    context = get_home_context()
    return render_template("home.html", **context)


@main.route("/stats")
def stats():
    """Render the public statistics page."""
    context = get_stats_context()
    return render_template("stats.html", **context)


@main.route("/take-action", methods=["GET", "POST"])
def take_action():
    """Render the take-action form and subscribe interested visitors."""
    form = TakeActionForm()
    if form.validate_on_submit():
        result = subscribe_email(form.email.data)
        flash(result["message"], result["category"])
        if result["ok"]:
            msg = Message(subject="Take Action", recipients=[form.email.data])
            msg.html = render_template("email/take_action_email.html", token=result["token"])
            mail.send(msg)
        return redirect(url_for("main.take_action"))
    return render_template("take_action.html", form=form)


@main.route("/unsubscribe/<token>")
def unsubscribe(token):
    """Remove a subscription using the signed unsubscribe token."""
    result = unsubscribe_email(token)
    flash(result["message"], result["category"])
    return redirect(url_for("main.take_action"))


@main.route("/api/calendar")
def calendar():
    """Return upcoming calendar events in JSON format."""
    events = build_calendar_events()
    return jsonify(events)


@main.app_errorhandler(400)
def bad_request(error):
    """Render the 400 error page."""
    return render_template("400.html"), 400


@main.app_errorhandler(403)
def forbidden(error):
    """Render the 403 error page."""
    return render_template("403.html"), 403


@main.app_errorhandler(404)
def page_not_found(error):
    """Render the 404 error page."""
    return render_template("404.html"), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    """Render the 500 error page and log the exception."""
    current_app.logger.error("500 Error: %s", error, exc_info=True)
    return render_template("500.html"), 500
