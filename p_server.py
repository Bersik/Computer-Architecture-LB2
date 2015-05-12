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
        self.num = self.get_random()
        self.current_num = 0
        self.search = False
        self.count_num = 10
        self.prime = 0
        self.session = 0
        self.timeout = 20
        self.stopped = []
        self.log = []
        self.time = 0


    def get_random(self):
        count = random.randint(1000, 3000)
        self.num = random.getrandbits(count)
        return self.num

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
            self.current_num += 1
        self.search = True
        self.prime = 0
        self.session = "%x" % random.getrandbits(32)
        self.stopped = []
        self.time = datetime.now()
        self.add_log(u"Задане число: %s" % num)
        self.add_log(u"Сесія: %s" % self.session)

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
        if self.prime == 0 or (self.prime != 0 and self.prime > prime):
            self.prime = prime
            self.add_log(u"Клієнт №%d знайшов просте число: %s" % (id, prime))

            find = True
            for i in self.clients:
                if i != id:
                    if self.clients[i]["start_num"] < self.clients[id]["start_num"]:
                        find = False
                        break

            if find:
                self.add_log(u"Знайдено наступне просте число: %s" % prime)
                self.add_log(u"Час виконання: %s" % str(datetime.now() - self.time))
                self.stop()
        else:
            self.add_log(u"Клієнт №%d знайшов більше просте число: %s" % (id, prime))

    def stop(self):
        self.search = False
        for i in self.clients:
                    if self.clients[i]["start_num"]:
                        del self.clients[i]["start_num"]
        self.time = 0

    def get_work(self, id):
        """
        Видає роботу клієнту.
        Якщо масив stopped не пустий (є зупинені частини пошуку) віддаємо цю частину клієнту
        інакше віддаємо нову частину.

        :param id - номер клієнта
        :return session - сесія
                data - дані пошуку
                    count_num - к-сть чисел для пошуку
                    start_num - початкове число
        """
        self.check_clients()
        id = int(id)
        ret = {"session": self.session}
        if len(self.stopped) > 0:
            self.clients[id]["start_num"] = self.stopped[0]
            self.add_log(u"Клієнт №%d отримав відмінену задачу %s" % (id, self.stopped[0]))
            self.stopped.remove(self.stopped[0])
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

    #-----------------------------------------------------------
    def check_client(self, parameters):
        """
        Клієнт виконав завдання і не знайшов просто числа
        :param parameters - параметри клієнта
                    id - номер клієнта
        """
        id = int(parameters.get("id"))
        num = long(self.clients[id]["start_num"])
        self.add_log(u"Клієнт №%d перевірив числа (%d - %d). Просте число не знайдене." % (
            id, num, num + self.count_num))


    def stop_client(self, id):
        """
        Видаляє клієнта з номером id. Задачу, яку виконував клієнт додаємо
        в масив stopped, для подальшої передачі її іншому клієнту.
        :param id: номер клієнта
        """
        id = int(id)
        num = self.clients[id].get("start_num")
        if num:
            self.stopped.append(num)
        del self.clients[id]
        self.add_log(u"Клієнт №%d відключився. Його задачу (%s) додано до списку відменених." % (id, num))

    def server_update(self):
        """
        Запускає перевірку активності клієнтів.
        :return: список клієнтів clients; журнал log; просте число prime, якщо воно вже знайдене
        """
        self.check_clients()
        res = {"clients": self.clients, "log": self.log}
        if self.prime != 0 and self.search == False:
            res["prime"] = self.prime
        return res