"""Groq API client singleton.

This client is reserved for future AI features (e.g. resume parsing,
job description analysis). It makes no requests during normal operation
and is simply initialized at application startup so the connection is
ready when needed.
"""

import os

from groq import Groq

_api_key = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=_api_key) if _api_key else None
