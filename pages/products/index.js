import Head from "next/head";
import Image from "next/image";
import styles from "@/styles/Product.module.css";
import Link from "next/link";
import shirts from "@/data/shirts"; // Adjust the path according to where your shirts.js is located

export default function Index() {
    return (
        <>  
            <Head>
                <title>สินค้าทั้งหมด | jopraetaro</title>
                <meta name="keywords" content="vintage,ขายเสื้อผ้า,รองเท้า"/>
            </Head> 
            <div className={styles.container}>
                {shirts.map(item => (
                    <div key={item.id}>
                        <Link href={'/products/' + item.id}>
                            <h2 className={styles.title}>{item.title}</h2>
                            <Image src={item.thumbnail} width={300} height={300} alt={item.title} />
                        </Link>
                    </div>
                ))}
            </div>
        </>
    );
}
