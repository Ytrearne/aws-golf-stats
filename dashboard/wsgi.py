"""Entry point for the web server (gunicorn wsgi:app).

Connects the app to the real API. Kept separate from app.py so the tests
can import app.py without any environment variables.
"""
import json
import os
import urllib.request

from app import create_app


def _get_json(url_variable):
    """Fetch JSON from the URL in the given environment variable.

    The URLs and the API key come from environment variables, never from the code.
    """
    request = urllib.request.Request(
        os.environ[url_variable],
        headers={"x-api-key": os.environ["API_KEY"]},
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read())


def fetch_rounds():
    return _get_json("API_URL")


def fetch_handicap():
    return _get_json("HANDICAP_URL")


app = create_app(fetch_rounds, fetch_handicap)