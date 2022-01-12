from controllers.loginctrl import LoginController

class LoginRoute:
    """Handle Login Route
    """

    def __init__(self, app, db):
        self.app = app
        self.db = db
    
        @app.route("/login", methods=["GET", "POST"])
        def login():
            return LoginController().login(self.db)