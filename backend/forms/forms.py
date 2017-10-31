from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, HiddenField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length


class UserForm(FlaskForm):
    """User info modifying form"""
    id = HiddenField('id')
    name = StringField('name', validators=[DataRequired(), Length(max=20)])
    alias = StringField('alias', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    role_id = SelectField('role_id', choices=[(
        '1', 'admin'), ('2', 'moderator'), ('3', 'user')], validators=[DataRequired()])
    delete_date = DateField('delete_date', validators=[Optional()])
    submit_button = SubmitField('Save')


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('login', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit_button = SubmitField('Login')

class SearchForm(FlaskForm):
    """Search form"""
    search = StringField('search', validators = [DataRequired("Please enter string")])
    field_by = SelectField('by', choices=[(1, 'name'), (2, 'alias'), (3, 'email'),(4, 'name+alias'), (5, 'alias+email'), (6, 'email+name'), (7, 'email+name+alias')],  validators=[DataRequired()])
