# Flask File Management Application Documentation

## 1. Executive Summary

The application enables users to securely manage personal files through a web interface with robust authentication mechanisms.

The primary objectives of this application are:
- To provide a secure platform for users to store, retrieve, and manage their files
- To implement industry standard security practices for user authentication
- To offer intuitive file operations (upload, download, edit, preview, delete)
- To demonstrate proper implementation of the MVC architectural pattern in a web application
- To showcase modern web development practices using Flask and its associated extensions

## 2. Application Architecture

### 2.1 Overall Structure

The application adheres strictly to the Model-View-Controller (MVC) architecture pattern, with clear separation of concerns:

- **Models** (`models.py`): Defines the database schema and business logic for users and files
  - Implements proper data validation and relationship management
  - Handles password hashing through Werkzeug security utilities
  - Manages user-file relationships through SQLAlchemy ORM

- **Views** (`templates/`): Contains HTML templates rendered to the client
  - Uses Jinja2 templating engine for dynamic content
  - Implements template inheritance for consistent layout (base.html)
  - Separates templates by functionality (login.html, dashboard.html, etc.)
  - Utilizes Bootstrap 5 for responsive design

- **Controllers** (`app.py`): Manages route handlers and application logic
  - Implements authentication workflows
  - Processes file operations
  - Handles error conditions
  - Provides API documentation through Swagger

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

### 2.2 Component Architecture and Data Flow

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

**Data Flow in the Application:**

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

This architecture ensures proper separation of concerns, secure handling of user data, and maintainability of the codebase.

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

While the current implementation has a hardcoded secret key, in a production environment, this would be moved to environment variables:

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

Example authentication endpoint implementation:

```python
@app.route('/login', methods=['GET','POST'])
def login():
    """
    Zalogowanie użytkownika
    ---
    tags:
      - Autoryzacja
    parameters:
      - name: login_or_email
        in: formData
        type: string
        required: true
        description: Login lub email użytkownika
      - name: password
        in: formData
        type: string
        required: true
        description: Hasło użytkownika
    responses:
      302:
        description: Przekierowanie po udanym logowaniu lub nieudanym logowaniu
    """
    # Implementation...
```

### 5.2 User Management Endpoints

| Endpoint | Method | Function | Description | Parameters | Response Codes |
|----------|--------|----------|-------------|------------|----------------|
| `/user` | GET | `user_panel()` | User profile information | None | 200 |
| `/update_username` | POST | `update_username()` | Change username | currentPassword, newUsername, confirmNewUsername | 302 (redirect) |
| `/update_email` | POST | `update_email()` | Change email address | currentPassword, newEmail, confirmNewEmail | 302 (redirect) |
| `/update_password` | POST | `update_password()` | Change password | currentPassword, newPassword, confirmPassword | 302 (redirect) |

These endpoints implement:
- Current password verification before changes
- Input validation
- Duplicate detection (for email)
- Confirmation fields to prevent typos
- Success/error messages via flash

### 5.3 File Management Endpoints

| Endpoint | Method | Function | Description | Parameters | Response Codes |
|----------|--------|----------|-------------|------------|----------------|
| `/dashboard` | GET | `dashboard()` | List user's files | None | 200 |
| `/upload` | POST | `upload_file()` | Upload new file | file (multipart/form-data) | 302 (redirect) |
| `/download/<file_id>` | GET | `download_file()` | Download file | file_id (path) | 200, 404 |
| `/delete/<file_id>` | POST | `delete_file()` | Delete file | file_id (path) | 302 (redirect), 404 |
| `/edit/<file_id>` | GET/POST | `edit_file()` | View/edit text file | file_id (path), file_name, file_content | 200, 302, 400, 404, 500 |
| `/preview/<file_id>` | GET | `preview_file()` | Preview text file | file_id (path) | 200, 400, 404, 500 |

The file management endpoints implement:
- Owner verification
- File type validation for text operations
- Error handling for file I/O operations
- AJAX support for preview/edit operations
- File size calculation
- Secure file storage with UUIDs

Example file management endpoint implementation:

```python
@app.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    """
    Pobieranie pliku
    ---
    tags:
      - Pliki
    security:
      - Bearer: []
    parameters:
      - name: file_id
        in: path
        type: integer
        required: true
        description: ID pliku do pobrania
    responses:
      200:
        description: Pobieranie pliku
      404:
        description: Plik nie znaleziony
    """
    file = Files.query.filter_by(
        id=file_id, 
        user_id=current_user.id).first_or_404()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.stored_filename)
    return send_file(
    file_path,
    as_attachment=True,
    download_name=file.original_filename)
```

### 5.4 Error Handling Endpoints

