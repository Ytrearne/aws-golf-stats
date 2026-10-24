import html
import math
from datetime import date

WIDTH = 600
HEIGHT = 240
LEFT = 40
TOP = 12
RIGHT = 12
BOTTOM = 28


def chart_points(values, width, height):
    """Map values to (x, y) positions. SVG's y axis points down, so high values get a low y."""
    low, high = min(values), max(values)
    spread = high - low
    last = len(values) - 1
    points = []
    for index, value in enumerate(values):
        if last == 0:
            x = width / 2
        else:
            x = width * index / last
        if spread == 0:
            y = height / 2
        else:
            y = height - height * (value - low) / spread
        points.append((x, y))
    return points


def time_points(dates, values, width, height):
    """Like chart_points, but x follows the calendar, so gaps between rounds show."""
    days = [date.fromisoformat(d).toordinal() for d in dates]
    span = days[-1] - days[0]
    ys = [y for _, y in chart_points(values, width, height)]
    xs = [width * (day - days[0]) / span if span else width / 2 for day in days]
    return list(zip(xs, ys))


def y_ticks(low, high):
    """Pick round tick values between low and high, about five of them."""
    raw_step = (high - low) / 6
    step = next((s for s in (1, 2, 5, 10, 20, 50, 100) if s >= raw_step), 100)
    ticks = []
    value = math.ceil(low / step) * step
    while value <= high:
        ticks.append(value)
        value += step
    return ticks


TICK_MONTHS = {1: "jan", 7: "jul"}


def x_ticks(first, last):
    """Return (date, label) pairs for 1 January and 1 July between two ISO dates."""
    start = date.fromisoformat(first)
    end = date.fromisoformat(last)
    ticks = []
    for year in range(start.year, end.year + 1):
        for month, name in TICK_MONTHS.items():
            tick = date(year, month, 1)
            if start <= tick <= end:
                ticks.append((tick.isoformat(), f"{name} {year}"))
    return ticks

def _y_for(value, low, high, height):
    """Vertical position of a value, on the same scale as chart_points."""
    if high == low:
        return height / 2
    return height - height * (value - low) / (high - low)


def _grid_line(tick, low, high):
    """A faint horizontal line across the chart, with the tick value to its left."""
    y = _y_for(tick, low, high, HEIGHT)
    return (
        f'<line class="hcp-grid" x1="0" x2="{WIDTH}" y1="{y:.1f}" y2="{y:.1f}"/>'
        f'<text class="hcp-label" x="-8" y="{y + 4:.1f}" text-anchor="end">{tick}</text>'
    )


def _x_for(day, first, last):
    """Horizontal position of a date, on the same scale as time_points."""
    start = date.fromisoformat(first).toordinal()
    span = date.fromisoformat(last).toordinal() - start
    if span == 0:
        return WIDTH / 2
    return WIDTH * (date.fromisoformat(day).toordinal() - start) / span


def _x_tick(day, label, first, last):
    """A small mark under the chart with a date label below it."""
    x = _x_for(day, first, last)
    return (
        f'<line class="hcp-grid" x1="{x:.1f}" x2="{x:.1f}" y1="{HEIGHT}" y2="{HEIGHT + 5}"/>'
        f'<text class="hcp-label" x="{x:.1f}" y="{HEIGHT + 20}" text-anchor="middle">{label}</text>'
    )

def hcp_chart(rounds):
    """Return an SVG line chart of handicap over time, or "" if there are fewer than two rounds."""
    if len(rounds) < 2:
        return ""
    values = [r["handicap_before"] for r in rounds]
    dates = [r["date"] for r in rounds]
    coords = time_points(dates, values, WIDTH, HEIGHT)
    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    low, high = min(values), max(values)
    grid = "".join(_grid_line(tick, low, high) for tick in y_ticks(low, high))
    x_axis = "".join(
        _x_tick(day, label, dates[0], dates[-1]) for day, label in x_ticks(dates[0], dates[-1])
    )
    dots = "".join(
        f'<circle class="hcp-dot" cx="{x:.1f}" cy="{y:.1f}" r="8">'
        f"<title>{html.escape(str(r['date']))}: HCP {r['handicap_before']}</title></circle>"
        for r, (x, y) in zip(rounds, coords)
    )
    return (
        f'<svg viewBox="0 0 {LEFT + WIDTH + RIGHT} {TOP + HEIGHT + BOTTOM}" class="hcp-chart">'
        f'<g transform="translate({LEFT},{TOP})">'
        f"{grid}"
        f"{x_axis}"
        f'<polyline class="hcp-line" points="{points}" fill="none"/>'
        f"{dots}"
        "</g></svg>"
    )