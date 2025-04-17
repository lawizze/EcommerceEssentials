# E-Commerce System Setup Guide

This document provides detailed setup instructions for installing and running the e-commerce system.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning repository)

## Installation Steps

1. **Clone or download the repository**

   ```
   git clone <repository-url>
   cd ecommerce-system
   ```

2. **Install required dependencies**

   ```
   pip install flask flask-login flask-sqlalchemy flask-wtf email-validator gunicorn psycopg2-binary werkzeug
   ```

3. **Initialize the database (first time only)**

   ```
   python app.py init_db
   ```

4. **Start the application**

   ```
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

   Or for development:
   
   ```
   flask run --host=0.0.0.0 --port=5000
   ```

## Environment Configuration

The application uses the following environment variables:

- `SESSION_SECRET`: For securing session cookies (optional, auto-generated if not set)
- `DATABASE_URL`: Database connection string (defaults to SQLite)

## Default Admin Account

An admin account is created automatically with the following credentials:
- **Username**: admin
- **Email**: admin@example.com  
- **Password**: admin123
- **Role**: admin

*Note: Change these credentials immediately after first login in a production environment*

## Directory Structure

The application is organized with the following structure:

```
.
├── static/                  # Static assets 
│   ├── css/                 # CSS stylesheets
│   ├── js/                  # JavaScript files
│   └── uploads/products/    # Uploaded product images
├── templates/               # HTML templates
│   ├── admin/               # Admin panel templates
│   ├── auth/                # Authentication templates  
│   └── shop/                # Store templates
├── main.py                  # Application entry point
├── app.py                   # Flask application setup
├── models.py                # Database models
├── admin.py                 # Admin routes and functionality
├── auth.py                  # Authentication routes
├── cart.py                  # Shopping cart functionality
├── shop.py                  # Store routes and functionality
└── ecommerce.db             # SQLite database
```

## Troubleshooting

### Database Issues

If you encounter database errors:

1. Ensure SQLite is working correctly
2. Check database file permissions
3. Delete and reinitialize the database if necessary:
   ```
   rm ecommerce.db
   python app.py init_db
   ```

### Port Already In Use

If port 5000 is already in use, change the port:

```
gunicorn --bind 0.0.0.0:5001 --reuse-port --reload main:app
```

### Static Files Not Loading

If static files (CSS, JavaScript, images) are not loading:

1. Check file paths in templates
2. Ensure static directory is properly structured
3. Clear browser cache

## Deployment Considerations

For production deployment:

1. Use a production-grade WSGI server (Gunicorn is recommended)
2. Set a strong SESSION_SECRET environment variable
3. Consider using a reverse proxy (Nginx/Apache) for production
4. Change default admin credentials
5. Implement HTTPS for secure connections