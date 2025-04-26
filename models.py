from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Inicjalizacja obiektu bazy danych
# (będzie używany przez całą aplikację)
db = SQLAlchemy()

class Files(db.Model):
    # Model pliku przechowywanego przez użytkownika
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(100), nullable=False)  # Oryginalna nazwa pliku
    stored_filename = db.Column(db.String(36), nullable=False, unique=True)  # Nazwa pliku na serwerze (UUID)
    size = db.Column(db.Float, nullable=False)  # Rozmiar pliku w MB
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ID właściciela pliku
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)  # Data przesłania pliku

    def __repr__(self):
        # Reprezentacja tekstowa obiektu File
        return f'<File {self.original_filename}>'

class Users(db.Model, UserMixin):
    # Model użytkownika
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False)  # Login użytkownika
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email użytkownika
    password_hash = db.Column(db.String(128))  # Zahaszowane hasło
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # Data rejestracji
    files = db.relationship('Files', backref='user', lazy=True)  # Relacja: użytkownik -> pliki

    @property
    def password(self):
        # Blokada odczytu hasła wprost
        raise AttributeError('Nie można odczytać hasła!')

    @password.setter
    def password(self, password):
        # Ustawianie hasła z automatycznym haszowaniem
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Weryfikacja hasła użytkownika
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        # Reprezentacja tekstowa obiektu User
        return f'<User {self.login}>'
