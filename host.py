from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from config import getData

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    ip = getData('host', 'ip')
    port = getData('host', 'port', int)
    print(f'Start server {ip}:{port}')

    http_server = WSGIServer((str(ip), port), app)
    http_server.serve_forever()