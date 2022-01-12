# from itsdangerous.url_safe import URLSafeTimedSerializer
from controllers.changepasswordctrl import ChangePasswordController


class ChangePasswordRoute:
    """Handle ChangePassword Route"""

    def __init__(self, app, db, **kwargs):
        self.app = app
        self.db = db
        self.token_max_age = 300
        # self.serial = URLSafeTimedSerializer(self.app.config["MAIL_SECRET"], salt=self.app.config["MAIL_SALT"])
        # self.message = ""
        # self.mail = ""

        try:
            base = kwargs["baseUrl"] if "baseUrl" in kwargs.keys() else "/user/changepassword"
            # settings = kwargs["settings"] if "settings" in kwargs.keys() else {}

            # setin = settings.mail_settings()
            # self.mail = setin["mail"]
            # self.message = setin["message"]
            # self.serial = setin["serial"]

        except AttributeError as er:
            print("An AttributeError exception occurred", er)
        except TypeError as er:
            print("An TypeError exception occurred", er)
            

        @app.route(base, methods=["POST"])
        def change_password():
            # return ResetPasswordController().change_password(self.db, self.app, self.serial, self.token_max_age)
            return ChangePasswordController().change_password(self.db)

        # @app.route(f"{base}/verify/<token>")
        # def mail_confirmation(token):
        #     return ResetPasswordController().mail_confirmation(self.app, token, self.serial, self.token_max_age)
