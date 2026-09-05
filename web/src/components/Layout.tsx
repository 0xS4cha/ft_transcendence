import { Outlet } from 'react-router-dom';
import { AppSidebar } from '@/components/App-sidebar';
import { SidebarInset, SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';

export default function Layout() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset className="relative min-h-screen bg-[#07070B]">
        <header className="sticky top-0 z-40 
                        flex h-14 w-full items-center
                        justify-between border-b
                        border-white/5 bg-[#07070B]/80
                        px-4 backdrop-blur md:hidden">
          <div className="flex items-center gap-3">
            <SidebarTrigger className="h-8 w-8 rounded-md text-neutral-400 
                                    over:bg-white/10 hover:text-white" />
            <span className="bg-gradient-to-r from-[#4E80EE] via-[#38E1FF] to-[#70A6FF] bg-clip-text text-base font-bold tracking-wide text-transparent">
              tactyx
            </span>
          </div>
        </header>
        <main>
          <Outlet />
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}