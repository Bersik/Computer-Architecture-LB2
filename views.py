# -*- coding: utf-8 -*-
"""
Модуль обробки запитів до серверу.
"""
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
    """
    Обробка запитів від server.
    :param GET
        num - встановити нове число для пошуку.
            :return ok
        update - запит на оновлення вмісту сторінки
            :return список клієнтів і log
        stop - зупинити пошук
            :return ok
    інакше
        :return: віддати server.html і поточний статус пошуку
    """
    if request.args.get("num"):
        serv.set_num(request.args.get('num'))
        return "ok"

    if request.args.get("update"):
        param = serv.server_update()
        return jsonify(param)

    if request.args.get("stop"):
        serv.search = False
        return "ok"

    if request.args.get("get_random"):
        if not serv.search:
            return str(serv.get_random())
        else:
            return ""
    return render_template("server.html", search=serv.search, start_num=str(serv.num))


@app.route('/client', methods=['GET'])
def client():
    return render_template("client.html")


@app.route('/worker', methods=['GET'])
def worker():
    """
    Обробка запитів від worker.
    :param GET type:
        start - клієнт підключився
            :return id клієнта
        get_work - клієнт просить роботу
            якщо пошук запущений
                :return див. p_server.get_work
            інакше
                :return no_work
        find - клієнт знайшов просте число; якщо сесії співпали, зупиняємо пошук
            якщо сервер працював і сесії співпадають
                :return ok
            інакше
                :return error
        check - прогрес клієнта
            якщо пошук запущений і сесії співпадають
                :return ok
            інакше
                :return error
        online - клієнт активний (не відключився)
            Якщо клієнт є в списку клієнтів
                :return ok
            інакше
                :return error
        stop - відключення клієнта
            :return ok
    інакше
        :return: error
    """
    parameters = request.args

    if parameters.get("type") == "start":
        id = serv.add_client(request.remote_addr)
        return str(id)

    if parameters.get("type") == "get_work" and parameters.get("id"):
        if serv.search:
            return jsonify(serv.get_work(request.args.get("id")))
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
    # app.run(debug=True,host="192.168.0.103",port=80)
    app.run(debug=True)