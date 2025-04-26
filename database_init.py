from app import app, db

# Tworzy wszystkie tabele w bazie danych na podstawie modeli
with app.app_context():
    db.create_all()
