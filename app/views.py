from app import app
from flask import jsonify
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/server')
def server():
    return render_template("server.html")

@app.route('/client')
def client():
    return render_template("client.html")

@app.route('/client_connect',methods=['GET'])
def client_connect():
    return jsonify({"num":"888","id":5});