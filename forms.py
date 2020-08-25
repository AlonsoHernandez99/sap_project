from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class PersonForm(FlaskForm):
    name = StringField('Name: ', validators=[validators.DataRequired()])
    lastname = StringField('LastName: ', validators=[validators.DataRequired()])
    email = StringField('Email: ', validators=[validators.DataRequired()])
    send = SubmitField('Send')
