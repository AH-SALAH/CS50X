from controllers.logoutctrl import LogoutController

class LogoutRoute:
    """Handle Logout Route
    """

    def __init__(self, app, db):
        self.app = app
        self.db = db

        @app.route("/logout")
        def logout():
            return LogoutController().logout()