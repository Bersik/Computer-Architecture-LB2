from time import sleep
import random
from datetime import datetime

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
        self.timeout = 20
        self.stopped = []

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
        self.clients[id] = {"ip":ip,"update":datetime.now()}
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
        if len(self.stopped)>0:
            self.clients[id]["start_num"]=self.stopped[0]
            self.stopped.remove(self.stopped[0])
        else:
            self.clients[id]["start_num"]=self.current_num
            self.current_num = self.current_num + self.count_num
        return self.clients[id]["start_num"]

    def check_clients(self):
        if len(self.clients) > 0:
            for key in self.clients.keys():
                print "Client id=" + str(key) + "  second=" + str((datetime.now() - self.clients[key]["update"]).seconds)
                if (datetime.now() - self.clients[key]["update"]).seconds > self.timeout:
                    if (self.clients[key].get("start_num")):
                        self.stopped.append(self.clients[key]["start_num"])
                    del self.clients[key]

    def check_client(self, id):
        self.clients[int(id)]["update"] = datetime.now()

    def stop_client(self, id):
        id=int(id)
        if (self.clients[id].get("start_num")):
            self.stopped.append(self.clients[id]["start_num"])
        del self.clients[id]
