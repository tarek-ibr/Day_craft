from GUI import GUI
import ttkbootstrap as tkk
import db_functions as db


if __name__ == '__main__':
    root = tkk.Window()
    app = GUI(root)
    root.mainloop()