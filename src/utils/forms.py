from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,TextAreaField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class ProjectForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    type = SelectField('type',choices = [ ('det', 'Detection'),('class', 'Classification')], validators=[DataRequired()])
    labels = TextAreaField('labels',validators=[DataRequired()])


