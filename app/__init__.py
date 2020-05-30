from flask import Flask
from ws_helpers import random_string


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = random_string(32)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .main import socketio

    socketio.init_app(
        app,
        async_mode=None,
        cookie=False
    )

    return app, socketio
