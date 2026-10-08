import {
  Home,
  Sword,
  Shield,
  Layers,
  FileText,
  Hammer,
  Sparkle,
  Trophy,
  PanelLeft,
  ChevronLeft,
  ChevronRight,
  User,
  LogOut,
  SearchIcon
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
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { useAppDispatch } from "@/store/hooks"
import { logoutUser } from "@/store/reducers/userSlice";
import { SearchInput } from '@/components/search/input';
import { useTranslation } from 'react-i18next';

interface NavItem {
  readonly label: string;
  readonly href: string;
  readonly icon: React.ComponentType<{ className?: string }>;
}

const NAV_ITEMS: readonly NavItem[] = [
  { label: 'nav.home', href: '/', icon: Home },
  { label: 'nav.units', href: '/units', icon: Sword },
  { label: 'nav.items', href: '/items', icon: Shield },
  { label: 'nav.traits', href: '/traits', icon: Layers },
  { label: 'nav.augments', href: '/augments', icon: Sparkle },
  { label: 'nav.teamBuilder', href: '/builder', icon: Hammer },
  { label: 'nav.set18Update', href: '/patch_note', icon: FileText },
  { label: 'nav.ranking', href: '/ranking', icon: Trophy },
] as const;

export function AppSidebar() {
  const { toggleSidebar, setOpen, open } = useSidebar();
  const dispatch = useAppDispatch();
  const { isAuthenticated, username, picture, email } = useAppSelector(state => state.user);
  const { t } = useTranslation();

  function handleLogout() {
    dispatch(logoutUser()).unwrap();
  };

  return (
    <Sidebar
      collapsible="icon"
      className="bg-background py-8 text-foreground dark:text-neutral-300"
      variant="floating"
    >
      <SidebarHeader className="flex h-14 flex-row items-center justify-between border-b border-border px-3 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0 dark:border-white/5">
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
          className="group/toggle relative flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-foreground group-data-[collapsible=icon]:hidden dark:text-neutral-400 dark:hover:bg-white/10 dark:hover:text-white"
        >
          <PanelLeft className="h-4 w-4 transition-opacity duration-150 group-hover/toggle:opacity-0" />
          <ChevronLeft className="absolute h-4 w-4 -translate-x-0.5 opacity-0 transition-all duration-150 group-hover/toggle:opacity-100" />
        </button>

        <button
          type="button"
          onClick={toggleSidebar}
          className="group/reopen relative hidden h-8 w-8 items-center justify-center rounded-md transition-colors hover:bg-muted group-data-[collapsible=icon]:flex dark:hover:bg-white/10"
        >
          <span className="bg-linear-to-r from-[#4E80EE] via-[#38E1FF] to-[#70A6FF] bg-clip-text font-mono text-[11px] font-black tracking-tighter text-transparent transition-opacity duration-150 group-hover/reopen:opacity-0">
            tactyx
          </span>
          <ChevronRight className="absolute h-4 w-4 translate-x-0.5 text-muted-foreground opacity-0 transition-all duration-150 group-hover/reopen:opacity-100 dark:text-neutral-200" />
        </button>
      </SidebarHeader>

      <SidebarContent className=" px-2 py-3 group-data-[collapsible=icon]:px-1.5 ">
        <SidebarGroup className="p-0">
          <SidebarGroupContent>
            <div className="mb-2 py-2 group-data-[collapsible=icon]:hidden">
              <SearchInput />
            </div>
            <SidebarMenu className="gap-2">
              {!open && (
                <SidebarMenuItem key="search">
                  <button
                    onClick={() => setOpen(true)}
                    className="group/item flex h-8 w-full items-center gap-3 rounded-md px-2.5 text-[13px] font-normal transition-colors group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0 text-muted-foreground hover:bg-muted/60 hover:text-foreground dark:text-neutral-400 dark:hover:bg-white/4 dark:hover:text-white"
                  >
                    <SearchIcon className="h-4 w-4 shrink-0 stroke-[1.5] text-muted-foreground transition-colors group-hover/item:text-foreground dark:text-neutral-400 dark:group-hover/item:text-white" />
                    <span className="truncate group-data-[collapsible=icon]:hidden">
                      Search
                    </span>
                  </button>
                </SidebarMenuItem>
              )}
              {NAV_ITEMS.map((item) => (
                <SidebarMenuItem key={item.href}>
                  <NavLink
                    to={item.href}
                    className={({ isActive }) =>
                      cn(
                        'group/item flex h-8 items-center gap-3 rounded-md px-2.5 text-[13px] font-normal transition-colors group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0',
                        isActive
                        ? 'bg-muted/80 font-medium text-foreground shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08)] dark:bg-white/10 dark:text-white'
                        : 'text-muted-foreground hover:bg-muted/60 hover:text-foreground dark:text-neutral-400 dark:hover:bg-white/4 dark:hover:text-white',
                      )
                    }
                    >
                    <item.icon className="h-4 w-4 shrink-0 stroke-[1.5] text-muted-foreground transition-colors group-hover/item:text-foreground dark:text-neutral-400 dark:group-hover/item:text-white"/>
                    <span className="truncate group-data-[collapsible=icon]:hidden">
                      {t(item.label)}
                    </span>
                  </NavLink>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter className="border-t border-border p-2 dark:border-white/5">
        <DropdownMenu>
          <DropdownMenuTrigger render={
            <button
              className="flex h-10 w-full items-center gap-3 rounded-md px-2 text-muted-foreground transition-colors hover:bg-muted/60 hover:text-foreground group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0 dark:text-neutral-400 dark:hover:bg-white/4 dark:hover:text-white"
            >
              <Avatar>
                <AvatarImage src={picture} alt={username} />
                <AvatarFallback>
                  <User />
                </AvatarFallback>
              </Avatar>

              <div className="flex flex-col overflow-hidden text-left group-data-[collapsible=icon]:hidden">
                <span className="truncate text-xs font-medium text-foreground dark:text-neutral-200">
                  {isAuthenticated ? username : t('common.guest')}
                </span>

                <span className="truncate text-[10px] text-muted-foreground dark:text-neutral-500">
                  {isAuthenticated ? email : t('common.login')}
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
                <DropdownMenuItem render={
                  <Link to="/profile">
                    {t('common.profile')}
                  </Link>
                }/>
                <DropdownMenuItem
                  variant="destructive"
                  onClick={handleLogout}
                >
                  <LogOut />
                  {t('common.logout')}
                </DropdownMenuItem>
              </>
            ) : (
              <DropdownMenuItem render={
                <Link to="/authenticate">
                  {t('common.login')}
                </Link>
              }/>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarFooter>
    </Sidebar>
  );
}