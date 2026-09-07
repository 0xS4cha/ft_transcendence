import fake_data from "@/assets/data.json";
import { UnitsColumns } from "@/components/units/columns";
import { DataTable } from "@/components/data-table/data-table";
import { UnitsCostFilter } from "@/components/units/cost_filter";
import { UnitsExpand } from "@/components/units/expand";
import type { Row, ColumnDef } from "@tanstack/react-table";
import type { dataTableFeatures } from "@/lib/data-table-features";
import type { UnitRow } from "@/components/units/schema";



interface UnitsExpandProps {
  unit: Row<typeof dataTableFeatures, UnitRow>;
  columns: ColumnDef<typeof dataTableFeatures, UnitRow>[];
}

function UnitsExpandRenderer({ unit, columns }: UnitsExpandProps) {
  return <UnitsExpand unit={unit} columns={columns} />;
}

export function UnitsTable() {
  const data = fake_data.units;


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
      columns={UnitsColumns}
      data={data}
      getRowId={(row) => row.unit}
      defaultSortId="unit"
      searchPlaceholder="Search units..."
      customToolbar={<UnitsCostFilter />}
      onExpand={renderSubComponent}
    />
  );
}