from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, FloatField


# flask_wtf uses python classes to represent web forms
# a form class defines the fields of the form as class variables
class MaceForms(FlaskForm):
    inputfile = FileField()
    priorsfile = FileField()
    alpha = FloatField()
    beta = FloatField()
    iterations = FloatField()
    threshold = FloatField()
    smoothing = FloatField()
    submit = SubmitField()
    email = StringField()
