import socket
import threading
import tkinter as tk
import json
from tkinter.scrolledtext import ScrolledText

import user_model
from communication import ConnectionProtocol


class Networking(ConnectionProtocol):
    def __init__(self, host, port):
        super().__init__(host, port)
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((self.host, self.port))
        self.logged_name = None

    def request(self, method: str, data: [dict, object]):
        if not isinstance(data, dict) and not isinstance(data, str):
            data = data.to_json()
        if self.logged_name:
            data = {'name': self.logged_name, 'msg': data}
        data_ = NativeFormat(method, data)

        self.client.send(data_.pack())

    @property
    def client(self) -> socket.socket:
        return self._client


class RequestsMethods:
    login = "login"
    register = "register"
    message = "msg"


class NativeFormat:
    def __init__(self, type: str, data: dict):
        self.type = type
        self.data = data

    def pack(self):
        return json.dumps(self.__dict__).encode()


class Screen:
    def __init__(self):
        self.network = Networking("127.0.0.1", 5555)
        self.win = tk.Tk()
        self.win.geometry("500x500")
        self.win.title("Chat Room!")
        self.send_btn = tk.Button(self.win, text="Send", command=self.send)
        self.chat_entry = tk.Entry(self.win)
        self.text_box = ScrolledText(self.win)
        self.entry_username = tk.Entry(self.win)
        self.password_entry = tk.Entry(self.win)
        self.login_btn = tk.Button(self.win, text="Login", command=self.login)
        self.register_btn = tk.Button(self.win, text="Register", command=self.register)
        self.entry_username.place(x=200, y=100)
        self.password_entry.place(x=200, y=200)
        self.login_btn.place(x=200, y=300)
        self.register_btn.place(x=300, y=300)
        self.buffer_text = ""
        self.user_temp = None

    def send(self):
        self.network.request(RequestsMethods.message, self.chat_entry.get())
        self.chat_entry.delete(0, "end")

    def response(self):
        while True:
            res = self.network.client.recv(1048).decode()
            if res == "ok":
                self.chat_screen()
            elif "logged in" in res:
                self.chat_screen()
                self.network.logged_name = self.user_temp
            elif res == "error":
                print(res)
            else:
                if self.network.logged_name:
                    self.buffer_text += res + "\n"
                    self.text_box.config(state=tk.NORMAL)
                    self.text_box.delete(1.0, "end")
                    self.text_box.insert(1.0, self.buffer_text)
                    self.text_box.config(state=tk.DISABLED)

    def chat_screen(self):
        self.entry_username.destroy()
        self.password_entry.destroy()
        self.login_btn.destroy()
        self.register_btn.destroy()
        self.text_box.pack()
        self.chat_entry.pack()
        self.send_btn.pack()

    def get_user_pass_data(self) -> user_model.User:
        username = self.entry_username.get()
        password = self.password_entry.get()
        self.entry_username.delete(0, "end")
        self.password_entry.delete(0, "end")
        user = user_model.User(username, password)
        return user

    def register(self):
        user = self.get_user_pass_data()
        self.network.request(RequestsMethods.register, user)

    def login(self):
        user = self.get_user_pass_data()
        self.network.request(RequestsMethods.login, user)
        self.user_temp = user.username

    def run(self):
        thread_recv = threading.Thread(target=self.response, daemon=True)
        thread_recv.start()

        self.win.mainloop()


if __name__ == '__main__':
    a = Screen()
    a.run()
