# -*- coding: utf-8 -*-
import random
import unittest
from selenium import webdriver
from time import sleep


class ClasterPrimeNumbers(unittest.TestCase):
    def setUp(self):
        self.server = webdriver.Firefox()
        self.client1 = webdriver.Firefox()
        self.client2 = webdriver.Firefox()
        self.count_num = 100
        self.num = 3992231807651010719611701868170507840025756582038953431446593124078648458199433073539376500971851906781588991003629587619911039778685705821334278508904893584468541826398138785947180623869682877751850248141344726228258117849171313709176179967369283780768725707282276724692940460895613262255627765651818


    def test_system(self):
        server = self.server
        client1 = self.client1
        client2 = self.client2
        server.get("http://127.0.0.1/server")
        self.assertIn("Server", server.title)
        if server.find_element_by_id("button_search").text==u"Зупинити":
            server.find_element_by_id("button_search").click()
            sleep(1)
        server.find_element_by_id("get_random").click()
        self.assertTrue(int(server.find_element_by_id("number").text) > 0)
        server.find_element_by_id("number").clear()
        server.find_element_by_id("number").send_keys(str(self.num))
        self.assertIn(u"Пошук", server.find_element_by_id("button_search").text)
        self.assertTrue(len(server.find_element_by_id("number").text) > 50)
        server.find_element_by_id("button_search").click()
        sleep(1)
        self.assertEquals(u"Зупинити", server.find_element_by_id("button_search").text)

        #Клієнт 1
        client1.get("http://127.0.0.1/client")
        self.assertEquals(u"Клієнт", client1.title)
        sleep(1)
        client1.find_element_by_id("button_con").click()

        #Клієнт 2
        client2.get("http://127.0.0.1/client")
        self.assertEquals(u"Клієнт", client2.title)
        sleep(1)
        client2.find_element_by_id("button_con").click()

        while(client1.find_element_by_id("id").text=="-"):
            sleep(1)
        self.assertEquals(client1.find_element_by_id("id").text, "1")
        self.assertEquals(client1.find_element_by_id("num").text, str(self.num+1))

        while(client2.find_element_by_id("id").text=="-"):
            sleep(1)
        self.assertEquals(client2.find_element_by_id("id").text, "2")
        self.assertEquals(client2.find_element_by_id("num").text, str(self.num + 1 + self.count_num))

        #Зупиняємо клієнта і запускаємо знову. Повинен взяти відмінену задачу
        client1.find_element_by_id("button_con").click()
        sleep(1)
        client1.find_element_by_id("button_con").click()
        while(client1.find_element_by_id("id").text=="-"):
            sleep(1)
        self.assertEquals(client1.find_element_by_id("id").text, "1")
        self.assertEquals(client1.find_element_by_id("num").text, str(self.num+1))


        while(server.find_element_by_id("prime_num").text==""):
            sleep(1)

        self.assertEquals(server.find_element_by_id("prime_num").text,"3992231807651010719611701868170507840025756582038953431446593124078648458199433073539376500971851906781588991003629587619911039778685705821334278508904893584468541826398138785947180623869682877751850248141344726228258117849171313709176179967369283780768725707282276724692940460895613262255627765652767")

    def tearDown(self):
        self.server.close()
        self.client1.close()
        self.client2.close()


if __name__ == "__main__":
    unittest.main()