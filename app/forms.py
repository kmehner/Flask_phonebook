from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    submit = SubmitField('Create')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In') 

class AddressForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

