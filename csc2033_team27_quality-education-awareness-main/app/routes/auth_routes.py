"""Authentication routes."""

from flask import current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.forms import ChangePasswordForm, LoginForm, PasswordResetForm, PasswordResetRequestForm, RegistrationForm
from app.services.auth_service import (
    authenticate_user,
    change_password as change_password_service,
    register_user,
    request_password_reset,
    reset_password_from_token,
    verify_password_reset_token,
)
from app.utils.security import is_safe_redirect_url

from . import main


@main.route("/register", methods=["GET", "POST"])
def register():
    """Render the registration form and create a new user account."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        result = register_user(
            username=form.username.data,
            name=form.name.data,
            password=form.password.data,
            bio=form.bio.data,
        )
        flash(result["message"], result["category"])
        if result["ok"]:
            return redirect(url_for("main.login"))
    return render_template("register.html", title="Register", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate a user and redirect them to the requested page."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate_user(form.username.data, form.password.data)
        if user:
            session.clear()
            login_user(user)
            session.permanent = True
            next_page = request.args.get("next")
            if not next_page or not is_safe_redirect_url(next_page):
                next_page = url_for("main.dashboard")
            return redirect(next_page)
        flash("Login unsuccessful, check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@main.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Request a password reset link for an account."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = PasswordResetRequestForm()
    reset_link = None
    if form.validate_on_submit():
        result = request_password_reset(form.email.data)
        flash(result["message"], result["category"])
        reset_token = result.get("token")
        if reset_token and (current_app.debug or current_app.testing):
            reset_link = url_for("main.reset_password", token=reset_token, _external=True)
        else:
            return redirect(url_for("main.login"))
    return render_template("forgot_password.html", title="Forgot Password", form=form, reset_link=reset_link)


@main.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Set a new password using a password reset token."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if not verify_password_reset_token(token):
        flash("The password reset link is invalid or has expired.", "danger")
        return redirect(url_for("main.forgot_password"))

    form = PasswordResetForm()
    if form.validate_on_submit():
        result = reset_password_from_token(token, form.password.data)
        flash(result["message"], result["category"])
        if result["ok"]:
            return redirect(url_for("main.login"))
    return render_template("reset_password.html", title="Reset Password", form=form)


@main.route("/logout")
@login_required
def logout():
    """Log the current user out and return them to the home page."""
    logout_user()
    return redirect(url_for("main.home"))


@main.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow the signed-in user to update their password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        result = change_password_service(
            user=current_user,
            current_password=form.current_password.data,
            new_password=form.new_password.data,
        )
        flash(result["message"], result["category"])
        if result["ok"]:
            return redirect(url_for("main.dashboard"))
    return render_template("change_password.html", form=form)
