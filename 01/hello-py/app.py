import os

from flask import Flask

app = Flask(__name__)


@app.route("/health")
def health():
    return "{'status': 'ok'}"


@app.route("/")
def hello():
    return f"Hello world {os.environ['HOSTNAME']}!"
