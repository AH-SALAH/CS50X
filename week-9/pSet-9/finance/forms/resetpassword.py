from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import required, length, regexp, equal_to

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[required(), length(min=3), regexp(regex='\w{3,}')])
    confirmation = PasswordField('confirmation', validators=[required(), length(min=3), regexp(regex='\w{3,}'), equal_to(fieldname='password')])