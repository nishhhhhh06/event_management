import pytest
from app import create_app, db
from app.models import User, Event
from flask import url_for
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Creates and configures a new app instance for each test."""
    app = create_app("app.config.TestConfig")  # Use test config
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory DB for testing
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing

    with app.app_context():
        db.create_all()
        yield app  # Provide app for testing
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def init_database(app):
    """Initialize test database with a user and event."""
    user = User(username="testuser", email="test@example.com", role="organizer",
                password_hash=generate_password_hash("password123"))
    event = Event(title="Test Event", location="Test City", date="2025-04-01", max_attendees=50)

    db.session.add(user)
    db.session.add(event)
    db.session.commit()
    return user, event
