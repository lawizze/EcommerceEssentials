# E-Commerce System Usage Guide

This guide provides essential information for using the e-commerce system.

## Accessing the Application

Once the application is running, you can access it at:
- http://localhost:5000 (local development)
- or the deployed URL if hosted on a server

## User Roles and Access

### Public Access (No Login Required)
- Browse all products
- View product details and reviews
- Register a new account or login

### Customer Features (Login Required)
- Browse and search products
- Add products to shopping cart
- Manage shopping cart (update quantities, remove items)
- Complete checkout process
- View order history and details
- Write product reviews
- Manage personal profile information

### Admin Features (Admin Login Required)
- Access admin dashboard with analytics
- Manage products (add, edit, delete)
- Process and update order status
- Manage user accounts
- View sales reports

## Navigation

### Main Navigation
- **Home**: Landing page with featured products
- **Products**: Browse all products or by category
- **Cart**: View and manage your shopping cart
- **Orders**: View your order history (when logged in)
- **Profile**: Manage your account (when logged in)
- **Admin**: Access admin panel (admin users only)
- **Login/Register**: Authentication options (when not logged in)
- **Logout**: Log out of your account (when logged in)

## Shop Features

### Product Browsing
- Use category filters to find products
- Sort products by price, name, or newest
- View detailed product information and specifications

### Shopping Cart
1. Add products to cart by clicking "Add to Cart" on product pages
2. Adjust quantities in the cart page
3. Remove items by clicking the trash icon
4. View cart total and proceed to checkout

### Checkout Process
1. Review cart items
2. Enter shipping information
3. Confirm your order
4. View order confirmation and details

### Account Management
- Update profile information
- Change password
- View order history

## Admin Features

### Product Management
1. **Adding Products**:
   - Go to Admin > Products > Add New Product
   - Fill in all required fields (name, description, price, category, stock)
   - Add product image (either by URL or file upload)
   - Click "Add Product"

2. **Editing Products**:
   - Go to Admin > Products
   - Click the edit (pencil) icon next to a product
   - Update information as needed
   - Click "Update Product"

3. **Deleting Products**:
   - Go to Admin > Products
   - Click the delete (trash) icon next to a product
   - Confirm deletion

### Order Management
1. Go to Admin > Orders
2. View all orders or search by order ID/customer
3. Click on an order to view details
4. Update order status as needed (Processing, Shipped, Delivered, etc.)

### User Management
1. Go to Admin > Users
2. View all users or search by username/email
3. Add, edit, or delete users as needed
4. Assign user roles (admin or customer)

## Product Images

The system supports both image URLs and direct file uploads:
- **Image URLs**: Enter a valid image URL in the provided field
- **File Upload**: Upload an image file (supported formats: jpg, png, gif, webp)

## Writing Reviews

1. Navigate to a product's detail page
2. Scroll to the "Reviews" section
3. If logged in, you'll see a review form
4. Enter your rating (1-5 stars) and comment
5. Click "Submit Review"

## Tips and Tricks

1. **Quick Cart View**: Hover over the cart icon to see a summary without leaving your page
2. **Order Tracking**: Use the order ID from your confirmation email to track your order status
3. **Product Availability**: Products with low stock will be marked with a warning indicator
4. **Admin Dashboard**: Get a quick overview of sales, inventory, and user activity from the admin dashboard

---

For technical setup and installation instructions, please refer to the SETUP.md file.