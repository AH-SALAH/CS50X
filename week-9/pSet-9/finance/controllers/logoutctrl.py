from flask import session, redirect

class LogoutController:
    def __init__(self):
        pass

    def logout(self):
        """Log user out"""

        # Forget any user_id
        session.clear()

        # Redirect user to login form
        return redirect("/")