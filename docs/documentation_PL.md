# Aplikacja do Zarządzania Plikami w Flask

## 1. Podsumowanie

**Aplikacja do Zarządzania Plikami w Flask** zapewnia bezpieczną i intuicyjną platformę do zarządzania plikami osobistymi poprzez interfejs webowy. Implementuje ona solidną autentykację, kompleksowe operacje na plikach i jest zgodna z architekturą Model-Widok-Kontroler (MVC).

### Główne cele
- Bezpieczne przechowywanie i zarządzanie plikami
- Autentykacja użytkowników zgodna ze standardami branżowymi
- Kompleksowe operacje na plikach (przesyłanie, pobieranie, podgląd, edycja, usuwanie)
- Demonstracja architektury MVC z wykorzystaniem Flask
- Prezentacja nowoczesnych praktyk programowania webowego

## 2. Architektura Aplikacji

### 2.1 Ogólna Struktura

Aplikacja ściśle przestrzega wzorca architektury Model-Widok-Kontroler (MVC), z wyraźnym rozgraniczeniem odpowiedzialności:

- **Modele** (`models.py`): Obsługują schemat bazy danych, logikę biznesową i relacje
  - Implementują właściwą walidację danych i zarządzanie relacjami
  - Obsługują haszowanie haseł przy użyciu narzędzi bezpieczeństwa Werkzeug
  - Zarządzają relacjami użytkownik-plik przez SQLAlchemy ORM

- **Widoki** (`templates/`): Zawierają szablony HTML renderowane dla klienta
  - Wykorzystują silnik szablonów Jinja2 do dynamicznej zawartości
  - Implementują dziedziczenie szablonów dla spójnego układu (base.html)
  - Rozdzielają szablony według funkcjonalności (login.html, dashboard.html, itp.)
  - Wykorzystują Bootstrap 5 do responsywnego designu

- **Kontrolery** (`app.py`): Zarządzają obsługą tras i logiką aplikacji
  - Implementują przepływy autentykacji
  - Przetwarzają operacje na plikach
  - Obsługują warunki błędów
  - Dostarczają dokumentację API przez Swagger

### 2.2 Kluczowe Rozszerzenia Flask

Aplikacja wykorzystuje kilka kluczowych rozszerzeń Flask, aby wzbogacić swoją funkcjonalność:

- **Flask-SQLAlchemy**: Mapowanie Obiektowo-Relacyjne dla interakcji z bazą danych
  - Upraszcza zapytania do bazy danych i zarządzanie relacjami
  - Zapewnia zarządzanie transakcjami dla integralności danych

- **Flask-Login**: Kompleksowe zarządzanie autentykacją użytkowników
  - Obsługuje sesje użytkowników
  - Zapewnia ochronę dla tras wymagających autentykacji
  - Zarządza tożsamością użytkownika

- **Flask-Migrate**: Wersjonowanie schematu bazy danych przez Alembic
  - Umożliwia strukturyzowane migracje bazy danych
  - Utrzymuje historię schematu bazy danych

- **Flask-WTF**: Obsługa formularzy i walidacja
  - Zapewnia ochronę CSRF
  - Implementuje walidację formularzy
  - Upraszcza renderowanie formularzy

- **Flasgger**: Dokumentacja API oparta na Swagger
  - Automatycznie generuje dokumentację API
  - Dostarcza interaktywny interfejs testowy
  - Dokumentuje endpointy API i parametry

### 2.3 Architektura Komponentów i Przepływ Danych

Architektura aplikacji opiera się na warstwowym podejściu z odrębnymi komponentami, które współdziałają poprzez dobrze zdefiniowane interfejsy:

```
+-------------------------+        +----------------------+
|  Warstwa Interfejsu Web |        |  Dokumentacja API    |
| (Szablony & JavaScript) |<------>| (Swagger/Flasgger)   |
+-------------------------+        +----------------------+
            ^
            |
            v
+-------------------------+        +----------------------+
|  Warstwa Aplikacji      |<------>|  Autentykacja        |
| (Trasy & Kontrolery)    |        | (Flask-Login)        |
+-------------------------+        +----------------------+
            ^
            |
            v
+-------------------------+        +----------------------+
|  Warstwa Dostępu do     |<------>|  System              |
|  Danych (Modele SQLAlch)|        |  Przechowywania      |
+-------------------------+        +----------------------+
            ^
            |
            v
+-------------------------+
|  Baza Danych            |
| (SQLite)                |
+-------------------------+
```

