# Flask File Management Application

## 1. Executive Summary

The **Flask File Management Application** provides a secure and intuitive platform for managing personal files through a web interface. It implements robust authentication, comprehensive file operations, and follows the Model-View-Controller (MVC) architectural pattern.

### Primary Objectives
- Secure file storage and management
- Industry-standard user authentication
- Comprehensive file operations (upload, download, preview, edit, delete)
- Demonstration of MVC architecture with Flask
- Showcase of modern web development practices

## 2. Application Architecture

### 2.1 Overall Structure

The application adheres strictly to the Model-View-Controller (MVC) architecture pattern, with clear separation of concerns:

- **Models** (`models.py`): Handle database schema, business logic, and relationships
  - Implement proper data validation and relationship management
  - Handle password hashing through Werkzeug security utilities
  - Manage user-file relationships through SQLAlchemy ORM

- **Views** (`templates/`): Contain HTML templates rendered to the client
  - Use Jinja2 templating engine for dynamic content
  - Implement template inheritance for consistent layout (base.html)
  - Separate templates by functionality (login.html, dashboard.html, etc.)
  - Utilize Bootstrap 5 for responsive design

- **Controllers** (`app.py`): Manage route handlers and application logic
  - Implement authentication workflows
  - Process file operations
  - Handle error conditions
  - Provide API documentation through Swagger

### 2.2 Key Flask Extensions

The application leverages several key Flask extensions to enhance its functionality:

- **Flask-SQLAlchemy**: Object-Relational Mapping for database interactions
  - Simplifies database queries and relationship management
  - Provides transaction management for data integrity

- **Flask-Login**: Comprehensive user authentication management
  - Handles user sessions
  - Provides protection for authenticated routes
  - Manages user identity

- **Flask-Migrate**: Database schema versioning through Alembic
  - Allows for structured database migrations
  - Maintains database schema history

- **Flask-WTF**: Form handling and validation
  - Provides CSRF protection
  - Implements form validation
  - Simplifies form rendering

- **Flasgger**: Swagger-based API documentation
  - Auto-generates API documentation
  - Provides interactive testing interface
  - Documents API endpoints and parameters

### 2.3 Component Architecture and Data Flow

The application's architecture follows a layered approach with distinct components that interact through well-defined interfaces:

```
+-------------------------+        +----------------------+
|  Web Interface Layer    |        |  API Documentation   |
| (Templates & JavaScript)|<------>| (Swagger/Flasgger)   |
+-------------------------+        +----------------------+
            ^
            |
            v
+-------------------------+        +----------------------+
|  Application Layer      |<------>|  Authentication      |
| (Routes & Controllers)  |        | (Flask-Login)        |
+-------------------------+        +----------------------+
            ^
            |
            v
+-------------------------+        +----------------------+
|  Data Access Layer      |<------>|  File Storage System |
| (SQLAlchemy Models)     |        | (Local Filesystem)   |
+-------------------------+        +----------------------+
            ^
            |
            v
+-------------------------+
|  Database               |
| (SQLite)                |
+-------------------------+
```

#### Key Data Flows

1. **Authentication Flow:**
   - User submits credentials through the login form
   - Application validates credentials against the database
   - On success, Flask-Login creates a user session
   - User is redirected to the dashboard

2. **File Upload Flow:**
   - User selects a file through the upload form
   - File is processed by the server (validation, size calculation)
   - A unique UUID is generated for secure storage
   - File is saved to the filesystem with the UUID as filename
   - File metadata is stored in the database with reference to the user

3. **File Operations Flow:**
   - User requests file operation (download, preview, edit, delete)
   - Application verifies user's ownership of the file
   - Requested operation is performed
   - Response is sent back to the user

## 3. Database Schema

The application employs SQLite with SQLAlchemy ORM for data persistence. The database schema is designed for security, performance, and data integrity.

### 3.1 Users Model

The Users model handles user authentication and profile management:

```python
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    files = db.relationship('Files', backref='user', lazy=True)
```

**Key features of the Users model:**

