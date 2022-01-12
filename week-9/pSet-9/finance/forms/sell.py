from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.validators import required, number_range

class SellForm(FlaskForm):
    symbol = SelectField('symbol', validators=[required()])
    shares = IntegerField('shares', validators=[required(), number_range(min=1)])