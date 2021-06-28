from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = TextField('username', validators=[DataRequired()])