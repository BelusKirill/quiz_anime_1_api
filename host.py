from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from config import getData

import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/get_questions_ru')
def get_questions_ru():
    res = {}
    con = sqlite3.connect('./db/example.sqlite')

    with con:
        data = con.execute("SELECT id, id_survey, question_ru FROM questions")
        for index, row in enumerate(data):
            res[index] = row

    print(res)
    return res

@app.route('/get_questions_en')
def get_questions_en():
    res = {}
    con = sqlite3.connect('./db/example.sqlite')

    with con:
        data = con.execute("SELECT id, id_survey, question_en FROM questions")
        for index, row in enumerate(data):
            res[index] = row

    print(res)
    return res

if __name__ == '__main__':
    ip = getData('host', 'ip')
    port = getData('host', 'port', int)
    print(f'Start server {ip}:{port}')

    http_server = WSGIServer((str(ip), port), app)
    http_server.serve_forever()