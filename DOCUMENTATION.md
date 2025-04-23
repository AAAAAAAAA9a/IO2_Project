---

# Flask File Management Application

## Introduction

The **Flask File Management Application** provides a secure and intuitive platform for managing personal files through a web interface. 
With features like robust authentication, file operations, and API documentation, it adheres to modern web development practices and the Model-View-Controller [MVC] architecture.

Primary objectives include:
- Secure file storage and management.
- Industry-standard user authentication.
- Comprehensive file operations (upload, download, preview, edit, delete).
- Demonstration of MVC architecture with Flask.
- Showcase of modern web development practices.

---

## Application Overview

### Architecture

The application strictly follows the **Model-View-Controller (MVC)** architecture:
- **Models**: Handle database schema, business logic, and relationships.
- **Views**: Render user-facing content using Jinja2 templates with Bootstrap 5 styling.
- **Controllers**: Manage routing, business logic, and API documentation.

#### Key Flask Extensions
- **Flask-SQLAlchemy**: Database ORM for interactions and relationships.
- **Flask-Login**: Manages user authentication and session handling.
- **Flask-Migrate**: Handles database schema versioning.
- **Flask-WTF**: Manages form validation and CSRF protection.
- **Flasgger**: Auto-generates API documentation using Swagger.

---

## Features and Functionality

### 1. User Authentication and Security
- **Password Security**: Secure password hashing via Werkzeug.
- **Strong Password Policy**: Minimum 15 characters with uppercase, lowercase, digit, and special character requirements.
- **Session Management**: Secure login/logout with session protection.
- **Form Protection**: CSRF protection for all forms.

### 2. File Management
- **File Operations**: Upload, download, preview, edit, and delete files.
- **Secure File Storage**: Files stored as UUIDs to prevent collisions and ensure security.
- **Validation**: File type and ownership validation for operations.
- **Statistics**: Tracks user file count and total storage usage.

### 3. API Endpoints
- RESTful endpoints for user management, file operations, and error handling.
- Comprehensive Swagger-based API documentation.

### 4. Database Schema
- **Users Model**: Handles authentication, profile management, and user-file relationships.
- **Files Model**: Manages file metadata and storage references.
- **Relationship Design**: One-to-many relationship between users and files.

---

## Technologies Used

### Backend
- **Flask**: Core web framework.
- **SQLAlchemy**: ORM for database interactions.
- **Flask-Login**: Authentication management.
- **Flask-Migrate**: Schema migrations.
- **Flasgger**: API documentation.

### Frontend
- **Bootstrap 5**: Responsive UI framework.
- **Jinja2**: Template engine for dynamic content.
- **JavaScript**: Enhances interactivity with AJAX support.

### Database
- **SQLite**: Lightweight database for development and small-scale applications.
- **Alembic**: Handles schema versioning and migrations.

---

## Application Workflow

### Authentication Flow
1. User submits login credentials.
2. Credentials validated against the database.
3. On success, a session is created, and the user is redirected to the dashboard.

### File Upload Flow
1. User selects a file via the upload form.
2. File is validated, and a UUID is generated for storage.
3. File saved to the filesystem, and metadata is recorded in the database.

### File Operation Flow
1. User requests an operation (download, edit, delete, etc.).
2. Application verifies file ownership.
3. Operation is performed, and feedback is provided to the user.

---

## Security Measures

### Authentication Security
- Password hashing with **Werkzeug**.
- Strong password policy enforced via regex.
- Session protection with Flask-Login.

### File Security
- Files stored using UUIDs to prevent naming conflicts.
- Strict access control ensures only file owners can perform operations.
- Validation restricts unsupported file types for operations like editing.

### Web Security
- CSRF protection for all forms.
- Error handling for graceful recovery and user feedback.
- Secure application configuration.

---

## API Documentation

### Authentication Endpoints
| Endpoint    | Method | Description           |
|-------------|--------|-----------------------|
| `/login`    | POST   | User login.           |
| `/register` | POST   | New user registration.|
| `/logout`   | GET    | User logout.          |

### File Management Endpoints
| Endpoint          | Method     | Description                 |
|-------------------|------------|-----------------------------|
| `/dashboard`      | GET        | List user's files.          |
| `/upload`         | POST       | Upload a new file.          |
| `/download/<id>`  | GET        | Download a file by ID.      |
| `/delete/<id>`    | POST       | Delete a file by ID.        |
| `/edit/<id>`      | GET/POST   | Edit a text file by ID.     |
| `/preview/<id>`   | GET        | Preview a text file by ID.  |

---

## Setup and Installation

### Prerequisites
- **Python 3.8+**
- **pip**: Python package manager.
- **SQLite**: Included with Python.
- **Virtual Environment**: Recommended for dependency isolation.

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd IO-2-Project
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Initialization
Run the database initialization script:
```bash
python database_init.py
```

### Running the Application
Start the Flask development server:
```bash
python app.py
```

Access the app at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Future Improvements
- **File Sharing**: Add options for sharing files with other users.
- **Two-Factor Authentication**: Enhance account security.
- **Search Functionality**: Allow users to search files by name or content.
- **Profile Management**: Add settings to personalize user profiles.

---
