# -*- coding: utf8 -*-

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

app_api = Flask(__name__)


@app_api.route("/test/")
def hello():
    return "Hello in api"


@app_api.route("/test/hello/")
def testhello():
    return "test hello"
