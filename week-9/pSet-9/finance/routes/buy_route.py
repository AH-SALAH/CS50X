from controllers.buyctrl import BuyController
from helpers import confirmation_required, login_required

class BuyRoute:
    """Handle Buy route
    """
    def __init__(self, app, db):
        self.app = app
        self.db = db
        
        @app.route("/buy", methods=["GET", "POST"])
        @login_required
        @confirmation_required
        def buy():
            return BuyController().buy(self.db)

    # @staticmethod
    # def init(app, db):
    #     this = BuyRoute(app, db)
    #     this._app = app

