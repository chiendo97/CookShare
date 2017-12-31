# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired

class FoodForm(FlaskForm):
    """
    Form for user to add or edit a Food
    """
    name = StringField('Name', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class StepForm(FlaskForm):
    """
    Form for user to add step
    """
    desc = StringField('Description', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Submit')

class ImageForm(FlaskForm):
    """
    Form for uploading image
    """
    image = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Submit image')

class PostForm(FlaskForm):
    """
    Form for posting command
    """
    desc = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')