#### Kluczowe Przepływy Danych

1. **Przepływ Autentykacji:**
   - Użytkownik przesyła dane uwierzytelniające przez formularz logowania
   - Aplikacja weryfikuje dane uwierzytelniające w bazie danych
   - W przypadku powodzenia, Flask-Login tworzy sesję użytkownika
   - Użytkownik jest przekierowany do panelu głównego

2. **Przepływ Przesyłania Plików:**
   - Użytkownik wybiera plik przez formularz przesyłania
   - Plik jest przetwarzany przez serwer (walidacja, obliczanie rozmiaru)
   - Generowany jest unikalny UUID dla bezpiecznego przechowywania
   - Plik jest zapisywany w systemie plików z UUID jako nazwą pliku
   - Metadane pliku są zapisywane w bazie danych z odniesieniem do użytkownika

3. **Przepływ Operacji na Plikach:**
   - Użytkownik żąda operacji na pliku (pobieranie, podgląd, edycja, usuwanie)
   - Aplikacja weryfikuje własność pliku przez użytkownika
   - Żądana operacja jest wykonywana
   - Odpowiedź jest wysyłana z powrotem do użytkownika

## 3. Schemat Bazy Danych

Aplikacja używa SQLite z SQLAlchemy ORM do trwałego przechowywania danych. Schemat bazy danych został zaprojektowany z myślą o bezpieczeństwie, wydajności i integralności danych.

### 3.1 Model Users

Model Users obsługuje autentykację użytkowników i zarządzanie profilami:

```python
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    files = db.relationship('Files', backref='user', lazy=True)
```

**Kluczowe cechy modelu Users:**

- **Integracja UserMixin**: Dziedziczy z UserMixin Flask-Login, aby zapewnić wymagane metody autentykacji
- **Bezpieczna obsługa haseł**: Implementuje haszowanie haseł z dekoratorami właściwości, aby zapobiec bezpośredniemu dostępowi
- **Unikalność emaila**: Wymusza unikalne adresy email, aby zapobiec duplikatom kont
- **Znacznik czasu rejestracji**: Zapisuje, kiedy użytkownicy dołączają do systemu
- **Definicja relacji**: Ustanawia relację jeden-do-wielu z modelem Files

**Metody obsługi haseł:**

```python
@property
def password(self):
    raise AttributeError('Nie można odczytać hasła!')

@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)

def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
```

Te metody zapewniają, że:
- Surowe hasła nigdy nie są przechowywane ani ujawniane
- Haszowanie hasła jest automatycznie stosowane podczas ustawiania hasła
- Weryfikacja hasła jest obsługiwana bezpiecznie

### 3.2 Model Files

Model Files zarządza metadanymi plików i odniesieniami do przechowywania:

```python
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(100), nullable=False)
    stored_filename = db.Column(db.String(36), nullable=False, unique=True)
    size = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
```

**Kluczowe cechy modelu Files:**

- **System podwójnych nazw plików**: Utrzymuje zarówno oryginalną nazwę pliku, jak i bezpieczną nazwę przechowywaną opartą na UUID
- **Śledzenie rozmiaru**: Zapisuje rozmiar pliku w MB dla statystyk użytkownika
- **Ograniczenie klucza obcego**: Łączy każdy plik z jego właścicielem poprzez user_id
- **Znacznik czasu przesyłania**: Zapisuje, kiedy każdy plik został przesłany
- **Unikalne nazwy przechowywania**: Wymusza unikalne nazwy przechowywanych plików, aby zapobiec kolizjom

### 3.3 Relacje w Bazie Danych

Baza danych implementuje starannie zaprojektowaną strukturę relacji:

