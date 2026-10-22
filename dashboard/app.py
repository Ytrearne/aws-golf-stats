from dashboard_stats import summarize
from flask import Flask, render_template_string

PAGE = """
<!doctype html>
<html lang="no">
<head><meta charset="utf-8"><title>Golf-statistikk</title></head>
<body>
  <h1>Mine runder</h1>
  <p>Runder: {{ stats.rounds }} ({{ stats.full_rounds }} med 18 hull)</p>
  <p>Beste 18-hullsrunde: {% if stats.best_full_round is not none %}{{ '%+d'|format(stats.best_full_round) }}{% else %}ingen{% endif %}</p>
  <p>Snitt 18-hullsrunde: {% if stats.average_full_round is not none %}{{ '%+.1f'|format(stats.average_full_round) }}{% else %}ingen{% endif %}</p>
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


def create_app(fetch_rounds):
    app = Flask(__name__)

    @app.get("/")
    def front_page():
        rounds = fetch_rounds()
        return render_template_string(PAGE, rounds=rounds, stats=summarize(rounds))

    return app
