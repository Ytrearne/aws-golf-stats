import json
import os
import urllib.request

from app import create_app


def fetch_rounds():
    request = urllib.request.Request(
        os.environ["API_URL"],
        headers={"x-api-key": os.environ["API_KEY"]},
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read())


app = create_app(fetch_rounds)
