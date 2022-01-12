from itsdangerous.exc import BadTimeSignature
from models.users import UsersModel
from flask import flash, session, render_template, redirect, request, url_for, Markup
from helpers import apology, send_mail
from werkzeug.security import generate_password_hash
from forms.register import RegisterForm
from itsdangerous import SignatureExpired


class RegisterController:
    def __init__(self):
        pass

    def register(self, db, app, serial, token_max_age=300):
        """Register user"""

        form = RegisterForm()

        if request.method == "POST":
            # use WTF validation
            if form.validate_on_submit():
                # normal validation
                # add fields to dict
                # data = {
                #     "Name": request.form.get("username"),
                #     "Password": request.form.get("password"),
                #     "Confirm": request.form.get("confirmation"),
                # }
                # Errors = []
                # # loop on fields and flash its msg
                # for field in data:
                #     if not data[field]:
                #         Errors.append(f"{field} is missing or not correct")

                # if Errors:
                #     for er in Errors:
                #         flash(er, "danger")
                #     return render_template("register.html")

                # #  chk if password & confirmation password not the same
                # if data["Password"] != data["Confirm"]:
                #     flash("password and confirmation are not the same!", "danger")
                #     return render_template("register.html")

                try:
                    # chk if already there
                    username_exists = UsersModel().check_username(db, form.username.data)
                    if username_exists:
                        form.username.errors.append("User name already exists")
                        flash(
                            "user name already exists, Please try another one", "danger"
                        )
                        return render_template("register.html", form=form)

                    email_exists = UsersModel().check_email(db, form.email.data)
                    if email_exists:
                        form.email.errors.append("email already exists")
                        flash("email already exists, Please try another one", "danger")
                        return render_template("register.html", form=form)

                except Exception as er:
                    print("user Registration Err", er)

                try:
                    # insert into table
                    id = UsersModel().create_user(
                        db,
                        username=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data),
                    )

                    # if id returned, then success. set in session & send confirmation mail
                    if id:
                        session["user_id"] = id

                        # generate confirmation token
                        token = serial.dumps(
                            form.email.data, 
                            salt=app.config["MAIL_SALT"]
                        )

                        # create link
                        link = url_for("mail_confirmation", token=token, _external=True)

                        # msg = f"""
                        #     <p>Please, click the link to Confirm your email:</p> 
                        #     <a href="{link}" target="_blank">Confirm</a> 
                        #     <br> 
                        #     <strong>Note</strong>: it's valid for {token_max_age} sec
                        # """

                        # send confirmation email
                        resp = send_mail(
                            subject="CS50 Confirmation",
                            from_email=(app.config["MAIL_USERNAME"], "CS50"),
                            to_emails=[form.email.data],
                            html_content=render_template("email-verify.html", username=form.username.data, confirm_link=link),
                            MAIL_CLIENT_API_KEY=app.config["SENDGRID_API_KEY"]
                        )

                        # if resp returned, then email has been sent
                        if resp:
                            flash(Markup(f"Registered Successfully!<br>A Confirmation Email has been sent to {form.email.data}") , "success")
                        else:
                            flash("Registered Successfully!", "success")

                        return redirect(url_for("login"))

                except Exception as er:
                    return apology(er, 500)

            return render_template("register.html", form=form)

        else:
            if session.get("user_id"):
                return redirect(request.referrer)

            return render_template("register.html", form=form)


    def mail_confirmation(self, db, app, token, serial, token_max_age=300):
        """email confirm

        Args:
            app (obj): app instance
            token (str): serialized token
            serial (obj): serial object
            token_max_age (int, optional): token timed max_age. Defaults to 30.

        Returns:
            html: template
        """
        try:
            # get the load from the token
            load = serial.loads(
                token, 
                salt=app.config["MAIL_SALT"], 
                max_age=token_max_age
            )

            # check mail
            email_exists = UsersModel().check_email(db, load)
            if not email_exists:
                flash("Email does not exists!", "danger")
                return apology("Who are You!")

            # update confirmed
            confirmed = UsersModel().update_user_confirm(db, load)
            # print("confirmed: ", confirmed)
            if confirmed:
                flash("Confirmed Successfully", "success")
                return render_template("login.html", confirmed_mail=load)

            return render_template("login.html", confirmed_mail=load)

        except SignatureExpired as er:
            print("Token Expired", er)
            return apology("Token Expired")
        except BadTimeSignature as er:
            print("Invalid Token", er)
            return apology("Invalid Token")
        except Exception as er:
            print("Email confirm exception", er)
            return apology("Email confirm exception")
