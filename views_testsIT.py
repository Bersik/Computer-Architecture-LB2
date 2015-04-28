# -*- coding: utf-8 -*-
import os
import views
import unittest
import json


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        views.app.config['TESTING'] = True
        self.app = views.app.test_client()

    def test_client_worker(self):
        # додаємо нових клієнтів
        self.assertEquals('1', self.send('/worker', {"type": "start"}).data)
        self.assertEquals('2', self.send('/worker', {"type": "start"}).data)
        self.assertEquals('3', self.send('/worker', {"type": "start"}).data)

        #перш ніж брати роботу, треба запустити сервер
        self.assertEquals('no_work', self.send('/worker', {"type": "get_work", "id": "2"}).data)

        #запускаємо сервер
        self.assertEquals('ok', self.send('/server', {"num": "5000000000000000"}).data)

        #беремо роботу1
        rv = self.send('/worker', {"type": "get_work", "id": 1})
        param = json.loads(rv.data)
        param_data = param["data"]
        self.assertEquals(param_data["start_num"], "5000000000000001")
        self.assertEquals(param_data["count_num"], 20)
        session = param["session"]
        #беремо роботу2
        rv = self.send('/worker', {"type": "get_work", "id": 2})
        param = json.loads(rv.data)
        param_data = param["data"]
        self.assertEquals(param_data["start_num"], "5000000000000021")
        self.assertEquals(param_data["count_num"], 20)
        self.assertEquals(session, param["session"])

        #перевіряємо прогрес клієнта
        rv = self.send("/worker", {"type": "check", "id": 1, "session": session})
        self.assertEquals("ok", rv.data)

        #клієнт 2 активний
        self.send("/worker", {"type": "online", "id": 2})

        #зупиняємо 1 клієнта
        rv = self.send("/worker", {"type": "stop", "id": 1})
        self.assertEquals("ok", rv.data)

        #знову підключаємо клієнта 1
        self.assertEquals('1', self.send('/worker', {"type": "start"}).data)
        #беремо роботу для клієнта 1
        rv = self.send('/worker', {"type": "get_work", "id": 1})
        param = json.loads(rv.data)
        param_data = param["data"]
        #повинно видатись зупинене завдання
        self.assertEquals(param_data["start_num"], "5000000000000001")
        self.assertEquals(param_data["count_num"], 20)
        self.assertEquals(session, param["session"])

        #беремо роботу для клієнта 3
        rv = self.send('/worker', {"type": "get_work", "id": 3})
        param = json.loads(rv.data)
        param_data = param["data"]
        #повинно видатись нове завдання
        self.assertEquals(param_data["start_num"], "5000000000000041")
        self.assertEquals(param_data["count_num"], 20)
        self.assertEquals(session, param["session"])

        #знайшли просте число
        rv = self.send("/worker", {"type": "find", "id": 2, "session": session, "prime": "5000000000000003"})
        self.assertEquals("ok", rv.data)

        rv = self.send("/worker", {"type": "find", "id": 1, "session": session, "prime": "5000000000000009"})
        #оскільки число вже знайдено, сервер зупинено, відповідно return error
        self.assertEquals("error", rv.data)

        rv = self.send("/worker", {"type": "check", "id": 3, "session": session})
        self.assertEquals("error", rv.data)

        #запускаємо сервер знову
        self.assertEquals('ok', self.send('/server', {"num": "165486487500"}).data)
        #беремо роботу1
        rv = self.send('/worker', {"type": "get_work", "id": 1})
        param = json.loads(rv.data)
        param_data = param["data"]
        self.assertEquals(param_data["start_num"], "165486487501")
        self.assertEquals(param_data["count_num"], 20)
        self.assertNotEqual(param["session"], session)
        session = param["session"]

        #зупиняємо сервер
        self.assertEquals('ok', self.send('/server', {"stop": True}).data)

        #беремо роботу2
        rv = self.send('/worker', {"type": "get_work", "id": 2})
        self.assertEquals(rv.data, "no_work")

    def send(self, url, param):
        link = url + '?'
        for i in param:
            link += str(i) + "=" + str(param[i]) + "&"
        return self.app.get(link[:-1])


if __name__ == '__main__':
    unittest.main()