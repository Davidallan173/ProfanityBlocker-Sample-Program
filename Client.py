import socket
import json
import time
import threading

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 1660))
        self.readTask = threading.Thread(target=self.ReadLoop, args=())
        self.readTask.start()

    def send(self, data):
        data = json.dumps(data).encode()
        self.s.send(data)

    def ReadLoop(self):
        while 1:
            time.sleep(0.4)
            data = self.s.recv(1024).decode()
            for d in data.split("}"):
                if d == "":
                    continue
                jd = json.loads(d+"}")
                if jd["Type"] == "Message":
                    Name = jd["Name"]
                    Message = jd["Message"]
                    print(Name + "> " + Message)

c = Client()

while 1:
    Text = input("")
    if Text.split(" ")[0].lower() == "!nick":
        c.send({"Type": "Nick", "Value": Text.lower().replace("!nick", "")})
    else:
        c.send({"Type": "Message", "Value": Text})