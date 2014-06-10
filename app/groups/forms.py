from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class GroupForm(Form):
    
    name = TextField('Group name', [Required()])
    slug = TextField('Slug')
    currency = TextField('Currency', [Required()])


class JoinGroupForm(Form):
    """Empty form - don't need anything"""
    
    pass
    

