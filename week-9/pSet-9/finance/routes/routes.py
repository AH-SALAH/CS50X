from routes.uploadfile_route import FileUploadRoute
from routes.forgetpassword_route import ForgetPasswordRoute
from routes.changepassword_route import ChangePasswordRoute
from routes.profile_route import ProfileRoute
from routes.buy_route import BuyRoute
from routes.index_route import IndexRoute
from routes.sell_route import SellRoute
from routes.history_route import HistoryRoute
from routes.quote_route import QuoteRoute
from routes.register_route import RegisterRoute
from routes.login_route import LoginRoute
from routes.logout_route import LogoutRoute


class Routes:
    
    def __init__(self, app, db, settings):        
        IndexRoute(app, db)
        BuyRoute(app, db)
        SellRoute(app, db)
        HistoryRoute(app, db)
        QuoteRoute(app, db)
        RegisterRoute(app, db, settings=settings)
        LoginRoute(app, db)
        ProfileRoute(app, db)
        FileUploadRoute(app, db)
        ChangePasswordRoute(app, db)
        ForgetPasswordRoute(app, db)
        LogoutRoute(app, db)