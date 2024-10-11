import { useRouter } from 'next/router';

const Status = () => {
  const router = useRouter();
  const { status } = router.query; // Get status from query parameters

  return (
    <div>
      <h1>Payment Status</h1>
      {status === 'pending' ? (
        <p>Your payment is pending. Please wait for confirmation.</p>
      ) : (
        <p>Invalid payment status.</p>
      )}
    </div>
  );
};

export default Status;
