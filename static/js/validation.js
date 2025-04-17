/**
 * Form validation for the e-commerce application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Registration form validation
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Username validation
            const username = document.getElementById('username');
            if (username.value.trim().length < 3) {
                showError(username, 'Username must be at least 3 characters');
                isValid = false;
            } else {
                removeError(username);
            }
            
            // Email validation
            const email = document.getElementById('email');
            if (!isValidEmail(email.value.trim())) {
                showError(email, 'Please enter a valid email address');
                isValid = false;
            } else {
                removeError(email);
            }
            
            // Password validation
            const password = document.getElementById('password');
            if (password.value.length < 6) {
                showError(password, 'Password must be at least 6 characters');
                isValid = false;
            } else {
                removeError(password);
            }
            
            // Confirm password validation
            const confirmPassword = document.getElementById('confirm_password');
            if (password.value !== confirmPassword.value) {
                showError(confirmPassword, 'Passwords do not match');
                isValid = false;
            } else {
                removeError(confirmPassword);
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Login form validation
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Username validation
            const username = document.getElementById('username');
            if (username.value.trim() === '') {
                showError(username, 'Username is required');
                isValid = false;
            } else {
                removeError(username);
            }
            
            // Password validation
            const password = document.getElementById('password');
            if (password.value === '') {
                showError(password, 'Password is required');
                isValid = false;
            } else {
                removeError(password);
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Product form validation
    const productForm = document.getElementById('product-form');
    if (productForm) {
        productForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Name validation
            const name = document.getElementById('name');
            if (name.value.trim() === '') {
                showError(name, 'Product name is required');
                isValid = false;
            } else {
                removeError(name);
            }
            
            // Description validation
            const description = document.getElementById('description');
            if (description.value.trim() === '') {
                showError(description, 'Description is required');
                isValid = false;
            } else {
                removeError(description);
            }
            
            // Price validation
            const price = document.getElementById('price');
            if (price.value.trim() === '' || isNaN(price.value) || parseFloat(price.value) <= 0) {
                showError(price, 'Please enter a valid price greater than 0');
                isValid = false;
            } else {
                removeError(price);
            }
            
            // Category validation
            const category = document.getElementById('category');
            if (category.value.trim() === '') {
                showError(category, 'Category is required');
                isValid = false;
            } else {
                removeError(category);
            }
            
            // Stock validation
            const stock = document.getElementById('stock');
            if (stock.value.trim() === '' || isNaN(stock.value) || parseInt(stock.value) < 0) {
                showError(stock, 'Please enter a valid stock value (0 or greater)');
                isValid = false;
            } else {
                removeError(stock);
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Checkout form validation
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Shipping address validation
            const shippingAddress = document.getElementById('shipping_address');
            if (shippingAddress.value.trim() === '') {
                showError(shippingAddress, 'Shipping address is required');
                isValid = false;
            } else {
                removeError(shippingAddress);
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
});

/**
 * Show error message for an input
 * @param {HTMLElement} input - The input element
 * @param {string} message - The error message
 */
function showError(input, message) {
    // Remove any existing error
    removeError(input);
    
    // Create error message
    const error = document.createElement('div');
    error.className = 'invalid-feedback';
    error.textContent = message;
    
    // Add invalid class to input
    input.classList.add('is-invalid');
    
    // Insert error after input
    input.parentNode.insertBefore(error, input.nextSibling);
}

/**
 * Remove error message from an input
 * @param {HTMLElement} input - The input element
 */
function removeError(input) {
    input.classList.remove('is-invalid');
    
    // Remove any existing error message
    const parent = input.parentNode;
    const errors = parent.querySelectorAll('.invalid-feedback');
    errors.forEach(error => error.remove());
}

/**
 * Validate email format
 * @param {string} email - The email address to validate
 * @returns {boolean} - True if email is valid
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}
