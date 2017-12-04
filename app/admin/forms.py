# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class FoodForm(FlaskForm):
    """
    Form for user to add or edit a Food
    """
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class StepForm(FlaskForm):
    """
    Form for user to add step
    """
    desc = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')