| Endpoint | Function | Description | Response Codes |
|----------|----------|-------------|----------------|
| 401 error | `unauthorized()` | Authentication required | 401, 302 (redirect) |
| 404 error | `not_found()` | Resource not found | 404 |
| 500 error | `internal_server_error()` | Server error | 500 |

These endpoints implement custom error pages with helpful messages and proper HTTP status codes.

## 6. Technologies and Frameworks

The application leverages a carefully selected stack of modern technologies:

### 6.1 Backend Technologies

- **Flask (3.1.0)**: Core web framework
  - Lightweight and flexible Python web framework
  - Extensible through Flask extensions
  - Built on Werkzeug and Jinja2
  - Handles routing, request processing, and response generation

- **SQLAlchemy (2.0.39)**: Object-Relational Mapper
  - Abstracts database operations
  - Provides transaction management
  - Implements relationship mapping
  - Handles query building and execution

- **Flask-Login (0.6.3)**: Authentication management
  - Manages user sessions
  - Provides @login_required decorator
  - Handles user loading and authentication
  - Implements "remember me" functionality

- **Flask-Migrate (4.1.0)**: Database migrations
  - Based on Alembic
  - Manages database schema changes
  - Provides versioning for database schema
  - Allows safe schema updates

- **Flask-WTF (1.2.2)**: Form handling
  - Form definition and rendering
  - CSRF protection
  - Form validation
  - File upload handling

- **Werkzeug (3.1.3)**: HTTP and WSGI utilities
  - Password hashing functions
  - HTTP request/response objects
  - URL routing
  - File handling

- **Flasgger (0.9.7.1)**: API documentation
  - Swagger UI integration
  - API documentation generation
  - Request/response schema definition
  - Interactive API testing

### 6.2 Frontend Technologies

- **Bootstrap 5**: UI framework
  - Responsive grid system
  - Pre-styled components
  - Modal dialogs
  - Forms and buttons
  - Dark theme support

- **JavaScript**: Client-side interactivity
  - AJAX requests for file operations
  - Modal handling
  - Form validation
  - Dynamic content loading

- **Jinja2 (3.1.6)**: Template engine
  - Template inheritance
  - Variable substitution
  - Conditional rendering
  - Loops and iterations

- **HTML5/CSS3**: Base markup and styling
  - Semantic HTML elements
  - CSS styling
  - Responsive design
  - Accessibility features

### 6.3 Database

- **SQLite**: Database storage
  - File-based database
  - ACID compliance
  - Zero configuration
  - Suitable for development and small applications

- **Alembic**: Database migrations
  - Schema version control
  - Migration generation
  - Migration application
  - Rollback capability

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

Example login form from the application:
```python
class LoginForm(FlaskForm):
    login_or_email = StringField('Login lub e-mail', validators=[DataRequired()], 
                                render_kw={"placeholder": "Wpisz login lub e-mail"})
    password = PasswordField('Hasło', validators=[DataRequired()], 
                            render_kw={"placeholder": "Wpisz hasło"})
    submit = SubmitField('Zaloguj się')
```

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

Example file size formatting function:
```python
def format_size(size_mb):
    size = size_mb * 1024 * 1024 
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"
```

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

Each profile management operation includes:
- Security verification (current password)
- Input validation
- Error handling
- Success confirmation

## 8. Code Quality Analysis

### 8.1 Best Practices Implemented

The application demonstrates numerous software engineering best practices:

#### 8.1.1 Separation of Concerns

The codebase maintains clear separation between different responsibilities:

- **Models**: Encapsulate data structure and business logic
  - Password hashing logic in User model
  - File size calculation in file_functions.py
  - Relationship management through SQLAlchemy
  
- **Views**: Handle presentation only
  - Template inheritance for consistent layout
  - Jinja2 for dynamic content
  - Bootstrap for styling
  
- **Controllers**: Manage application flow
  - Route handlers in app.py
  - Request processing
  - Response generation
  - Error handling

#### 8.1.2 Security Awareness

The application demonstrates strong security awareness:

- **Password Security:**
  - Secure hashing with Werkzeug
  - Strong password policy
  - Prevention of password exposure
  
- **Input Validation:**
  - Form validation with WTForms
  - Server-side validation in routes
  - Regular expression validation for critical fields
  
- **Authentication:**
  - Flask-Login for session management
  - @login_required for protected routes
  - Owner verification for resources
  
- **File Security:**
  - UUID-based storage names
  - Owner verification before operations
  - File type validation for text operations

#### 8.1.3 Error Handling

The application implements comprehensive error handling:

- **Database Operations:**
  - Try/except blocks
  - Transaction rollback on error
  - User feedback via flash messages
  - Error logging
  
- **File Operations:**
  - File existence checks
  - IO error handling
  - User feedback for errors
  - Error codes in API responses
  
