# vue/flask implementation of rcdbot
import requests
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from rdb import Rdb
import db


app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/submissions", methods=["GET", "POST"])
def search_submissions():
    rdb = Rdb()
    response_object = {}
    if "sphrase" in request.args and "sortmode" in request.args:
        sphrase = request.args["sphrase"]
        sortmode = request.args["sortmode"]
        response_object = rdb.get_submissions(sphrase, sortmode)
    else:
        response_object = rdb.get_submissions()

    return jsonify(response_object)


@app.route("/api/process_selections", methods=["GET", "POST"])
def process_selections():
    rdb = Rdb()
    response_object = {}
    idlist = []
    for i in range(0, len(request.args)):
        idlist.append(request.args.get(str(i)))

    response_object = rdb.scan_submissions(idlist)
    return jsonify(response_object)


@app.route("/api/historic_data", methods=["GET", "POST"])
def historic_data():
    response_data = db.grab_all()
    return jsonify(response_data)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # if app.debug:
    #   return requests.get("https://rdbdemofront.herokuapp.com/{}".format(path)).text
    return render_template("index.html")
