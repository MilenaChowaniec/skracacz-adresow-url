"""
Endpointy aplikacji
Obsługa żądań HTTP
"""

from flask import Blueprint, render_template, request, redirect, url_for
import validators
from app.database import db
from app.models import URL
from app.utils import id_to_short_code

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Formularz do skracania URL oraz lista wszystkich skroconych URLi.

    Returns:
        Rendered template z formularzem i listą skroconych URLi
    """
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return render_template("index.html", urls=urls)


@main_bp.route("/shorten", methods=["POST"])
def shorten():
    """Skraca URL, czyli tworzy kod z Base62.

    POST data:
        url: oryginalny URL do skrócenia

    Returns:
        Redirect do strony głównej
    """
    original_url = request.form.get("url", "").strip()

    # Walidacja podanego adresu URL
    if not validators.url(original_url) or len(original_url) > 2048:
        return redirect(url_for("main.index"))

    # Zapisanie do bazy z tymczasowym kodem
    new_url = URL(original_url=original_url, short_code="temp")
    db.session.add(new_url)
    db.session.flush()

    # Wygenerowanie i dodanie kodu do rekordu
    new_url.short_code = id_to_short_code(new_url.id)
    db.session.commit()

    return redirect(url_for("main.index"))


@main_bp.route("/<short_code>")
def redirect_url(short_code):
    """Przekierowanie, gdy użytkownik wejdzie na krótki URL.

    Args:
        short_code: Krótki kod URL

    Returns:
        Redirect do oryginalnego URL

    Raises:
        404: jeśli kod nie istnieje
    """
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url.original_url)


@main_bp.route("/delete/<int:url_id>", methods=["POST"])
def delete_url(url_id):
    """Usuwa URL z bazy.

    Args:
        url_id: ID URL do usunięcia

    Returns:
        Redirect do strony głównej

    Raises:
        404: jeśli URL nie istnieje
    """
    url = URL.query.get_or_404(url_id)
    db.session.delete(url)
    db.session.commit()

    return redirect(url_for("main.index"))
