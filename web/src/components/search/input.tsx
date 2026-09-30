import { Fragment, useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion, useReducedMotion, type Variants } from "motion/react";
import {
  GemIcon,
  HexagonIcon,
  PackageIcon,
  SearchIcon,
  SearchXIcon,
  SwordsIcon,
  UserIcon,
  XIcon,
  type LucideIcon,
} from "lucide-react";

import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Kbd } from "@/components/ui/kbd";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { Spinner } from "@/components/ui/spinner";
import {
  Empty,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
  EmptyDescription,
} from "@/components/ui/empty";
import { toast } from "@/components/ui/toast";
import { cn, initialsOf, errorMessage } from "@/lib/utils";
import { getSearchFromQuery } from "@/services/searchService";
import { type search as SearchResult } from "@/types/search";


type SearchEntry = {
  id?: string | number;
  name?: string;
  username?: string;
  picture?: string;
  icon?: string;
};

type SectionKey = "unit" | "user" | "trait" | "augment" | "item";

const SECTIONS: { key: SectionKey; label: string; icon: LucideIcon }[] = [
  { key: "unit", label: "Units", icon: SwordsIcon },
  { key: "user", label: "Users", icon: UserIcon },
  { key: "trait", label: "Traits", icon: HexagonIcon },
  { key: "augment", label: "Augments", icon: GemIcon },
  { key: "item", label: "Items", icon: PackageIcon },
];

const EMPTY_RESULT: SearchResult = {
  length: 0,
  unit: [],
  user: [],
  trait: [],
  augment: [],
  item: [],
};

const DEBOUNCE_MS = 250;

const labelOf = (entry: SearchEntry) => entry.name ?? entry.username ?? "";
const imageOf = (entry: SearchEntry) => entry.picture ?? entry.icon;

const listVariants: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.03 } },
};

const rowVariants: Variants = {
  hidden: { opacity: 0, y: 6 },
  visible: { opacity: 1, y: 0 },
};

function Highlight({ text, query }: { text: string; query: string }) {
  if (!query) return <>{text}</>;
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const parts = text.split(new RegExp(`(${escaped})`, "ig"));
  return (
    <>
      {parts.map((part, index) =>
        part.toLowerCase() === query.toLowerCase() ? (
          <mark key={index} className="text-foreground rounded-sm bg-primary/20 px-0.5">
            {part}
          </mark>
        ) : (
          <Fragment key={index}>{part}</Fragment>
        ),
      )}
    </>
  );
}

function ResultsSkeleton() {
  return (
    <div className="flex flex-col gap-3 p-3" aria-hidden>
      {["w-32", "w-44", "w-28"].map((width) => (
        <div key={width} className="flex items-center gap-3">
          <Skeleton className="size-7 shrink-0 rounded-full" />
          <Skeleton className={cn("h-4", width)} />
        </div>
      ))}
    </div>
  );
}

