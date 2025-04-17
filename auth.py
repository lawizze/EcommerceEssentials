from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from app import get_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.get_by_username(username)
        
        if not user:
            flash('Username does not exist.', 'danger')
            return render_template('auth/login.html')
            
        conn = get_db_connection()
        stored_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if stored_user and check_password_hash(stored_user['password'], password):
            user = User(
                id=stored_user['id'],
                username=stored_user['username'],
                email=stored_user['email'],
                role=stored_user['role']
            )
            login_user(user, remember=remember)
            
            # Get next page or default based on role
            next_page = request.args.get('next')
            if not next_page or url_for('index') in next_page:
                if user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('shop.products'))
            return redirect(next_page)
        else:
            flash('Password is incorrect.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Form validation
        if not username or not email or not password or not confirm_password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')
            
        # Check if username or email already exists
        conn = get_db_connection()
        if conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
            flash('Username already exists.', 'danger')
            conn.close()
            return render_template('auth/register.html')
            
        if conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
            flash('Email already exists.', 'danger')
            conn.close()
            return render_template('auth/register.html')
            
        # Create new user
        hashed_password = generate_password_hash(password)
        
        cursor = conn.execute(
            'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
            (username, email, hashed_password, 'customer')
        )
        user_id = cursor.lastrowid
        conn.commit()
        
        # Get the newly created user
        user_data = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        
        # Automatically log in the new user
        user = User(
            id=user_data['id'],
            username=user_data['username'],
            email=user_data['email'],
            role=user_data['role']
        )
        login_user(user)
        
        flash('Registration successful! Welcome to our store.', 'success')
        return redirect(url_for('shop.products'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
