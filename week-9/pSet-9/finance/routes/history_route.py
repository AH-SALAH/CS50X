from controllers.historyctrl import HistoryController
from helpers import login_required

class HistoryRoute:
    """Handle History Route
    """
    def __init__(self, app, db):
        self.app = app
        self.db = db

        @app.route("/history", methods=["GET", "POST"])
        @login_required
        def history():
            return HistoryController().history(self.db)