import tkinter as tk
import ttkbootstrap as ttk
import db_functions as db
import Destroy as ds
import functions as fn


class GUI():
    def __init__(self, root):  # Initialize the Gui class
        self.loginWindow = root
        self.login_Window()  # Call the login_Window method

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
                self.team(username)
            else:
                self.invalid.config(text="Invalid username or password")
        elif self.role_combobox.get() == "User":
            if db.authenticateUser(username, password):
                self.user(username)
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

    def user(self, username):
        # Destroy previous UI components
        ds.destroy(self)

        # Set up the main user window
        self.loginWindow.geometry('800x600')
        self.loginWindow.title(f"User Dashboard - {username}")
        self.loginWindow.resizable(True, True)

        # Add Task Button
        self.add_task_button = ttk.Button(self.loginWindow, text="Add Task", bootstyle="primary", command=lambda: self.add_task_user(username))
        self.add_task_button.place(x=20, y=20)

        # Duration Entry Label
        self.duration_label = ttk.Label(self.loginWindow, text="Task Duration (hours):")
        self.duration_label.place(x=140, y=20)

        # Duration Entry
        self.duration_entry = ttk.Entry(self.loginWindow)
        self.duration_entry.place(x=290, y=20, width=100)

        # Refresh Button
        self.refresh_button = ttk.Button(self.loginWindow, text="Refresh", bootstyle="warning", command=lambda: self.refresh_user(username, self.duration_entry.get()))
        self.refresh_button.place(x=720, y=20)

        # Calendar/Task List Section
        self.task_frame = ttk.Labelframe(self.loginWindow, text="Calendar or Task List")
        self.task_frame.place(x=20, y=70, width=760, height=300)

        # Placeholder content for tasks
        self.task_list = tk.Listbox(self.task_frame, height=10, width=80)
        self.task_list.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize canvas
        self.canvas = tk.Canvas(self.loginWindow, width=600, height=60, bg="white")
        self.canvas.place(x=50, y=300)  # Adjust position as needed

        # Performance Section
        self.performance_frame = ttk.Labelframe(self.loginWindow, text="Performance")
        self.performance_frame.place(x=20, y=400, width=760, height=150)

        # Placeholder content for performance
        self.performance_label = ttk.Label(self.performance_frame, text="Performance metrics will be shown here.")
        self.performance_label.pack(pady=10)

        # Log Out Button
        self.logout_button = ttk.Button(self.loginWindow, text="Log Out", bootstyle="danger",
                                        command=self.login_Window)  # Navigate back to login window
        self.logout_button.place(x=20, y=550)

    def add_task_user(self, username):
        new_window = tk.Toplevel(self.loginWindow)  # Create a new window
        new_window.title('Add Task')

        # Create labels and entry fields for the task details
        name_label = ttk.Label(new_window, text="Task Name", font=("Comic Sans MS", 12))
        name_label.grid(row=0, column=0)
        name_entry = ttk.Entry(new_window, font=("Comic Sans MS", 10))
        name_entry.grid(row=0, column=1)

        priority_label = ttk.Label(new_window, text="Priority (Positive Number)", font=("Comic Sans MS", 12))
        priority_label.grid(row=2, column=0)
        priority_entry = ttk.Entry(new_window, font=("Comic Sans MS", 10))
        priority_entry.grid(row=2, column=1)

        time_label = ttk.Label(new_window, text="Time needed to complete the task", font=("Comic Sans MS", 12))
        time_label.grid(row=3, column=0)
        time_entry = ttk.Entry(new_window, font=("Comic Sans MS", 10))
        time_entry.grid(row=3, column=1)

        category_label = ttk.Label(new_window, text="Category of the task", font=("Comic Sans MS", 12))
        category_label.grid(row=4, column=0)
        category_entry = ttk.Entry(new_window, font=("Comic Sans MS", 10))
        category_entry.grid(row=4, column=1, pady=1)

        prerequisite_label = ttk.Label(new_window, text="Prerequisite of the task if any", font=("Comic Sans MS", 12))
        prerequisite_label.grid(row=5, column=0)

        # Retrieve tasks for the user and populate dropdown
        user_tasks = db.get_user_tasks(username)
        task_names = [task[1] for task in user_tasks]  # Assuming task name is at index 1
        task_names.append("None")  # Add "None" as a default option for no prerequisite

        prerequisite_var = tk.StringVar(new_window)
        prerequisite_var.set("None")  # Set default value to "None"
        prerequisite_menu = ttk.OptionMenu(new_window, prerequisite_var, *task_names)
        prerequisite_menu.grid(row=5, column=1, pady=1)

        def add_task_to_db():  # Function to add the task to the database
            name = name_entry.get()
            priority = priority_entry.get()
            time = time_entry.get()
            category = category_entry.get()
            prerequisite = prerequisite_var.get()  # Get the selected value from the dropdown

            # Clear any previous error message
            if hasattr(self, "error_label") and self.error_label:
                self.error_label.destroy()

            # Validate fields
            if not name.isalpha():  # Ensure name contains only alphabetic characters
                self.error_label = ttk.Label(new_window, text="Name must contain only letters!", foreground="red",
                                             font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            if not priority.isdigit():  # Ensure priority is numeric
                self.error_label = ttk.Label(new_window, text="Priority must be a positive number!", foreground="red",
                                             font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            if not time.isdigit():  # Ensure time is numeric
                self.error_label = ttk.Label(new_window, text="Time must be a positive number!", foreground="red",
                                             font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            if not category.replace(" ", "").isalpha():  # Ensure category is text (allows spaces)
                self.error_label = ttk.Label(new_window, text="Category must contain only letters and spaces!",
                                             foreground="red", font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            # Add the task to the database if all validations pass
            prerequisite_value = None if prerequisite == "None" else prerequisite
            if prerequisite == "None":
                prerequisite = None
            db.add_user_task(username, name, int(priority), int(time), category, prerequisite_value)
            new_window.destroy()
            self.user(username)

        add_button = tk.Button(new_window, text="Add Task", font=("Comic Sans MS", 12), foreground="blue",
                               command=lambda: [add_task_to_db()])
        add_button.grid(row=6, column=0, columnspan=2)

    def refresh_user(self, username, duration):
        # Validate duration input
        if not (duration.isdigit() and int(duration) > 0):  # Ensure duration is numeric and positive
            self.error_label = ttk.Label(self.loginWindow, text="Duration must be a positive number!", foreground="red",
                                         font=("Comic Sans MS", 10))
            self.error_label.place(x=400, y=20)
            return

        # Clear any existing error message
        if hasattr(self, "error_label") and self.error_label:
            self.error_label.destroy()

        # Fetch tasks
        tasks = fn.get_tasks(username, duration)

        # Clear the task frame before adding new tasks
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        # Add a scrollbar for vertical scrolling
        canvas = tk.Canvas(self.task_frame)
        scrollbar = ttk.Scrollbar(self.task_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if tasks:
            total_duration = sum(task[3] for task in tasks)  # Sum of task durations for bar width proportion
            max_width = 500  # Maximum width for a task bar

            self.task_vars = []  # List to store task names and their BooleanVars

            for task in tasks:
                task_name = task[1]  # Assuming task name is at index 1
                task_duration = task[3]  # Assuming duration is at index 3

                # Create a frame for each task row
                task_row = ttk.Frame(scrollable_frame)
                task_row.pack(fill="x", pady=5, padx=10)

                # Initialize the BooleanVar to False (unchecked by default)
                var = tk.BooleanVar(value=False)  # Ensure no indeterminate state
                self.task_vars.append((task_name, var))

                # Create the Checkbutton and ensure proper binding using lambda with default arguments
                task_checkbox = ttk.Checkbutton(
                    task_row,
                    variable=var,
                    command=lambda task_name=task_name, var=var: self.done(task, var)
                )
                task_checkbox.pack(side="left", padx=10)

                # Canvas for task bar
                task_canvas = tk.Canvas(task_row, height=30, width=max_width, bg="white")
                task_canvas.pack(side="left", padx=10, fill="x", expand=True)

                # # Draw a proportional bar for the task
                # bar_width = (task_duration / total_duration) * max_width
                task_canvas.create_rectangle(0, 0, max_width, 30, fill="blue")

                # Add task name as text inside the bar
                task_canvas.create_text(
                    max_width / 2, 15, text=task_name, fill="white", anchor="center", font=("Arial", 12, "bold")
                )
        else:
            no_task_label = ttk.Label(scrollable_frame, text="No tasks available for the specified duration.",
                                      foreground="red")
            no_task_label.pack(pady=10)

    def done(self, task, var):
        """Handles checkbox state changes."""
        try:
            if var.get():  # Check if the checkbox is checked
                db.edit_user_task(task[0], task[1], task[2], task[3], task[4], task[5], 1)
            else:
                db.edit_user_task(task[0], task[1], task[2], task[3], task[4], task[5], 0)
        except Exception as e:
            print(f"Error in done function: {e}")

    def team(self, teamname):
        # Destroy previous UI components
        ds.destroy(self)

        # Set up the main team window
        self.loginWindow.geometry('800x600')
        self.loginWindow.title(f"Team Dashboard - {teamname}")
        self.loginWindow.resizable(True, True)

        # Add Task Button
        self.add_task_button = ttk.Button(self.loginWindow, text="Add Task", bootstyle="primary",
                                          command=lambda: self.add_task_team(teamname))
        self.add_task_button.place(x=20, y=20)

        # Duration Entry Label
        self.duration_label = ttk.Label(self.loginWindow, text="Task Duration (hours):")
        self.duration_label.place(x=140, y=20)

        # Duration Entry
        self.duration_entry = ttk.Entry(self.loginWindow)
        self.duration_entry.place(x=290, y=20, width=100)

        # Refresh Button
        self.refresh_button = ttk.Button(self.loginWindow, text="Refresh", bootstyle="warning",
                                         command=self.refresh_team)
        self.refresh_button.place(x=720, y=20)

        # Dropdown for Each Person
        user_list = db.get_team_users(teamname)  # Retrieve user list from the database

        self.dropdown_label = ttk.Label(self.loginWindow, text="Select Team Member:")
        self.dropdown_label.place(x=20, y=70)

        # Dynamically populate the dropdown with the user list
        self.person_combobox = ttk.Combobox(self.loginWindow, state="readonly", values=user_list)
        self.person_combobox.place(x=175, y=70, width=200)

        # Task List Section
        self.task_frame = ttk.Labelframe(self.loginWindow, text="Task List")
        self.task_frame.place(x=20, y=120, width=760, height=200)

        # Placeholder content for task list
        self.task_list = tk.Listbox(self.task_frame, height=10, width=80)
        self.task_list.pack(fill="both", expand=True, padx=10, pady=10)

        # Performance Section
        self.performance_frame = ttk.Labelframe(self.loginWindow, text="Performance")
        self.performance_frame.place(x=20, y=340, width=760, height=200)

        # Placeholder content for performance
        self.performance_label = ttk.Label(self.performance_frame, text="Performance metrics will be shown here.")
        self.performance_label.pack(pady=10)

        # Log Out Button
        self.logout_button = ttk.Button(self.loginWindow, text="Log Out", bootstyle="danger",
                                        command=self.login_Window)  # Navigate back to login window
        self.logout_button.place(x=20, y=550)

    def add_task_team(self, teamname):
        new_window = tk.Toplevel(self.loginWindow)  # Create a new window
        new_window.title('Add Task')

        # Create labels and entry fields for the book details
        name_label = ttk.Label(new_window, text="Task Name", font=("Comic Sans MS", 12))
        name_label.grid(row=0, column=0)
        name_entry = ttk.Entry(new_window, font=("Comic Sans MS", 10))
        name_entry.grid(row=0, column=1)

        priority_label = ttk.Label(new_window, text="Priority (Positive Number)", font=("Comic Sans MS", 12))
        priority_label.grid(row=2, column=0)
        priority_entry = ttk.Entry(new_window, font=("Comic Sans MS", 10))
        priority_entry.grid(row=2, column=1)

        time_label = ttk.Label(new_window, text="Time needed to complete the task", font=("Comic Sans MS", 12))
        time_label.grid(row=3, column=0)
        time_entry = ttk.Entry(new_window, font=("Comic Sans MS", 10))
        time_entry.grid(row=3, column=1)

        category_label = ttk.Label(new_window, text="Category of the task", font=("Comic Sans MS", 12))
        category_label.grid(row=4, column=0)
        category_entry = ttk.Entry(new_window, font=("Comic Sans MS", 10))
        category_entry.grid(row=4, column=1, pady=1)

        prerequisite_label = ttk.Label(new_window, text="Prerequisite of the task if there any", font=("Comic Sans MS", 12))
        prerequisite_label.grid(row=5, column=0)
        prerequisite_entry = ttk.Entry(new_window, font=("Comic Sans MS", 10))
        prerequisite_entry.grid(row=5, column=1, pady=1)

        def add_task_to_db():  # Function to add the task to the database
            name = name_entry.get()
            priority = priority_entry.get()
            time = time_entry.get()
            category = category_entry.get() # Correctly retrieve text from Text widget
            prerequisite = prerequisite_entry.get()  # Correctly retrieve text from Text widget

            # Clear any previous error message
            if hasattr(self, "error_label") and self.error_label:
                self.error_label.destroy()

            # Validate fields
            if not name.isalpha():  # Ensure name contains only alphabetic characters
                self.error_label = ttk.Label(new_window, text="Name must contain only letters!", foreground="red",
                                             font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            if not priority.isdigit():  # Ensure priority is numeric
                self.error_label = ttk.Label(new_window, text="Priority must be a positive number!", foreground="red",
                                             font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            if not time.isdigit():  # Ensure time is numeric
                self.error_label = ttk.Label(new_window, text="Time must be a positive number!", foreground="red",
                                             font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            if not category.replace(" ", "").isalpha():  # Ensure category is text (allows spaces)
                self.error_label = ttk.Label(new_window, text="Category must contain only letters and spaces!",
                                             foreground="red", font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            if not prerequisite.replace(" ", "").isalpha():  # Ensure prerequisite is text (allows spaces)
                self.error_label = ttk.Label(new_window, text="Prerequisite must contain only letters and spaces!",
                                             foreground="red", font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            # Add the task to the database if all validations pass
            db.add_team_task(teamname, name, int(priority), int(time), category, prerequisite)
            new_window.destroy()
            self.team(teamname)

        add_button = tk.Button(new_window, text="Add Task", font=("Comic Sans MS", 12), foreground="blue",
                               command=lambda: [add_task_to_db()])
        add_button.grid(row=6, column=0, columnspan=2)

    def refresh_team(self):
        pass