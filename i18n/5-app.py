#!/usr/bin/env python3
"""
Basic Flask app that implements i18n and internationalization.

This app demonstrates the use of Flask and Flask-Babel for handling 
multi-language support, switching between languages based on user preferences.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel

app = Flask(__name__)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """Config class for your application, it deals with babel mostly."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


def get_user(id):
    """
    Retrieve user information based on user ID.

    Args:
        id (int): The ID of the user.

    Returns:
        dict or None: User dictionary if found, otherwise None.
    """
    try:
        return users.get(int(id))
    except (ValueError, TypeError):
        return None


@app.before_request
def before_request():
    """Fetch user before handling a request and store it in the global context."""
    login_as = request.args.get('login_as')
    g.user = get_user(login_as)


@babel.localeselector
def get_locale():
    """
    Determine the best match for supported languages.

    Returns:
        str: The locale to use for this request.
    """
    return request.args.get('locale', 'en')


@app.route('/')
def index():
    """
    Render the index page with the user's name and appropriate locale-based messages.

    If the user is logged in, display a welcome message with their username.
    If the user is not logged in, display a generic message.
    The language of the messages depends on the selected locale (English or French).

    Returns:
        str: A rendered HTML template with localized content.
    """
    username = g.user["name"] if g.user else None
    current_locale = get_locale()
    return render_template('5-index.html', username=username, current_locale=current_locale)


if __name__ == '__main__':
    app.run(debug=True)
