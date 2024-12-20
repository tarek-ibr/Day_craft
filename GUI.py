import tkinter as tk
import ttkbootstrap as tkk
import db_functions

def destroy(self):
    try:
        self.app.destroy()
    except Exception:
        pass

class GUI():
    def __init__(self, root):  # Initialize the Gui class
        self.loginWindow = root
        self.login_Window()  # Call the login_Window method

    def login_Window(self):
        destroy(self)
        self.loginWindow.geometry('800x900')
        self.loginWindow.title('Login')
        self.loginWindow.resizable(False, False)


        self.loginWindow.bind("<MouseWheel>",
                              lambda event: None)
        # Then create a frame for the labels and entries
        self.frame = tk.Frame(self.loginWindow)
        self.frame.pack(expand=True)

        self.username_label = tkk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tkk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tkk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tkk.Entry(self.frame, show="•")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tkk.Button(self.frame, text="Login", command=self.authenticate, bootstyle="dark")
        self.login_button.grid(row=3, column=0, columnspan=2, pady=0)
        self.loginWindow.bind("<Return>", lambda event: self.authenticate())

        self.createuser = tkk.Button(self.frame, text="Create new user", bootstyle="dark-link")
        self.createuser.grid(row=4, column=0, columnspan=2, pady=5)
        self.createuser.bind("<Button-1>", lambda event: self.create_account())

        self.invalid = tkk.Label(self.frame, text="", foreground="red")
        self.invalid.grid(row=2, column=0, columnspan=2, pady=5)

        self.loginWindow.mainloop()
        self.frame.destroy()
        self.username_entry.destroy()

    def authenticate(self):
        pass

    def create_account(self):
        pass

    def check_username(self, username, password, name):
        pass


