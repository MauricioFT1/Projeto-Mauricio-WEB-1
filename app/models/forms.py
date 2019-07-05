from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length, Regexp
from app.models.tables import User
from app import db

 



class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class RegisterForm(Form):
    username = StringField('Usuário', validators=[DataRequired()])
    name = StringField('Nome', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField('Confirmar Senha', validators=[
        DataRequired(), EqualTo('password', message='Senhas não conferem.')])
    email = StringField('email', validators=[DataRequired(), Email()])
    email2 = StringField('Confirmar Email', validators=[
        DataRequired(), EqualTo('email', message='Email não conferem.')])
    submit = SubmitField('register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Usuário já registrado.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("email já registrado.")






