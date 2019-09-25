from flask_wtf import FlaskForm
from app.models import User
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, Email, EqualTo, DataRequired


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    phone = IntegerField('Phone')
    messenger_type = StringField('Messenger type')
    messenger = StringField('Messenger')
    password = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Sorry, email already exist')
