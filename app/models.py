"""Model bazy danych."""

from datetime import datetime
from app.database import db


class URL(db.Model):
    """Model tabeli 'urls', ktora przechowuje skrocone adresy URL.

    Attributes:
        id: klucz glowny (auto-increment)
        original_url: oryginalny adres URL
        short_code: kod Base62
        created_at: data utworzenia
    """
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(
        db.String(10),
        unique=True,
        nullable=False,
        index=True,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
