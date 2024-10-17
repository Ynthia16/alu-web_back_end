#!/usr/bin/env python3
"""Basic Flask app that implements i18n and internationalization"""

from flask import Flask, render_template, request, g
from flask_babel import Babel

app = Flask(__name__)

# Mocked user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration for Babel and i18n"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.get('user') and g.user.get("locale") in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """Get user based on the login_as URL parameter"""
    try:
        login_as = int(request.args.get('login_as'))
        return users.get(login_as)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set g.user before each request if the user exists"""
    user = get_user()
    if user:
        g.user = user
    else:
        g.user = None


@app.route('/', methods=['GET'])
def home():
    """Render the homepage"""
    login = g.user is not None
    return render_template('5-index.html', login=login)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
