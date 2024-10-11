import { useCart } from '../context/CartContext'; // Ensure this path is correct
import { useState } from 'react';
import { useRouter } from 'next/router'; // Import useRouter for redirection

const Checkout = () => {
  const { cartItems } = useCart();
  const [discountCode, setDiscountCode] = useState('');
  const [discountApplied, setDiscountApplied] = useState(false);
  const router = useRouter(); // Initialize the router

  // Calculate total price before discount
  const calculateTotal = () => {
    if (cartItems.length === 0) return 0;

    return cartItems.reduce((sum, item) => {
      const price = parseFloat(item.price) || 0;
      const quantity = parseInt(item.quantity) || 0;
      return sum + (price * quantity);
    }, 0);
  };

  // Calculate discounted total if discount is applied
  const calculateDiscountedTotal = () => {
    const total = calculateTotal();
    return discountApplied ? total * 0.9 : total;
  };

  const handleDiscountApply = () => {
    if (discountCode === '111') {
      setDiscountApplied(true);
    } else {
      alert('Invalid discount code');
    }
  };

  const handleConfirmPayment = () => {
    // Simulate a real payment process here (or integrate with an actual API)
    // Redirect to the status page with payment status set to 'pending'
    router.push('/status?status=pending');
  };

  return (
    <div>
      <h1>Checkout</h1>
      {cartItems.length === 0 ? (
        <p>Your cart is empty. Please add items to your cart before proceeding.</p>
      ) : (
        <div>
          <h2>Your Order</h2>
          <ul>
            {cartItems.map((item) => (
              <li key={item.id}>
                <p>
                  {item.title} - Quantity: {item.quantity} - Price: ${item.price.toFixed(2)}
                </p>
              </li>
            ))}
          </ul>
          <h3>Total: ${calculateDiscountedTotal().toFixed(2)}</h3>
          <div>
            <input
              type="text"
              placeholder="Enter discount code"
              value={discountCode}
              onChange={(e) => setDiscountCode(e.target.value)}
            />
            <button onClick={handleDiscountApply}>Apply Discount</button>
            {discountApplied && <p>Discount applied!</p>}
          </div>
          <button onClick={handleConfirmPayment}>Confirm Payment</button>
        </div>
      )}
    </div>
  );
};

export default Checkout;
