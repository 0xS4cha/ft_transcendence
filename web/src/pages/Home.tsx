import { Hero } from "@/components/Hero"
import Layout from "@/components/Layout"

export default function Home() {
    return (
    <div>
        <Hero />
        <div className="absolute inset-0 z-0 bg-red"></div>
    </div>
    )
}