- **Relacja jeden-do-wielu**: Każdy użytkownik może mieć wiele plików, ale każdy plik należy do dokładnie jednego użytkownika
- **Nawigacja dwukierunkowa**: 
  - Od użytkownika do plików: `user.files` zwraca wszystkie pliki dla użytkownika
  - Od pliku do użytkownika: `file.user` zwraca właściciela pliku
- **Operacje kaskadowe**: Gdy użytkownik jest usuwany, wszystkie powiązane pliki są automatycznie usuwane
- **Leniwe ładowanie**: Pliki są ładowane tylko na wyraźne żądanie, poprawiając wydajność

### 3.4 Migracje Bazy Danych

Aplikacja implementuje wersjonowanie bazy danych przez Flask-Migrate i Alembic:

1. **Początkowa migracja** (`a611435940cc_initial_migration.py`): 
   - Tworzy tabelę Users
   - Dodaje kolumnę password_hash i inne pola użytkownika
   - Ustawia ograniczenia i indeksy

2. **Druga migracja** (`b074a4b2988e_files_added.py`): 
   - Tworzy tabelę Files
   - Ustanawia relacje klucza obcego
   - Ustawia ograniczenia dla przechowywania plików

Ten system migracji pozwala na:
- Śledzenie zmian schematu bazy danych w czasie
- Stosowanie przyrostowych aktualizacji bazy danych
- Wycofywanie zmian w razie potrzeby
- Utrzymanie spójnego stanu bazy danych w różnych środowiskach

## 4. Funkcje Bezpieczeństwa

Aplikacja implementuje kompleksowe środki bezpieczeństwa na wszystkich warstwach:

### 4.1 Bezpieczeństwo Autentykacji

#### 4.1.1 Haszowanie Haseł

Aplikacja wykorzystuje funkcje kryptograficzne Werkzeug do bezpiecznego zarządzania hasłami:

```python
@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)

def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
```

Ta implementacja zapewnia:
- Hasła nigdy nie są przechowywane w formie zwykłego tekstu
- Hashe haseł używają bezpiecznych algorytmów
- Weryfikacja hasła jest odporna na ataki czasowe
- Oryginalne hasła nie mogą być odzyskane z haszy

#### 4.1.2 Silna Polityka Haseł

Aplikacja wymusza rygorystyczną politykę haseł, aby zapobiec słabym danym uwierzytelniającym:

```python
re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{15,}$', password)
```

