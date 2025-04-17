/**
 * Cart functionality for the e-commerce application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add to cart form submission with AJAX
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const formData = new FormData(form);
            const url = form.getAttribute('action');
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showNotification('Product added to cart', 'success');
                    
                    // Update cart count
                    updateCartCount(data.cart_count);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Failed to add product to cart', 'danger');
            });
        });
    });
    
    // Update cart quantity
    const quantityInputs = document.querySelectorAll('.cart-quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const productId = this.dataset.productId;
            const quantity = parseInt(this.value);
            
            if (quantity < 0) {
                this.value = 0;
                return;
            }
            
            const formData = new FormData();
            formData.append('quantity', quantity);
            
            fetch(`/cart/update/${productId}`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update UI
                    const itemTotalElement = document.getElementById(`item-total-${productId}`);
                    if (itemTotalElement) {
                        itemTotalElement.textContent = `$${data.item_total.toFixed(2)}`;
                    }
                    
                    const cartTotalElement = document.getElementById('cart-total');
                    if (cartTotalElement) {
                        cartTotalElement.textContent = `$${data.cart_total.toFixed(2)}`;
                    }
                    
                    // Update cart count
                    updateCartCount(data.cart_count);
                    
                    // Show success message
                    showNotification('Cart updated', 'success');
                    
                    // If quantity is 0, remove the row
                    if (quantity === 0) {
                        const row = document.getElementById(`cart-row-${productId}`);
                        if (row) {
                            row.remove();
                        }
                        
                        // If cart is empty, show empty message
                        if (data.cart_count === 0) {
                            const cartTable = document.querySelector('.cart-table');
                            if (cartTable) {
                                cartTable.innerHTML = '<tr><td colspan="5" class="text-center">Your cart is empty</td></tr>';
                            }
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Failed to update cart', 'danger');
            });
        });
    });
    
    // Remove from cart
    const removeButtons = document.querySelectorAll('.remove-from-cart');
    removeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            const productId = this.dataset.productId;
            const url = `/cart/remove/${productId}`;
            
            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Remove row from table
                    const row = document.getElementById(`cart-row-${productId}`);
                    if (row) {
                        row.remove();
                    }
                    
                    // Update cart count
                    updateCartCount(data.cart_count);
                    
                    // Update cart total
                    const cartTotalElement = document.getElementById('cart-total');
                    if (cartTotalElement) {
                        cartTotalElement.textContent = `$${data.cart_total.toFixed(2)}`;
                    }
                    
                    // Show success message
                    showNotification('Product removed from cart', 'info');
                    
                    // If cart is empty, show empty message
                    if (data.cart_count === 0) {
                        const cartTable = document.querySelector('.cart-table');
                        if (cartTable) {
                            cartTable.innerHTML = '<tr><td colspan="5" class="text-center">Your cart is empty</td></tr>';
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Failed to remove product from cart', 'danger');
            });
        });
    });
});

/**
 * Update the cart count in the navbar
 * @param {number} count - The new cart count
 */
function updateCartCount(count) {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
        
        // Show or hide based on count
        if (count > 0) {
            cartCountElement.classList.remove('d-none');
        } else {
            cartCountElement.classList.add('d-none');
        }
    }
}

/**
 * Show a notification message
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, info, warning, danger)
 */
function showNotification(message, type) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0 position-fixed bottom-0 end-0 m-3`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Create toast content
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add to document
    document.body.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();
    
    // Remove from DOM after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        document.body.removeChild(toast);
    });
}
