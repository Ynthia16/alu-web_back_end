#!/usr/bin/env python3
"""Basic Flask app that implements i18n and internationalization"""

from flask import Flask, render_template, request, g
from flask_babel import Babel

app = Flask(__name__)

# Users database for testing
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """Config class for Babel and other app settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)
babel = Babel(app)

@babel.localeselector
def get_locale():
    """Select the best match language based on user settings or request headers"""
    # Check if the user provides 'locale' in the query parameters
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    # Otherwise, try to find the best match in the accepted languages
    return request.accept_languages.best_match(app.config['LANGUAGES'])

def get_user():
    """Retrieve user information based on 'login_as' query parameter"""
    try:
        login_as = int(request.args.get('login_as'))
        return users.get(login_as)
    except Exception:
        return None

@app.before_request
def before_request():
    """Run before every request to set the user if they are logged in"""
    user = get_user()
    if user:
        g.user = user  # Set the user in the global object

@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """Home page route"""
    login = 'user' in g
    return render_template('5-index.html', login=login)

if __name__ == "__main__":
    app.run()
