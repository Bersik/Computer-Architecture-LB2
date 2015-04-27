# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template

from p_server import PServer

app = Flask(__name__)

serv = PServer()

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/server', methods=['GET'])
def server():

    if request.args.get("num"):
        serv.set_num(request.args.get('num'))
        return "ok"

    if request.args.get("update"):
        param = serv.server_update()
        return jsonify(param)

    if request.args.get("stop"):
        serv.search = False
        return "ok"
    return render_template("server.html", search=serv.search)


@app.route('/client', methods=['GET'])
def client():
    return render_template("client.html")


@app.route('/worker', methods=['GET'])

def worker():
    """
    Обробка запитів від worker.
    :param GET type:
        start - додаємо клієнта
        get_work - дати роботу клієнту,
            якщо пошук запущений
                :return поточне число, к-сть чисел, сессія;
            інакше
                :return no_work
        find - клієнт знайшов просте число; якщо сесії співпали, зупиняємо пошук
            якщо сервер працював і сесії співпадають
                :return ok
            інакше
                :return error
        check - додаємо клієнта
        start - додаємо клієнта
        start - додаємо клієнта

    :return:
    """
    parameters = request.args

    if parameters.get("type") == "start":
        id = serv.add_client(request.remote_addr)
        return str(id)

    if parameters.get("type") == "get_work" and parameters.get("id"):
        if serv.search:
            param = {
                "num": serv.get_work(request.args.get("id")),
                "count_num": serv.count_num,
                "session": serv.session
            }
            return jsonify(param)
        else:
            return "no_work"

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

if __name__ == '__main__':
    #app.run(debug=True,host="192.168.0.103",port=80)
    app.run(debug=True)