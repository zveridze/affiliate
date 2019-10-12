from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Email, DataRequired, Length


class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=60)])
    site = StringField('Site', validators=[DataRequired(), Length(min=1, max=120)])
    submit = SubmitField('New link')


class PersonalDataEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    # messenger_type = SelectField('Messenger type', choices=app.config['MESSENGERS'])
    messenger_type = SelectField('Messenger type')
    messenger = StringField('Messenger')
    submit = SubmitField('Save')

