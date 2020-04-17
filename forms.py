from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length

class ContactForm(FlaskForm):
    """Contact form."""
    name = TextField('Quel est ton prénom ?', [
        DataRequired()])
    lieu = TextField('Où te trouves-tu ?', [
        DataRequired()])
    techno = TextField('Quelle est la techno utilisée lors du stage ?', [
        DataRequired()])
    date = TextField('Quel est la date ?', [
        DataRequired()])
    enfants = TextAreaField('liste des prénoms enfants un par ligne', [
        DataRequired()])

    submit = SubmitField('Submit')