from werkzeug.security import generate_password_hash
from forms.forgetpassword import ForgetPasswordForm
from itsdangerous.exc import BadTimeSignature
from models.users import UsersModel
from flask import flash, session, render_template, redirect, request, url_for, Markup
from helpers import apology, send_mail
from forms.resetpassword import ResetPasswordForm
from itsdangerous import SignatureExpired


class ForgetPasswordController:
    def __init__(self):
        pass

    def forget_password(
        self, db, app, serial, token_max_age=30
    ):
        """ForgetPassword"""

        form = ForgetPasswordForm()

        # check for POST
        if request.method == "POST":
            # use WTF validation
            if form.validate_on_submit():

                try:

                    # chk if already there
                    email_exists = UsersModel().check_email(db, form.email.data)
                    if not email_exists:
                        form.email.errors.append("Email not exists")
                        flash("Email does not exist", "danger")
                        session["attempts"] -= 1
                        return render_template("forget-password.html", form=form)

                except Exception as er:
                    print("forget password Err", er)
                    return apology("there is forget password error!")

                try:
                    email = email_exists[0]["email"] or form.email.data
                    # get username
                    username = UsersModel().get_user_by_email(db, email)

                    # generate confirmation token
                    token = serial.dumps(email, salt=app.config["MAIL_SALT"])

                    # create link
                    link = url_for("reset_password", token=token, _external=True)
                    # print("link: ", link, "token: ", token)
                    # send confirmation email
                    resp = send_mail(
                        subject="CS50 Reset Password",
                        from_email=(app.config["MAIL_USERNAME"], "CS50"),
                        to_emails=[email],
                        html_content=render_template(
                            "email-resetpassword.html",
                            username=username[0]["username"],
                            confirm_link=link,
                        ),
                        MAIL_CLIENT_API_KEY=app.config["SENDGRID_API_KEY"],
                    )

                    # print("resp: ", resp)
                    # if resp returned, then email has been sent
                    if resp:
                        flash(
                            Markup(
                                f"OK, You should recieve a reset password Email shortly to {form.email.data}"
                            ),
                            "success",
                        )
                        return redirect(url_for("login"))
                    else:
                        flash(
                            "Something went wrong, Email has not been sent!", "warning"
                        )

                    return render_template("forget-password.html", form=form)

                except Exception as er:
                    return apology(er, 500)

            return render_template("forget-password.html", form=form)

        else:
            if session.get("user_id"):
                return redirect(request.referrer)

            return render_template("forget-password.html", form=form)

    def reset_password(self, db, app, token, serial, token_max_age=30):
        """reset password

        Args:
            app (obj): app instance
            token (str): serialized token
            serial (obj): serial object
            token_max_age (int, optional): token timed max_age. Defaults to 30.

        Returns:
            html: template
        """



        form = ResetPasswordForm()

        if request.method == "POST":

            # use WTF validation
            if form.validate_on_submit():

                try:

                    # get user id
                    user_id = UsersModel().get_user_by_email(
                        db, session.get("user_email"), "id"
                    )

                    # insert into table
                    id = UsersModel().update_user_password(
                        db,
                        userId=user_id[0]["id"],
                        password=generate_password_hash(form.password.data),
                    )

                    # if id returned, then success. redirect to login
                    if id:

                        flash("Password Updated Successfully!", "success")

                        return redirect(url_for("login"))

                except Exception as er:
                    print("password update error", er)

                return render_template("reset-password.html", form=form)

            return render_template("reset-password.html", form=form)

        else:

            try:

                # get the load from the token
                load = serial.loads(
                    token, salt=app.config["MAIL_SALT"], max_age=token_max_age
                )

                # check mail
                email_exists = UsersModel().check_email(db, load)
                if not email_exists:
                    flash("Email does not exists!", "danger")
                    return apology("Who are You!")

                session["user_email"] = load
                flash("You can Reset your password", "info")
                return render_template(
                    "reset-password.html", form=form, confirmed_mail=load, token=token
                )

            except SignatureExpired as er:
                print("Token Expired", er)
                return apology("Token Expired")
            except BadTimeSignature as er:
                print("Invalid Token", er)
                return apology("Invalid Token")
            except Exception as er:
                print("Password Reset exception", er)
                return apology("Password Reset exception")
