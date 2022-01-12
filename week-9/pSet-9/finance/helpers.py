from datetime import datetime
import os
import requests
import urllib.parse
import imghdr

from flask import (
    flash,
    redirect,
    render_template,
    session,
    url_for,
    current_app,
)
from functools import wraps
from werkzeug.utils import secure_filename


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def confirmation_required(f):
    """
    Decorate routes to require confirmation.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_confirmed"):
            flash("Email Confirmation Required", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        # print("quote", quote)
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"],
            "latest Time": quote["latestTime"],
            "change": quote["change"],
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


# ###############
# mail client
def send_mail(MAIL_CLIENT_API_KEY="", **kwargs):
    # using SendGrid's Python Library
    # https://github.com/sendgrid/sendgrid-python
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    message = Mail(**kwargs)
    response = ""

    try:
        sg = SendGridAPIClient(MAIL_CLIENT_API_KEY)
        response = sg.send(message)

        # print("statuscode: ", response.status_code)
        # print("body: ", response.body)
        # print("headers: ", response.headers)
    except Exception as e:
        print(e)
    finally:
        return response


# ###############
# file upload handling

def validate_image(stream):
    """validate image

    Args:
        stream (binaryIO|str): image stream

    Returns:
        str: image extension | None
    """
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")


# handle file upload
def upload_files(
    file=None,
    user_folder_name="",
    file_name="",
    upload_extensions="",
    upload_path="",
    multiple=False,
    cb=()
):
    if not file:
        return "No file has been presented!", 400
    
    uploaded_file = file

    # multiple files
    if multiple:
        files = {"ok": 200, "path": []}
        for f in uploaded_file:

            filename = secure_filename(f.filename)
            if filename == "":
                return "No file has been presented!", 400

            file_ext = os.path.splitext(filename)[1]

            filename = str(datetime.now().timestamp()).replace(".", "") + file_ext

            if file_ext not in upload_extensions or (
                "image" in f.mimetype and file_ext != validate_image(f.stream)
            ):
                return "Invalid file", 400

            f.save(os.path.join(upload_path, user_folder_name, filename))
            files["path"].append(
                {filename: os.path.join(upload_path, user_folder_name, filename)}
            )

        return files
    else:

        # single file
        filename = secure_filename(uploaded_file.filename)
        if filename == "":
            return "No file has been presented!", 400

        file_ext = os.path.splitext(filename)[1]

        if file_name:
            filename = file_name + file_ext

        if file_ext not in upload_extensions or (
            "image" in uploaded_file.mimetype
            and file_ext != validate_image(uploaded_file.stream)
        ):
            return "Invalid file", 400

        # callback fn if found [created to remove old file first]
        if cb:
            cb(user_folder_name)

        uploaded_file.save(os.path.join(upload_path, user_folder_name, filename))

        return {
            "ok": 200,
            "path": {
                "filename": filename,
                "filepath": os.path.join(
                    upload_path, user_folder_name, filename
                ).replace("\\", "/"),
            },
        }

# is file exists
def is_avatar_exists():
    dir = os.path.join(current_app.config["UPLOAD_PATH"], str(session.get("user_id")) + "\\avatar")
    file_exist = os.path.exists(os.path.join(dir, os.listdir(dir)[0]) if os.listdir(dir) else "")

    if not file_exist:
        return False
    return os.listdir(dir)[0]