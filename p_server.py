# -*- coding: utf-8 -*-
import random
from datetime import datetime


class PServer():
    def __init__(self):
        self.clients = dict()
        self.num = 0
        self.current_num = 0
        self.search = False
        self.count_num = 20
        self.prime = 0
        self.session = 0
        self.timeout = 20
        self.stopped = []
        self.log = []
        self.time = 0

    def add_log(self, info):
        self.log.append("[" + str(datetime.now()) + "]: " + info)

    def set_num(self, num):
        self.num = long(num)
        self.current_num = self.num + 1
        if self.current_num % 2 == 0:
            self.current_num = self.current_num + 1
        self.search = True
        self.prime = 0
        self.session = "%x" % random.getrandbits(32)
        self.stopped = []
        self.time = datetime.now()
        self.add_log(u"Задане число: %s" % num)
        self.add_log(u"Сессія: %s" % self.session)

    def add_client(self, ip):
        id = 1
        while self.clients.get(id):
            id += 1
        self.clients[id] = {"ip": ip, "update": datetime.now()}
        self.add_log(u"Підключився новий клієнт: id:%d; ip:%s" % (id, str(ip)))
        return id

    def find(self, id, prime):
        self.search = False
        self.prime = prime
        self.add_log(u"Клієнт №%d знайшов просте число: %s" % (id, prime))
        self.add_log(u"Час виконання: %s" % str(datetime.now() - self.time))
        self.time = 0

    def get_clients(self):
        return self.clients

    def get_work(self, id):
        id = int(id)
        if len(self.stopped) > 0:
            self.clients[id]["start_num"] = self.stopped[0]
            self.add_log(u"Клієнт №%d отримав відмінену задачу. Початкове число: %s" % (id, self.stopped[0]))
            self.stopped.remove(self.stopped[0])
        else:
            self.clients[id]["start_num"] = str(self.current_num)
            self.add_log(u"Клієнт №%d отримав задачу. Початкове число: %s" % (id, str(self.current_num)))
            self.current_num = self.current_num + self.count_num
        return str(self.clients[id]["start_num"])

    def check_clients(self):
        if len(self.clients) > 0:
            for key in self.clients.keys():
                print "Client id=" + str(key) + "  second=" + str(
                    (datetime.now() - self.clients[key]["update"]).seconds)
                if (datetime.now() - self.clients[key]["update"]).seconds > self.timeout:
                    self.stop_client(key)

    def online_client(self, id):
        id = int(id)
        if self.clients.get(id):
            self.clients[id]["update"] = datetime.now()
            return True
        return False

    def check_client(self, parameters):
        id = int(parameters.get("id"))
        i = parameters.get("i")
        count = parameters.get("count")
        current_num = parameters.get("current_num")
        iteration = parameters.get("iteration")

        if parameters.get("not_prime") == "true":
            self.add_log(u"Клієнт №%d перевірив число %s (%s/%s). Воно складене, ділиться на %s" % (
                id, current_num, i, count, iteration))
        else:
            self.add_log(
                u"Клієнт №%d перевіряє число %s (%s/%s). Зараз ділить на %s" % (id, current_num, i, count, iteration))

    def stop_client(self, id):
        id = int(id)
        if (self.clients[id].get("start_num")):
            self.stopped.append(self.clients[id]["start_num"])
        del self.clients[id]
        self.add_log(u"Клієнт №%d відключився. " % id)

    def server_update(self):
        self.check_clients()
        res = {"clients": self.clients, "log": self.log}
        if self.prime != 0:
            res["prime"] = self.prime
        return res