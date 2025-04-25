# Flask File Management Application

A secure web application for managing personal files with robust authentication and comprehensive file operations.

## Key Features

- User authentication with strong password requirements
- File upload, download, preview, edit, and delete functionality
- User profile management
- Secure file storage using UUID-based naming
- RESTful API with Swagger documentation

## Quick Start

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database_init.py

# Run the application
python app.py
```

Access the application at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)  
API documentation is available at [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

## Documentation

For comprehensive documentation, including architecture details, API reference, and setup instructions, see the [docs/documentation.md](docs/documentation.md) file.

## Technologies

- Backend: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- Frontend: Bootstrap 5, JavaScript, Jinja2
- Database: SQLite
- Documentation: Flasgger (Swagger)