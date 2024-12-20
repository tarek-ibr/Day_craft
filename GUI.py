import tkinter as tk
import ttkbootstrap as ttk
import db_functions as db
import Destroy as ds


class GUI():
    def __init__(self, root):  # Initialize the Gui class
        self.loginWindow = root
        self.login_Window()  # Call the login_Window method

    import tkinter as tk
    from tkinter import ttk

    def login_Window(self):
        ds.destroy(self)
        self.loginWindow.geometry('800x900')
        self.loginWindow.title('Login')
        self.loginWindow.resizable(False, False)

        self.loginWindow.bind("<MouseWheel>", lambda event: None)

        # Create a frame for the labels and entries
        self.frame = tk.Frame(self.loginWindow)
        self.frame.pack(expand=True)

        # Dropdown menu for selecting "Team" or "User"
        self.role_label = ttk.Label(self.frame, text="Role:")
        self.role_label.grid(row=0, column=0, padx=5, pady=5)

        self.role_combobox = ttk.Combobox(self.frame, state="readonly", values=["Team", "User"])
        self.role_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.role_combobox.current(0)  # Set default value to "Team"

        # Username label and entry
        self.username_label = ttk.Label(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        # Password label and entry
        self.password_label = ttk.Label(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.frame, show="•")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Login button
        self.login_button = ttk.Button(self.frame, text="Login", command=self.authenticate)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=0)
        self.loginWindow.bind("<Return>", lambda event: self.authenticate())

        # Create new user button
        self.createuser = ttk.Button(self.frame, text="Create new user", bootstyle="dark-link")
        self.createuser.grid(row=4, column=0, columnspan=2, pady=5)
        self.createuser.bind("<Button-1>", lambda event: self.create_account())

        # Label for invalid login attempts
        self.invalid = ttk.Label(self.frame, text="", foreground="red")
        self.invalid.grid(row=5, column=0, columnspan=2, pady=5)

        self.loginWindow.mainloop()

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.role_combobox.get() == "Team":
            if db.authenticateTeam(username, password):
                self.Teams(username)
            else:
                self.invalid.config(text="Invalid username or password")
        elif self.role_combobox.get() == "User":
            if db.authenticateUser(username, password):
                self.Users(username)
            else:
                self.invalid.config(text="Invalid username or password")


    def create_account(self):
        # Ensure the current window or view is properly destroyed
        ds.destroy(self)

        # Set up the window for account creation
        self.loginWindow.title('Create Account')

        # Create a frame to hold the widgets
        self.frame = ttk.Frame(self.loginWindow)
        self.frame.pack(expand=True)
        self.loginWindow.bind("<MouseWheel>", lambda event: None)

        # Dropdown menu for selecting "Team" or "User"
        self.role_label = ttk.Label(self.frame, text="Role:")
        self.role_label.grid(row=0, column=0, padx=5, pady=5)

        self.role_combobox = ttk.Combobox(self.frame, state="readonly", values=["Team", "User"])
        self.role_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.role_combobox.current(0)  # Set default value to "Team"

        # Bind selection change to a callback function
        self.role_combobox.bind("<<ComboboxSelected>>", self.toggle_team_entry)

        # Username label and entry
        self.username_label = ttk.Label(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        # Password label and entry
        self.password_label = ttk.Label(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.frame, show="•")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Sign-up button
        self.signup_button = ttk.Button(
            self.frame,
            text="Sign Up",
            command=lambda: self.check_username(
                self.username_entry.get(),
                self.password_entry.get(),
                self.role_combobox.get(),
                self.team_entry.get() if self.team_entry else None
            ),
            width=7,
            bootstyle="success"
        )
        self.signup_button.grid(row=4, column=1, columnspan=1, padx=5, pady=10)

        # Bind Return (Enter) key to the sign-up action
        self.loginWindow.bind(
            "<Return>",
            lambda event: self.check_username(
                self.username_entry.get(),
                self.password_entry.get(),
                self.role_combobox.get(),
                self.team_entry.get() if self.team_entry else None
            )
        )

        # Feedback labels for duplicate username or success messages
        self.duplicate = ttk.Label(self.frame, text="", foreground="red")
        self.duplicate.grid(row=5, column=0, columnspan=2, pady=5)
        self.success = ttk.Label(self.frame, text="", foreground="green")
        self.success.grid(row=6, column=0, columnspan=2, pady=5)

        # Label for invalid login attempts
        self.invalid = ttk.Label(self.frame, text="", foreground="red")
        self.invalid.grid(row=6, column=0, columnspan=2, pady=5)

        # Label for valid login attempts
        self.valid = ttk.Label(self.frame, text="", foreground="green")
        self.valid.grid(row=7, column=0, columnspan=2, pady=5)

        # Button to return to the login window
        self.tologin_button = ttk.Button(
            self.frame,
            text="Login",
            command=self.login_Window,
            width=7,
            bootstyle="dark"
        )
        self.tologin_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

        # Placeholder for team label and entry
        self.team_label = None
        self.team_entry = None

    def toggle_team_entry(self, event):
        """Show or hide the Team label and entry based on the selected role."""
        selected_role = self.role_combobox.get()

        if selected_role == "User":
            # If "User" is selected, add the team label and entry if not already present
            if self.team_label is None and self.team_entry is None:
                self.team_label = ttk.Label(self.frame, text="Team:")
                self.team_label.grid(row=3, column=0, padx=5, pady=5)
                self.team_entry = ttk.Entry(self.frame)
                self.team_entry.grid(row=3, column=1, padx=5, pady=5)
        elif selected_role == "Team":
            # If "Team" is selected, remove the team label and entry if present
            if self.team_label is not None:
                self.team_label.destroy()
                self.team_label = None
            if self.team_entry is not None:
                self.team_entry.destroy()
                self.team_entry = None


    def check_username(self, username, password, role, team):
        if role == "Team":
            if db.checkTeamduplicates(username):
                db.add_team(username, password)
                try:
                    self.invalid.destroy()
                except Exception:
                    pass
                self.valid.config(text="team added successfully")

            else:
                self.invalid.config(text="team name already exists")
        elif role == "User":
            if db.checkUserduplicates(username):
                if db.checkTeamduplicates(team):
                    self.invalid.config(text="Invalid team name and your not assigned to a team")
                    self.valid.config(text="user added successfully")
                    db.add_user(username, password, None)
                else:
                    db.add_user(username, password, team)
                    try:
                        self.invalid.destroy()
                    except Exception:
                        pass
                    self.valid.config(text="user added successfully")

            else:
                self.invalid.config(text="username already exists")

    def Users(self, username):
        pass

    def Teams(self, teamname):
        pass