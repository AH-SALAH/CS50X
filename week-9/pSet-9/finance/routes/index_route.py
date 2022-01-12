from controllers.indexctrl import IndexController
from helpers import login_required


class IndexRoute:
    """Handle Index Route
    """
    def __init__(self, app, db):
        self.app = app
        self.db = db

        @app.route("/")
        @app.route("/home")
        @login_required
        def index():
            return IndexController().index(self.db)

    # @staticmethod
    # def init(app, db):
    #     this = IndexRoute(app, db)
    #     this._app = app
