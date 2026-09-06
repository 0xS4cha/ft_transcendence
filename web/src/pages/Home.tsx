import { AppPreview } from "@/components/App-preview"
import { Hero } from "@/components/Hero"

export default function Home() {
    return (
    <div>
        <Hero />
        <AppPreview />
        <div className="absolute inset-0 z-0 bg-red"></div>
    </div>
    )
}