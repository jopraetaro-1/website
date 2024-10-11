import React from 'react';
import { useCart } from '../context/CartContext'; // Adjust the path as needed
import { useRouter } from 'next/router'; // Import useRouter

const Cart = () => {
  const { cartItems, removeFromCart } = useCart();
  const router = useRouter(); // Initialize the useRouter hook

  const handleCheckout = () => {
    // Navigate to the checkout page
    router.push('/checkout');
  };

  return (
    <div>
      <h1>Your Cart</h1>
      {cartItems.length === 0 ? (
        <p>Your cart is empty</p>
      ) : (
        <ul>
          {cartItems.map((item) => (
            <li key={item.id}>
              <img src={item.thumbnail} alt={item.title} width="50" />
              <p>{item.title}</p>
              <p>Quantity: {item.quantity}</p>
              <p>Price: ${item.price}</p>
              <button onClick={() => removeFromCart(item.id)}>Remove</button>
            </li>
          ))}
        </ul>
      )}
      {cartItems.length > 0 && (
        <button onClick={handleCheckout}>Proceed to Checkout</button>
      )}
    </div>
  );
};

export default Cart;
