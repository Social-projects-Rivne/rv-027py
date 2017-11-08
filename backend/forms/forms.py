from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, DateField,
                     HiddenField, PasswordField, SelectField,
                     SubmitField)
from wtforms.validators import (DataRequired, Email, Optional,
                                Length, Regexp, ValidationError)

from app import db
from models.users import User


class UniqueValue(object):

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
        
        record_id = None
        if form.id.data:
            record_id = form.id.data

        query = db.session.query(self.model).filter(
            self.model.id != record_id).filter(
            self.property_to_find == field.data).first()

        if query:
            raise ValidationError(self.message)

check_email = UniqueValue(
    User, User.email,
    message="This email is already exists in database.")

check_alias = UniqueValue(
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


class SearchForm(FlaskForm):

    """Search form"""

    search = StringField(
        'search',
        validators=[
            DataRequired(),
            Length(min=2)
            ]
        )
    field_by = SelectField(
        'by',
        choices=[
            ('0', 'name'),
            ('1', 'alias'),
            ('2', 'email'),
            ('3', 'name+alias'),
            ('4', 'alias+email'),
            ('5', 'email+name'),
            ('6', 'email+name+alias')
            ]
        )
