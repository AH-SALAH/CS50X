from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import required, number_range

class BuyForm(FlaskForm):
    symbol = StringField('symbol', validators=[required()])
    shares = IntegerField('shares', validators=[required(), number_range(min=1)])