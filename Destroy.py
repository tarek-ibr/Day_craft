def destroy(self):
    try:
        self.app.destroy()
    except Exception:
        pass

    try:
        self.frame.destroy()
    except Exception:
        pass

    try:
        self.role_label.destroy()
    except Exception:
        pass

    try:
        self.role_combobox.destroy()
    except Exception:
        pass

    try:
        self.username_label.destroy()
    except Exception:
        pass

    try:
        self.username_entry.destroy()
    except Exception:
        pass

    try:
        self.password_label.destroy()
    except Exception:
        pass

    try:
        self.password_label.destroy()
    except Exception:
        pass

    try:
        self.password_entry.destroy()
    except Exception:
        pass

    try:
        self.login_button.destroy()
    except Exception:
        pass

    try:
        self.createuser.destroy()
    except Exception:
        pass

    try:
        self.invalid.destroy()
    except Exception:
        pass

    try:
        self.team_label.destroy()
    except Exception:
        pass

    try:
        self.team_entry.destroy()
    except Exception:
        pass

    try:
        self.add_task_button.destroy()
    except Exception:
        pass

    try:
        self.duration_label.destroy()
    except Exception:
        pass

    try:
        self.duration_entry.destroy()
    except Exception:
        pass

    try:
        self.refresh_button.destroy()
    except Exception:
        pass

    try:
        self.task_frame.destroy()
    except Exception:
        pass

    try:
        self.task_list.destroy()
    except Exception:
        pass

    try:
        self.performance_frame.destroy()
    except Exception:
        pass

    try:
        self.performance_label.destroy()
    except Exception:
        pass

    try:
        self.priority_label.destroy()
    except Exception:
        pass

    try:
        self.priority_entry.destroy()
    except Exception:
        pass

    try:
        self.time_label.destroy()
    except Exception:
        pass

    try:
        self.time_entry.destroy()
    except Exception:
        pass

    try:
        self.category_label.destroy()
    except Exception:
        pass

    try:
        self.category_entry.destroy()
    except Exception:
        pass

    try:
        self.prerequisite_label.destroy()
    except Exception:
        pass

    try:
        self.prerequisite_entry.destroy()
    except Exception:
        pass

    try:
        self.error_label.destroy()
    except Exception:
        pass

    try:
        self.dropdown_label.destroy()
    except Exception:
        pass

    try:
        self.person_combobox.destroy()
    except Exception:
        pass

    try:
        self.logout_button.destroy()
    except Exception:
        pass


