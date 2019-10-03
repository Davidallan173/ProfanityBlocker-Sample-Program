import socket
import json
from Modules.Client import Client

host = '127.0.0.1'
port = 1660
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(10)


while True:
    print("Waiting For Connections...")
    conn, addr = s.accept()
    print("Accepted from: " + str(addr))
    Client(conn)
