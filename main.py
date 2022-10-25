import threading
from tkinter import messagebox


from gui import *
import schemas
class App:
    def __init__(self):
        self.win = tk.Tk()
        self.network = Networking("127.0.0.1", 5555)
        self.screen = AuthenticationScreen(self.win, self.network)
        self.thread_recv = threading.Thread(target=self.response, daemon=True)

    def response(self):
        while True:
            res = self.network.client.recv(1048).decode()

            if res == "ok":
                messagebox.showinfo(title="Register", message="YOU REGISTER COMPLETE")

            elif "logged in" in res:
                self.screen.destroy()
                self.network.logged_name = self.screen.user_temp
                self.screen = ChatScreen(self.win, self.network, self.screen.user_temp)

            elif "error" in res:
                res = schemas.NativeFormat(**json.loads(res))
                res = schemas.ErrorSchemas(**res.data)
                print(res)
                if schemas.ErrorInfo.USER_NOT_FOUND in res.info:
                    messagebox.showerror(title="Login",message="Username Not Found")
                elif schemas.ErrorInfo.USER_EXISTS in res.info:
                    messagebox.showerror(title="Register", message="Username Already Exists")
                elif schemas.ErrorInfo.PASSWORD_NOT_MATCH in res.info:
                    messagebox.showerror(title="Login", message="Password Not Match")
            else:
                if self.network.logged_name:
                    self.screen.buffer_text += res + "\n"
                    self.screen.text_box.config(state=tk.NORMAL)
                    self.screen.text_box.delete(1.0, "end")
                    self.screen.text_box.insert(1.0, self.screen.buffer_text)
                    self.screen.text_box.config(state=tk.DISABLED)

    def main_loop(self):
        self.thread_recv.start()
        self.screen.run()


if __name__ == '__main__':
    a = App()
    a.main_loop()