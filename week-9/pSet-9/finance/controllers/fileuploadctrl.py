from datetime import datetime
import os
from flask import jsonify, current_app, request, session, send_from_directory
from helpers import upload_files


class FileUploadController:
    def __init__(self):
        pass

    def upload_avatar(self):
        """FileUpload"""
        
        if request.method == "POST" and session.get("user_id"):
            user_folder_name = str(session.get("user_id")) + "\\avatar"
            file_name = str(session.get("user_id")) + '_' + str(datetime.now().timestamp()).replace(".", "")

            try:

                result = upload_files(
                    file=request.files["file"],
                    user_folder_name=user_folder_name,
                    file_name=file_name,
                    upload_extensions=current_app.config["UPLOAD_EXTENSIONS"],
                    upload_path=current_app.config["UPLOAD_PATH"],
                    # for now it should be 1 avatar file, so we overwrite if exists
                    cb=self.remove_old
                )

            except OSError as er:
                print("An exception occurred", er)
                return er, 500

            print("result:", result)

            # set in session
            session["user_avatar"] = result["path"]["filename"] if type(result) == dict and "ok" in result.keys() else session.get("user_avatar")
            session.modified = True

            # er format
            if type(result) == tuple:
                return result

            return jsonify(result)

        return "Invalid Method", 400
        # return render_template("profile.html", change_password_form=self.get_reset_form())


    def get_avatar(self, filename):
        dir = os.path.join(current_app.config["UPLOAD_PATH"], str(session.get("user_id")) + "\\avatar")
        file = os.path.join(dir, filename)
        file_exists = os.path.exists(file)
        if not file_exists:
            return ""
        return send_from_directory(dir, filename)


    def remove_old(self, user_folder_name):
        """remove old file

        Args:
            user_folder_name (path): user folder path

        Returns:
            tuple: ok tuple | er tuple
        """
        try:
            path = os.path.join(
                current_app.config["UPLOAD_PATH"],
                user_folder_name,
            )
            dir_exists = os.path.exists(path)
            # print("path: ", path, "dir_exists: ", dir_exists)
            if not dir_exists:
                os.makedirs(path)

            old = os.listdir(path)[0] if os.listdir(path) else ""
            # print("old: ", old)
            file_exists = os.path.exists(os.path.join(path, old))

            if file_exists:
                os.remove(os.path.join(path, old))
                # print("rm: ", os.path.join(path, old))

            return "ok", 204
            
        except OSError as er:
            print('An exception occurred', er)
            return er, 500