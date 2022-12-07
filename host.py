from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from config import getData

import sqlite3

app = Flask(__name__)
CORS(app)

def get_data(sql):
    res = {}
    con = sqlite3.connect('./db/example.sqlite')

    with con:
        data = con.execute(sql)
        for index, row in enumerate(data):
            res[index] = row

    return res

@app.route('/get_questions_ru')
def get_questions_ru():
    res = get_data("SELECT b.id, b.question_ru FROM surveys a LEFT JOIN questions b on a.id = b.id_survey where a.id = 1")
    print(res)
    return res

@app.route('/get_questions_en')
def get_questions_en():
    res = get_data("SELECT b.id, b.question_en FROM surveys a LEFT JOIN questions b on a.id = b.id_survey where a.id = 1")
    print(res)
    return res

@app.route('get_question_ru/<question_id>/', methods = ['GET', 'POST'])
def get_response_ru(question_id):
    res = get_data(f"SELECT id, response_options_ru FROM responses WHERE id_question = {question_id}")
    print(res)
    return res

@app.route('get_question_en/<question_id>/', methods = ['GET', 'POST'])
def get_response_en(question_id):
    res = get_data(f"SELECT id, response_options_en FROM responses WHERE id_question = {question_id}")
    print(res)
    return res
    

if __name__ == '__main__':
    ip = getData('host', 'ip')
    port = getData('host', 'port', int)
    print(f'Start server {ip}:{port}')

    http_server = WSGIServer((str(ip), port), app)
    http_server.serve_forever()