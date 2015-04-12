from app import app
from flask import jsonify, request, render_template
import Queue

from p_server import PServer

serv = PServer()
queue = Queue.Queue()

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/server',methods=['GET'])
def server():
    if request.args.get("num"):
        serv.set_num(request.args.get('num'))
        return jsonify({})
    if request.args.get("update"):
        clients = serv.get_clients()
        json = jsonify(clients)
        return json
    if request.args.get("stop"):
        serv.search = False
        return jsonify({})
    return render_template("server.html", search=serv.search)

@app.route('/client',methods=['GET'])
def client():
    return render_template("client.html")

@app.route('/worker',methods=['GET'])
def worker():
    id = serv.add_client(request.remote_addr)
    num = serv.get_num(id)
    return jsonify({"num":str(num),"id":id})
