from flask import Flask
from flask_socketio import SocketIO, emit
from dummy_sync import DummySync
from pi_sync import PISync
import string, random

sync_object = PISync({'blue': True,'green':True}) if True else DummySync({'red': True})

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '9fAgMmc9hl6VXIsFu3ddb5MJ2U86qEad'#''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
socketio = SocketIO(app, async_mode=None)
namespace = '/duplopi'


@app.route('/')
def index():
    return app.send_static_file('index.html')


@socketio.on('connect', namespace=namespace)
def on_connect():
    sync_all()


@socketio.on('sync_all', namespace=namespace)
def sync_all():
    emit('sync_response', {'data': sync_object.sync()}, broadcast=False)


@socketio.on('sync_one', namespace=namespace)
def sync_one(message):
    emit('sync_response', {'data': sync_object.sync(message['data'])}, broadcast=True)


if __name__ == '__main__':
    socketio.run(
        app,
        debug=False,
        host='0.0.0.0'
    )
