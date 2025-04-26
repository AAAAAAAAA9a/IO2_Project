import os

class Config:
    # Podstawowa konfiguracja aplikacji
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
    SECRET_KEY = "Super klucz tajnosci"  # jest hardcoded ale gdyby bylo to w srodowisku produkcyjnym, wyrzucilbym na zmienna env
    UPLOAD_FOLDER = 'uploads'
    
    @staticmethod
    def init_app(app):
        # Tworzenie folderu na pliki, jeśli nie istnieje
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
