import sqlite3
from flask_login import UserMixin
from app import login_manager, get_db_connection

class User(UserMixin):
    def __init__(self, id, username, email, role):
        self.id = id
        self.username = username
        self.email = email
        self.role = role

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user:
            return User(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                role=user['role']
            )
        return None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user:
            return User(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                role=user['role']
            )
        return None

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user:
            return User(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                role=user['role']
            )
        return None

    def is_admin(self):
        return self.role == 'admin'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

class Product:
    def __init__(self, id, name, description, price, image_url, category, size, stock, created_at):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.category = category
        self.size = size
        self.stock = stock
        self.created_at = created_at

    @staticmethod
    def get_all():
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products').fetchall()
        conn.close()
        return products

    @staticmethod
    def get_by_id(product_id):
        conn = get_db_connection()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        conn.close()
        return product

    @staticmethod
    def create(name, description, price, image_url, category, size, stock):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, description, price, image_url, category, size, stock)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, price, image_url, category, size, stock))
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        return product_id

    @staticmethod
    def update(product_id, name, description, price, image_url, category, size, stock):
        conn = get_db_connection()
        conn.execute('''
            UPDATE products 
            SET name = ?, description = ?, price = ?, image_url = ?, category = ?, size = ?, stock = ?
            WHERE id = ?
        ''', (name, description, price, image_url, category, size, stock, product_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(product_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()

class Cart:
    @staticmethod
    def add_item(user_id, product_id, quantity=1):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if item already exists in cart
        existing_item = cursor.execute(
            'SELECT * FROM cart_items WHERE user_id = ? AND product_id = ?', 
            (user_id, product_id)
        ).fetchone()
        
        if existing_item:
            # Update quantity if item exists
            cursor.execute(
                'UPDATE cart_items SET quantity = quantity + ? WHERE user_id = ? AND product_id = ?',
                (quantity, user_id, product_id)
            )
        else:
            # Add new item if it doesn't exist
            cursor.execute(
                'INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)',
                (user_id, product_id, quantity)
            )
        
        conn.commit()
        conn.close()

    @staticmethod
    def update_item(user_id, product_id, quantity):
        conn = get_db_connection()
        
        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            conn.execute(
                'DELETE FROM cart_items WHERE user_id = ? AND product_id = ?',
                (user_id, product_id)
            )
        else:
            # Update quantity
            conn.execute(
                'UPDATE cart_items SET quantity = ? WHERE user_id = ? AND product_id = ?',
                (quantity, user_id, product_id)
            )
        
        conn.commit()
        conn.close()

    @staticmethod
    def remove_item(user_id, product_id):
        conn = get_db_connection()
        conn.execute(
            'DELETE FROM cart_items WHERE user_id = ? AND product_id = ?',
            (user_id, product_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_items(user_id):
        conn = get_db_connection()
        cart_items = conn.execute('''
            SELECT c.id, c.product_id, c.quantity, p.name, p.price, p.image_url
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
        ''', (user_id,)).fetchall()
        conn.close()
        return cart_items

    @staticmethod
    def clear(user_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def count(user_id):
        conn = get_db_connection()
        count = conn.execute(
            'SELECT SUM(quantity) FROM cart_items WHERE user_id = ?', 
            (user_id,)
        ).fetchone()[0]
        conn.close()
        return count or 0

class Order:
    @staticmethod
    def create(user_id, total, shipping_address):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create order
        cursor.execute('''
            INSERT INTO orders (user_id, total, shipping_address, status)
            VALUES (?, ?, ?, ?)
        ''', (user_id, total, shipping_address, 'pending'))
        
        order_id = cursor.lastrowid
        
        # Get cart items
        cart_items = Cart.get_items(user_id)
        
        # Move cart items to order items
        for item in cart_items:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['product_id'], item['quantity'], item['price']))
            
            # Update product stock
            cursor.execute('''
                UPDATE products
                SET stock = stock - ?
                WHERE id = ?
            ''', (item['quantity'], item['product_id']))
        
        # Clear cart
        Cart.clear(user_id)
        
        conn.commit()
        conn.close()
        
        return order_id

    @staticmethod
    def get_user_orders(user_id):
        conn = get_db_connection()
        orders = conn.execute('''
            SELECT * FROM orders
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,)).fetchall()
        conn.close()
        return orders

    @staticmethod
    def get_all_orders():
        conn = get_db_connection()
        orders = conn.execute('''
            SELECT o.*, u.username
            FROM orders o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.created_at DESC
        ''').fetchall()
        conn.close()
        return orders

    @staticmethod
    def get_order_items(order_id):
        conn = get_db_connection()
        items = conn.execute('''
            SELECT oi.*, p.name, p.image_url
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,)).fetchall()
        conn.close()
        return items

    @staticmethod
    def update_status(order_id, status):
        conn = get_db_connection()
        conn.execute('''
            UPDATE orders
            SET status = ?
            WHERE id = ?
        ''', (status, order_id))
        conn.commit()
        conn.close()
        
class Review:
    def __init__(self, id, product_id, user_id, rating, comment, created_at, username=None):
        self.id = id
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
        self.username = username
    
    @staticmethod
    def create(product_id, user_id, rating, comment):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reviews (product_id, user_id, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (product_id, user_id, rating, comment))
        review_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return review_id
    
    @staticmethod
    def get_by_product(product_id):
        conn = get_db_connection()
        reviews = conn.execute('''
            SELECT r.*, u.username 
            FROM reviews r 
            JOIN users u ON r.user_id = u.id 
            WHERE r.product_id = ? 
            ORDER BY r.created_at DESC
        ''', (product_id,)).fetchall()
        conn.close()
        return reviews
    
    @staticmethod
    def get_average_rating(product_id):
        conn = get_db_connection()
        result = conn.execute('''
            SELECT AVG(rating) as avg_rating, COUNT(*) as count
            FROM reviews
            WHERE product_id = ?
        ''', (product_id,)).fetchone()
        conn.close()
        
        if result and result['count'] > 0:
            return {
                'avg_rating': round(result['avg_rating'], 1),
                'count': result['count']
            }
        else:
            return {
                'avg_rating': 0,
                'count': 0
            }
            
    @staticmethod
    def delete(review_id, user_id=None):
        conn = get_db_connection()
        
        if user_id:
            # Only delete if user is the author
            conn.execute('''
                DELETE FROM reviews
                WHERE id = ? AND user_id = ?
            ''', (review_id, user_id))
        else:
            # Allow admin to delete any review
            conn.execute('''
                DELETE FROM reviews
                WHERE id = ?
            ''', (review_id,))
            
        conn.commit()
        conn.close()
