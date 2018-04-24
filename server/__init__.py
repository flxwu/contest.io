from flask import Flask, render_template, jsonify
from werkzeug.routing import BaseConverter
from .api.problems import getProblems
import requests, json

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__,
            static_folder = "../client/dist/static",
            template_folder = "../client/dist")

app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def index():
    if app.debug:
        return requests.get('http://localhost:3000/index.html').text
    return render_template("index.html")

# TODO: Query with tags as parameters
# TODO: Database Connection - #15, #16, #17
@app.route('/api/problems')
def problemset():
    return json.dumps(getProblems('graphs'))

@app.route('/sockjs-node/<path>')
def sockjs():
    if app.debug:
        return requests.post('http://localhost:3000/sockjs-node/{}'.format(path))
    return render_template("index.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:3000/{}'.format(path)).text
    return render_template("index.html")
    