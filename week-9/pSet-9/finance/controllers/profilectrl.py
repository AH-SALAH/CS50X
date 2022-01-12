import os
from forms.resetpassword import ResetPasswordForm
from flask import session, render_template, current_app
from models.users import UsersModel


class ProfileController:
    def __init__(self):
        pass

    @staticmethod
    def get_reset_form():
        change_password_form = ResetPasswordForm()
        return change_password_form
    
    @staticmethod
    def get_user_data(db):
        return UsersModel().select_from_user(db, session.get("user_id"), username="username", email="email", cash="cash", confirmed="confirmed")

    def profile(self, db):
        """Profile shares of stock"""

        dir = os.path.join(
            current_app.config["UPLOAD_PATH"], str(session.get("user_id")) + "\\avatar"
        )
        dir_exists = os.path.exists(dir)
        get_user_avatar = None
        if dir_exists:
            get_user_avatar = (
                {"user_id": str(session.get("user_id")), "file": os.listdir(dir)[0]}
                if os.listdir(dir)
                else ""
            )

        data = self.get_user_data(db)[0]

        return render_template(
            "profile.html",
            change_password_form=self.get_reset_form(),
            get_user_avatar=get_user_avatar,
            data=data
        )
