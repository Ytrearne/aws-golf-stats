import json
import os
import urllib.error
import urllib.request

API_URL = os.environ["API_URL"]
API_KEY = os.environ["API_KEY"]


def call_api(headers):
    request = urllib.request.Request(API_URL, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()


def test_rejects_request_without_key():
    status, _ = call_api({})
    assert status == 403


def test_returns_rounds_newest_first_with_key():
    status, body = call_api({"x-api-key": API_KEY})
    assert status == 200
    rounds = json.loads(body)
    assert len(rounds) > 0
    start_times = [r["start_time"] for r in rounds]
    assert start_times == sorted(start_times, reverse=True)
    assert "playerProfileId" not in body
