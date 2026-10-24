from app import create_app

HANDICAP = [
    {"date": "2026-04-02", "handicap_before": 12.3},
    {"date": "2026-05-01", "handicap_before": 11.0},
]


def test_front_page_shows_the_handicap_chart():
    app = create_app(lambda: [], lambda: HANDICAP)

    html = app.test_client().get("/").get_data(as_text=True)

    assert "<svg" in html


def test_front_page_explains_when_there_is_too_little_data():
    app = create_app(lambda: [], lambda: [])

    html = app.test_client().get("/").get_data(as_text=True)

    assert "For få runder til en graf" in html