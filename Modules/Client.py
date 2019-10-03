import json
import ProfanityBlocker
import time
import threading

global ProfaneService
ProfaneService = ProfanityBlocker.ProfanityService("LICENCEKEY", True, True, True)

global Clients
Clients = []

class Client:
    def __init__(self, connection):
        self.conn = connection
        self.CloseConnection = False
        self.name = "Q"
        global Clients
        Clients.append(self)
        self.readTask = threading.Thread(target=self.recvTsk, args=())
        self.readTask.start()

    def recvTsk(self):
        while not self.CloseConnection:
            time.sleep(0.4)
            try:
                d = self.conn.recv(1024)
                data = json.loads(d.decode())
                if data["Type"] == "Nick":
                    self.name = data["Value"]
                else:
                    # They Sent a message
                    Message = ProfaneService.ParseText(data["Value"])
                    global Clients
                    for client in Clients:
                        client.send({"Name": self.name, "Message": Message, "Type": "Message"})
            except Exception as e: # Client was closed unexpectedly
                print(e)
                self.disconnect()

    def send(self, message):
        try:
            self.conn.sendall(json.dumps(message).encode())
        except Exception as e: # Client was closed unexpectedly
            print(e.message)
            self.disconnect()

    def disconnect(self):
        self.CloseConnection = True
        self.conn = None