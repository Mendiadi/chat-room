import socket
import threading
import tkinter as tk
import json
import user_model
from communication import ConnectionProtocol
class Networking(ConnectionProtocol):
    def __init__(self,host,port):
        super().__init__(host,port)
        self._client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._client.connect((self.host,self.port))



    @property
    def client(self) -> socket.socket:
        return self._client


class Screen:
    def __init__(self):
        self.network = Networking("127.0.0.1",5555)
        self.win = tk.Tk()
        self.win.geometry("500x500")
        self.send_btn = tk.Button(self.win,text="Send",command=self.send)
        self.chat_entry = tk.Entry(self.win)
        self.entry_username = tk.Entry(self.win)
        self.password_entry = tk.Entry(self.win)
        self.login_btn = tk.Button(self.win,text="Login",command=self.login)
        self.entry_username.pack()
        self.password_entry.pack()
        self.login_btn.pack()

    def send(self):
        self.network.client.send(self.chat_entry.get().encode())
        self.chat_entry.delete("1.0","end")


    def response(self):
        while True:
            res = self.network.client.recv(1048).decode()
            if res == "ok":
                self.chat_screen()
                print(res)
            else:
                print(res)

    def chat_screen(self):
        self.entry_username.forget()
        self.password_entry.forget()
        self.login_btn.forget()
        self.chat_entry.pack()
        self.send_btn.pack()


    def login(self):
        username = self.entry_username.get()
        password = self.password_entry.get()
        self.entry_username.delete(0,"end")
        self.password_entry.delete(0, "end")
        user = user_model.User(username,password)
        data = {"type":"login","data":user.to_json()}
        self.network.client.send(json.dumps(data).encode())


    def run(self):
        thread_recv = threading.Thread(target=self.response,daemon=True)
        thread_recv.start()

        self.win.mainloop()


if __name__ == '__main__':
    a = Screen()
    a.run()