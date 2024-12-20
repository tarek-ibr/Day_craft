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

