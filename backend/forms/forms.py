from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, DateField,
                     HiddenField, PasswordField, SelectField,
                     SubmitField)
from wtforms.validators import (DataRequired, Email, Optional,
                                Length, Regexp, ValidationError)

from app import db
from models.users import User


class Check_users_field(object):

    """Custom validator.

    Validate for unique field value.
    Skips record in database with current user's id.

    """

    def __init__(self, model, property_to_find, message=None):
        if not message:
            message = "This field's value is already exists in database."
        self.message = message
        self.model = model
        self.property_to_find = property_to_find

    def __call__(self, form, field):
        if not form.id.data:
            form.id.data = None
        self.query = db.session.query(self.model).filter(
            self.model.id != form.id.data).filter(
            self.property_to_find == field.data).first()
        if self.query:
            raise ValidationError(self.message)

check_email = Check_users_field(
    User, User.email,
    message="This email is already exists in database.")

check_alias = Check_users_field(
    User, User.alias,
    message="This alias is already exists in database.")


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
            check_alias,
            Length(min=3, max=32),
            Regexp(
                r"^[\w]+$",
                message='Only letters, numbers and "_" may be used.')
        ]
    )
    email = StringField('email', validators=[Email(), check_email])

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
