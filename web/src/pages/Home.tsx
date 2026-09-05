import { Hero } from "@/components/hero"

export default function Home() {
    return (
    <div className="relative w-full min-h-screen bg-[red]">
        <Hero />
        <div className="absolute inset-0 z-0 bg-red"></div>
    </div>
    )
}