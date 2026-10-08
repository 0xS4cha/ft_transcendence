import { NavLink, Link } from "react-router-dom";
import { cn } from "@/lib/utils";
import { useAppSelector } from "@/store/hooks";
import { useTranslation } from "react-i18next";

interface NavItem {
  readonly label: string;
  readonly href: string;
}

const NAV_ITEMS: readonly NavItem[] = [
  { label: 'nav.units', href: '/units' },
  { label: 'nav.items', href: '/items' },
  { label: 'nav.traits', href: '/traits' },
  { label: 'nav.augments', href: '/augments' },
  { label: 'nav.patchNote', href: '/patch_note' },
  { label: 'nav.teamBuilder', href: '/builder' },
  { label: 'nav.meta', href: '/meta' },
  { label: 'nav.ranking', href: '/ranking' },
] as const;

export function Navbar() {
  const { isAuthenticated, email } = useAppSelector(state => state.user);
  const { t } = useTranslation();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-card/80 backdrop-blur dark:border-white/5 dark:bg-[#202020]">
      <div className="flex h-16 w-full items-center justify-between px-8 ">
        <Link
          to="/"
          className="bg-linear-to-r from-[#4E80EE] via-[#38E1FF] to-[#70A6FF] bg-clip-text text-xl font-bold tracking-wide text-transparent"
        >
          tactyx
        </Link>
        <nav className="flex items-center gap-8">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.href}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  'text-sm font-normal transition-colors',
                  isActive ? 'text-foreground dark:text-white' : 'text-muted-foreground hover:text-foreground dark:text-neutral-400 dark:hover:text-neutral-200',
                )
              }
            >
              {t(item.label)}
            </NavLink>
          ))}
        </nav>
        <Link
          to={isAuthenticated ? "/profile" : "/authenticate"}
          className="flex items-center gap-2.5 text-sm font-normal text-muted-foreground transition-colors hover:text-foreground dark:text-neutral-400 dark:hover:text-white"
        >
          <div className="h-7 w-7 rounded-full border border-border bg-muted dark:border-white/10 dark:bg-neutral-800" />
          <span>{isAuthenticated ? email : t('common.guest')}</span>
        </Link>
      </div>
    </header>
  );
}
