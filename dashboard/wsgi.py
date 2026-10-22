"""Entry point for the web server (gunicorn wsgi:app).

Connects the app to the real API. Kept separate from app.py so the tests
can import app.py without any environment variables.
"""
import json
import os
import urllib.request

from app import create_app


def fetch_rounds():
    """Fetch all rounds from the API.

    The URL and the API key come from environment variables, never from the code.
    """
    request = urllib.request.Request(
        os.environ["API_URL"],
        headers={"x-api-key": os.environ["API_KEY"]},
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read())


app = create_app(fetch_rounds)
