import { Outlet } from 'react-router-dom';
import { Navbar } from "@/components/ui/navbar";

export default function Layout() {
    return (
        <div className="min-h-screen flex flex-col">
            <Navbar />
            <main className="flex-1">
                <Outlet />
                <span> <br /> <br /> <br />coucou</span>
            </main>
        </div>
    )
}