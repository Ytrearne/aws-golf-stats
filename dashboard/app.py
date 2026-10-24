from charts import hcp_chart
from dashboard_stats import summarize
from flask import Flask, render_template_string
from markupsafe import Markup

# Jinja escapes every {{ value }} automatically, so a course name like
# "<script>" is shown as text instead of running as code.
# Never add "| safe" to values that come from the API.
PAGE = """
<!doctype html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Golf-statistikk</title>
<style>
  :root {
    color-scheme: light;
    --surface: #fcfcfb;
    --text: #0b0b0b;
    --text-muted: #52514e;
    --grid: #e4e3df;
    --series: #2a78d6;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      color-scheme: dark;
      --surface: #1a1a19;
      --text: #f0efec;
      --text-muted: #c3c2b7;
      --grid: #343432;
      --series: #3987e5;
    }
  }
  body { background: var(--surface); color: var(--text); font-family: system-ui, sans-serif;
         margin: 0 auto; max-width: 720px; padding: 16px; }
  table { border-collapse: collapse; width: 100%; }
  th, td { border-bottom: 1px solid var(--grid); padding: 6px 8px; text-align: left; }
  th { color: var(--text-muted); font-weight: 600; }
  .hcp-chart { width: 100%; height: auto; }
  .hcp-line { stroke: var(--series); stroke-width: 2; stroke-linejoin: round; stroke-linecap: round; }
  .hcp-grid { stroke: var(--grid); stroke-width: 1; }
  .hcp-label { fill: var(--text-muted); font-size: 11px; }
  .hcp-dot { fill: transparent; stroke: transparent; stroke-width: 2; }
  .hcp-dot:hover, .hcp-chart circle:last-of-type { fill: var(--series); stroke: var(--surface); }
  .hcp-chart circle:last-of-type { r: 4; }
</style>
</head>
<body>
  <h1>Mine golfrunder</h1>
  <p>Runder: {{ stats.rounds }} ({{ stats.full_rounds }} med 18 hull)</p>
  {# Compare with none, not truthiness: a round exactly at par has score 0. #}
  <p>Beste 18-hullsrunde: {% if stats.best_full_round is not none %}{{ '%+d'|format(stats.best_full_round) }}{% else %}ingen{% endif %}</p>
  <p>Snitt 18-hullsrunde: {% if stats.average_full_round is not none %}{{ '%+.1f'|format(stats.average_full_round) }}{% else %}ingen{% endif %}</p>
  <h2>Handicap-utvikling</h2>
  {% if chart %}{{ chart }}{% else %}<p>For få runder til en graf.</p>{% endif %}
  <h2>Runder</h2>
  <table>
    <tr><th>Dato</th><th>Bane</th><th>Hull</th><th>Slag</th><th>Mot par</th></tr>
    {% for r in rounds %}
    <tr>
      <td>{{ r.start_time[:10] }}</td>
      <td>{{ r.course_name }}</td>
      <td>{{ r.holes_played }}</td>
      <td>{{ r.total_strokes }}</td>
      <td>{{ r.score_to_par }}</td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>
"""


def create_app(fetch_rounds, fetch_handicap=lambda: []):
    """Build the Flask app.

    fetch_rounds and fetch_handicap are passed in instead of imported, so tests
    can give the app fake data without calling the real API.
    """
    app = Flask(__name__)

    @app.get("/")
    def front_page():
        rounds = fetch_rounds()
        # Markup tells Jinja the SVG is already safe. It is, because hcp_chart
        # escapes every value that comes from the API.
        chart = Markup(hcp_chart(fetch_handicap()))
        return render_template_string(PAGE, rounds=rounds, stats=summarize(rounds), chart=chart)

    @app.get("/health")
    def health():
        # Called by the load balancer. It must not call the API, otherwise an
        # API outage would make the load balancer restart a healthy container.
        return "ok"

    return app