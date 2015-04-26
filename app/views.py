from app import app
from flask import jsonify, request, render_template

from p_server import PServer

serv = PServer()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/server', methods=['GET'])
def server():
    if request.args.get("num"):
        serv.set_num(request.args.get('num'))
        return jsonify({})
    if request.args.get("update"):
        serv.check_clients()
        res = {"clients": serv.get_clients(), "log": serv.log}
        if serv.prime != 0:
            res["prime"] = serv.prime
        json = jsonify(res)
        return json
    if request.args.get("stop"):
        serv.search = False
        return "ok"
    return render_template("server.html", search=serv.search)


@app.route('/client', methods=['GET'])
def client():
    return render_template("client.html")


@app.route('/worker', methods=['GET'])
def worker():
    parameters = request.args

    if parameters.get("type") == "start":
        id = serv.add_client(request.remote_addr)
        return str(id)

    if parameters.get("type") == "get_work" and parameters.get("id"):
        if serv.search:
            return jsonify(
                {"num": serv.get_work(request.args.get("id")), "count_num": serv.count_num, "session": serv.session})
        else:
            return "error"

    if parameters.get("type") == "find" and parameters.get("session"):
        if serv.search and serv.session == parameters.get("session"):
            serv.find(int(parameters.get("id")), parameters.get("prime"))
            return "ok"
        else:
            return "error"

    if parameters.get("type") == "check":
        if serv.search and request.args.get("session") == serv.session and parameters.get("id"):
            serv.check_client(parameters)
            return "ok"
        return "error"

    if parameters.get("type") == "online":
        if serv.online_client(parameters.get("id")):
            return "ok"
        return "error"

    if parameters.get("type") == "stop":
        serv.stop_client(parameters.get("id"))
        return "ok"
    return "error"

