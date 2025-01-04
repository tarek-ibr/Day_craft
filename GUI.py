import tkinter as tk
import ttkbootstrap as ttk
import db_functions as db
import Destroy as ds
import functions as fn
from tkinter import IntVar, Canvas
from functools import partial #for mark as complete
from PIL import Image, ImageTk  # For handling images



class GUI():
    def __init__(self, root):  # Initialize the Gui class
        self.loginWindow = root
        self.login_Window()  # Call the login_Window method

    def login_Window(self):

        # Destroy current content
        for widget in self.loginWindow.winfo_children():
            widget.destroy()

        self.loginWindow.geometry('1000x800')
        self.loginWindow.title('Login')
        self.loginWindow.resizable(False, False)

        # Main container frame
        main_frame = tk.Frame(self.loginWindow, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel
        left_panel = tk.Frame(main_frame, bg='white', width=500)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Styling and Widgets in the Left Panel
        left_content = tk.Frame(left_panel, bg='white')
        left_content.pack(expand=True)

        self.role_label = ttk.Label(left_content, text="Role:", font=("Arial", 12))
        self.role_label.pack(anchor="center", pady=(20, 5))

        self.role_combobox = ttk.Combobox(left_content, state="readonly", values=["Team", "User"], font=("Arial", 12))
        self.role_combobox.pack(pady=(0, 20), fill='x', padx=50)
        self.role_combobox.current(0)

        self.username_label = ttk.Label(left_content, text="Username:", font=("Arial", 12))
        self.username_label.pack(anchor="center", pady=(10, 5))

        self.username_entry = ttk.Entry(left_content, font=("Arial", 12))
        self.username_entry.pack(pady=(0, 20), fill='x', padx=50)

        self.password_label = ttk.Label(left_content, text="Password:", font=("Arial", 12))
        self.password_label.pack(anchor="center", pady=(10, 5))

        self.password_entry = ttk.Entry(left_content, font=("Arial", 12), show="•")
        self.password_entry.pack(pady=(0, 20), fill='x', padx=50)

        self.login_button = ttk.Button(left_content, text="Login", command=self.authenticate, style="Accent.TButton")
        self.login_button.pack(pady=(15, 15), fill='x', padx=50)
        self.loginWindow.bind("<Return>", lambda event: self.authenticate())

        self.createuser = ttk.Button(left_content, text="Create new user", command=self.create_account,
                                     style="Link.TButton")
        self.createuser.pack(pady=(0, 10), fill='x', padx=50)

        self.invalid = ttk.Label(left_content, text="", foreground="red", font=("Arial", 10))
        self.invalid.pack(pady=(10, 0))

        # Right panel for artwork
        right_panel = tk.Frame(main_frame, bg='white', width=500)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load and Display the Image
        image = Image.open("login.png")  # Replace with your actual image path
        image = image.resize((650, 800), Image.Resampling.LANCZOS)  # Resize image to fit the frame
        image_tk = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(right_panel, image=image_tk, bg='white')
        self.image_label.image = image_tk  # Keep a reference to avoid garbage collection
        self.image_label.pack(fill=tk.BOTH, expand=True)  # Fill the entire right panel

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
        # Destroy the current window content
        for widget in self.loginWindow.winfo_children():
            widget.destroy()

        # Set up the window for account creation
        self.loginWindow.title('Create Account')

        # Define a custom style for larger buttons
        style = ttk.Style()
        style.configure("Large.TButton", font=("Arial", 12), padding=(10, 10))

        # Main container frame
        main_frame = tk.Frame(self.loginWindow, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel
        left_panel = tk.Frame(main_frame, bg='white', width=500)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Styling and Widgets in the Left Panel
        self.left_content = tk.Frame(left_panel, bg='white')
        self.left_content.pack(expand=True)

        self.role_label = ttk.Label(self.left_content, text="Role:", font=("Arial", 12))
        self.role_label.grid(row=0, column=0, padx=5, pady=5)

        self.role_combobox = ttk.Combobox(self.left_content, state="readonly", values=["Team", "User"],
                                          font=("Arial", 12))
        self.role_combobox.grid(row=1, column=0, padx=5, pady=5)
        self.role_combobox.current(0)

        # Bind selection change to a callback function
        self.role_combobox.bind("<<ComboboxSelected>>", self.toggle_team_entry)

        # Username label and entry
        self.username_label = ttk.Label(self.left_content, text="Username:", font=("Arial", 12))
        self.username_label.grid(row=2, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.left_content, font=("Arial", 12))
        self.username_entry.grid(row=3, column=0, padx=5, pady=5)

        # Password label and entry
        self.password_label = ttk.Label(self.left_content, text="Password:", font=("Arial", 12))
        self.password_label.grid(row=4, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.left_content, font=("Arial", 12), show="•")
        self.password_entry.grid(row=5, column=0, padx=5, pady=5)

        # Sign-up button
        self.signup_button = ttk.Button(
            self.left_content,
            text="Sign Up",
            command=lambda: self.check_username(
                self.username_entry.get(),
                self.password_entry.get(),
                self.role_combobox.get(),
                self.team_entry.get() if hasattr(self, 'team_entry') and self.team_entry else None
            ),
            style="Large.TButton"  # Use the larger button style
        )
        self.signup_button.grid(row=11, column=0, padx=20, pady=15)
        self.loginWindow.bind("<Return>", lambda event: self.check_username(
                self.username_entry.get(),
                self.password_entry.get(),
                self.role_combobox.get(),
                self.team_entry.get() if hasattr(self, 'team_entry') and self.team_entry else None
            ))

        # Feedback labels for duplicate username or success messages
        self.success = ttk.Label(self.left_content, text="", foreground="green")
        self.success.grid(row=8, column=0, columnspan=2, pady=5)

        # Label for invalid login attempts
        self.invalid = ttk.Label(self.left_content, text="", foreground="red")
        self.invalid.grid(row=9, column=0, columnspan=2, pady=5)

        # Label for valid login attempts
        self.valid = ttk.Label(self.left_content, text="", foreground="green")
        self.valid.grid(row=10, column=0, columnspan=2, pady=5)

        # Button to return to the login window
        self.tologin_button = ttk.Button(
            self.left_content,
            text="Back To Login",
            command=self.login_Window,
            style="Link.TButton"  # Use the larger button style
        )
        self.tologin_button.grid(row=12, column=0, columnspan=2, padx=20, pady=15)

        # Right panel for artwork
        right_panel = tk.Frame(main_frame, bg='white', width=500)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load and Display the Image
        image = Image.open("login.png")  # Replace with your actual image path
        image = image.resize((650, 800), Image.Resampling.LANCZOS)  # Resize to the panel's full dimensions
        image_tk = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(right_panel, image=image_tk, bg='white')
        self.image_label.image = image_tk  # Keep a reference to avoid garbage collection

        # Adjust the packing to dock the image to the right
        self.image_label.pack(side="right", anchor="e", fill=tk.Y, expand=False)

        # Placeholder for team label and entry
        self.team_label = None
        self.team_entry = None

    def toggle_team_entry(self, event):
        """Show or hide the Team label and entry based on the selected role."""
        selected_role = self.role_combobox.get()

        if selected_role == "User":
            # If "User" is selected, add the team label and entry if not already present
            if self.team_label is None and self.team_entry is None:
                self.team_label = ttk.Label(self.left_content, text="Team:", font=("Arial", 12))
                self.team_label.grid(row=6, column=0, padx=5, pady=5)
                self.team_entry = ttk.Entry(self.left_content, font=("Arial", 12))
                self.team_entry.grid(row=7, column=0, padx=5, pady=5)


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
                self.invalid.config(text="")  # Clear invalid message
                self.valid.config(text="Team added successfully")
            else:
                self.invalid.config(text="Team name already exists")
                self.valid.config(text="")  # Clear valid message
        elif role == "User":
            self.invalid.config(text="")  # Clear invalid message
            if db.checkUserduplicates(username):
                if not db.checkTeamduplicates(team):
                    db.add_user(username, password, team)
                    self.valid.config(text="User added successfully")
                else:
                    db.add_user(username, password, team)
                    self.invalid.config(text="Invalid team name or team not assigned")
                    self.valid.config(text="User added successfully")
            else:
                self.invalid.config(text="Username already exists")
                self.valid.config(text="")

    def draw_custom_progress_bar(self, canvas, width, height, completion_percentage):
        """
        Draws a custom progress bar with completed (green) and not completed (red) portions.
        """
        canvas.delete("all")  # Clear previous content
        completed_width = (completion_percentage / 100) * width

        # Draw the completed portion in green
        canvas.create_rectangle(0, 0, completed_width, height, fill="green", outline="")

        # Draw the not completed portion in red
        if completed_width < width:
            canvas.create_rectangle(completed_width, 0, width, height, fill="red", outline="")

        # Add percentage text in the center
        canvas.create_text(
            width / 2, height / 2,
            text=f"{completion_percentage:.2f}%",
            fill="white",
            font=("Arial", 12, "bold")
        )

    def user(self, username):
        # Destroy previous UI components
        ds.destroy(self)

        # Destroy current content
        for widget in self.loginWindow.winfo_children():
            widget.destroy()

        # Set up the main user window
        self.loginWindow.geometry('800x600')
        self.loginWindow.title(f"User Dashboard - {username}")
        self.loginWindow.resizable(True, True)

        # Add Task Button
        self.add_task_button = ttk.Button(self.loginWindow, text="Add Task", bootstyle="primary",
                                          command=lambda: self.add_task_user(username))
        self.add_task_button.place(x=20, y=20)

        # Duration Entry Label
        self.duration_label = ttk.Label(self.loginWindow, text="Task Duration (hours):")
        self.duration_label.place(x=140, y=20)

        # Duration Entry
        self.duration_entry = ttk.Entry(self.loginWindow)
        self.duration_entry.place(x=290, y=20, width=100)

        # List all tasks Button
        self.list_button = ttk.Button(self.loginWindow, text="List all tasks", bootstyle="primary",
                                      command=lambda: self.list_user(username))
        self.list_button.place(x=520, y=20)

        # Refresh Button
        self.refresh_button = ttk.Button(self.loginWindow, text="Refresh", bootstyle="primary",
                                         command=lambda: self.refresh_user(username, self.duration_entry.get()))
        self.refresh_button.place(x=720, y=20)

        # Calendar/Task List Section
        self.task_frame = ttk.Labelframe(self.loginWindow, text="Calendar or Task List")
        self.task_frame.place(x=20, y=70, width=760, height=300)

        # Placeholder content for tasks
        self.task_list = tk.Listbox(self.task_frame, height=10, width=80)
        self.task_list.pack(fill="both", expand=True, padx=10, pady=10)

        # Pomodoro Timer Section
        self.pomodoro_frame = ttk.Labelframe(self.loginWindow, text="Pomodoro Timer")
        self.pomodoro_frame.place(x=20, y=400, width=300, height=150)

        # Timer Display
        self.timer_label = ttk.Label(self.pomodoro_frame, text="25:00", font=("Arial", 24))
        self.timer_label.pack(pady=10)

        # Timer Buttons
        self.start_button = ttk.Button(self.pomodoro_frame, text="Start", bootstyle="success", command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        self.pause_button = ttk.Button(self.pomodoro_frame, text="Pause", bootstyle="warning", command=self.pause_timer)
        self.pause_button.pack(side="left", padx=10)

        self.reset_button = ttk.Button(self.pomodoro_frame, text="Reset", bootstyle="danger", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10)

        # Performance Section
        self.performance_frame = ttk.Labelframe(self.loginWindow, text="Performance")
        self.performance_frame.place(x=340, y=400, width=440, height=150)

        # Placeholder content for performance
        self.performance_label = ttk.Label(self.performance_frame, text="Performance metrics will be shown here.")
        self.performance_label.pack(pady=10)

        # Task Completion Rate
        self.completion_label = ttk.Label(self.performance_frame, text="Task Completion Rate:")
        self.completion_label.pack(pady=5)

        # Custom Progress Bar
        self.progress_canvas = Canvas(self.performance_frame, width=300, height=30, bg="white", highlightthickness=0)
        self.progress_canvas.pack()

        tasks = db.get_user_tasks(username)
        done_counter = sum(1 for task in tasks if task[6] == 1)  # Count completed tasks
        total_counter = len(tasks)  # Count total tasks
        if total_counter > 0:
            completion_percentage = (done_counter / total_counter) * 100
        else:
            completion_percentage = 0  # Avoid division by zero when there are no tasks

        self.draw_custom_progress_bar(self.progress_canvas, 300, 30, (done_counter / total_counter) * 100)

        # Log Out Button
        self.logout_button = ttk.Button(self.loginWindow, text="Log Out", bootstyle="danger",
                                        command=self.login_Window)  # Navigate back to login window
        self.logout_button.place(x=20, y=550)

        # Initialize Timer Variables
        self.is_timer_running = False
        self.remaining_time = 1500  # Default 25 minutes (in seconds)

    def start_timer(self):
        """Start the Pomodoro timer."""
        if not self.is_timer_running:
            self.is_timer_running = True
            self.update_timer()

    def pause_timer(self):
        """Pause the Pomodoro timer."""
        self.is_timer_running = False

    def reset_timer(self):
        """Reset the Pomodoro timer to default."""
        self.is_timer_running = False
        self.remaining_time = 1500  # 25 minutes
        self.update_timer_display()

    def update_timer(self):
        """Update the timer display."""
        if self.is_timer_running and self.remaining_time > 0:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
            self.remaining_time -= 1
            self.loginWindow.after(1000, self.update_timer)  # Call this method every second
        elif self.remaining_time == 0:
            self.is_timer_running = False
            self.timer_label.config(text="Time's up!")
            # You can add a sound or notification here.

    def update_timer_display(self):
        """Manually update the timer display."""
        minutes, seconds = divmod(self.remaining_time, 60)
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}")

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
        user_tasks = db.get_user_tasks(username) or []  # Fallback to empty list if None or invalid
        task_names = [task[1] for task in user_tasks]  # Assuming task name is at index 1
        task_names.insert(0, "None")  # Insert "None" as the first element
        task_names.append("None")

        # Create a StringVar to track the selected prerequisite
        prerequisite_var = tk.StringVar(new_window)
        prerequisite_var.set("None")  # Set default value to "None"

        # Create an OptionMenu for prerequisites
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
            if not name.replace(" ", "").isalpha():  # Ensure name contains only alphabetic characters
                self.error_label = ttk.Label(new_window, text="Name must contain only letters!", foreground="red",
                                             font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            if name in task_names:
                self.error_label = ttk.Label(new_window, text="This task is already added to your list", foreground="red",
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

    def list_user(self, username):
        # Clear any existing error message
        if hasattr(self, "error_label") and self.error_label:
            self.error_label.destroy()

        # Fetch tasks
        user_tasks = db.get_user_tasks(username)

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

        if user_tasks:
            for task in user_tasks:
                task_name = task[1]  # Assuming task name is at index 1
                task_done = task[6] == 1  # Assuming completion status is at index 6 (1 means done)

                # Create a frame for each task row
                task_row = ttk.Frame(scrollable_frame)
                task_row.pack(fill="x", pady=5, padx=10)

                # Task Name Label
                task_label = ttk.Label(task_row, text=task_name, font=("Arial", 12))
                task_label.pack(side="left", padx=10)

                # Delete Button
                delete_button = ttk.Button(
                    task_row, text="Delete", bootstyle="danger",
                    command=lambda t=task_name: self.delete_task(username, t)
                )
                delete_button.pack(side="right", padx=10)

                # Completion Checkbox (read-only)
                task_checkbox = ttk.Checkbutton(
                    task_row,
                    text="Completed",
                    variable=tk.BooleanVar(value=task_done),
                    state="disabled"
                )
                task_checkbox.pack(side="right", padx=10)
        else:
            no_task_label = ttk.Label(scrollable_frame, text="No tasks available.",
                                      foreground="red")
            no_task_label.pack(pady=10)

        # Update the progress bar with the new completion percentage
        tasks = db.get_user_tasks(username)
        done_counter = sum(1 for task in tasks if task[6] == 1)  # Count completed tasks
        total_counter = len(tasks)  # Count total tasks

        if total_counter > 0:
            completion_percentage = (done_counter / total_counter) * 100
        else:
            completion_percentage = 0  # Avoid division by zero when there are no tasks

        self.progress_canvas.delete("all")  # Clear the canvas
        self.draw_custom_progress_bar(self.progress_canvas, 300, 30, completion_percentage)

    def delete_task(self, username, taskname):
        """Delete a task and refresh the task list."""
        result = db.delete_user_task(username, taskname)
        if result:
            self.list_user(username)  # Refresh the task list
        else:
            print(f"Failed to delete task '{taskname}'.")

    def refresh_user(self, username, duration):
        # Validate duration input
        if not (duration.isdigit() and int(duration) > 0):  # Ensure duration is numeric and positive
            self.error_label = ttk.Label(self.loginWindow, text="Duration must be a positive number!", foreground="red",
                                         font=("Comic Sans MS", 10))
            self.error_label.place(x=250, y=370)
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

                # Create the Checkbutton and bind using functools.partial
                task_checkbox = ttk.Checkbutton(
                    task_row,
                    variable=var,
                    command=partial(self.done, task, var)
                )
                task_checkbox.pack(side="left", padx=10)

                # Canvas for task bar
                task_canvas = tk.Canvas(task_row, height=30, width=max_width, bg="white")
                task_canvas.pack(side="left", padx=10, fill="x", expand=True)

                # Draw a proportional bar for the task
                task_canvas.create_rectangle(0, 0, max_width, 30, fill="blue")

                # Add task name as text inside the bar
                task_canvas.create_text(
                    max_width / 2, 15, text=task_name, fill="white", anchor="center", font=("Arial", 12, "bold")
                )
        else:
            no_task_label = ttk.Label(scrollable_frame, text="No tasks available for the specified duration.",
                                      foreground="red")
            no_task_label.pack(pady=10)

        tasks = db.get_user_tasks(username)

        # Update the progress bar with the new completion percentage
        done_counter = sum(1 for task in tasks if task[6] == 1)  # Count completed tasks
        total_counter = len(tasks)  # Count total tasks

        if total_counter > 0:
            completion_percentage = (done_counter / total_counter) * 100
        else:
            completion_percentage = 0  # Avoid division by zero when there are no tasks

        self.progress_canvas.delete("all")  # Clear the canvas
        self.draw_custom_progress_bar(self.progress_canvas, 300, 30, completion_percentage)

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

        # Destroy current content
        for widget in self.loginWindow.winfo_children():
            widget.destroy()

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

        # Dropdown for Each Person
        try:
            user_list = db.get_team_users(teamname) or []  # Ensure user_list is valid
        except Exception as e:
            print(f"Error retrieving team users: {e}")
            user_list = []

        self.dropdown_label = ttk.Label(self.loginWindow, text="Select Team Member:")
        self.dropdown_label.place(x=20, y=70)

        # Dynamically populate the dropdown with the user list
        self.person_combobox = ttk.Combobox(self.loginWindow, state="readonly", values=user_list)
        self.person_combobox.place(x=175, y=70, width=200)
        self.person_combobox.set(user_list[0] if user_list else "")  # Set a default value if the list is not empty

        # Refresh Button
        self.refresh_button = ttk.Button(self.loginWindow, text="Refresh", bootstyle="primary",
                                         command=lambda: self.refresh_team(teamname, self.person_combobox.get(),
                                                                           self.duration_entry.get()))
        self.refresh_button.place(x=720, y=20)

        # Task List Section
        self.task_frame = ttk.Labelframe(self.loginWindow, text="Task List")
        self.task_frame.place(x=20, y=120, width=760, height=200)

        # Calendar/Task List Section
        self.task_frame = ttk.Labelframe(self.loginWindow, text="Calendar or Task List")
        self.task_frame.place(x=20, y=110, width=760, height=300)

        # Placeholder content for tasks
        self.task_list = tk.Listbox(self.task_frame, height=10, width=80)
        self.task_list.pack(fill="both", expand=True, padx=10, pady=10)

        # # Initialize canvas
        # self.canvas = tk.Canvas(self.loginWindow, width=600, height=60, bg="white")
        # self.canvas.place(x=50, y=300)  # Adjust position as needed

        # Performance Section
        self.performance_frame = ttk.Labelframe(self.loginWindow, text="Performance")
        self.performance_frame.place(x=20, y=400, width=760, height=150)

        # Placeholder content for performance
        self.performance_label = ttk.Label(self.performance_frame, text="Performance metrics will be shown here.")
        self.performance_label.pack(pady=10)

        # Task Completion Rate
        # Inside the user method or wherever you're creating the performance section
        self.completion_label = ttk.Label(self.performance_frame, text="Task Completion Rate:")
        self.completion_label.pack(pady=5)

        # Custom Progress Bar

        # Initialize the canvas for the custom progress bar
        self.progress_canvas = Canvas(self.performance_frame, width=300, height=30, bg="white", highlightthickness=0)
        self.progress_canvas.pack()

        tasks = db.get_team_tasks(teamname)
        # Update the progress bar with the new completion percentage
        done_counter = sum(1 for task in tasks if task[6] == 1)  # Count completed tasks
        total_counter = len(tasks)  # Count total tasks
        if total_counter > 0:
            completion_percentage = (done_counter / total_counter) * 100
        else:
            completion_percentage = 0  # Avoid division by zero when there are no tasks

        self.draw_custom_progress_bar(self.progress_canvas, 300, 30, (done_counter / total_counter) * 100)

        # Log Out Button
        self.logout_button = ttk.Button(self.loginWindow, text="Log Out", bootstyle="danger",
                                        command=self.login_Window)  # Navigate back to login window
        self.logout_button.place(x=20, y=550)

    def load_team_tasks(self, teamname):
        """Populate the task list with tasks for the team."""
        try:
            tasks = db.get_team_tasks(teamname)  # Replace with your database query for tasks
            if tasks:
                for task in tasks:
                    self.task_list.insert(tk.END, f"{task[0]}: {task[1]}")  # Example: Display taskname
            else:
                self.task_list.insert(tk.END, "No tasks available.")
        except Exception as e:
            self.task_list.insert(tk.END, f"Error loading tasks: {e}")

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

        # Retrieve tasks for the user and populate dropdown
        team_tasks = db.get_team_tasks(teamname) or []  # Fallback to empty list if None or invalid
        task_names = [task[1] for task in team_tasks]  # Assuming task name is at index 1
        task_names.insert(0, "None")  # Insert "None" as the first element
        task_names.append("None")

        # Create a StringVar to track the selected prerequisite
        prerequisite_var = tk.StringVar(new_window)
        prerequisite_var.set("None")  # Set default value to "None"

        # Create an OptionMenu for prerequisites
        prerequisite_menu = ttk.OptionMenu(new_window, prerequisite_var, *task_names)
        prerequisite_menu.grid(row=5, column=1, pady=1)

        def add_team_task_to_db():  # Function to add the task to the database
            name = name_entry.get()
            priority = priority_entry.get()
            time = time_entry.get()
            category = category_entry.get() # Correctly retrieve text from Text widget
            prerequisite = prerequisite_var.get()  # Correctly retrieve text from Text widget

            # Clear any previous error message
            if hasattr(self, "error_label") and self.error_label:
                self.error_label.destroy()

            # Validate fields
            if not name.replace(" ", "").isalpha():  # Ensure name contains only alphabetic characters
                self.error_label = ttk.Label(new_window, text="Name must contain only letters!", foreground="red",
                                             font=("Comic Sans MS", 10))
                self.error_label.grid(row=7, column=0, columnspan=2, pady=5)
                return

            if name in task_names:
                self.error_label = ttk.Label(new_window, text="This task is already added to your list", foreground="red",
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
            prerequisite = None if prerequisite == "None" else prerequisite
            if prerequisite == "None":
                prerequisite = None

            # Add the task to the database if all validations pass
            db.add_team_task(teamname, name, int(priority), int(time), category, prerequisite)
            new_window.destroy()
            self.team(teamname)

        add_button = tk.Button(new_window, text="Add Task", font=("Comic Sans MS", 12), foreground="blue",
                               command=lambda: [add_team_task_to_db()])
        add_button.grid(row=6, column=0, columnspan=2)

    def refresh_team(self, teamname, username, duration):

        # Validate duration input
        if not (duration.isdigit() and int(duration) > 0):  # Ensure duration is numeric and positive
            self.error_label = ttk.Label(self.loginWindow, text="Duration must be a positive number!", foreground="red",
                                         font=("Comic Sans MS", 10))
            self.error_label.place(x=250, y=370)
            return

            # Validate fields
        if not username.replace(" ", "").isalpha():  # Ensure name contains only alphabetic characters
            self.error_label = ttk.Label(self.loginWindow, text="Select a user", foreground="red",
                                         font=("Comic Sans MS", 10))
            self.error_label.place(x=250, y=370)
            return

        # Clear any existing error message
        if hasattr(self, "error_label") and self.error_label:
            self.error_label.destroy()

        # Fetch tasks
        tasks = fn.get_user_from_team_tasks(teamname, username, duration)

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

                # Create the Checkbutton and bind using functools.partial
                task_checkbox = ttk.Checkbutton(
                    task_row,
                    variable=var,
                    command=partial(self.done, task, var)
                )
                task_checkbox.pack(side="left", padx=10)

                # Canvas for task bar
                task_canvas = tk.Canvas(task_row, height=30, width=max_width, bg="white")
                task_canvas.pack(side="left", padx=10, fill="x", expand=True)

                # Draw a proportional bar for the task
                task_canvas.create_rectangle(0, 0, max_width, 30, fill="blue")

                # Add task name as text inside the bar
                task_canvas.create_text(
                    max_width / 2, 15, text=task_name, fill="white", anchor="center", font=("Arial", 12, "bold")
                )
        else:
            no_task_label = ttk.Label(scrollable_frame, text="No tasks available for the specified duration.",
                                      foreground="red")
            no_task_label.pack(pady=10)

        tasks = db.get_team_tasks(teamname)

        # Update the progress bar with the new completion percentage
        done_counter = sum(1 for task in tasks if task[6] == 1)  # Count completed tasks
        total_counter = len(tasks)  # Count total tasks

        if total_counter > 0:
            completion_percentage = (done_counter / total_counter) * 100
        else:
            completion_percentage = 0  # Avoid division by zero when there are no tasks

        self.progress_canvas.delete("all")  # Clear the canvas
        self.draw_custom_progress_bar(self.progress_canvas, 300, 30, completion_percentage)