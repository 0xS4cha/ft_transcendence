import { UnitsColumns } from "@/components/units/columns";
import { DataTable } from "@/components/data-table/data-table";
import { UnitsCostFilter } from "@/components/units/cost_filter";
import { UnitsExpand } from "@/components/units/expand";
import type { Row, ColumnDef } from "@tanstack/react-table";
import type { dataTableFeatures } from "@/lib/data-table-features";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { toast } from "@/components/ui/toast";
import { type UnitRow } from "@/components/units/schema";
import { getUnitsStats } from "@/services/statsService";
import { type FilterType } from "@/types/stats";


interface UnitsExpandProps {
  unit: Row<typeof dataTableFeatures, UnitRow>;
  columns: ColumnDef<typeof dataTableFeatures, UnitRow>[];
}

function UnitsExpandRenderer({ unit, columns }: UnitsExpandProps) {
  return <UnitsExpand unit={unit} columns={columns} />;
}

export function UnitsTable() {
  const [filter, setFilter] = useState<FilterType>({
      queue: "1100",
    ranked: "PLATINUM",
    server: "EUW1"
  });
  const [data, setData] = useState<UnitRow[]>([]);
  const [searchParams] = useSearchParams();
  const initialSearchQuery = searchParams.get("q")?.trim() ?? "";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getUnitsStats(filter.queue, filter.ranked, filter.server);
        setData(result);
      } catch (error) {
        toast.add({
          type: "error",
          title: `Fetch failed: ${error}`,
        });
      }
    };

    fetchData();
  }, [filter]);

  function renderSubComponent(row: Row<typeof dataTableFeatures, UnitRow>) {
    
    return (
      <UnitsExpandRenderer
        unit={row}
        columns={row.getVisibleCells().map((cell) => cell.column.columnDef) as ColumnDef<typeof dataTableFeatures, UnitRow>[]}
      />
    );
  }

  return (
    <DataTable
      setFilter={setFilter}
      filter={filter}
      columns={UnitsColumns}
      data={data}
      getRowId={(row) => row.unit}
      defaultSortId="unit"
      searchPlaceholder="Search units..."
      customToolbar={<UnitsCostFilter />}
      onExpand={renderSubComponent}
      initialSearchQuery={initialSearchQuery}
    />
  );
}