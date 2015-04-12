from time import sleep

class PServer():

    def __init__(self):
        self.clients = dict()
        self.num = 0
        self.current_num = 0
        self.search = False

    def set_num(self, num):
        self.num = long(num)
        self.current_num = self.num
        self.search = True
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

