from controllers.sellctrl import SellController
from helpers import login_required

class SellRoute:
    """Handle Sell Route
    """

    def __init__(self, app, db):
        self.app = app
        self.db = db

        @app.route("/sell", methods=["GET", "POST"])
        @login_required
        def sell():
            return SellController().sell(self.db)