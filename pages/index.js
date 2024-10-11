import styles from "@/styles/Home.module.css"
import Image from "next/image"
import Link from "next/link"
import Head from "next/head"
export default function Home() {
  return (
    <>
    <Head>
      <title>หน้าแรก | jopraetaro</title>
      <meta name="keywords" content="vintage,ขายเสื้อผ้า,รองเท้า"/>
    </Head>
      <div className={styles.container}>
        <h1 className={styles.title}>หน้าแรกของเว็บไชต์</h1>
        <Image src="/shopping.svg" width={300} height={300} alt="logo"/>
        <p>welcome to prae shop</p>
        <Link href="/products" className={styles.btn}>ดูสินค้าทั้งหมด</Link>
      </div>

    </>
  )
}
