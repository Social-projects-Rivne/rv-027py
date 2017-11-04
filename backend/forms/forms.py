from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, DateField,
                     HiddenField, PasswordField, SelectField,
                     SubmitField)
from wtforms.validators import DataRequired, Email, Optional, Length, Regexp


class UserForm(FlaskForm):

    """User info modifying form."""

    id = HiddenField('id')
    name = StringField(
        'name',
        description=u'Length between 3 and 32 chars.',
        validators=[
            DataRequired(),
            Length(min=3, max=32),
            Regexp(
                r"^[\w]+$",
                message='Only letters, numbers and "_" may be used.')
        ]
    )
    alias = StringField(
        'alias',
        description=u'Length between 3 and 32 chars.',
        validators=[
            DataRequired(),
            Length(min=3, max=32),
            Regexp(
                r"^[\w]+$",
                message='Only letters, numbers and "_" may be used.')
        ]
    )
    email = StringField('email', validators=[Email()])

    role_id = SelectField(
        'role_id',
        choices=[
            ('1', 'admin'),
            ('2', 'moderator'),
            ('3', 'user')
        ],
        validators=[DataRequired()]
    )

    submit_button = SubmitField('Save')


class LoginForm(FlaskForm):

    """Login form."""

    email = StringField('login', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit_button = SubmitField('Login')
