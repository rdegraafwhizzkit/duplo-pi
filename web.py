from flask import Flask
import json
# from dummy_sync import DummySync
from pi_sync import PISync

app = Flask(__name__, static_url_path='/static')

# sync_object = DummySync()
sync_object = PISync()

def state(status):
    return json.dumps(status), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/sync')
def route_sync():
    return state(sync_object.sync())


@app.route('/')
def route():
    return app.send_static_file('index.html')


@app.route("/<color>")
def route_color(color):
    return state(sync_object.sync(color))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