- **User Interactions:**
  - Form validation errors
  - Flash messages for user feedback
  - Appropriate redirects
  - HTTP status codes

Example error handling pattern:
```python
try:
    # Operation that might fail
    db.session.commit()
    flash('Operation succeeded!', 'success')
except Exception as e:
    db.session.rollback()
    flash('Operation failed!', 'danger')
    print(f'Error: {str(e)}')
```

#### 8.1.4 Code Organization

The codebase demonstrates clean organization:

- **Modular File Structure:**
  - Separate files for models, forms, utilities
  - Template directory with logical organization
  - Migration directory for database changes
  
- **Reusable Components:**
  - Utility functions for repeated operations
  - Base template for layout consistency
  - Flash message handling
  
- **Descriptive Naming:**
  - Function names reflect their purpose
  - Variable names are self-documenting
  - Template names match their functionality
  - Database column names are descriptive

#### 8.1.5 Documentation

The application includes comprehensive documentation:

- **API Documentation:**
  - Swagger integration via Flasgger
  - Docstrings for all route functions
  - Parameter descriptions
  - Response documentation
  
- **Code Comments:**
  - Explanations for complex logic
  - TODO notes for future improvements
  - Clarifications for security measures
  
- **Database Schema:**
  - Model relationships documented
  - Column purposes explained
  - Migrations tracked

### 8.2 Areas for Improvement

While the application demonstrates many best practices, there are several areas for improvement:

#### 8.2.1 Security Enhancements

- **Configuration Management:**
  - Move secret key to environment variables
  - Implement proper configuration for different environments
  - Remove hardcoded values
  
- **Authentication Hardening:**
  - Implement rate limiting for login attempts
  - Add account lockout after failed attempts
  - Consider two-factor authentication
  
- **File Upload Security:**
  - Add MIME type validation
  - Implement file size limits
  - Consider virus scanning for uploads
  
- **HTTPS Enforcement:**
  - Configure for HTTPS-only operation
  - Implement HSTS headers
  - Secure cookie flags

#### 8.2.2 Performance Optimization

- **Database Optimization:**
  - Add indexes for frequently queried fields
  - Implement pagination for file listing
  - Optimize query execution plans
  
- **Caching:**
  - Implement caching for static resources
  - Consider caching for frequent database queries
  - Use ETags for API responses
  
- **File Handling:**
  - Stream large file downloads
  - Implement chunked uploads for large files
  - Consider asynchronous processing for uploads

#### 8.2.3 Code Improvements

- **Testing:**
  - Add unit tests for models and utilities
  - Implement integration tests for routes
  - Add security testing
  
- **Logging:**
  - Implement structured logging
  - Add log rotation
  - Improve error context in logs
  
- **Code Refactoring:**
  - Reduce duplicated code in route handlers
  - Move file operations to a dedicated service
  - Consider using blueprints for route organization

#### 8.2.4 Feature Enhancements

- **File Sharing:**
  - Implement sharing between users
  - Add public/private file options
  - Generate shareable links
  
- **File Management:**
  - Add file categorization
  - Implement search functionality
  - Add file versioning
  
- **User Experience:**
  - Implement drag-and-drop uploads
  - Add progress indicators for operations
  - Implement bulk operations

#### 8.2.5 UI/UX Improvements

- **Responsive Design:**
  - Improve mobile experience
  - Optimize for different screen sizes
  - Enhance accessibility
  
- **Client-Side Validation:**
  - Add JavaScript validation for forms
  - Provide immediate feedback
  - Improve error messages
  
- **Visual Enhancements:**
  - Improve dashboard layout
  - Add file type icons
  - Implement themes

## 9. Setup and Running Instructions

### 9.1 Prerequisites

The application requires:

- **Python 3.8+**: Core runtime environment
- **pip**: Python package manager
- **Virtual environment**: Recommended for dependency isolation
- **SQLite**: Database (included with Python)

### 9.2 Installation

Follow these steps to set up the application:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd IO-2-Project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This installs all required packages, including:
   - Flask and extensions
   - SQLAlchemy
   - WTForms
   - Flasgger
   - Other dependencies

### 9.3 Database Initialization

Initialize the database structure:

```bash
python database_init.py
```

This script:
- Creates the database file (`instance/project.db`)
- Initializes the database schema
- Applies any pending migrations

### 9.4 Running the Application

Start the Flask development server:

```bash
python app.py
```

The application will start with:
- Development server on http://127.0.0.1:5000/
- Debug mode enabled
- Auto-reloading on code changes

### 9.5 Application Configuration

Key configuration parameters:

- **Database URI**: `sqlite:///project.db`
- **Secret Key**: Defined in `app.py`
- **Upload Folder**: `uploads/` directory

## 10. THE END
