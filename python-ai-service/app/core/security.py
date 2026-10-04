from typing import Optional
from fastapi import Header, HTTPException, status

from app.core.config import settings


def verify_api_key(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> Optional[str]:
    """Optional API key verification dependency.

    If `settings.API_KEY` is configured (non-empty), requests must provide a matching
    `X-API-Key` header. When `settings.API_KEY` is empty (default for local dev/tests),
    all requests are allowed through.
    """
    expected_key = settings.API_KEY
    if not expected_key:
        return x_api_key

    if not x_api_key or x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
    return x_api_key
