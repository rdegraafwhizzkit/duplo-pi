from flask import copy_current_request_context
from flask_socketio import emit
from threading import Thread
from ws_helpers import load
import os
import time
import json

from . import socketio, sync_object, namespace

loop = False


@socketio.on('save', namespace=namespace)
def on_save(message):
    os.makedirs('patterns', exist_ok=True)
    with open(f'patterns/{message["name"]}.json', 'w') as p:
        p.write(json.dumps(message))
    emit('sync_patterns', {'data': load()}, broadcast=True)


@socketio.on('connect', namespace=namespace)
def on_connect():
    sync_all()


@socketio.on('sync_all', namespace=namespace)
def sync_all():
    emit('sync_response', {'data': sync_object.sync()}, broadcast=False)
    emit('sync_patterns', {'data': load()}, broadcast=True)
    global loop
    emit('loop_status', {'data': 'started' if loop else 'stopped'}, broadcast=True)


@socketio.on('sync_one', namespace=namespace)
def sync_one(message):
    emit('sync_response', {'data': sync_object.sync(message['data'])}, broadcast=True)


@socketio.on('start', namespace=namespace)
def start(message):
    @copy_current_request_context
    def loop_thread(pattern):
        global loop
        loop = True
        while loop:
            emit('loop_status', {'data': 'started'}, broadcast=True)
            for data in pattern['data']:
                if not loop:
                    break
                colors = data['colors']
                d = {color.strip(): True for color in colors}
                emit('sync_response', {'data': sync_object.set({} if '' in d else d)}, broadcast=True)
                time.sleep(data['duration'] / 1000.0)

    global loop
    if not loop:
        loop = True
        Thread(target=loop_thread, args=(message,)).start()


@socketio.on('stop', namespace=namespace)
def stop():
    global loop
    loop = False
    emit('loop_status', {'data': 'stopped'}, broadcast=True)
