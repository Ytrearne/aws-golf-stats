import pytest
from charts import chart_points, hcp_chart, time_points, y_ticks


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


def test_hcp_chart_rejects_values_that_are_not_dates():
    with pytest.raises(ValueError):
        hcp_chart(
            [
                hcp_round("<script>alert(1)</script>", 12.3),
                hcp_round("2026-05-01", 11.0),
            ]
        )


def test_time_points_spaces_x_by_date_not_by_order():
    points = time_points(
        ["2026-01-01", "2026-01-02", "2026-01-11"],
        [10, 10, 10],
        width=100,
        height=50,
    )

    xs = [x for x, _ in points]
    assert xs == [0, 10, 100]


def test_hcp_chart_places_rounds_by_date():
    svg = hcp_chart(
        [
            hcp_round("2026-01-01", 10.0),
            hcp_round("2026-01-02", 10.5),
            hcp_round("2026-01-11", 9.0),
        ]
    )

    points = svg.split('points="')[1].split('"')[0].split()
    assert points[1].startswith("60.0,")


def test_y_ticks_picks_round_numbers_inside_the_range():
    assert y_ticks(3.9, 54.0) == [10, 20, 30, 40, 50]


def test_hcp_chart_labels_the_y_axis():
    svg = hcp_chart([hcp_round("2026-01-01", 3.9), hcp_round("2026-06-01", 54.0)])

    assert ">10</text>" in svg
    assert ">50</text>" in svg


def test_hcp_chart_labels_the_x_axis():
    svg = hcp_chart([hcp_round("2024-03-15", 54.0), hcp_round("2025-08-01", 10.0)])

    assert ">jul 2024</text>" in svg
    assert ">jan 2025</text>" in svg