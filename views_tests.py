# -*- coding: utf-8 -*-
import os
from app import views,app
import unittest
import json
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        views.app.config['TESTING'] = True
        self.app = views.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        assert 'Client' in rv.data
        assert 'Server' in rv.data

    def test_view1(self):
        #додаємо нових клієнтів
        self.assertEquals('1',self.app.get('/worker?type=start').data)
        self.assertEquals('2',self.app.get('/worker?type=start').data)

        #перш ніж брати роботу, треба запустити сервер
        self.assertEquals('error',self.app.get('/worker?type=get_work&id=2').data)

        #запускаємо сервер
        self.assertEquals('ok',self.app.get('/server?num=500000').data)

        #беремо роботу
        rv = self.app.get('/worker?type=get_work&id=1')
        param = json.loads(rv.data)
        self.assertEquals(param["num"],"500001")
        self.assertEquals(param["count_num"],20)

        session = param["session"]

        #assert 'error' in self.app.get('/worker?type=get_work&id=2')
        #print rv.data

if __name__ == '__main__':
    unittest.main()