To wyrażenie regularne wymusza:
- Minimalną długość 15 znaków
- Co najmniej jedną małą literę
- Co najmniej jedną wielką literę
- Co najmniej jedną cyfrę
- Co najmniej jeden znak specjalny (!@#$%^&*)

Te wymagania znacząco redukują podatność na ataki brute force i słownikowe.

#### 4.1.3 Zarządzanie Sesjami

Aplikacja implementuje bezpieczną obsługę sesji przez Flask-Login:

- **Tworzenie sesji**: Tylko po pomyślnej autentykacji
- **Ochrona sesji**: Trasy chronione dekoratorem `@login_required`
- **Weryfikacja sesji**: Automatyczne sprawdzanie statusu autentykacji użytkownika
- **Zakończenie sesji**: Właściwa funkcjonalność wylogowania

Przykład ochrony trasy:
```python
@app.route('/dashboard')
@login_required
def dashboard():
    # Kod chronionej trasy
```

#### 4.1.4 Ochrona Formularzy

Wszystkie formularze w aplikacji są chronione przed atakami CSRF:

- **Tokeny CSRF**: Generowane automatycznie przez Flask-WTF
- **Walidacja tokenów**: Wymagana dla wszystkich żądań POST
- **Walidatory formularzy**: Zapewniają integralność danych i zapobiegają atakom iniekcji

### 4.2 Bezpieczeństwo Plików

#### 4.2.1 Bezpieczne Przechowywanie Plików

Aplikacja implementuje liczne zabezpieczenia dla przechowywania plików:

```python
stored_filename = str(uuid.uuid4())
file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
```

To podejście zapewnia:
- Pliki są przechowywane z losowymi nazwami UUID (36-znakowe stringi)
- Oryginalne nazwy plików są zachowywane w bazie danych, ale nie są używane do przechowywania
- Ataki typu path traversal są uniemożliwione (brak danych wejściowych użytkownika w ścieżkach plików)
- Kolizje nazw plików są praktycznie niemożliwe

#### 4.2.2 Kontrola Dostępu

Aplikacja implementuje ścisłą kontrolę dostępu dla operacji na plikach:

```python
file = Files.query.filter_by(id=file_id, user_id=current_user.id).first_or_404()
```

Ten wzorzec jest używany przed każdą operacją na pliku, aby zapewnić:
- Użytkownicy mogą uzyskać dostęp tylko do swoich własnych plików
- Nieautoryzowane próby dostępu zwracają błędy 404
- Brak ujawniania informacji o plikach innych użytkowników
- Weryfikacja właściciela odbywa się przed każdą operacją na pliku

#### 4.2.3 Ograniczenia Typów Plików

Dla operacji na plikach tekstowych aplikacja implementuje walidację typu zawartości:

```python
text_extensions = ['.txt', '.md', '.log', '.csv']
file_extension = os.path.splitext(file.original_filename)[1].lower()

if file_extension not in text_extensions:
    return jsonify({'error': 'Edycja tego pliku jest niemożliwa!'}), 400
```

To zapobiega:
- Uszkodzeniu plików binarnych podczas operacji edycji
- Potencjalnym lukom w zabezpieczeniach wynikającym z edycji plików wykonywalnych
- Błędom użytkownika prowadzącym do utraty danych

### 4.3 Bezpieczeństwo Webowe

#### 4.3.1 Obsługa Błędów

Aplikacja implementuje kompleksową obsługę błędów:

- **Niestandardowe strony błędów**: Dla błędów 401, 404 i 500
- **Przechwytywanie wyjątków**: Wszystkie operacje bazodanowe opakowane w try/except
- **Eleganckie odzyskiwanie po błędach**: Sesje wycofywane w przypadku niepowodzenia
- **Informacje zwrotne dla użytkownika**: Odpowiednie komunikaty flash dla błędów
- **Logowanie błędów**: Logowanie konsoli wyjątków z kontekstem

Przykład obsługi błędów:
```python
try:
    db.session.add(new_file)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    flash('Wystąpił błąd w przesyłaniu pliku!', 'danger')
    print(f'Błąd w trakcie przesyłania pliku od użytkownika {current_user.login} error message: {str(e)}')
```

#### 4.3.2 Walidacja Danych Wejściowych

Aplikacja implementuje wiele warstw walidacji danych wejściowych:

- **Walidacja formularzy**: Walidatory WTForms dla pól formularzy
- **Walidacja po stronie serwera**: Dodatkowe sprawdzenia w obsłudze tras
- **Walidacja wyrażeń regularnych**: Dla krytycznych pól jak hasła
- **Ograniczenia bazodanowe**: Ograniczenia unikalności i null

#### 4.3.3 Bezpieczna Konfiguracja

Aplikacja implementuje praktyki bezpiecznej konfiguracji:

- **Klucz tajny**: Do szyfrowania sesji i ochrony CSRF
- **Konfiguracja folderu przesyłania**: Zapewnia istnienie folderu
- **URI bazy danych**: Właściwie skonfigurowane dla aplikacji

Uwaga: W środowisku produkcyjnym, klucz tajny powinien być przeniesiony do zmiennych środowiskowych:

```python
app.config['SECRET_KEY']="Super klucz tajnosci" #jest hardcoded ale gdyby bylo to w srodowisku produkcyjnym, wyrzucilbym na zmienna env
```

## 5. Endpointy API

Aplikacja implementuje zasady RESTful API i dokumentuje wszystkie endpointy za pomocą Swagger/Flasgger. Każdy endpoint ma kompleksową dokumentację, w tym parametry, kody odpowiedzi i wymagania dotyczące autentykacji.

### 5.1 Endpointy Autentykacji

| Endpoint | Metoda | Funkcja | Opis | Parametry | Kody Odpowiedzi |
|----------|--------|---------|------|-----------|----------------|
| `/login` | GET/POST | `login()` | Autentykacja użytkownika | login_or_email, password | 302 (przekierowanie) |
| `/register` | GET/POST | `register()` | Rejestracja nowego użytkownika | login, email, password_hash | 302 (przekierowanie) |  
| `/logout` | GET | `logout()` | Wylogowanie użytkownika | Brak | 302 (przekierowanie) |

### 5.2 Endpointy Zarządzania Użytkownikiem

| Endpoint | Metoda | Funkcja | Opis | Parametry | Kody Odpowiedzi |
|----------|--------|---------|------|-----------|----------------|
| `/user` | GET | `user_panel()` | Informacje o profilu użytkownika | Brak | 200 |
| `/update_username` | POST | `update_username()` | Zmiana nazwy użytkownika | currentPassword, newUsername, confirmNewUsername | 302 (przekierowanie) |
| `/update_email` | POST | `update_email()` | Zmiana adresu email | currentPassword, newEmail, confirmNewEmail | 302 (przekierowanie) |
| `/update_password` | POST | `update_password()` | Zmiana hasła | currentPassword, newPassword, confirmPassword | 302 (przekierowanie) |

### 5.3 Endpointy Zarządzania Plikami

| Endpoint | Metoda | Funkcja | Opis | Parametry | Kody Odpowiedzi |
|----------|--------|---------|------|-----------|----------------|
| `/dashboard` | GET | `dashboard()` | Lista plików użytkownika | Brak | 200 |
| `/upload` | POST | `upload_file()` | Przesyłanie nowego pliku | file (multipart/form-data) | 302 (przekierowanie) |
| `/download/<file_id>` | GET | `download_file()` | Pobieranie pliku | file_id (ścieżka) | 200, 404 |
| `/delete/<file_id>` | POST | `delete_file()` | Usuwanie pliku | file_id (ścieżka) | 302 (przekierowanie), 404 |
| `/edit/<file_id>` | GET/POST | `edit_file()` | Podgląd/edycja pliku tekstowego | file_id (ścieżka), file_name, file_content | 200, 302, 400, 404, 500 |
| `/preview/<file_id>` | GET | `preview_file()` | Podgląd pliku tekstowego | file_id (ścieżka) | 200, 400, 404, 500 |

### 5.4 Endpointy Obsługi Błędów

| Endpoint | Funkcja | Opis | Kody Odpowiedzi |
|----------|---------|------|----------------|
| błąd 401 | `unauthorized()` | Wymagana autentykacja | 401, 302 (przekierowanie) |
| błąd 404 | `not_found()` | Zasób nie znaleziony | 404 |
| błąd 500 | `internal_server_error()` | Błąd serwera | 500 |

## 6. Technologie i Frameworki

### 6.1 Technologie Backendowe

- **Flask (3.1.0)**: Główny framework webowy
- **SQLAlchemy (2.0.39)**: Mapper Obiektowo-Relacyjny
- **Flask-Login (0.6.3)**: Zarządzanie autentykacją
- **Flask-Migrate (4.1.0)**: Migracje bazy danych
- **Flask-WTF (1.2.2)**: Obsługa formularzy
- **Werkzeug (3.1.3)**: Narzędzia HTTP i WSGI
- **Flasgger (0.9.7.1)**: Dokumentacja API

### 6.2 Technologie Frontendowe

- **Bootstrap 5**: Framework UI
- **JavaScript**: Interaktywność po stronie klienta
- **Jinja2 (3.1.6)**: Silnik szablonów
- **HTML5/CSS3**: Podstawowe znaczniki i stylowanie

### 6.3 Baza Danych

- **SQLite**: Przechowywanie bazy danych
- **Alembic**: Migracje bazy danych

## 7. Funkcje Aplikacji

### 7.1 Autentykacja Użytkowników

Aplikacja implementuje kompleksowy system autentykacji:

- **Rejestracja Użytkownika:**
  - Bezpieczny formularz z walidacją
  - Weryfikacja unikalności emaila
  - Silne wymagania dotyczące hasła
  - Informacje zwrotne o sukcesie/błędzie
  
- **Logowanie Użytkownika:**
  - Logowanie za pomocą nazwy użytkownika lub emaila
  - Weryfikacja hasła
  - Tworzenie sesji
  - Informacje zwrotne o sukcesie/błędzie
  
- **Wymuszanie Siły Hasła:**
  - Minimum 15 znaków
  - Wymaganie mieszanych wielkości liter
  - Wymaganie cyfr
  - Wymaganie znaków specjalnych
  
- **Zarządzanie Sesjami:**
  - Bezpieczne sesje oparte na ciasteczkach
  - Chronione trasy
  - Zakończenie sesji przy wylogowaniu
  - Identyfikacja użytkownika

### 7.2 Zarządzanie Plikami

Aplikacja zapewnia kompleksowe możliwości zarządzania plikami:

- **Przesyłanie Plików:**
  - Bezpieczna obsługa plików
  - Nazwy przechowywania oparte na UUID
  - Obliczanie i śledzenie rozmiaru
  - Tworzenie rekordów w bazie danych
  
- **Pobieranie Plików:**
  - Weryfikacja właściciela
  - Zachowanie oryginalnej nazwy pliku
  - Właściwa obsługa typów MIME
  - Dyspozycja załącznika
  
- **Podgląd Plików Tekstowych:**
  - Weryfikacja typu zawartości
  - Wyświetlanie tylko do odczytu
  - Ładowanie oparte na AJAX
  - Obsługa błędów
  
- **Edycja Plików Tekstowych:**
  - Weryfikacja typu zawartości
  - Edycja nazwy pliku
  - Edycja zawartości
  - Przeliczanie rozmiaru
  
- **Usuwanie Plików:**
  - Weryfikacja właściciela
  - Czyszczenie systemu plików
  - Usuwanie rekordu z bazy danych
  - Dialog potwierdzenia
  
- **Statystyki Przechowywania:**
  - Śledzenie liczby plików
  - Obliczanie rozmiaru całkowitego
  - Formatowanie rozmiaru czytelne dla człowieka
  - Izolacja dla poszczególnych użytkowników

### 7.3 Zarządzanie Profilem Użytkownika

Aplikacja implementuje kompleksowe zarządzanie profilem:

- **Informacje Profilowe:**
  - Wyświetlanie nazwy użytkownika
  - Wyświetlanie emaila
  - Statystyki plików
  - Wykorzystanie przestrzeni
  
- **Zmiana Nazwy Użytkownika:**
  - Weryfikacja aktualnego hasła
  - Pole potwierdzenia
  - Ograniczenia długości
  - Informacje zwrotne o sukcesie/błędzie
  
- **Zmiana Emaila:**
  - Weryfikacja aktualnego hasła
  - Pole potwierdzenia
  - Weryfikacja unikalności
  - Informacje zwrotne o sukcesie/błędzie
  
- **Zmiana Hasła:**
  - Weryfikacja aktualnego hasła
  - Pole potwierdzenia
  - Silna polityka haseł
  - Informacje zwrotne o sukcesie/błędzie

## 8. Instalacja i Konfiguracja

### 8.1 Wymagania Wstępne

- **Python 3.8+**
- **pip**: Menedżer pakietów Python
- **SQLite**: Dołączony do Pythona
- **Wirtualne Środowisko**: Zalecane dla izolacji zależności

### 8.2 Kroki Instalacji

1. Klonowanie repozytorium:
   ```bash
   git clone https://github.com/AAAAAAAAA9a/IO2_Project.git
   cd IO-2-Project
   ```

2. Tworzenie i aktywacja wirtualnego środowiska:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # W Windows: venv\Scripts\activate
   ```

3. Instalacja zależności:
   ```bash
   pip install -r requirements.txt
   ```

### 8.3 Inicjalizacja Bazy Danych

Uruchom skrypt inicjalizacji bazy danych:
```bash
python database_init.py
```

### 8.4 Uruchamianie Aplikacji

Uruchom serwer deweloperski Flask:
```bash
python app.py
```

Uzyskaj dostęp do aplikacji pod adresem: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### 8.5 Dokumentacja API

Uzyskaj dostęp do dokumentacji API Swagger pod adresem: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)