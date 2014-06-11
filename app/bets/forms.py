from flask.ext.wtf import Form
from wtforms import TextField, DecimalField, IntegerField
from wtforms.validators import Required

class BetForm(Form):
    
    amount = DecimalField()
    outcome = IntegerField()
