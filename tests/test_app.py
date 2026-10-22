from app import create_app


def fake_fetch_rounds():
    return [
        {"course_name": "Atlungstad Golf", "start_time": "2026-10-12T11:15:17.000Z", "holes_played": 9, "total_strokes": 40, "score_to_par": 4},
        {"course_name": "Bane B", "start_time": "2026-09-30T10:00:00.000Z", "holes_played": 18, "total_strokes": 86, "score_to_par": 14},
    ]


def test_front_page_lists_rounds():
    client = create_app(fake_fetch_rounds).test_client()
    response = client.get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Atlungstad Golf" in html
    assert "Bane B" in html


def test_course_name_is_escaped_in_html():
    def evil_rounds():
        return [{"course_name": "<script>alert(1)</script>", "start_time": "2026-10-12T11:15:17.000Z", "holes_played": 18, "total_strokes": 80, "score_to_par": 8}]

    html = create_app(evil_rounds).test_client().get("/").get_data(as_text=True)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_front_page_shows_summary():
    client = create_app(fake_fetch_rounds).test_client()
    html = client.get("/").get_data(as_text=True)
    assert "Runder: 2" in html
    assert "Beste 18-hullsrunde: +14" in html


def test_health_endpoint_does_not_call_the_api():
    def fail_fetch():
        raise AssertionError("health check must not fetch rounds")

    response = create_app(fail_fetch).test_client().get("/health")
    assert response.status_code == 200
