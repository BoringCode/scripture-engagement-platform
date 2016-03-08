
from flask import Flask, render_template, g


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    app = Flask(app_name)

    return app

app = create_app(app_name=__name__)

app.run(debug=True, port=8080)
