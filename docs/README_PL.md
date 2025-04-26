# Aplikacja do Zarządzania Plikami w Flask

Bezpieczna aplikacja webowa do zarządzania plikami osobistymi z solidną autentykacją i kompleksowymi operacjami na plikach.

## Kluczowe Funkcje

- Autentykacja użytkowników z silnymi wymaganiami dotyczącymi haseł
- Funkcjonalność przesyłania, pobierania, podglądu, edycji i usuwania plików
- Zarządzanie profilem użytkownika
- Bezpieczne przechowywanie plików z wykorzystaniem nazewnictwa opartego na UUID
- RESTful API z dokumentacją Swagger

## Szybki Start

```bash
# Utworzenie i aktywacja wirtualnego środowiska
python3 -m venv venv
source venv/bin/activate  # W Windows: venv\Scripts\activate

# Instalacja zależności
pip install -r requirements.txt

# Inicjalizacja bazy danych
python database_init.py

# Uruchomienie aplikacji
python app.py
```

Dostęp do aplikacji pod adresem [http://127.0.0.1:5000/](http://127.0.0.1:5000/)  
Dokumentacja API dostępna pod adresem [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

## Dokumentacja

Aby zapoznać się z kompleksową dokumentacją, w tym szczegółami architektury, referencją API i instrukcjami konfiguracji, zobacz plik [docs/documentation.md](docs/documentation.md).

## Technologie

- Backend: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- Frontend: Bootstrap 5, JavaScript, Jinja2
- Baza danych: SQLite
- Dokumentacja: Flasgger (Swagger)