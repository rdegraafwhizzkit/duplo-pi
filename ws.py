from flask import Flask, session
from flask_socketio import SocketIO, emit
# from dummy_sync import DummySync
from pi_sync import PISync
import string, random
# sync_object = DummySync()
sync_object = PISync()
async_mode = None

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
socketio = SocketIO(app, async_mode=async_mode)
namespace = '/test'


@app.route('/')
def index():
    return app.send_static_file('index.html')


@socketio.on('sync_all', namespace=namespace)
def sync():
    emit('sync_response', {'data': sync_object.sync()}, broadcast=False)


@socketio.on('sync_one', namespace=namespace)
def test_broadcast_message(message):
    emit('sync_response', {'data': sync_object.sync(message['data'])}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
