"""This module contains forms classes for admin manage."""
from flask_wtf import FlaskForm
from wtforms import (StringField, HiddenField, TextAreaField,
                     PasswordField, SelectField, SubmitField,
                     FloatField)
from wtforms.validators import (DataRequired, Email,
                                Length, Regexp, ValidationError)

from backend.app import db
from backend.models.users import User
from backend.models.issues import Issue


class UniqueValue(object):
    """Custom validator.

    Validate for unique field value.
    Skips record in database with current user's id.

    """

    # pylint: disable=too-few-public-methods

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


class BaseForm(FlaskForm):
    """Adds csrf"""
    class Meta:
        csrf = True


class UserForm(BaseForm):
    """User info modifying form."""

    id = HiddenField('id')
    name = StringField(
        'name',
        description=u'Length between 3 and 15 chars.',
        validators=[
            DataRequired(),
            Length(min=3, max=15),
            Regexp(
                r"^[\w]+$",
                message='Only letters, numbers and "_" may be used.')
        ]
    )
    alias = StringField(
        'alias',
        description=u'Length between 3 and 15 chars.',
        validators=[
            DataRequired(),
            check_alias,
            Length(min=3, max=15),
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


class UserAddForm(BaseForm):
    """User add form."""

    id = HiddenField('id')
    name = StringField(
        'name',
        description=u'Length between 3 and 15 chars.',
        validators=[
            DataRequired(),
            Length(min=3, max=15),
            Regexp(
                r"^[\w]+$",
                message='Only letters, numbers and "_" may be used.')
        ]
    )
    alias = StringField(
        'alias',
        description=u'Length between 3 and 15 chars.',
        validators=[
            DataRequired(),
            check_alias,
            Length(min=3, max=15),
            Regexp(
                r"^[\w]+$",
                message='Only letters, numbers and "_" may be used.')
        ]
    )
    email = StringField('email', validators=[Email(), check_email])

    password = PasswordField(
        'password',
        description=u'Length between 3 and 20 chars.',
        validators=[
            DataRequired(),
            Length(min=3, max=20),
            Regexp(
                r"^[\w]+$",
                message='Only letters, numbers and "_" may be used.')
        ]
    )

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


class IssueForm(BaseForm):
    """Issue edit form"""

    id = HiddenField('id')
    title = StringField(
        'title',
        description=u'Length between 3 and 15 chars.',
        validators=[
            DataRequired(),
            Length(min=3, max=15)
        ]
    )

    status = SelectField(
        'status',
        choices=[
            ('new', 'new'),
            ('on moderation', 'on moderation'),
            ('open', 'open'),
            ('closed', 'closed')
        ],
        validators=[DataRequired()]
    )

    description = TextAreaField(
        'description',
        description=u'Length between 10 and 144 chars.',
        validators=[
            DataRequired(),
            Length(min=10, max=144)
        ]
    )

    location_lat = FloatField(
        'location lat',
        validators=[
            DataRequired(),
        ]
    )

    location_lon = FloatField(
        'location lot',
        validators=[
            DataRequired(),
        ]
    )

    category_id = SelectField(
        'category',
        choices=[
            ('1', 'road accident'),
            ('2', 'infrastructure accident'),
            ('3', 'another accident')
        ],
        validators=[DataRequired()]
    )

    submit_button = SubmitField('Save')


class LoginForm(BaseForm):
    """Login form."""

    email = StringField('login', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit_button = SubmitField('Login')


class SearchUserForm(BaseForm):
    """Search form"""

    search = StringField(
        'search'
    )
    search_by = SelectField(
        'search_by',
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
    order_by = SelectField(
        'order_by',
        choices=[
            ('0', 'id'),
            ('1', 'role'),
            ('2', 'delete date')
        ]
    )

    class Meta:
        csrf = False


class SearchIssuesForm(BaseForm):
    """Search form"""

    search = StringField(
        'search'
    )
    search_by = SelectField(
        'search_by',
        choices=[
            ('0', 'title'),
            ('1', 'category'),
        ]
    )
    order_by = SelectField(
        'order_by',
        choices=[
            ('0', 'title'),
            ('1', 'category'),
        ]
    )

    class Meta:
        csrf = False
