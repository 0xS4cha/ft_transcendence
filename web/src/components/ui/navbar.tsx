import { NavLink, Link } from "react-router-dom";
import { cn } from "@/lib/utils";

interface NavItem {
  readonly label: string;
  readonly href: string;
}

const NAV_ITEMS: readonly NavItem[] = [
  { label: 'units', href: '/units' },
  { label: 'items', href: '/items' },
  { label: 'traits', href: '/traits' },
  { label: 'patch note', href: '/patch_note' },
  { label: 'builder', href: '/builder' },
  { label: 'meta', href: '/meta' },
  { label: 'ranking', href: '/ranking' },
] as const;

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/5 bg-[#07070B]/90 backdrop-blur-md">
      <div className="flex h-16 w-full items-center justify-between px-8">
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
                  isActive ? 'text-white' : 'text-neutral-400 hover:text-neutral-200',
                )
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <Link
          to="/profile"
          className="flex items-center gap-2.5 text-sm font-normal text-neutral-400 transition-colors hover:text-white"
        >
          <div className="h-7 w-7 rounded-full border border-white/10 bg-neutral-800" />
          <span>user</span>
        </Link>
      </div>
    </header>
  );
}
