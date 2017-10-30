from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Email, Optional

class UserForm(FlaskForm):
	"""User info modifying form"""
	id = HiddenField('id')
	name = StringField('name', validators=[DataRequired()])
	alias = StringField('alias', validators=[DataRequired()])
	email = StringField('email', validators=[Email()])
	role_id = IntegerField('role_id', validators=[DataRequired()])
	delete_date = DateField('delete_date',validators=[Optional()])


class LoginForm(FlaskForm):
	"""Login form"""
	email = StringField('login', validators=[Email()])
	password = PasswordField('password', validators=[DataRequired()])