from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email

# Formularz rejestracji użytkownika
class RegisterForm(FlaskForm):
    login = StringField('Wpisz login', validators=[DataRequired()])  # Login użytkownika
    email = StringField('Wpisz e-mail', validators=[DataRequired(), Email()])  # Email użytkownika
    password_hash = PasswordField('Wpisz hasło', validators=[
        DataRequired(), 
        Length(min=15, message='Hasło potrzebuje minimum 15 znaków!'),
        EqualTo('password_reply', message='Hasła się nie zgadzają!')])  # Hasło z walidacją długości i powtórzenia

    password_reply = PasswordField('Powtórz hasło', validators=[DataRequired()])  # Powtórzenie hasła
    submit_button = SubmitField('Zarejestruj się')  # Przycisk rejestracji

# Formularz logowania użytkownika
class LoginForm(FlaskForm):
    login_or_email = StringField('Login lub e-mail', validators=[DataRequired()], render_kw={"placeholder": "Wpisz login lub e-mail"})  # Login lub email
    password = PasswordField('Hasło', validators=[DataRequired()], render_kw={"placeholder": "Wpisz hasło"})  # Hasło
    submit = SubmitField('Zaloguj się')  # Przycisk logowania
