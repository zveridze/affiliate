from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import Email, EqualTo, DataRequired, Length
from app import app


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    messenger_type = SelectField('Messenger type', choices=app.config['MESSENGERS'])
    messenger = StringField('Messenger')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=60)])
    submit = SubmitField('New link')


class PersonalDataEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    messenger_type = SelectField('Messenger type', choices=app.config['MESSENGERS'])
    messenger = StringField('Messenger')
    submit = SubmitField('Save')
