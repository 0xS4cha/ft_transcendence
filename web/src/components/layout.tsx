import { Outlet } from 'react-router-dom';
import { AppSidebar } from '@/components/app_sidebar';
import { SidebarInset, SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';

export default function Layout() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset className="relative min-h-screen">
        <header 
          className="sticky z-40 
            flex h-14 w-full border-b
            border-border bg-card px-4 backdrop-blur md:hidden dark:border-white/5 dark:bg-[#202020]"
            >
          <div className="flex items-center gap-3">
            <SidebarTrigger
              className="h-8 w-8 text-muted-foreground
                hover:bg-muted hover:text-foreground dark:text-neutral-400 dark:hover:bg-white/10 dark:hover:text-white"
                />
            <span className="bg-linear-to-r from-[#4E80EE] via-[#38E1FF] to-[#70A6FF] bg-clip-text text-base font-bold tracking-wide text-transparent">
              tactyx
            </span>
          </div>
        </header>
        <main className="mx-3 py-8">
        <Outlet />
      </main>
      </SidebarInset>
    </SidebarProvider>
  );
}