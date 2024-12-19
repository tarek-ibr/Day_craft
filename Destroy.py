def destruction(self):
    try:
        self.app.destroy()
    except Exception:
        pass
