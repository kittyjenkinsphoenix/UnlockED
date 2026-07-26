"""Security helpers."""

from urllib.parse import urlparse

BLACKLIST = ["Password123$", "Qwerty123!", "Adminadmin1@", "weLcome123!"]


def is_blacklisted_password(password):
    """Return True when a password is on the project blacklist."""
    return password in BLACKLIST


def is_safe_redirect_url(target_url):
    """Return True when a redirect target stays on the same site."""
    return urlparse(target_url).netloc == ""
