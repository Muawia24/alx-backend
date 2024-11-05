#!/usr/bin/env python3
"""
4. Force locale with URL parameter
"""

from typing import Dict, Union
from flask import Flask, render_template
from flask_babel import Babel
from flask import request, g


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


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id: str) -> Union[Dict[str, Union[str, None]], None]:
    """
    return:
        dictionary or None if the ID cannot be found
        or if login_as was not passed.
    """
    return users.get(int(id), 0)


@app.before_request
def before_request():
    user_id = request.args.get('login_as', 0)
    user_dict = get_user(user_id)

    setattr(g, 'user', user_dict)


@app.route("/", strict_slashes=False)
def hello_holberton() -> str:
    """
    Welcome to Holberton
    """
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(debug=True)
