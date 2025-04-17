from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import Product, Cart, Order
from app import get_db_connection

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/')
@login_required
def view_cart():
    cart_items = Cart.get_items(current_user.id)
    
    # Calculate total
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    return render_template('shop/cart.html', cart_items=cart_items, total=total)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('shop.products'))
    
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        flash('Quantity must be greater than 0.', 'danger')
        return redirect(url_for('shop.product_detail', product_id=product_id))
    
    if quantity > product['stock']:
        flash(f'Sorry, only {product["stock"]} available in stock.', 'danger')
        return redirect(url_for('shop.product_detail', product_id=product_id))
    
    Cart.add_item(current_user.id, product_id, quantity)
    
    flash('Product added to cart.', 'success')
    
    # Check if Ajax request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'cart_count': Cart.count(current_user.id)})
    
    return redirect(url_for('shop.product_detail', product_id=product_id))

@cart_bp.route('/update/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('cart.view_cart'))
    
    quantity = int(request.form.get('quantity', 0))
    
    if quantity <= 0:
        Cart.remove_item(current_user.id, product_id)
        flash('Product removed from cart.', 'info')
    else:
        if quantity > product['stock']:
            flash(f'Sorry, only {product["stock"]} available in stock.', 'danger')
            quantity = product['stock']
        
        Cart.update_item(current_user.id, product_id, quantity)
        flash('Cart updated.', 'success')
    
    # Check if Ajax request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_items = Cart.get_items(current_user.id)
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        return jsonify({
            'success': True, 
            'cart_count': Cart.count(current_user.id),
            'item_total': product['price'] * quantity,
            'cart_total': total
        })
    
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    Cart.remove_item(current_user.id, product_id)
    
    flash('Product removed from cart.', 'info')
    
    # Check if Ajax request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_items = Cart.get_items(current_user.id)
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        return jsonify({
            'success': True, 
            'cart_count': Cart.count(current_user.id),
            'cart_total': total
        })
    
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = Cart.get_items(current_user.id)
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('shop.products'))
    
    # Calculate total
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address')
        
        if not shipping_address:
            flash('Shipping address is required.', 'danger')
            return render_template('shop/checkout.html', cart_items=cart_items, total=total)
        
        # Create order
        order_id = Order.create(current_user.id, total, shipping_address)
        
        # Get order details for confirmation page
        conn = get_db_connection()
        order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
        items = Order.get_order_items(order_id)
        conn.close()
        
        flash('Order placed successfully.', 'success')
        return render_template('shop/order_confirmation.html', order=order, items=items)
    
    return render_template('shop/checkout.html', cart_items=cart_items, total=total)
