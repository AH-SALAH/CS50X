from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import required, length, regexp, equal_to, email

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[required(), length(min=3)])
    email = EmailField('email', validators=[required(), email()])
    password = PasswordField('password', validators=[required(), length(min=3), regexp(regex='\w{3,}')])
    confirmation = PasswordField('confirmation', validators=[required(), length(min=3), regexp(regex='\w{3,}'), equal_to(fieldname='password')])