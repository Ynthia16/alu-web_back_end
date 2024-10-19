#!/usr/bin/env python3
"""Basic Flask app that implements i18n and internationalization"""

from flask import Flask, g, request, render_template
from flask_babel import Babel

class Config(object):
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user(id):
    try:
        return users.get(int(id))
    except (ValueError, TypeError):
        return None

@app.before_request
def before_request():
    login_as = request.args.get('login_as')
    g.user = get_user(login_as)

@babel.localeselector
def get_locale():
    return request.args.get('locale', 'en')

@app.route('/')
def index():
    username = g.user["name"] if g.user else None
    current_locale = get_locale()  # Fetch the current locale using Babel's `get_locale()`
    return render_template('5-index.html', username=username, current_locale=current_locale)

if __name__ == '__main__':
    app.run(debug=True)
