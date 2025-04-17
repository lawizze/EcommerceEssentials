from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from models import Product, User, Order
from app import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin access decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    conn = get_db_connection()
    
    # Get stats for dashboard
    product_count = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    order_count = conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
    user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    
    # Get recent orders
    recent_orders = conn.execute('''
        SELECT o.*, u.username 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        ORDER BY o.created_at DESC LIMIT 5
    ''').fetchall()
    
    # Get low stock products
    low_stock_products = conn.execute('SELECT * FROM products WHERE stock < 10').fetchall()
    
    conn.close()
    
    return render_template('admin/dashboard.html', 
                          product_count=product_count,
                          order_count=order_count,
                          user_count=user_count,
                          recent_orders=recent_orders,
                          low_stock_products=low_stock_products)

@admin_bp.route('/products')
@login_required
@admin_required
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        category = request.form.get('category')
        stock = request.form.get('stock')
        
        # Validate inputs
        if not name or not description or not price or not category or not stock:
            flash('All fields except image URL are required.', 'danger')
            return redirect(url_for('admin.add_product'))
        
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            flash('Price must be a number and stock must be an integer.', 'danger')
            return redirect(url_for('admin.add_product'))
        
        # Create product
        Product.create(name, description, price, image_url, category, stock)
        
        flash('Product added successfully.', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/products.html', is_add=True)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('admin.products'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        category = request.form.get('category')
        stock = request.form.get('stock')
        
        # Validate inputs
        if not name or not description or not price or not category or not stock:
            flash('All fields except image URL are required.', 'danger')
            return redirect(url_for('admin.edit_product', product_id=product_id))
        
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            flash('Price must be a number and stock must be an integer.', 'danger')
            return redirect(url_for('admin.edit_product', product_id=product_id))
        
        # Update product
        Product.update(product_id, name, description, price, image_url, category, stock)
        
        flash('Product updated successfully.', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/products.html', product=product, is_edit=True)

@admin_bp.route('/products/delete/<int:product_id>')
@login_required
@admin_required
def delete_product(product_id):
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('admin.products'))
    
    Product.delete(product_id)
    
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('admin.products'))

@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    orders = Order.get_all_orders()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/orders/<int:order_id>')
@login_required
@admin_required
def order_detail(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT o.*, u.username, u.email FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = ?', 
                        (order_id,)).fetchone()
    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('admin.orders'))
    
    items = Order.get_order_items(order_id)
    conn.close()
    
    return render_template('admin/orders.html', order=order, items=items, is_detail=True)

@admin_bp.route('/orders/update-status/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    status = request.form.get('status')
    
    if not status:
        flash('Status is required.', 'danger')
        return redirect(url_for('admin.order_detail', order_id=order_id))
    
    Order.update_status(order_id, status)
    
    flash('Order status updated successfully.', 'success')
    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY id DESC').fetchall()
    conn.close()
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        
        # Validate inputs
        if not username or not email or not password or not confirm_password or not role:
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin.add_user'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('admin.add_user'))
        
        conn = get_db_connection()
        
        # Check if username or email already exists
        if conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
            flash('Username already exists.', 'danger')
            conn.close()
            return redirect(url_for('admin.add_user'))
            
        if conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
            flash('Email already exists.', 'danger')
            conn.close()
            return redirect(url_for('admin.add_user'))
        
        # Create new user
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)
        
        conn.execute(
            'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
            (username, email, hashed_password, role)
        )
        conn.commit()
        conn.close()
        
        flash('User added successfully.', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users.html', is_add=True)

@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.users'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        
        # Validate inputs
        if not username or not email or not role:
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        # Check if username is already taken by another user
        check_username = conn.execute('SELECT id FROM users WHERE username = ? AND id != ?', 
                                    (username, user_id)).fetchone()
        if check_username:
            flash('Username is already taken.', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        # Check if email is already taken by another user
        check_email = conn.execute('SELECT id FROM users WHERE email = ? AND id != ?', 
                                 (email, user_id)).fetchone()
        if check_email:
            flash('Email is already taken.', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        # Update user
        conn.execute('UPDATE users SET username = ?, email = ?, role = ? WHERE id = ?',
                   (username, email, role, user_id))
        conn.commit()
        
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.users'))
    
    conn.close()
    return render_template('admin/users.html', user=user, is_edit=True)

@admin_bp.route('/users/delete/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.users'))
    
    # Don't allow deleting the current user
    if user['id'] == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    # Delete user's cart items
    conn.execute('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
    
    # Update orders to show "deleted user"
    conn.execute('UPDATE orders SET user_id = NULL WHERE user_id = ?', (user_id,))
    
    # Delete user
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.users'))
