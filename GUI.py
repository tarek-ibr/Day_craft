import tkinter as tk
import ttkbootstrap as tkk


class GUI():
    def __init__(self, root):  # Initialize the Gui class
        self.loginWindow = root
        self.login_Window()  # Call the login_Window method

    def login_Window(self):
        pass

    def authenticate(self):
        pass

    def create_account(self):
        pass

    def check_username(self, username, password, name):
        pass


def destroy(self):
    try:
        self.app.destroy()
    except Exception:
        pass
