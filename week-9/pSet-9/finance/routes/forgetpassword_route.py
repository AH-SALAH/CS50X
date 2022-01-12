from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer
from flask import request, session
from controllers.forgetpasswordctrl import ForgetPasswordController


class ForgetPasswordRoute:
    """Handle ForgetPassword Route"""

    def __init__(self, app, db, **kwargs):
        self.app = app
        self.db = db
        self.token_max_age = 600
        self.serial = URLSafeTimedSerializer(self.app.config["MAIL_SECRET"], salt=self.app.config["MAIL_SALT"])
        self.forget_password_instance = ForgetPasswordController()
        # self.attempts = 3
        # self.lock_time = datetime.now().time().replace(minute=datetime.now().time().minute + 1)
        # self.ip = {}

        try:
            base = kwargs["baseUrl"] if "baseUrl" in kwargs.keys() else "/user/forgetpassword"
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
        def forget_password():
            # session["ip"] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            # self.attempts = session["attempts"]
            return self.forget_password_instance.forget_password(self.db, self.app, self.serial, self.token_max_age)

        @app.route(f"{base}/reset/<token>", methods=["GET", "POST"])
        def reset_password(token):
            return self.forget_password_instance.reset_password(self.db, self.app, token, self.serial, self.token_max_age)
