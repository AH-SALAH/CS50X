from itsdangerous.url_safe import URLSafeTimedSerializer
from controllers.registerctrl import RegisterController


class RegisterRoute:
    """Handle Register Route"""

    def __init__(self, app, db, **kwargs):
        self.app = app
        self.db = db
        self.token_max_age = 60*60*24
        self.serial = URLSafeTimedSerializer(self.app.config["MAIL_SECRET"], salt=self.app.config["MAIL_SALT"])
        # self.message = ""
        # self.mail = ""

        try:
            base = kwargs["baseUrl"] if "baseUrl" in kwargs.keys() else "/register"
            # settings = kwargs["settings"] if "settings" in kwargs.keys() else {}

            # setin = settings.mail_settings()
            # self.mail = setin["mail"]
            # self.message = setin["message"]
            # self.serial = setin["serial"]

        except AttributeError as er:
            print("An AttributeError exception occurred", er)
        except TypeError as er:
            print("An TypeError exception occurred", er)
            

        @app.route(base, methods=["GET", "POST"])
        def register():
            return RegisterController().register(self.db, self.app, self.serial, self.token_max_age)

        @app.route(f"{base}/verify/<token>")
        def mail_confirmation(token):
            return RegisterController().mail_confirmation(self.db, self.app, token, self.serial, self.token_max_age)
