#!/usr/bin/env python3
"""
4. Force locale with URL parameter
"""


from flask import Flask, render_template
from flask_babel import Babel
from flask import request


class Config(object):
    """
    Config class
    """

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)

app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    determine the best match with our supported languages.
    """
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/", strict_slashes=False)
def hello_holberton() -> str:
    """
    Welcome to Holberton
    """
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run(debug=True)
