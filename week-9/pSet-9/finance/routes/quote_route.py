from controllers.quotectrl import QuoteController
from helpers import login_required

class QuoteRoute:
    """Handle Quote Route
    """

    def __init__(self, app, db):
        self.app = app
        self.db = db

        @app.route("/quote", methods=["GET", "POST"])
        @login_required
        def quote():
            return QuoteController().quote()