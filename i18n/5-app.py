#!/usr/bin/env python3
"""Basic Flask app that implements i18n and internationalization"""

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
    """Config class for your application, it deals with babel mostly"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)
babel = Babel(app)

@babel.localeselector
def get_locale():
    """Get locale for your application"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """Home page for your application"""
    user_id = request.args.get('login_as')
    if user_id:
        g.user = get_user(user_id)
    return render_template('5-index.html')

def get_user(user_id):
    """Get user based on the login_as URL parameter"""
    try:
        user_id = int(user_id)
        return users.get(user_id)  # Returns user object or None
    except (TypeError, ValueError):
        return None

@app.before_request
def before_request():
    """Set g.user before each request if the user exists"""
    user_id = request.args.get('login_as')
    if user_id:
        g.user = get_user(user_id)
    else:
        g.user = None

if __name__ == "__main__":
    app.run(debug=True)

