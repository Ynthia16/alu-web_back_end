#!/usr/bin/env python3
"""
A Basic flask application
"""
from typing import (
    Dict, Union
)

from flask import Flask, g, request, render_template
from flask_babel import Babel


class Config(object):
    """
    Application configuration class
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Instantiate the application object
app = Flask(__name__)
app.config.from_object(Config)

# Wrap the application with Babel
babel = Babel(app)

@babel.localeselector  # This is correct for Flask-Babel 2.x
def get_locale():
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# Mock database of users
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id) -> Union[Dict[str, Union[str, None]], None]:
    """
    Validate user login details.
    Args:
        id (str): user id.
    Returns:
        (Dict): user dictionary if id is valid else None.
    """
    try:
        return users.get(int(id))
    except (ValueError, TypeError):
        return None


@app.before_request
def before_request():
    """
    Adds valid user to the global session object `g`.
    """
    login_as = request.args.get('login_as')
    g.user = get_user(login_as)  # Now returns None if login_as is not found or invalid


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders a basic html template
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run()
