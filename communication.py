import json
import socket
import threading

from database import DataBase

class ConnectionProtocol:


    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.is_connect = False

class BindingConnection(ConnectionProtocol):
    def __init__(self,host,port):
        super().__init__(host,port)
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.host,self.port))

    def stop(self):
        self.is_connect = False

    def start(self,handler):
        print("[SERVER] starting server..")
        self.server.listen(10)
        self.is_connect = True
        while self.is_connect:
            client, addr = self.server.accept()
            print(f"[SERVER] {client} connected!")
            client_thread = threading.Thread(target=handler,args=(client,),daemon=True)
            client_thread.start()
        self.server.close()
        print("[SERVER] closed.")


class ConnectionHandler:
    buffer = 1048
    def __init__(self):
        self.db = DataBase()
        self.db.load()
        self.clients = set()

    def broadcast(self,msg:str):
        for client in self.clients:
            client.send(msg.encode())

    def new_connection(self,client:socket.socket):
        self.clients.add(client)
        self.handle_client_requests(client)

    def handle_client_requests(self,client:socket.socket):
        client.send("Connected".encode())
        while True:
            try:
                req = client.recv(self.buffer).decode()
                print(f"[Server] res = {req}")
                req = json.loads(req)
                if req["type"] == "login":
                    self.db.add(req["data"])
                    client.send("ok".encode())
                    self.db.commit()
                elif req["type"] == "msg":
                    self.broadcast(req["data"])


            except Exception as e:
                print(e)
                break
        self.clients.remove(client)
        print(f"[SERVER] client {client} disconnected.")


if __name__ == '__main__':
    try:
        server = BindingConnection("127.0.0.1",5555)
        conn = ConnectionHandler()
        server.start(conn.new_connection)
    except Exception as e:
        print(e)
