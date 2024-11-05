#!/usr/bin/env python3
"""
1. Basic Babel setup
"""


from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)

app.config.from_object('config.Config')

babel = Babel(app)


@app.route("/")
def hello_holberton():
    """
    Welcome to Holberton
    """
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(debug=True)
