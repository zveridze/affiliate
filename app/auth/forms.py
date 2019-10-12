from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    # messenger_type = SelectField('Messenger type', choices=current_app.config['MESSENGERS'])
    messenger_type = SelectField('Messenger type')
    messenger = StringField('Messenger')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
