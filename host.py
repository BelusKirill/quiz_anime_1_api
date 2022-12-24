from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from config import getData
from log import add_log

import logging
import logging.handlers as handlers
import sqlite3

app = Flask(__name__)
CORS(app)

def get_data(sql):
    try:
        res = []
        con = sqlite3.connect('./db/example.sqlite')

        with con:
            data = con.execute(sql)
            for index, row in enumerate(data):
                res.append({"id":row[0], "text":str(row[1])})

        return res
    except Exception as ex:
        add_log(ex,'get_data')

@app.route('/get_questions_ru')
def get_questions_ru():
    try:
        res = get_data("SELECT b.id, b.question_ru FROM surveys a LEFT JOIN questions b on a.id = b.id_survey where a.id = 1")
        add_log(res,'get_questions_ru')
        return res
    except Exception as ex:
        add_log(ex,'get_questions_ru')

@app.route('/get_questions_en')
def get_questions_en():
    try:
        res = get_data("SELECT b.id, b.question_en FROM surveys a LEFT JOIN questions b on a.id = b.id_survey where a.id = 1")
        add_log(res,'get_questions_en')
        return res
    except Exception as ex:
        add_log(ex,'get_questions_en')

@app.route('/get_question_ru/<question_id>/', methods = ['GET', 'POST'])
def get_response_ru(question_id):
    try:
        res = get_data(f"SELECT id, response_options_ru FROM responses WHERE id_question = {question_id}")
        add_log(res,'get_response_ru')
        return res
    except Exception as ex:
        add_log(ex,'get_response_ru')

@app.route('/get_question_en/<question_id>/', methods = ['GET', 'POST'])
def get_response_en(question_id):
    try:
        res = get_data(f"SELECT id, response_options_en FROM responses WHERE id_question = {question_id}")
        add_log(res,'get_response_en')
        return res
    except Exception as ex:
        add_log(ex,'get_response_en')
    

if __name__ == '__main__':
    try:
        #log
        logging.basicConfig(level=logging.DEBUG, filename="logWSGI.log", filemode="w")
        logger = logging.getLogger(__name__)

        ch = logging.FileHandler("http-log.log")
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter("[%(levelname)s] %(message)s",
                              "%Y-%m-%d %H:%M:%S")

        ch.setFormatter(formatter)

        httpLogger = logging.getLogger("HTTP")
        httpLogger.addHandler(ch)
        httpLogger.addFilter(logging.Filter("HTTP"))

        #param server
        ip = getData('host', 'ip')
        port = getData('host', 'port', int)
        add_log(f'Start server {ip}:{port}','host')

        #start server
        http_server = WSGIServer((str(ip), port), app, log=httpLogger)
        http_server.serve_forever()

        add_log(f'Quit server {ip}:{port}','host')
    except Exception as ex:
        add_log(ex,'host')