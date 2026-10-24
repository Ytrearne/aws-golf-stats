import html

WIDTH = 600
HEIGHT = 240


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


def hcp_chart(rounds):
    """Return an SVG line chart of handicap over time, or "" if there are fewer than two rounds."""
    if len(rounds) < 2:
        return ""
    values = [r["handicap_before"] for r in rounds]
    coords = chart_points(values, WIDTH, HEIGHT)
    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    dots = "".join(
        f'<circle class="hcp-dot" cx="{x:.1f}" cy="{y:.1f}" r="8">'
        f"<title>{html.escape(str(r['date']))}: HCP {r['handicap_before']}</title></circle>"
        for r, (x, y) in zip(rounds, coords)
    )
    return (
        f'<svg viewBox="0 0 {WIDTH} {HEIGHT}" class="hcp-chart">'
        f'<polyline class="hcp-line" points="{points}" fill="none"/>'
        f"{dots}"
        "</svg>"
    )