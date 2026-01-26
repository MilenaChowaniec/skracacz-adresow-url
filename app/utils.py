"""Generowanie kodu."""

import base62


def id_to_short_code(url_id: int) -> str:
    """Konwertuje ID URL na kod uzywajac base62.

    Args:
        url_id (int): ID rekordu URL

    Returns:
    """
    return base62.encode(url_id)


def short_code_to_id(code: str) -> int:
    """Konwertuje kod spowrotem na ID URL.

    Args:
        code (str): krotki kod Base62

    Returns:
    """
    return base62.decode(code)

print(base62.encode(12345))