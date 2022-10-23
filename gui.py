import tkinter as tk
from tkinter.scrolledtext import ScrolledText


import db_model
from client_net import *



class Screen:
    def __init__(self, win, net):
        self.network = net
        self.buffer_text = ""
        self.win = win
        self.win.geometry("700x700")
        self.win.title("Chat Room!")
        self.win.maxsize(700, 700)
        self.win.minsize(700, 700)
        self.user_temp = None

    def run(self):
        self.win.mainloop()


class AuthenticationScreen(Screen):
    def __init__(self, win, net):
        super().__init__(win, net)
        self.win.configure(background="green")
        self._job = None
        ###################### LOGIN ###########################

        # ********* ENTRIES *******#
        self.username_entry = tk.Entry(self.win, width=20, bg="green", bd=0, font="none 10 bold")
        self.password_entry = tk.Entry(self.win, width=20, bg="green", bd=0, font="none 10 bold", show="*")

        # ********* LABELS *******#
        self.username_verify = tk.Label(self.win, fg="red", text="Invalid", font="none 10 bold", bg="green")
        self.password_verify = tk.Label(self.win, fg="red", text="Invalid", font="none 10 bold", bg="green")
        self.head_login_frame_text = tk.Label(self.win, text="Please Login or SignUp",
                                              font="none 20 bold", bg="green")
        self.username_text = tk.Label(self.win, text="Username:", font="none 12 bold", bg="green")
        self.password_text = tk.Label(self.win, text="Password:", font="none 12 bold", bg="green")

        # ********* BUTTONS *******#
        self.show_hide_btn = tk.Button(self.win, text="Show", font="none 8 bold", command=self.show_hide,
                                       bg="green",
                                       highlightthickness=0, border=0)
        self.register_btn = tk.Button(self.win, text="Sign up & Login", command=self.register, bg="gray",
                                      font="none 10 bold", state=tk.DISABLED)
        self.log_in_btn = tk.Button(self.win, text="Login", command=self.login, bg="gray", font="none 10 bold",
                                    state=tk.DISABLED)
        self.checkVar1 = tk.IntVar()
        self.keep_me_log_in_btn = tk.Checkbutton(self.win, text="keep me login", variable=self.checkVar1
                                                 , onvalue=1, offvalue=0, height=1, width=14, bg="green")

        # ********* CANVASES *******#
        self.decorate_label_u = tk.Canvas(self.win, width=100, height=2.0, bg="black", highlightthickness=0)
        self.decorate_label_p = tk.Canvas(self.win, width=100, height=2.0, bg="black", highlightthickness=0)

        # ********* MISC *******#
        self.pass_shown = True

        self.head_login_frame_text.pack()
        self.username_text.place(x=300, y=100)
        self.username_entry.place(x=300, y=150)
        self.username_verify.place(x=240, y=150)
        self.decorate_label_u.place(x=300, y=170)
        self.password_text.place(x=300, y=200)
        self.password_verify.place(x=240, y=250)
        self.password_entry.place(x=300, y=250)
        self.show_hide_btn.place(x=500, y=250)
        self.decorate_label_p.place(x=300, y=270)
        self.keep_me_log_in_btn.place(x=300, y=280)
        self.register_btn.place(x=300, y=300)
        self.log_in_btn.place(x=300, y=350)
        self.scan()

    def register(self):
        user = self.get_user_pass_data()
        self.network.request(RequestsMethods.register, user)

    def login(self):
        user = self.get_user_pass_data()
        self.network.request(RequestsMethods.login, user)
        self.user_temp = user.username

    def get_user_pass_data(self) -> db_model.User:
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        user = db_model.User(username, password)
        return user

    def destroy(self):
        self.win.after_cancel(self._job)
        self.keep_me_log_in_btn.destroy()
        self.show_hide_btn.destroy()
        self.password_verify.destroy()
        self.username_verify.destroy()
        self.password_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.destroy()
        self.username_entry.destroy()
        self.username_text.destroy()
        self.password_text.destroy()
        self.register_btn.destroy()
        self.log_in_btn.destroy()
        self.head_login_frame_text.destroy()
        self.decorate_label_u.destroy()
        self.decorate_label_p.destroy()

    def scan(self):
        if len(self.username_entry.get()) <= 5:
            self.username_verify.configure(text="Invalid", fg="red")
            user_pass = False
        else:
            self.username_verify.configure(text="Valid", fg="black")
            user_pass = True
        if len(self.password_entry.get()) <= 5:
            self.password_verify.configure(text="Invalid", fg="red")
            pass_pass = False
        else:
            self.password_verify.configure(text="Valid", fg="black")
            pass_pass = True
        if pass_pass and user_pass:
            self.register_btn.configure(state=tk.ACTIVE)
            self.log_in_btn.configure(state=tk.ACTIVE)
        else:
            self.register_btn.configure(state=tk.DISABLED)
            self.log_in_btn.configure(state=tk.DISABLED)

        self._job = self.win.after(1000, self.scan)

    def show_hide(self):
        if self.pass_shown:
            self.password_entry.configure(show="")
            self.show_hide_btn.configure(text="hide")
            self.pass_shown = not self.pass_shown
        else:
            self.password_entry.configure(show="*")
            self.pass_shown = not self.pass_shown
            self.show_hide_btn.configure(text="show")


class ChatScreen(Screen):
    def __init__(self, win, net, user):
        super().__init__(win, net)
        self.send_btn = tk.Button(self.win, text="Send", command=self.send)
        self.chat_entry = tk.Entry(self.win)
        self.text_box = ScrolledText(self.win, state=tk.DISABLED)
        self.user_temp = user
        self.chat_screen()

    def send(self):
        self.network.request(RequestsMethods.message, self.chat_entry.get())
        self.chat_entry.delete(0, "end")

    def chat_screen(self):
        self.text_box.pack()
        self.chat_entry.pack()
        self.send_btn.pack()

    def destroy(self):
        self.text_box.destroy()
        self.chat_entry.destroy()
        self.send_btn.destroy()



