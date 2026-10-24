from charts import chart_points, hcp_chart


def test_chart_points_spreads_values_over_the_whole_area():
    points = chart_points([10, 20], width=100, height=50)

    assert points == [(0, 50), (100, 0)]


def test_chart_points_places_a_middle_value_halfway():
    points = chart_points([10, 15, 20], width=100, height=50)

    assert points == [(0, 50), (50, 25), (100, 0)]


def test_chart_points_puts_flat_values_in_the_middle():
    points = chart_points([12, 12, 12], width=100, height=50)

    assert points == [(0, 25), (50, 25), (100, 25)]

def test_chart_points_centers_a_single_value():
    points = chart_points([12], width=100, height=50)

    assert points == [(50, 25)]

def hcp_round(date, handicap):
    return {"date": date, "handicap_before": handicap}


def test_hcp_chart_needs_at_least_two_rounds():
    assert hcp_chart([]) == ""
    assert hcp_chart([hcp_round("2026-04-02", 12.3)]) == ""


def test_hcp_chart_draws_one_line_point_per_round():
    svg = hcp_chart(
        [
            hcp_round("2026-04-02", 12.3),
            hcp_round("2026-05-01", 11.0),
            hcp_round("2026-06-01", 10.0),
        ]
    )

    points = svg.split('points="')[1].split('"')[0].split()
    assert svg.startswith("<svg")
    assert len(points) == 3

def test_hcp_chart_gives_each_point_a_tooltip():
    svg = hcp_chart([hcp_round("2026-04-02", 12.3), hcp_round("2026-05-01", 11.0)])

    assert "<title>2026-04-02: HCP 12.3</title>" in svg
    assert "<title>2026-05-01: HCP 11.0</title>" in svg


def test_hcp_chart_escapes_dates_in_tooltips():
    svg = hcp_chart(
        [
            hcp_round("<script>alert(1)</script>", 12.3),
            hcp_round("2026-05-01", 11.0),
        ]
    )

    assert "<script>" not in svg