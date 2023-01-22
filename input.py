from ast import Pass, Sub
from re import S
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class StockListForm(FlaskForm):
    stock = StringField('Stock Ticker', validators=[DataRequired()])
    interval = StringField('Interval (1min 5min 15min 30min 60min)', validators=[DataRequired()])
    submit = SubmitField('Set')

class SharesForm(FlaskForm):
    shares = IntegerField('', validators = [DataRequired(), NumberRange(min=1,max=1000000000000000000000000)])
    submit = SubmitField('BUY')
    
class Sell(FlaskForm):
    submit = SubmitField('SELL')

