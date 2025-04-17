# E-Commerce System

A full-featured e-commerce platform built with Flask and SQLite, featuring role-based access control, product management, shopping cart functionality, and order processing.

## Features

### Public Access
- Browse products by category
- View product details and reviews
- Register a new account

### Customer Features
- User authentication (login/register)
- Browse and search products
- Add products to cart
- Manage shopping cart
- Complete checkout process
- View order history
- Write product reviews
- Manage personal profile

### Admin Features
- Complete product management (CRUD)
- User management
- Order processing and status updates
- Dashboard with sales analytics
- Inventory management
- Product image upload support

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **Authentication**: Flask-Login
- **Form Handling**: Flask-WTF
- **Frontend**: HTML5, Bootstrap CSS, JavaScript

## Installation and Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ecommerce-system
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```
   pip install flask flask-login flask-sqlalchemy flask-wtf email-validator gunicorn psycopg2-binary werkzeug
   ```

3. Initialize the database (first time only):
   ```
   python app.py init_db
   ```

4. Start the application:
   ```
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

## Usage

### Accessing the Application

Once the application is running, you can access it at:
- http://localhost:5000 (local development)


### Default Admin Account

An admin account is created automatically with the following credentials:
- **Username**: admin
- **Email**: admin@example.com
- **Password**: admin123
- **Role**: admin

(Note: Change these credentials immediately after first login in a production environment)

### User Roles

The system has two user roles:
1. **Customer**: Can browse products, make purchases, and leave reviews
2. **Admin**: Has full access to manage products, users, and orders

### Directory Structure

```
├── static                  # Static assets
│   ├── css                 # CSS stylesheets
│   ├── js                  # JavaScript files
│   └── uploads/products    # Uploaded product images
├── templates               # HTML templates
│   ├── admin               # Admin panel templates
│   ├── auth                # Authentication templates
│   └── shop                # Store templates
├── main.py                 # Application entry point
├── app.py                  # Flask application setup
├── models.py               # Database models
├── admin.py                # Admin routes and functionality
├── auth.py                 # Authentication routes
├── cart.py                 # Shopping cart functionality
├── shop.py                 # Store routes and functionality
└── ecommerce.db            # SQLite database
```

## Development

### Adding Products

As an admin, you can add products with the following information:
- Name
- Description
- Price
- Category
- Size information
- Stock quantity
- Product image (upload file or URL)

### Product Images

The system supports both image URLs and direct file uploads:
- **Image URLs**: Enter a valid image URL
- **File Upload**: Upload an image file (jpg, png, gif, webp)

### Customization

You can customize the system by:
1. Modifying templates in the templates directory
2. Adding new CSS in static/css/custom.css
3. Extending models in models.py to add new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.
