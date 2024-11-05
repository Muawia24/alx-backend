#!/usr/bin/env python3
"""
2. Get locale from request
"""


from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Config class"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)

app.config.from_object(Config)
app.url_map.strict_slashes = False

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    determine the best match with our supported languages.
    """
    return request.accept_languages.best_match(app.config[''LANGUAGES])


@app.route("/")
def hello_holberton() -> str:
    """
    Welcome to Holberton
    """
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run(debug=True)
