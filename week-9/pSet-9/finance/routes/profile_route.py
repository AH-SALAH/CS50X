from controllers.profilectrl import ProfileController
from helpers import login_required

class ProfileRoute:
    """Handle Profile route
    """
    def __init__(self, app, db):
        self.app = app
        self.db = db
        
        @app.route("/user/profile", methods=["GET", "POST"])
        @login_required
        def profile():
            return ProfileController().profile(self.db)

