import { Fragment, useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion, useReducedMotion, type Variants } from "motion/react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import {
  Sword,
  Layers,
  Sparkle,
  SearchIcon,
  SearchXIcon,
  Shield,
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
import { type SearchResult } from "@/types/search";

type SearchEntry = {
  id?: string | number;
  name?: string;
  username?: string;
  picture?: string;
  icon?: string;
  source?: "local" | "riot";
  region?: string;
  tier?: string;
  rank?: string;
  leaguePoints?: number;
  type?: string;
  rarity?: string;
  breakpoint?: string;
};

type SectionKey = "unit" | "user" | "trait" | "augment" | "item";

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

function subtitleOf(
  section: SectionKey,
  entry: SearchEntry,
  t: (key: string, options?: Record<string, unknown>) => string,
): string {
  if (section === "user") {
    const rank = [entry.tier, entry.rank].filter(Boolean).join(" ");
    const lp = entry.leaguePoints != null ? `${entry.leaguePoints} ${t("search.lp")}` : "";
    const source = entry.source === "riot" ? t("search.riot") : t("search.app");
    return [source, entry.region, rank, lp].filter(Boolean).join(" • ");
  }

  if (section === "item") return entry.type ? `${t("search.type")}: ${entry.type}` : "";
  if (section === "trait") return entry.breakpoint ? `${t("search.breakpoint")}: ${entry.breakpoint}` : "";
  if (section === "augment") return entry.rarity ? `${t("search.rarity")}: ${entry.rarity}` : "";

  return "";
}

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
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);
  const { t } = useTranslation();
  const [query, setQuery] = useState("");
  const [data, setData] = useState<{ query: string; result: SearchResult } | null>(null);
  const [failedQuery, setFailedQuery] = useState<string | null>(null);
  const [activeSection, setActiveSection] = useState<"all" | SectionKey>("all");
  const [activeIndex, setActiveIndex] = useState(-1);

  const SECTIONS: { key: SectionKey; label: string; icon: LucideIcon }[] = useMemo(() => [
    { key: "unit", label: t("search.units"), icon: Sword },
    { key: "user", label: t("search.users"), icon: UserIcon },
    { key: "trait", label: t("search.traits"), icon: Layers },
    { key: "augment", label: t("search.augments"), icon: Sparkle },
    { key: "item", label: t("search.items"), icon: Shield },
  ], [t]);

  const trimmed = query.trim();
  const loading = trimmed.length > 0 && data?.query !== trimmed && failedQuery !== trimmed;

  useEffect(() => {
    if (!trimmed) {
      return;
    }

    let cancelled = false;

    const timeout = setTimeout(async () => {
      try {
        const result = await getSearchFromQuery(trimmed);
        if (!cancelled) setData({ query: trimmed, result });
      } catch (error) {
        if (!cancelled) {
          setFailedQuery(trimmed);
          toast.add({
            type: "error",
            title: t("search.failed"),
            description: errorMessage(error),
          });
        }
      }
    }, DEBOUNCE_MS);

    return () => {
      cancelled = true;
      clearTimeout(timeout);
    };
  }, [trimmed, t]);

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
        entries: ((result[section.key] ?? []) as SearchEntry[]).filter((entry) => Boolean(labelOf(entry))),
      })).filter((section) => section.entries.length > 0),
    [SECTIONS, result],
  );

  const visibleSections = useMemo(() => {
    if (activeSection === "all") return sections;
    return sections.filter((section) => section.key === activeSection);
  }, [activeSection, sections]);

  const indexedSections = useMemo(() => {
    let index = 0;
    return visibleSections.map((section) => ({
      ...section,
      indexedEntries: section.entries.map((entry) => ({ entry, index: index++ })),
    }));
  }, [visibleSections]);

  const flatResults = useMemo(
    () =>
      indexedSections.flatMap((section) =>
        section.indexedEntries.map((indexedEntry) => ({
          section: section.key,
          entry: indexedEntry.entry,
        })),
      ),
    [indexedSections],
  );

  const resultsKey = `${trimmed}|${activeSection}|${flatResults.length}`;
  const [activeIndexKey, setActiveIndexKey] = useState(resultsKey);
  if (activeIndexKey !== resultsKey) {
    setActiveIndexKey(resultsKey);
    setActiveIndex(flatResults.length > 0 ? 0 : -1);
  }

  const total = visibleSections.reduce((sum, section) => sum + section.entries.length, 0);
  const isOpen = trimmed.length > 0;
  const hasNoResults = !loading && data?.query === trimmed && total === 0;
  const showSkeleton = loading && total === 0;

  function clear() {
    setQuery("");
    setActiveIndex(-1);
    inputRef.current?.focus();
  }

  async function handleSelect(section: SectionKey, entry: SearchEntry) {
    if (onSelect) {
      onSelect(section, entry);
      return;
    }

    const label = labelOf(entry);
    if (!label) return;

    if (section === "item") navigate(`/items?q=${encodeURIComponent(label)}`);
    if (section === "unit") navigate(`/units?q=${encodeURIComponent(label)}`);
    if (section === "trait") navigate(`/traits?q=${encodeURIComponent(label)}`);
    if (section === "augment") navigate(`/augments?q=${encodeURIComponent(label)}`);
    if (section === "user") {
      navigate(`/users?q=${encodeURIComponent(label)}`, {
        state: { user: entry },
      });
    }

    clear();
  }

  const animation = reduceMotion ? { duration: 0 } : { duration: 0.15, ease: "easeOut" as const };

  return (
    <div className="relative w-full max-w-sm">
      <InputGroup>
        <InputGroupInput
          ref={inputRef}
          placeholder={t("common.search")}
          value={query}
          autoComplete="off"
          aria-label={t("common.search")}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => setQuery(event.target.value)}
          onKeyDown={(event: React.KeyboardEvent<HTMLInputElement>) => {
            if (event.key === "Escape") clear();
            if (event.key === "ArrowDown") {
              event.preventDefault();
              if (flatResults.length === 0) return;
              setActiveIndex((current) => (current + 1) % flatResults.length);
            }
            if (event.key === "ArrowUp") {
              event.preventDefault();
              if (flatResults.length === 0) return;
              setActiveIndex((current) => (current - 1 + flatResults.length) % flatResults.length);
            }
            if (event.key === "Enter" && activeIndex >= 0) {
              event.preventDefault();
              const selected = flatResults[activeIndex];
              if (selected) void handleSelect(selected.section, selected.entry);
            }
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
              {total} {t("search.result", { count: total })}
            </Badge>
          ) : (
            <Kbd>/</Kbd>
          )}
          {isOpen && (
            <InputGroupButton size="icon-xs" onClick={clear} aria-label={t("search.clear")}>
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
            transition={animation}
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

              {!showSkeleton && sections.length > 0 && (
                <div className="flex flex-wrap gap-1 border-b p-2">
                  <Badge
                    variant={activeSection === "all" ? "default" : "outline"}
                    className="cursor-pointer"
                    onClick={() => setActiveSection("all")}
                  >
                    {t("search.all")}
                  </Badge>
                  {SECTIONS.map((section) => {
                    const count = (result[section.key] ?? []).length;
                    if (!count) return null;
                    return (
                      <Badge
                        key={section.key}
                        variant={activeSection === section.key ? "default" : "outline"}
                        className="cursor-pointer"
                        onClick={() => setActiveSection(section.key)}
                      >
                        {section.label} ({count})
                      </Badge>
                    );
                  })}
                </div>
              )}

              {hasNoResults && (
                <Empty className="p-6">
                  <EmptyHeader>
                    <EmptyMedia variant="icon">
                      <SearchXIcon />
                    </EmptyMedia>
                    <EmptyTitle>{t("search.noResults")}</EmptyTitle>
                    <EmptyDescription>{t("search.noResultsDescription", { query: trimmed })}</EmptyDescription>
                  </EmptyHeader>
                </Empty>
              )}

              {indexedSections.map((section, index) => (
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
                      {section.indexedEntries.map(({ entry, index: sectionIndex }, entryIndex) => {
                        const label = labelOf(entry);
                        const subtitle = subtitleOf(section.key, entry, t);
                        return (
                          <motion.li
                            key={entry.id ?? `${label}-${entryIndex}`}
                            variants={rowVariants}
                            transition={animation}
                          >
                            <button
                              type="button"
                              onClick={() => void handleSelect(section.key, entry)}
                              className={cn(
                                "hover:bg-accent focus-visible:bg-accent flex w-full items-center gap-3 rounded-lg px-2 py-1.5 text-left text-sm transition-colors focus-visible:outline-none",
                                sectionIndex === activeIndex && "bg-accent",
                              )}
                            >
                              <Avatar className="size-7 shrink-0">
                                <AvatarImage src={imageOf(entry)} />
                                <AvatarFallback className="text-[10px]">
                                  {initialsOf(label)}
                                </AvatarFallback>
                              </Avatar>
                              <span className="min-w-0 flex-1">
                                <span className="block truncate">
                                  <Highlight text={label} query={trimmed} />
                                </span>
                                {subtitle && (
                                  <span className="text-muted-foreground block truncate text-xs">
                                    {subtitle}
                                  </span>
                                )}
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