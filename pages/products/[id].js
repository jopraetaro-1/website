import Head from "next/head";
import Image from "next/image";
import Styles from "@/styles/detail.module.css";
import shirts from "@/data/shirts"; // Adjust the path based on your project structure
import { useState } from "react"; // Import useState
import { useCart } from "@/context/CartContext"; // Import useCart

export async function getStaticPaths() {
    const paths = shirts.map((item) => {
        return {
            params: { id: String(item.id) }
        };
    });
    return {
        paths,
        fallback: false
    };
}

export async function getStaticProps({ params }) {
    const id = params.id;
    const product = shirts.find((item) => item.id === parseInt(id));
    
    return {
        props: { product }
    };
}

export default function ProductDetail({ product }) {
    const [quantity, setQuantity] = useState(1);
    const { addToCart } = useCart(); // Use the addToCart function from context
    const [message, setMessage] = useState(""); // State to hold confirmation message

    const handleAddToCart = () => {
        const validQuantity = Math.min(Math.max(quantity, 1), product.stock); // Ensure quantity is valid
        addToCart(product, validQuantity); // Add the product with valid quantity to the cart
        console.log(`Added ${validQuantity} of ${product.title} to cart`);
        setMessage(`Added ${validQuantity} of ${product.title} to cart!`); // Set confirmation message
    };

    const handleQuantityChange = (e) => {
        const value = Math.max(1, Math.min(product.stock, parseInt(e.target.value) || 1));
        setQuantity(value);
    };

    return (
        <>
            <Head>
                <title>{product.title}</title>
            </Head>
            <div className={Styles.container}>
                <div>
                    <Image src={product.thumbnail} width={300} height={300} alt={product.title} />
                </div>
                <div className={Styles.detail}>
                    <h1>ชื่อสินค้า : {product.title}</h1>
                    <h2>ราคา : ${product.price}</h2>
                    <h2>หมวดหมู่ : {product.category}</h2>
                    <h3>ไซส์ : {product.size}</h3>
                    <h4>สต๊อก : {product.stock}</h4>
                    <p>ข้อมูล : {product.description}</p>
                    
                    <div>
                        <label htmlFor="quantity">จำนวน: </label>
                        <input
                            type="number"
                            id="quantity"
                            value={quantity}
                            min="1"
                            max={product.stock}
                            onChange={handleQuantityChange} // Update the handler here
                            onBlur={() => setQuantity(Math.min(quantity, product.stock))} // Reset on blur
                        />
                    </div>

                    <button onClick={handleAddToCart}>
                        เพิ่มไปยังรถเข็น
                    </button>

                    {message && <p>{message}</p>} {/* Display confirmation message */}
                </div>
            </div>
        </>
    );
}