export function SearchInput({
  onSelect,
}: {
  onSelect?: (section: SectionKey, entry: SearchEntry) => void;
}) {
  const reduceMotion = useReducedMotion();
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState("");
  const [data, setData] = useState<{ query: string; result: SearchResult } | null>(null);
  const [loading, setLoading] = useState(false);

  const trimmed = query.trim();

  useEffect(() => {
    if (!trimmed) {
      setData(null);
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);

    const timeout = setTimeout(async () => {
      try {
        const result = await getSearchFromQuery(trimmed);
        if (!cancelled) setData({ query: trimmed, result });
      } catch (error) {
        if (!cancelled) {
          toast.add({
            type: "error",
            title: "Search failed",
            description: errorMessage(error),
          });
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }, DEBOUNCE_MS);

    return () => {
      cancelled = true;
      clearTimeout(timeout);
    };
  }, [trimmed]);

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      const target = event.target as HTMLElement;
      const typing =
        target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable;
      if (event.key === "/" && !typing) {
        event.preventDefault();
        inputRef.current?.focus();
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const result = data?.result ?? EMPTY_RESULT;

  const sections = useMemo(
    () =>
      SECTIONS.map((section) => ({
        ...section,
        entries: (result[section.key] ?? []) as SearchEntry[],
      })).filter((section) => section.entries.length > 0),
    [result],
  );

  const total = sections.reduce((sum, section) => sum + section.entries.length, 0);
  const isOpen = trimmed.length > 0;
  const hasNoResults = !loading && data?.query === trimmed && total === 0;
  const showSkeleton = loading && total === 0;

  function clear() {
    setQuery("");
    inputRef.current?.focus();
  }

  const t = reduceMotion ? { duration: 0 } : { duration: 0.15, ease: "easeOut" as const };

  return (
    <div className="relative w-full max-w-sm">
      <InputGroup>
        <InputGroupInput
          ref={inputRef}
          placeholder="Search units, items, users…"
          value={query}
          autoComplete="off"
          aria-label="Search"
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => setQuery(event.target.value)}
          onKeyDown={(event: React.KeyboardEvent<HTMLInputElement>) => {
            if (event.key === "Escape") clear();
          }}
        />
        <InputGroupAddon>
          <SearchIcon />
        </InputGroupAddon>
        <InputGroupAddon align="inline-end" className="gap-1">
          {loading ? (
            <Spinner />
          ) : isOpen ? (
            <Badge variant="secondary" className="tabular-nums">
              {total} {total === 1 ? "result" : "results"}
            </Badge>
          ) : (
            <Kbd>/</Kbd>
          )}
          {isOpen && (
            <InputGroupButton size="icon-xs" onClick={clear} aria-label="Clear search">
              <XIcon />
            </InputGroupButton>
          )}
        </InputGroupAddon>
      </InputGroup>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            key="panel"
            initial={{ opacity: 0, y: -6, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -6, scale: 0.98 }}
            transition={t}
            className="bg-popover text-popover-foreground absolute top-full z-50 mt-2 w-full origin-top overflow-hidden rounded-xl border shadow-md"
          >
            <div
              className={cn(
                "max-h-80 overflow-y-auto transition-opacity",
                loading && total > 0 && "opacity-60",
              )}
              aria-live="polite"
              aria-busy={loading}
            >
              {showSkeleton && <ResultsSkeleton />}

              {hasNoResults && (
                <Empty className="p-6">
                  <EmptyHeader>
                    <EmptyMedia variant="icon">
                      <SearchXIcon />
                    </EmptyMedia>
                    <EmptyTitle>No results</EmptyTitle>
                    <EmptyDescription>Nothing matches “{trimmed}”.</EmptyDescription>
                  </EmptyHeader>
                </Empty>
              )}

              {sections.map((section, index) => (
                <div key={section.key}>
                  {index > 0 && <Separator />}
                  <div className="p-2">
                    <div className="text-muted-foreground flex items-center gap-2 px-2 py-1.5 text-xs font-medium">
                      <section.icon className="size-3.5" />
                      {section.label}
                      <Badge variant="outline" className="ml-auto tabular-nums">
                        {section.entries.length}
                      </Badge>
                    </div>

                    <motion.ul
                      key={`${section.key}-${data?.query}`}
                      variants={listVariants}
                      initial={reduceMotion ? "visible" : "hidden"}
                      animate="visible"
                    >
                      {section.entries.map((entry, entryIndex) => {
                        const label = labelOf(entry);
                        return (
                          <motion.li
                            key={entry.id ?? `${label}-${entryIndex}`}
                            variants={rowVariants}
                            transition={t}
                          >
                            <button
                              type="button"
                              onClick={() => onSelect?.(section.key, entry)}
                              className="hover:bg-accent focus-visible:bg-accent flex w-full items-center gap-3 rounded-lg px-2 py-1.5 text-left text-sm transition-colors focus-visible:outline-none"
                            >
                              <Avatar className="size-7 shrink-0">
                                <AvatarImage src={imageOf(entry)} />
                                <AvatarFallback className="text-[10px]">
                                  {initialsOf(label)}
                                </AvatarFallback>
                              </Avatar>
                              <span className="min-w-0 flex-1 truncate">
                                <Highlight text={label} query={trimmed} />
                              </span>
                            </button>
                          </motion.li>
                        );
                      })}
                    </motion.ul>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}