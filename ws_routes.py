from flask import Blueprint

static_html = Blueprint('static_html', __name__, static_url_path='/static', static_folder='static')


@static_html.route('/')
def index():
    return static_html.send_static_file('index.html')
