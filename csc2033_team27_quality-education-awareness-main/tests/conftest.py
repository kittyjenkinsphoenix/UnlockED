import os
import sys
import tempfile

import pytest
from cryptography.fernet import Fernet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("SECRET_KEY", "ci-test-secret-key")
os.environ.setdefault("SECURITY_PEPPER", "ci-test-pepper")
os.environ.setdefault("BIO_ENCRYPTION_KEY", Fernet.generate_key().decode())

from app import create_app, db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    _app = create_app(
        {
            "TESTING": True,
            "RATELIMIT_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        }
    )

    yield _app

    with _app.app_context():
        db.drop_all()
        db.engine.dispose()

    os.close(db_fd)
    try:
        os.unlink(db_path)
    except OSError:
        pass


@pytest.fixture
def client(app):
    return app.test_client()
