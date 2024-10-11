import "@/styles/globals.css";
import Layout from "@/components/Layout";
import { CartProvider } from "@/context/CartContext"; // Adjust the path based on your project structure

export default function App({ Component, pageProps }) {
  return (
    <CartProvider>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </CartProvider>
  );
}
