import { useState, useMemo, Fragment } from "react";
import {
  type ColumnFiltersState,
  type ColumnVisibilityState,
  type PaginationState,
  type SortingState,
  type ExpandedState,
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
import { Model } from "@/components/models/model";

import { DataTableFilter } from "./data-table-filter";
import { DataTablePagination } from "./data-table-pagination";

const sortOptions = [
  { value: "name-asc", label: "Name A-Z" },
  { value: "name-desc", label: "Name Z-A" },
] as const;

interface DataTableProps {
  columns: any;
  data: any;
  getRowId: (originalRow: any, index: number, parent?: any) => string;
  defaultSortId: string;
  searchPlaceholder?: string;
  customToolbar?: React.ReactNode;
  onExpand?: (unit: any, columns: any) => React.ReactNode;
}

export function DataTable({
  columns,
  data,
  getRowId,
  defaultSortId,
  searchPlaceholder = "Search...",
  onExpand,
  customToolbar,
}: DataTableProps) {
  const sortOptionState = useMemo(() => ({
    "name-asc": [{ id: defaultSortId, desc: false }],
    "name-desc": [{ id: defaultSortId, desc: true }],
  }), [defaultSortId]);

  const [rowSelection, setRowSelection] = useState({});
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [sorting, setSorting] = useState<SortingState>([{ id: defaultSortId, desc: false }]);
  const [expanded, setExpanded] = useState<ExpandedState>({});
  const [columnVisibility] = useState<ColumnVisibilityState>({
    search: false,
  });
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  });

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

  const searchQuery = (table.getColumn("search")?.getFilterValue() as string | undefined) ?? "";

  const sortValue = useMemo(() => {
    const currentSort = sorting[0];
    if (currentSort?.id === defaultSortId && !currentSort.desc) return "name-asc";
    if (currentSort?.id === defaultSortId && currentSort.desc) return "name-desc";
    return "newest";
  }, [sorting, defaultSortId]);

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <DataTableFilter table={table} />
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center xl:w-auto">
          {customToolbar}
          <div className="relative w-full lg:w-80">
            <Search className="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              className="h-7 rounded-[min(var(--radius-md),12px)] pl-8"
              placeholder={searchPlaceholder}
              value={searchQuery}
              onChange={(event) => {
                table.getColumn("search")?.setFilterValue(event.target.value || undefined);
                table.setPageIndex(0);
              }}
            />
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger>
              <Button variant="outline" size="sm">
                <ArrowUpDown />
                Sort
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuRadioGroup
                value={sortValue}
                onValueChange={(value) => {
                  table.setSorting(sortOptionState[value as keyof typeof sortOptionState] ?? sortOptionState["name-asc"]);
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
            {table.getHeaderGroups().map((headerGroup: any) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header: any) => (
                  <TableHead key={header.id} colSpan={header.colSpan} className="h-11 p-3 font-medium">
                    {header.isPlaceholder ? null : <table.FlexRender header={header} />}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.length ? (
              table.getRowModel().rows.map((row: any) => (
                <Fragment key={row.id}>
                  <TableRow key={row.id} data-state={table.state.rowSelection[row.id] && "selected"}>
                    {row.getVisibleCells().map((cell: any) => (
                      <TableCell key={cell.id} className="p-3 align-middle">
                        <table.FlexRender cell={cell} />
                      </TableCell>
                    ))}
                  </TableRow>
                 {onExpand && row.getIsExpanded() && (
                  <>
                    {onExpand(row, columns)}
                 </>
                )}
                </Fragment>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={table.getVisibleLeafColumns().length} className="h-24 text-center">
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex items-center justify-between px-1">
        <div className="hidden flex-1 text-muted-foreground text-sm lg:flex">
          {table.getFilteredSelectedRowModel().rows.length} of {table.getFilteredRowModel().rows.length} row(s)
          selected.
        </div>
        <div className="flex w-full items-center gap-8 lg:w-fit">
          <div className="hidden items-center gap-2 lg:flex">
            <Label htmlFor="rows-per-page" className="font-medium text-sm">
              Rows per page
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
