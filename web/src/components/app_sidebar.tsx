import {
  Home,
  Sword,
  Shield,
  Layers,
  FileText,
  Hammer,
  TrendingUp,
  Trophy,
  PanelLeft,
  ChevronLeft,
  ChevronRight,
  User,
  LogOut
} from 'lucide-react';
import { NavLink, Link } from 'react-router-dom';

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  useSidebar,
} from '@/components/ui/sidebar';
import { cn } from '@/lib/utils';
import { useAppSelector } from '@/store/hooks';

import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import {
  InputGroup,
  InputGroupInput,
} from "@/components/ui/input-group"

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { useAppDispatch } from "@/store/hooks"
import { logoutUser } from "@/store/reducers/userSlice";


interface NavItem {
  readonly label: string;
  readonly href: string;
  readonly icon: React.ComponentType<{ className?: string }>;
}

const NAV_ITEMS: readonly NavItem[] = [
  { label: 'Home', href: '/', icon: Home },
  { label: 'Top comps', href: '/top_comp', icon: TrendingUp },
  { label: 'Units', href: '/units', icon: Sword },
  { label: 'Items', href: '/items', icon: Shield },
  { label: 'Traits', href: '/traits', icon: Layers },
  { label: 'Team builder', href: '/builder', icon: Hammer },
  { label: 'Set 18 update', href: '/patch_note', icon: FileText },
  { label: 'Ranking', href: '/ranking', icon: Trophy },
] as const;

export function AppSidebar() {
  const { state, toggleSidebar } = useSidebar();
  const dispatch = useAppDispatch();
  const isCollapsed = state === 'collapsed';
  const { isAuthenticated, username, picture } = useAppSelector(state => state.user);
  console.log(isCollapsed);

  function handleLogout() {
    dispatch(logoutUser()).unwrap();
  };

  return (
    <Sidebar
      collapsible="icon"
      className="text-neutral-300 bg-background py-8"
      variant="floating"
    >
      <SidebarHeader className="flex h-14 flex-row items-center justify-between border-b border-white/5 px-3 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0">
        <Link
          to="/"
          className="flex items-center px-2 group-data-[collapsible=icon]:hidden"
        >
          <span className="bg-linear-to-r from-[#4E80EE] via-[#38E1FF] to-[#70A6FF] bg-clip-text text-lg font-bold tracking-wide text-transparent">
            tactyx
          </span>
        </Link>

        <button
          type="button"
          onClick={toggleSidebar}
          className="group/toggle relative flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-neutral-400 transition-colors hover:bg-white/10 hover:text-white group-data-[collapsible=icon]:hidden"
        >
          <PanelLeft className="h-4 w-4 transition-opacity duration-150 group-hover/toggle:opacity-0" />
          <ChevronLeft className="absolute h-4 w-4 -translate-x-0.5 opacity-0 transition-all duration-150 group-hover/toggle:opacity-100" />
        </button>

        <button
          type="button"
          onClick={toggleSidebar}
          className="group/reopen relative hidden h-8 w-8 items-center justify-center rounded-md transition-colors hover:bg-white/10 group-data-[collapsible=icon]:flex"
        >
          <span className="bg-linear-to-r from-[#4E80EE] via-[#38E1FF] to-[#70A6FF] bg-clip-text font-mono text-[11px] font-black tracking-tighter text-transparent transition-opacity duration-150 group-hover/reopen:opacity-0">
            TACTYX
          </span>
          <ChevronRight className="absolute h-4 w-4 translate-x-0.5 text-neutral-200 opacity-0 transition-all duration-150 group-hover/reopen:opacity-100" />
        </button>
      </SidebarHeader>

      <SidebarContent className=" px-2 py-3 group-data-[collapsible=icon]:px-1.5 ">
        <SidebarGroup className="p-0">
          <SidebarGroupContent>
            <div className="mb-2 py-2 group-data-[collapsible=icon]:hidden">
             <InputGroup>
            <InputGroupInput placeholder="Search..." />
          </InputGroup>
            </div>
            <SidebarMenu className="gap-2">
              {NAV_ITEMS.map((item) => (
                <SidebarMenuItem key={item.href}>
                  <NavLink
                    to={item.href}
                    className={({ isActive }) =>
                      cn(
                        'group/item flex h-8 items-center gap-3 rounded-md px-2.5 text-[13px] font-normal transition-colors group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0',
                        isActive
                          ? 'bg-white/10 font-medium text-white shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08)]'
                          : 'text-neutral-400 hover:bg-white/[0.04] hover:text-white',
                      )
                    }
                  >
                    <item.icon className="h-4 w-4 shrink-0 stroke-[1.5] text-neutral-400 transition-colors group-hover/item:text-white"/>
                    <span className="truncate group-data-[collapsible=icon]:hidden">
                      {item.label}
                    </span>
                  </NavLink>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter className="border-t border-white/5 p-2">
        <DropdownMenu>
          <DropdownMenuTrigger render={
            <button
              className="flex h-10 w-full items-center gap-3 rounded-md px-2 text-neutral-400 transition-colors hover:bg-white/[0.04] hover:text-white group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0"
            >
              <Avatar>
                <AvatarImage src={picture} alt={username} />
                <AvatarFallback>
                  <User />
                </AvatarFallback>
              </Avatar>

              <div className="flex flex-col overflow-hidden text-left group-data-[collapsible=icon]:hidden">
                <span className="truncate text-xs font-medium text-neutral-200">
                  {isAuthenticated ? username : "Guest"}
                </span>

                <span className="truncate text-[10px] text-neutral-500">
                  {isAuthenticated ? username : "Log in"}
                </span>
              </div>
            </button>
          }/>

          <DropdownMenuContent
            side="top"
            align="start"
            className="w-52"
          >
            {isAuthenticated ? (
              <>
                <DropdownMenuItem
                  variant="destructive"
                  onClick={handleLogout}
                >
                  <LogOut />
                  Logout
                </DropdownMenuItem>
              </>
            ) : (
              <DropdownMenuItem render={
                <Link to="/authenticate">
                  Log in
                </Link>
              }/>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarFooter>
    </Sidebar>
  );
}