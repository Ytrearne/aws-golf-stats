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