# import os
from controllers.profilectrl import ProfileController
# from itsdangerous.exc import BadTimeSignature
from models.users import UsersModel
from flask import flash, session, render_template, redirect, request, url_for
from helpers import apology
from werkzeug.security import generate_password_hash
# from forms.resetpassword import ResetPasswordForm
# from itsdangerous import SignatureExpired


class ChangePasswordController(ProfileController):
    def __init__(self):
        pass

    def change_password(self, db):
        """Change Password"""
        
        change_password_form = ProfileController().get_reset_form()

        if request.method == "POST" and session.get("user_id"):
            # use WTF validation
            if change_password_form.validate_on_submit():

                # try:
                    # chk if already there

                    # email_exist = UsersModel().check_email(db, change_password_form.email.data)
                    # if email_exist:
                    #     change_password_form.email.errors.append("email already exists")
                    #     flash("email already exits, Please try another one", "danger")
                    #     return render_template("reset-password.html", change_password_form=change_password_form)

                # except Exception as er:
                #     print("user Registration Err", er)

                try:
                    # insert into table
                    id = UsersModel().update_user_password(
                        db,
                        userId=session.get("user_id"),
                        password=generate_password_hash(change_password_form.password.data),
                    )

                    # if id returned, then success. set in session & send confirmation mail
                    if id:
                        # session["user_id"] = id

                        # generate confirmation token
                        # token = serial.dumps(
                        #     change_password_form.email.data, 
                        #     salt=app.config["MAIL_SALT"]
                        # )

                        # create link
                        # link = url_for("mail_confirmation", token=token, _external=True)

                        # msg = f"""
                        #     <p>Please, click the link to Confirm your email:</p> 
                        #     <a href="{link}" target="_blank">Confirm</a> 
                        #     <br> 
                        #     <strong>Note</strong>: it's valid for {token_max_age} sec
                        # """

                        # send confirmation email
                        # resp = send_mail(
                        #     subject="CS50 Confirmation",
                        #     from_email=(app.config["MAIL_USERNAME"], "CS50"),
                        #     to_emails=[change_password_form.email.data],
                        #     html_content=render_template("email-verify.html", username=change_password_form.username.data, confirm_link=link),
                        #     MAIL_CLIENT_API_KEY=app.config["SENDGRID_API_KEY"]
                        # )

                        # if resp returned, then email has been sent
                        # if resp:
                        #     flash(Markup(f"Registered Successfully!<br>A Confirmation Email has been sent to {change_password_form.email.data}") , "success")
                        # else:
                        flash("Password Updated Successfully!", "success")

                        return redirect(url_for("login"))

                except Exception as er:
                    return apology(er, 500)

            return render_template("profile.html", change_password_form=change_password_form)

        else:
            return redirect(request.referrer)



    # def mail_confirmation(self, app, token, serial, token_max_age=30):
    #     """email confirm

    #     Args:
    #         app (obj): app instance
    #         token (str): serialized token
    #         serial (obj): serial object
    #         token_max_age (int, optional): token timed max_age. Defaults to 30.

    #     Returns:
    #         html: template
    #     """
    #     try:
    #         # get the load from the token
    #         load = serial.loads(
    #             token, 
    #             salt=app.config["MAIL_SALT"], 
    #             max_age=token_max_age
    #         )

    #         flash("Confirmed Successfully", "success")
    #         return render_template("login.html", confirmed_mail=load)

    #     except SignatureExpired as er:
    #         print("Token Expired", er)
    #         return apology("Token Expired")
    #     except BadTimeSignature as er:
    #         print("Invalid Token", er)
    #         return apology("Invalid Token")
    #     except Exception as er:
    #         print("Email confirm exception", er)
    #         return apology("Email confirm exception")
