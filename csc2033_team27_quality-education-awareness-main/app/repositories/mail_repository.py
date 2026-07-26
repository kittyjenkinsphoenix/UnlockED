"""Mail subscription repository helpers."""

from app import db
from app.models import MailList


def get_subscriber(email):
    """Return a mailing-list record for the given email address."""
    return MailList.query.filter_by(email=email).first()


def add_subscriber(email):
    """Persist a new mailing-list subscription."""
    record = MailList(email=email)
    db.session.add(record)
    db.session.commit()
    return record


def delete_subscriber(email):
    """Delete a mailing-list subscription when it exists."""
    record = get_subscriber(email)
    if not record:
        return False

    db.session.delete(record)
    db.session.commit()
    return True
