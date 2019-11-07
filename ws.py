from flask import Flask, copy_current_request_context
from flask_socketio import SocketIO, emit
from dummy_sync import DummySync
from pi_sync import PISync
import os, time
from threading import Thread

sync_object = PISync({'blue': True, 'green': True}) if 'Darwin' != os.name else DummySync({'red': True})

app = Flask(__name__, static_url_path='/static')
app.config[
    'SECRET_KEY'] = '9fAgMmc9hl6VXIsFu3ddb5MJ2U86qEad'  # ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
socketio = SocketIO(app, async_mode=None)
namespace = '/duplopi'

loop = False


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


@socketio.on('start', namespace=namespace)
def start(message):
    @copy_current_request_context
    def loop_thread(message):
        global loop
        loop = True
        while loop:
            for data in message['data'].split(","):
                if not loop:
                    break
                colors=data.strip().split(" ")
                d = {color.strip(): True for color in colors if not color.isnumeric()}
                emit('sync_response', {'data': sync_object.set({} if '' in d else d)}, broadcast=True)
                time.sleep(int(colors[len(colors)-1])/1000.0)

    global loop
    if not loop:
        loop = True
        Thread(target=loop_thread, args=(message,)).start()


@socketio.on('stop', namespace=namespace)
def stop():
    global loop
    loop = False


if __name__ == '__main__':
    socketio.run(
        app,
        debug=False,
        host='0.0.0.0'
    )
