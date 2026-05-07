"""Anthropic client — lazily initialised singleton.

Usage:
    from app.llm import get_client
    client = get_client()
    response = client.messages.create(...)

Raises RuntimeError on first call if ANTHROPIC_API_KEY is not configured.
"""

from __future__ import annotations

import anthropic

from app.config import settings

_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        if not settings.anthropic_api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. "
                "Add it to your environment or to a .env file. "
                "See .env.example for details."
            )
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client
