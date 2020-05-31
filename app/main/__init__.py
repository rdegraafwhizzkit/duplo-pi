from flask import Blueprint
from flask_socketio import SocketIO
from backend.sync_objects.dummy_sync import DummySync
from backend.sync_objects.pi_sync import PISync
import os

sync_object = PISync({'blue': True, 'green': True}) if 'Darwin' != os.name else DummySync({'red': True})
namespace = '/duplopi'

main = Blueprint('main', __name__, static_url_path='/static', static_folder='static')
socketio = SocketIO()

from . import routes, events
