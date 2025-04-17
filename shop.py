from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Product, Cart, Order
from app import get_db_connection

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')

@shop_bp.route('/products')
def products():
    category = request.args.get('category')
    search = request.args.get('search')
    
    conn = get_db_connection()
    
    if category:
        products = conn.execute('SELECT * FROM products WHERE category = ? ORDER BY id DESC', 
                               (category,)).fetchall()
    elif search:
        search_query = f'%{search}%'
        products = conn.execute('''
            SELECT * FROM products 
            WHERE name LIKE ? OR description LIKE ? 
            ORDER BY id DESC
        ''', (search_query, search_query)).fetchall()
    else:
        products = conn.execute('SELECT * FROM products ORDER BY id DESC').fetchall()
    
    # Get all categories for filter
    categories = conn.execute('SELECT DISTINCT category FROM products').fetchall()
    
    conn.close()
    
    return render_template('shop/products.html', products=products, categories=categories,
                          current_category=category, search_query=search)

@shop_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('shop.products'))
    
    conn = get_db_connection()
    
    # Get related products (same category)
    related_products = conn.execute('''
        SELECT * FROM products 
        WHERE category = ? AND id != ? 
        ORDER BY id DESC LIMIT 4
    ''', (product['category'], product_id)).fetchall()
    
    conn.close()
    
    return render_template('shop/product_detail.html', product=product, related_products=related_products)

@shop_bp.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (current_user.id,)).fetchone()
    
    # Get order history
    orders = Order.get_user_orders(current_user.id)
    
    conn.close()
    
    return render_template('shop/profile.html', user=user, orders=orders)

@shop_bp.route('/orders')
@login_required
def orders():
    orders = Order.get_user_orders(current_user.id)
    return render_template('shop/orders.html', orders=orders)

@shop_bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ? AND user_id = ?', 
                        (order_id, current_user.id)).fetchone()
    
    if not order:
        flash('Order not found or access denied.', 'danger')
        return redirect(url_for('shop.orders'))
    
    items = Order.get_order_items(order_id)
    conn.close()
    
    return render_template('shop/orders.html', order=order, items=items, is_detail=True)
