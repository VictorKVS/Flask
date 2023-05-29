from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date of birth', validators=[DataRequired()])
    agreement = BooleanField('Agreement', default=False, validators=[DataRequired()])
