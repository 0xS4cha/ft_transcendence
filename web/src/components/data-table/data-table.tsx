import { useState, useMemo, Fragment, type Dispatch, type SetStateAction } from "react";
import {
  type ColumnDef,
  type ColumnFiltersState,
  type ColumnVisibilityState,
  type PaginationState,
  type SortingState,
  type ExpandedState,
  type Row,
  type RowData,
  useTable,
} from "@tanstack/react-table";

import {
  ArrowUpDown,
  Search,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { dataTableFeatures } from "@/lib/data-table-features";
import { DataTableFilter } from "@/components/data-table/data-table-filter";
import { DataTablePagination } from "@/components/data-table/data-table-pagination";
import { useTranslation } from "react-i18next";

import { type FilterType } from "@/types/stats";

function hasModel(original: unknown): boolean {
  return typeof original === "object" && original !== null && "model" in original && Boolean(original.model);
}

interface DataTableProps<TData extends RowData> {
  columns: ColumnDef<typeof dataTableFeatures, TData>[];
  data: TData[];
  getRowId: (originalRow: TData, index: number) => string;
  defaultSortId: string;
  searchPlaceholder?: string;
  initialSearchQuery?: string;
  filter: FilterType;
  setFilter: Dispatch<SetStateAction<FilterType>>;
  customToolbar?: React.ReactNode;
  onExpand?: (row: Row<typeof dataTableFeatures, TData>, columns: unknown[]) => React.ReactNode;
  hideRankFilter?: boolean;
  hideQueueFilter?: boolean;
  addAvgSort?: boolean;
  addGlobalServerFilter?: boolean;
}

export function DataTable<TData extends RowData>({
  columns,
  data,
  getRowId,
  setFilter,
  filter,
  defaultSortId,
  addGlobalServerFilter,
  addAvgSort,
  searchPlaceholder = "Search...",
  initialSearchQuery = "",
  onExpand,
  customToolbar,
  hideRankFilter,
  hideQueueFilter,
}: DataTableProps<TData>) {
  
  const { sortOptions, sortOptionState } = useMemo(() => {
    const config = {
      "name-asc":  { label: "Name A-Z", sorting: [{ id: defaultSortId, desc: false }] },
      "name-desc": { label: "Name Z-A", sorting: [{ id: defaultSortId, desc: true }] },
      ...(addAvgSort && {
        "avg-asc":  { label: "Avg. place asc",  sorting: [{ id: "avg_place", desc: false }] },
        "avg-desc": { label: "Avg. place desc", sorting: [{ id: "avg_place", desc: true }] },
      }),
    };

    const entries = Object.entries(config);

    return {
      sortOptions: entries.map(([value, { label }]) => ({ value, label })),
      sortOptionState: Object.fromEntries(
        entries.map(([value, { sorting }]) => [value, sorting])
      ),
    };
  }, [defaultSortId, addAvgSort]);

  const { t } = useTranslation();
  const [rowSelection, setRowSelection] = useState({});
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>(() =>
    initialSearchQuery ? [{ id: "search", value: initialSearchQuery }] : []
  );
  const [sorting, setSorting] = useState<SortingState>([{ id: defaultSortId, desc: false }]);
  const [expanded, setExpanded] = useState<ExpandedState>({});
  const [columnVisibility] = useState<ColumnVisibilityState>({
    search: false,
    avg_place: false,
    name: false
  });
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  });
  const [searchQuery, setSearchQuery] = useState(initialSearchQuery);
  const [syncedSearchQuery, setSyncedSearchQuery] = useState(initialSearchQuery);

  if (syncedSearchQuery !== initialSearchQuery) {
    setSyncedSearchQuery(initialSearchQuery);
    setSearchQuery(initialSearchQuery);
    setColumnFilters((current) => [
      ...current.filter((columnFilter) => columnFilter.id !== "search"),
      ...(initialSearchQuery ? [{ id: "search", value: initialSearchQuery }] : []),
    ]);
    setPagination((current) => ({ ...current, pageIndex: 0 }));
  }

  const table = useTable({
    features: dataTableFeatures,
    data,
    columns,
    state: {
      rowSelection,
      columnFilters,
      sorting,
      columnVisibility,
      pagination,
      expanded
    },
    getRowId,
    enableRowSelection: true,
    onRowSelectionChange: setRowSelection,
    onColumnFiltersChange: setColumnFilters,
    onSortingChange: setSorting,
    onPaginationChange: setPagination,
    onExpandedChange: setExpanded,
    getRowCanExpand: () => true,
  });

  const sortValue = useMemo(() => {
    const currentSort = sorting[0];
    if (currentSort?.id === defaultSortId && !currentSort.desc) return "name-asc";
    if (currentSort?.id === defaultSortId && currentSort.desc) return "name-desc";
    if (currentSort?.id === "avg_place" && !currentSort.desc) return "avg-asc";
    if (currentSort?.id === "avg_place" && currentSort.desc) return "avg-desc"; 
    return "newest";
  }, [sorting, defaultSortId]);

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <DataTableFilter setFilter={setFilter} filter={filter} hideRankFilter={hideRankFilter} hideQueueFilter={hideQueueFilter} addGlobalServerFilter={addGlobalServerFilter}/>
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center xl:w-auto">
          {customToolbar}
          <div className="relative w-full lg:w-80">
            <Search className="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              className="h-7 rounded-[min(var(--radius-md),12px)] pl-8"
              placeholder={searchPlaceholder}
              value={searchQuery}
              onChange={(event) => {
                setSearchQuery(event.target.value);
                table.getColumn("search")?.setFilterValue(event.target.value || undefined);
                table.setPageIndex(0);
              }}
            />
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger render={
              <Button variant="outline" size="sm">
                <ArrowUpDown />
                {t("table.sort", "Sort")}
              </Button>}
              />
            <DropdownMenuContent align="end">
              <DropdownMenuRadioGroup
                value={sortValue}
                onValueChange={(value) => {
                  const next = sortOptionState[value] ?? sortOptionState["name-asc"];
                  table.setSorting(next);
                  table.setPageIndex(0);
                }}
              >
                {sortOptions.map((option) => (
                  <DropdownMenuRadioItem key={option.value} value={option.value}>
                    {option.label}
                  </DropdownMenuRadioItem>
                ))}
              </DropdownMenuRadioGroup>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      <div className="overflow-hidden rounded-lg border bg-card">
        <Table>
          <TableHeader className="bg-muted/15">
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id} colSpan={header.colSpan} className="h-11 p-3 font-medium">
                    {header.isPlaceholder ? null : <table.FlexRender header={header} />}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.length ? (
              table.getRowModel().rows.map((row) => (
                <Fragment key={row.id}>
                  <TableRow key={row.id} data-state={table.state.rowSelection[row.id] && "selected"}>
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id} className="p-3 align-middle">
                        <table.FlexRender cell={cell} />
                      </TableCell>
                    ))}
                  </TableRow>
                 {onExpand && row.getIsExpanded() && hasModel(row.original) && (
                  <>
                    {onExpand(row, columns)}
                 </>
                )}
                </Fragment>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={table.getVisibleLeafColumns().length} className="h-24 text-center">
                  {t("table.noresult", "No results.")}
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex items-center justify-between px-1">
        <div className="flex w-full items-center gap-8 lg:w-fit">
          <div className="hidden items-center gap-2 lg:flex">
            <Label htmlFor="rows-per-page" className="font-medium text-sm">
              {t("table.pagination", "Row per page")}
            </Label>
            <Select
              value={`${table.state.pagination.pageSize}`}
              onValueChange={(value) => {
                table.setPageSize(Number(value));
              }}
            >
              <SelectTrigger size="sm" className="w-20" id="rows-per-page">
                <SelectValue placeholder={table.state.pagination.pageSize} />
              </SelectTrigger>
              <SelectContent side="top">
                <SelectGroup>
                  {[10, 20, 30, 40, 50].map((pageSize) => (
                    <SelectItem key={pageSize} value={`${pageSize}`}>
                      {pageSize}
                    </SelectItem>
                  ))}
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>
          <DataTablePagination table={table} />
        </div>
      </div>
    </div>
  );
}
