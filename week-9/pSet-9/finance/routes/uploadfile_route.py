from flask import current_app
from controllers.fileuploadctrl import FileUploadController
from helpers import login_required

class FileUploadRoute:
    """Handle FileUpload route
    """
    def __init__(self, app, db):
        self.app = app
        self.db = db
        
        @current_app.route("/user/uploads", methods=["POST"])
        @login_required
        def uploads():
            return FileUploadController().upload_avatar()

        @current_app.get('/uploads/<file>')
        @login_required
        def get_uploads(file):
            return FileUploadController().get_avatar(file)

