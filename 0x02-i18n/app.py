#!/usr/bin/env python3
"""
7. Infer appropriate time zone
"""


from typing import Dict, Union
from flask import Flask, render_template
from flask_babel import Babel, format_datetime
from flask import request, g
import pytz
import datetime


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
    if g.get('user') and g.user.get('locale') in Config.LANGUAGES:
        return g.user['locale']
    header_locale = request.accept_languages.best_match(
            app.config['LANGUAGES'])
    if header_locale:
        return header_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """
        return:
            timezone
    """
    timezone = request.args.get('timezone', '').strip()
    if timezone:
        return timezone
    if not timezone and g.get('user') and g.user.get('timezone'):
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


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
    """
    use the app.before_request decorator to make it be
    executed before all other functions. before_request
    should use get_user to find a user if any, and set
    it as a global on flask.g.user.
    """
    user_id = request.args.get('login_as', 0)
    user_dict = get_user(user_id)

    setattr(g, 'user', user_dict)
    setattr(g, 'time', format_datetime(datetime.datetime.now()))


@app.route("/", strict_slashes=False)
def hello_holberton() -> str:
    """
    Welcome to Holberton
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
