from time import sleep
import random

class PServer():

    def __init__(self):
        self.clients = dict()
        self.num = 0
        self.current_num = 0
        self.search = False
        self.count_op = 1000000
        self.count_num = 20
        self.prime = 0
        self.session = 0

    def set_num(self, num):
        self.num = long(num)
        self.current_num = self.num + 1
        if self.current_num % 2 == 0:
            self.current_num = self.current_num + 1
        self.search = True
        self.prime = 0
        self.session = "%x" % random.getrandbits(32)
        print self.session
        print self.current_num
        print "new_num=" + str(self.num)

    def add_client(self, ip):
        id = 1
        while self.clients.get(id):
            id += 1
        self.clients[id] = {"ip":ip}
        print "connected client: " + str(id) + ") " + str(ip)
        return id

    def delete_client(self, id):
        del self.clients[id]
        return id

    def get_num(self, id):
        return self.num

    def get_clients(self):
        return self.clients

    def get_work(self, id):
        id = int(id)
        self.clients[id]["start_num"]=self.current_num

        self.current_num = self.current_num + self.count_num
        return self.clients[id]["start_num"]

