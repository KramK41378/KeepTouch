from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class RegisterForm(FlaskForm):
    fullname = StringField('Полное имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=3, max=32),
        Regexp(r'^\w+$', message='Только буквы, цифры и _')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, message='Минимум 8 символов'),
        Regexp(r'(?=.*[A-Za-z])(?=.*\d)', message='Нужны буквы и цифры')
    ])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли не совпадают')
    ])
    submit = SubmitField('Зарегистрироваться')