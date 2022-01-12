from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.validators import required, email

class ForgetPasswordForm(FlaskForm):
    email = EmailField('email', validators=[required(), email()])