- **UserMixin integration**: Inherits from Flask-Login's UserMixin to provide required authentication methods
- **Secure password handling**: Implements password hashing with property decorators to prevent direct access
- **Email uniqueness**: Enforces unique email addresses to prevent duplicate accounts
- **Registration timestamp**: Records when users join the system
- **Relationship definition**: Establishes one-to-many relationship with the Files model

**Password handling methods:**

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

These methods ensure that:
- Raw passwords are never stored or exposed
- Password hashing is automatically applied when setting a password
- Password verification is handled securely

### 3.2 Files Model

The Files model manages file metadata and storage references:

```python
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(100), nullable=False)
    stored_filename = db.Column(db.String(36), nullable=False, unique=True)
    size = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
```

**Key features of the Files model:**

- **Dual filename system**: Maintains both the original filename and a secure UUID-based stored filename
- **Size tracking**: Records file size in MB for user statistics
- **Foreign key constraint**: Links each file to its owner through user_id
- **Upload timestamp**: Records when each file was uploaded
- **Unique storage names**: Enforces unique stored filenames to prevent collisions

### 3.3 Database Relationships

The database implements a carefully designed relationship structure:

- **One-to-many relationship**: Each user can have multiple files, but each file belongs to exactly one user
- **Bidirectional navigation**: 
  - From user to files: `user.files` returns all files for a user
  - From file to user: `file.user` returns the owner of a file
- **Cascading operations**: When a user is deleted, all associated files are automatically deleted
- **Lazy loading**: Files are loaded only when explicitly requested, improving performance

### 3.4 Database Migrations

The application implements database versioning through Flask-Migrate and Alembic:

1. **Initial migration** (`a611435940cc_initial_migration.py`): 
   - Creates the Users table
   - Adds password_hash column and other user fields
   - Sets up constraints and indexes

2. **Second migration** (`b074a4b2988e_files_added.py`): 
   - Creates the Files table
   - Establishes foreign key relationships
   - Sets up constraints for file storage

This migration system allows for:
- Tracking database schema changes over time
- Applying incremental updates to the database
- Rolling back changes if necessary
- Maintaining a consistent database state across environments

## 4. Security Features

The application implements comprehensive security measures across all layers:

### 4.1 Authentication Security

#### 4.1.1 Password Hashing

The application uses Werkzeug's cryptographic functions for secure password management:

```python
@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)

def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
```

This implementation ensures:
- Passwords are never stored in plaintext
- Password hashes use secure algorithms
- Password verification is timing-attack resistant
- Original passwords cannot be recovered from hashes

#### 4.1.2 Strong Password Policy

The application enforces a rigorous password policy to prevent weak credentials:

```python
re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{15,}$', password)
```

