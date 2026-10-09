import { Button } from "@/components/ui/button";
import {
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import type { ReactTable, RowData } from "@tanstack/react-table";
import { dataTableFeatures } from "@/lib/data-table-features";

interface DataTablePaginationProps<TData extends RowData> {
  table: ReactTable<typeof dataTableFeatures, TData>;
}

export function DataTablePagination<TData extends RowData>({ table }: DataTablePaginationProps<TData>) {
  const { t } = useTranslation();

  return (
    <>
      <div className="flex w-fit items-center justify-center font-medium text-sm">
        Page {table.state.pagination.pageIndex + 1} of {table.getPageCount()}
      </div>
      <div className="ml-auto flex items-center gap-2 lg:ml-0">
        <Button
          variant="outline"
          className="hidden size-8 lg:flex"
          size="icon"
          onClick={() => table.setPageIndex(0)}
          disabled={!table.getCanPreviousPage()}
        >
          <span className="sr-only">{t("table.firstpage", "Go to first page")}</span>
          <ChevronsLeft className="size-4" />
        </Button>
        <Button
          variant="outline"
          className="size-8"
          size="icon"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          <span className="sr-only">{t("table.previouspage", "Go to previous page")}</span>
          <ChevronLeft className="size-4" />
        </Button>
        <Button
          variant="outline"
          className="size-8"
          size="icon"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          <span className="sr-only">{t("table.nextpage", "Go to next page")}</span>
          <ChevronRight className="size-4" />
        </Button>
        <Button
          variant="outline"
          className="hidden size-8 lg:flex"
          size="icon"
          onClick={() => table.setPageIndex(table.getPageCount() - 1)}
          disabled={!table.getCanNextPage()}
        >
          <span className="sr-only">{t("table.lastpage", "Go to last page")}</span>
          <ChevronsRight className="size-4" />
        </Button>
      </div>
    </>
  );
}
