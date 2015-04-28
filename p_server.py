# -*- coding: utf-8 -*-
"""
Модуль для організації пошуку наступного простого числа.
"""
import random
from datetime import datetime


class PServer():
    """
    Клас для організації пошуку наступного простого числа.
    :param clients - словник клієнтів; key - номер клієнта, value - різні параметри клієнта
    :param num - задане число, звідки починається пошук
    :param current_num - число, з якого новий клієнт буде починати пошук
    :param search - статус пошуку: true - здійснюється пошук; false - пошук зупинений
    :param prime - тут буде зберігатись знайдене просте число
    :param session - унікальний ключ для ідентифікації пошуку
    :param timeout - к-сть секунд, після яких неактивні клієнти відключаються
    :param stopped - масив, який складається із зупинених частин пошуку
    :param log - журнал пошуку
    :param time - час початку пошуку
    """

    def __init__(self):
        """
        Ініціалізація полів класу
        """
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
        """
        Додавання запису в журнал
        :param info рядок, який потрібно додати у журнал
        """
        self.log.append("[" + str(datetime.now()) + "]: " + info)

    def set_num(self, num):
        """
        Якщо num - парне, додати до нього 1
        Запускає пошук наступного простого числа за числом num;
        self.session присвоюється випадкове значення із 32 біт для ідентифікації поточного пошуку
        :param num - число, з якого починається пошук
        """
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
        """
        Додати нового клієнта.
        :param ip - ip-адреса клієнта
        :return id - номер клієнта
        """
        id = 1
        while self.clients.get(id):
            id += 1
        self.clients[id] = {"ip": ip, "update": datetime.now()}
        self.add_log(u"Підключився новий клієнт: id:%d; ip:%s" % (id, str(ip)))
        return id

    def find(self, id, prime):
        """
        Зупиняє пошук, встановлює знайдене просте число, вираховує час пошуку
        :param id - номер клієнта
        :param prime - знайдене просте число
        """
        self.search = False
        self.prime = prime
        self.add_log(u"Клієнт №%d знайшов просте число: %s" % (id, prime))
        for i in self.clients:
            if self.clients[i]["start_num"]:
                del self.clients[i]["start_num"]
        self.add_log(u"Час виконання: %s" % str(datetime.now() - self.time))
        self.time = 0


    def get_work(self, id):
        """
        Видає роботу клієнту.
        Якщо масив stopped не пустий (є зупинені частини пошуку) віддаємо цю частину клієнту
            data
                count_num - к-сть чисел для пошуку
                start_num - початкове число
                i - позиція числа,з якого потрібно продовжити пошук
                iteration - число, на яке потрібно почати ділити поточне число
            stopped - True, зупинена частина
        інакше
            data
                count_num - к-сть чисел для пошуку
                start_num - початкове число
            stopped - False, новий пошук
        :param id - номер клієнта
        :return session - сесія
                stopped - тип пошуку
                data - дані пошуку
        """
        self.check_clients()
        id = int(id)
        ret = {"session": self.session, "stopped": False}
        if len(self.stopped) > 0:
            if type(self.stopped[0]) is not str:
                self.clients[id].update(self.stopped[0])
                self.add_log(
                    u"Клієнт №%d отримав відмінену задачу. Початкове число: %s" % (id, self.stopped[0]["start_num"]))
                self.stopped.remove(self.stopped[0])
                client = self.clients[id]
                ret["stopped"] = True
                ret["data"] = {"count_num": self.count_num, "start_num": client["start_num"], "i": client["i"],
                               "iteration": client["iteration"]}
            else:
                self.clients[id]["start_num"] = self.stopped[0]
                self.add_log(u"Клієнт №%d отримав відмінену задачу. Початкове число: %s" % (id, self.stopped[0]))
                self.stopped.remove(self.stopped[0])
                ret["data"] = {"start_num": str(self.clients[id]["start_num"]), "count_num": self.count_num}
        else:
            self.clients[id]["start_num"] = str(self.current_num)
            self.add_log(u"Клієнт №%d отримав задачу. Початкове число: %s" % (id, str(self.current_num)))
            self.current_num += self.count_num
            ret["data"] = {"start_num": str(self.clients[id]["start_num"]), "count_num": self.count_num}
        return ret

    def check_clients(self):
        """
        Перевіряє активність клієнтів. Якщо якийсь клієн не відправляв запит online на
        протязі останніх self.timeout секунд, він відключається
        """
        if len(self.clients) > 0:
            for key in self.clients.keys():
                print "Client id=" + str(key) + "  second=" + str(
                    (datetime.now() - self.clients[key]["update"]).seconds)
                if (datetime.now() - self.clients[key]["update"]).seconds > self.timeout:
                    self.stop_client(key)

    def online_client(self, id):
        """
        Встановити час останньої активності клієнта
        :param id - номер клієнта
        :return True - клієнт з таким id існує
                False - клієнта з таким id не існує

        """
        id = int(id)
        if self.clients.get(id):
            self.clients[id]["update"] = datetime.now()
            return True
        return False

    def check_client(self, parameters):
        """
        Вивід статусу виконання пошуку клієнтом
        :param parameters - параметри клієнта
                    id - номер клієнта
                    i - номер числа, яке перевіряється max=count
                    count - к-сть числе, що перевіряються
                    iteration - поточний дільник
                    current_num - поточне число
                    not_prime - якщо true, current_num ділиться націло на iteration
        """
        id = int(parameters.get("id"))
        i = parameters.get("i")
        count = parameters.get("count")
        iteration = parameters.get("iteration")
        current_num = parameters.get("current_num")
        not_prime = parameters.get("not_prime")

        self.clients[id]["i"] = i
        self.clients[id]["count"] = count
        self.clients[id]["iteration"] = iteration
        self.clients[id]["current_num"] = current_num
        self.clients[id]["not_prime"] = not_prime
        if not_prime == "true":
            self.add_log(u"Клієнт №%d перевірив число %s (%s/%s). Воно складене, ділиться на %s" % (
                id, current_num, i, count, iteration))
        else:
            self.add_log(
                u"Клієнт №%d перевіряє число %s (%s/%s). Зараз ділить на %s" % (id, current_num, i, count, iteration))


    def stop_client(self, id):
        """
        Видаляє клієнта з номером id. Задачу, яку виконував клієнт додаємо
        в масив stopped, для подальшої передачі її іншому клієнту.
        :param id: номер клієнта
        """
        id = int(id)
        if self.clients[id].get("start_num"):
            client = self.clients[id]
            if client.get("i") is not None and client.get("count") is not None and client.get("not_prime") is not None:
                if (client.get("not_prime") == 'true' and client.get("i") != client.get("count")
                    or
                        (client.get("not_prime") == 'false')):
                    self.stopped.append({
                        "start_num": client.get("start_num"),
                        "i": client.get("i"),
                        "count": client.get("count"),
                        "iteration": client.get("iteration"),
                        "current_num": client.get("current_num")
                    })
            else:
                self.stopped.append(client.get("start_num"))
        del self.clients[id]
        self.add_log(u"Клієнт №%d відключився. " % id)

    def server_update(self):
        """
        Запускає перевірку активності клієнтів.
        :return: список клієнтів clients; журнал log; просте число prime, якщо воно вже знайдене
        """
        self.check_clients()
        res = {"clients": self.clients, "log": self.log}
        if self.prime != 0:
            res["prime"] = self.prime
        return res