This regular expression enforces:
- Minimum 15 characters length
- At least one lowercase letter
- At least one uppercase letter
- At least one numeric digit
- At least one special character (!@#$%^&*)

These requirements significantly reduce vulnerability to brute force and dictionary attacks.

#### 4.1.3 Session Management

The application implements secure session handling through Flask-Login:

- **Session creation**: Only after successful authentication
- **Session protection**: Routes protected with `@login_required` decorator
- **Session verification**: Automatic checking of user authentication status
- **Session termination**: Proper logout functionality

Example route protection:
```python
@app.route('/dashboard')
@login_required
def dashboard():
    # Protected route code
```

#### 4.1.4 Form Protection

All forms in the application are protected against CSRF attacks:

- **CSRF tokens**: Generated automatically by Flask-WTF
- **Token validation**: Required for all POST requests
- **Form validators**: Ensure data integrity and prevent injection attacks

### 4.2 File Security

#### 4.2.1 Secure File Storage

The application implements numerous protections for file storage:

```python
stored_filename = str(uuid.uuid4())
file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
```

This approach ensures:
- Files are stored with random UUID names (36-character strings)
- Original filenames are preserved in the database but not used for storage
- Path traversal attacks are prevented (no user input in file paths)
- File name collisions are virtually impossible

#### 4.2.2 Access Control

The application implements strict access control for file operations:

```python
file = Files.query.filter_by(id=file_id, user_id=current_user.id).first_or_404()
```

This pattern is used before every file operation to ensure:
- Users can only access their own files
- Unauthorized access attempts return 404 errors
- No information disclosure about other users' files
- Owner verification occurs before any file operation

#### 4.2.3 File Type Restrictions

For text file operations, the application implements content type validation:

```python
text_extensions = ['.txt', '.md', '.log', '.csv']
file_extension = os.path.splitext(file.original_filename)[1].lower()

if file_extension not in text_extensions:
    return jsonify({'error': 'Edycja tego pliku jest niemożliwa!'}), 400
```

This prevents:
- Binary file corruption during edit operations
- Potential security vulnerabilities from editing executable files
- User errors leading to data loss

### 4.3 Web Security

#### 4.3.1 Error Handling

The application implements comprehensive error handling:

- **Custom error pages**: For 401, 404, and 500 errors
- **Exception catching**: All database operations wrapped in try/except
- **Graceful error recovery**: Sessions rolled back on failure
- **User feedback**: Appropriate flash messages for errors
- **Error logging**: Console logging of exceptions with context

Example error handling:
```python
try:
    db.session.add(new_file)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    flash('Wystąpił błąd w przesyłaniu pliku!', 'danger')
    print(f'Błąd w trakcie przesyłania pliku od użytkownika {current_user.login} error message: {str(e)}')
```

#### 4.3.2 Input Validation

The application implements multiple layers of input validation:

- **Form validation**: WTForms validators for form fields
- **Server-side validation**: Additional checks in route handlers
- **Regular expression validation**: For critical fields like passwords
- **Database constraints**: Unique constraints and nullability checks

#### 4.3.3 Secure Configuration

The application implements secure configuration practices:

- **Secret key**: For session encryption and CSRF protection
- **Upload folder configuration**: Ensures folder exists
- **Database URI**: Properly configured for the application

Note: In a production environment, the secret key should be moved to environment variables:

```python
app.config['SECRET_KEY']="Super klucz tajnosci" #jest hardcoded ale gdyby bylo to w srodowisku produkcyjnym, wyrzucilbym na zmienna env
```

## 5. API Endpoints

The application implements RESTful API principles and documents all endpoints with Swagger/Flasgger. Each endpoint has comprehensive documentation including parameters, responses, and authentication requirements.

### 5.1 Authentication Endpoints

| Endpoint | Method | Function | Description | Parameters | Response Codes |
|----------|--------|----------|-------------|------------|----------------|
| `/login` | GET/POST | `login()` | User authentication | login_or_email, password | 302 (redirect) |
| `/register` | GET/POST | `register()` | New user registration | login, email, password_hash | 302 (redirect) |  
| `/logout` | GET | `logout()` | User logout | None | 302 (redirect) |

### 5.2 User Management Endpoints

| Endpoint | Method | Function | Description | Parameters | Response Codes |
|----------|--------|----------|-------------|------------|----------------|
| `/user` | GET | `user_panel()` | User profile information | None | 200 |
| `/update_username` | POST | `update_username()` | Change username | currentPassword, newUsername, confirmNewUsername | 302 (redirect) |
| `/update_email` | POST | `update_email()` | Change email address | currentPassword, newEmail, confirmNewEmail | 302 (redirect) |
| `/update_password` | POST | `update_password()` | Change password | currentPassword, newPassword, confirmPassword | 302 (redirect) |

### 5.3 File Management Endpoints

| Endpoint | Method | Function | Description | Parameters | Response Codes |
|----------|--------|----------|-------------|------------|----------------|
| `/dashboard` | GET | `dashboard()` | List user's files | None | 200 |
| `/upload` | POST | `upload_file()` | Upload new file | file (multipart/form-data) | 302 (redirect) |
| `/download/<file_id>` | GET | `download_file()` | Download file | file_id (path) | 200, 404 |
| `/delete/<file_id>` | POST | `delete_file()` | Delete file | file_id (path) | 302 (redirect), 404 |
| `/edit/<file_id>` | GET/POST | `edit_file()` | View/edit text file | file_id (path), file_name, file_content | 200, 302, 400, 404, 500 |
| `/preview/<file_id>` | GET | `preview_file()` | Preview text file | file_id (path) | 200, 400, 404, 500 |

### 5.4 Error Handling Endpoints

| Endpoint | Function | Description | Response Codes |
|----------|----------|-------------|----------------|
| 401 error | `unauthorized()` | Authentication required | 401, 302 (redirect) |
| 404 error | `not_found()` | Resource not found | 404 |
| 500 error | `internal_server_error()` | Server error | 500 |

## 6. Technologies and Frameworks

### 6.1 Backend Technologies

- **Flask (3.1.0)**: Core web framework
- **SQLAlchemy (2.0.39)**: Object-Relational Mapper
- **Flask-Login (0.6.3)**: Authentication management
- **Flask-Migrate (4.1.0)**: Database migrations
- **Flask-WTF (1.2.2)**: Form handling
- **Werkzeug (3.1.3)**: HTTP and WSGI utilities
- **Flasgger (0.9.7.1)**: API documentation

### 6.2 Frontend Technologies

- **Bootstrap 5**: UI framework
- **JavaScript**: Client-side interactivity
- **Jinja2 (3.1.6)**: Template engine
- **HTML5/CSS3**: Base markup and styling

### 6.3 Database

- **SQLite**: Database storage
- **Alembic**: Database migrations

## 7. Application Features

### 7.1 User Authentication

The application implements a comprehensive authentication system:

- **User Registration:**
  - Secure form with validation
  - Email uniqueness verification
  - Strong password requirements
  - Success/error feedback
  
- **User Login:**
  - Login with username or email
  - Password verification
  - Session creation
  - Success/error feedback
  
- **Password Strength Enforcement:**
  - Minimum 15 characters
  - Mixed case requirement
  - Digit requirement
  - Special character requirement
  
- **Session Management:**
  - Secure cookie-based sessions
  - Protected routes
  - Session termination on logout
  - User identification

### 7.2 File Management

The application provides comprehensive file management capabilities:

- **File Upload:**
  - Secure file handling
  - UUID-based storage names
  - Size calculation and tracking
  - Database record creation
  
- **File Downloading:**
  - Owner verification
  - Original filename preservation
  - Proper MIME type handling
  - Attachment disposition
  
- **Text File Preview:**
  - Content type verification
  - Read-only display
  - AJAX-based loading
  - Error handling
  
- **Text File Editing:**
  - Content type verification
  - File name editing
  - Content editing
  - Size recalculation
  
- **File Deletion:**
  - Owner verification
  - Filesystem cleanup
  - Database record removal
  - Confirmation dialog
  
- **Storage Statistics:**
  - File count tracking
  - Total size calculation
  - Human-readable size formatting
  - Per-user isolation

### 7.3 User Profile Management

The application implements comprehensive profile management:

- **Profile Information:**
  - Username display
  - Email display
  - File statistics
  - Storage usage
  
- **Change Username:**
  - Current password verification
  - Confirmation field
  - Length constraints
  - Success/error feedback
  
- **Change Email:**
  - Current password verification
  - Confirmation field
  - Uniqueness verification
  - Success/error feedback
  
- **Change Password:**
  - Current password verification
  - Confirmation field
  - Strong password policy
  - Success/error feedback

## 8. Setup and Installation

### 8.1 Prerequisites

- **Python 3.8+**
- **pip**: Python package manager
- **SQLite**: Included with Python
- **Virtual Environment**: Recommended for dependency isolation

### 8.2 Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/AAAAAAAAA9a/IO2_Project.git
   cd IO-2-Project
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 8.3 Database Initialization

Run the database initialization script:
```bash
python database_init.py
```

### 8.4 Running the Application

Start the Flask development server:
```bash
python app.py
```

Access the app at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### 8.5 API Documentation

Access the Swagger API documentation at: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)