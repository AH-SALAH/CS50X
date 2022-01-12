from datetime import timedelta
# import os
from tempfile import mkdtemp
from flask_session import Session
from helpers import usd
# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer

class Settings:
    def __init__(self, app):
        self.app = app

        self.app.config.from_envvar("APP_SETTINGS")
        # Ensure templates are auto-reloaded
        self.app.config["TEMPLATES_AUTO_RELOAD"] = True

        # Ensure responses aren't cached
        @self.app.after_request
        def after_request(response):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Expires"] = 0
            response.headers["Pragma"] = "no-cache"
            return response

        # Custom filter
        self.app.jinja_env.filters["usd"] = usd

        # Configure session to use filesystem (instead of signed cookies)
        self.app.config["SESSION_FILE_DIR"] = mkdtemp()
        self.app.config["SESSION_PERMANENT"] = True
        self.app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=20)
        self.app.config["SESSION_TYPE"] = "filesystem"
        Session(self.app)

    # def mail_settings(self):
        # mail settings
        # MAIL_SERVER : default 'localhost'
        # MAIL_PORT : default 25
        # MAIL_USE_TLS : default False
        # MAIL_USE_SSL : default False
        # MAIL_DEBUG : default app.debug
        # MAIL_USERNAME : default None
        # MAIL_PASSWORD : default None
        # MAIL_DEFAULT_SENDER : default None
        # MAIL_MAX_EMAILS : default None
        # MAIL_SUPPRESS_SEND : default app.testing
        # MAIL_ASCII_ATTACHMENTS : default False

        # self.app.config['MAIL_SERVER']='smtp.gmail.com'
        # self.app.config['MAIL_PORT'] = 587
        # self.app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
        # self.app.config['MAIL_USERNAME'] = "testosuru@gmail.com" #os.environ.get('MAIL_USERNAME')
        # self.app.config['MAIL_PASSWORD'] = "kawairashii1989"#os.environ.get('MAIL_PASSWORD')
        # self.app.config['MAIL_USE_TLS'] = False
        # self.app.config['MAIL_USE_SSL'] = True
        # self.app.config['MAIL_DEBUG'] = True

        # mail = Mail(self.app)

        # serial = URLSafeTimedSerializer("secret", salt="confirm-email")
        # serial = URLSafeTimedSerializer(os.environ.get("APP_SETTINGS"))

        # return {"mail": mail, "message": Message, "serial": serial}
