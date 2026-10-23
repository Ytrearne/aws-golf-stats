from charts import chart_points


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