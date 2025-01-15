import pytest
from app import create_app, db
from sqlalchemy import text

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:admin@localhost/weather_db",  # Usar PostgreSQL
    })

    return app
