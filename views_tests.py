# -*- coding: utf-8 -*-
import os
import views
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
        self.assertEquals('no_work',self.app.get('/worker?type=get_work&id=2').data)

        #запускаємо сервер
        self.assertEquals('ok',self.app.get('/server?num=500000').data)

        #беремо роботу1
        rv = self.send('/worker',{"type":"get_work","id":1})
        param = json.loads(rv.data)
        self.assertEquals(param["num"],"500001")
        self.assertEquals(param["count_num"],20)
        session = param["session"]
        #беремо роботу2
        rv = self.send('/worker',{"type":"get_work","id":2})
        param = json.loads(rv.data)
        self.assertEquals(param["num"],"500021")
        self.assertEquals(param["count_num"],20)
        self.assertEquals(session,param["session"])
        rv = self.send("/worker",{"type":"check","id":1,"session":session})
        self.assertEquals("ok",rv.data)
        rv = self.send("/worker",{"type":"online","id":1})


    def send(self,url,param):

        link = url + '?'
        for i in param:
            link += str(i)+"="+str(param[i])+"&"
        print link[:-1]
        return self.app.get(link[:-1])

if __name__ == '__main__':
    unittest.main()