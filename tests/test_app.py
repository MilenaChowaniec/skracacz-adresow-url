"""Testy jednostkowe dla aplikacji skracacz URL."""

import pytest
from app import create_app
from app.database import db
from app.models import URL


@pytest.fixture
def app():
    """Fixture - tworzy aplikacje testowa."""
    app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Fixture - klient testowy do wysylania requestow."""
    return app.test_client()


def test_index_page(client):
    """Strona glowna sie laduje."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Skracacz URL" in response.data


def test_shorten_url(client, app):
    """Skracanie URL dziala poprawnie."""
    response = client.post("/shorten", data={"url": "https://example.com"})

    # Przekierowanie do strony glownej
    assert response.status_code == 302
    assert "/" in response.location

    # Sprawdzenie czy URL jest w bazie
    with app.app_context():
        url = URL.query.first()
        assert url is not None
        assert url.original_url == "https://example.com"
        assert url.short_code == "1"


def test_shorten_empty_url(client):
    """Przy pustym URL po prostu przekierowuje na strone glowna."""
    response = client.post("/shorten", data={"url": ""})
    assert response.status_code == 302
    assert "/" in response.location


def test_shorten_too_long_url(client):
    """Przy za dlugim URL po prostu przekierowuje na strone glowna."""
    long_url = "https://example.com/" + "a" * 3000
    response = client.post("/shorten", data={"url": long_url})
    assert response.status_code == 302
    assert "/" in response.location


def test_redirect_url(client, app):
    """Test: Przekierowanie na oryginalny URL dziala."""
    # Dodanie URL do bazy
    with app.app_context():
        new_url = URL(original_url="https://google.com", short_code="abc")
        db.session.add(new_url)
        db.session.commit()

    # Test przekierowania
    response = client.get("/abc")
    assert response.status_code == 302
    assert response.location == "https://google.com"


def test_redirect_nonexistent_code(client):
    """404 dla nieistniejacego kodu."""
    response = client.get("/nieistniejacy")
    assert response.status_code == 404


def test_index_empty(client):
    """Zachowanie strony glownej z pusta baza."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Brak URLi" in response.data


def test_index_with_data(client, app):
    """Zachowanie strony glownej z danymi."""
    # Dodanie danych
    with app.app_context():
        url = URL(original_url="https://github.com", short_code="xyz")
        db.session.add(url)
        db.session.commit()

    response = client.get("/")
    assert response.status_code == 200
    assert b"github.com" in response.data
    assert b"xyz" in response.data


def test_delete_url(client, app):
    """Usuwanie URL dziala."""
    # Dodanie danych
    with app.app_context():
        url = URL(original_url="https://test.com", short_code="test")
        db.session.add(url)
        db.session.commit()
        url_id = url.id

    response = client.post(f"/delete/{url_id}")
    assert response.status_code == 302

    with app.app_context():
        url = db.session.get(URL, url_id)
        assert url is None


def test_base62_encoding(app):
    """Kodowanie Base62 dziala poprawnie."""
    from app.utils import id_to_short_code

    assert id_to_short_code(1) == "1"
    assert id_to_short_code(10) == "A"
    assert id_to_short_code(100) == "1c"
    assert id_to_short_code(12345) == "3D7"


def test_full_workflow(client, app):
    """Sprawdza czy cała aplikacja działa.

    Ten test przechodzi przez pełny workflow:
    1. Strona glowna sie laduje
    2. Dodanie URL
    3. Przekierowanie dziala
    4. Usuniecie URL

    """
    # Strona glowna sie laduje
    response = client.get("/")
    assert response.status_code == 200
    assert b"Skracacz URL" in response.data

    # Dodanie URL
    response = client.post("/shorten", data={"url": "https://example.com/test"})
    assert response.status_code == 302

    # Sprawdzenie, czy URL znajduje sie w bazie
    with app.app_context():
        url = URL.query.first()
        assert url is not None
        assert url.original_url == "https://example.com/test"
        short_code = url.short_code
        url_id = url.id

    # Przekierowanie na skrocony URL
    response = client.get(f"/{short_code}")
    assert response.status_code == 302
    assert response.location == "https://example.com/test"

    # Usuniecie URL
    response = client.post(f"/delete/{url_id}")
    assert response.status_code == 302

    # Sprawdzenie, czy URL zostal usuniety z bazy
    with app.app_context():
        url = db.session.get(URL, url_id)
        assert url is None
