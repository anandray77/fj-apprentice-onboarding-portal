from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8),
        Regexp(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message="Password must contain at least one letter, one number, and one special character."
        )
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=50)])
    submit = SubmitField('Register')
