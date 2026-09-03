import fake_data from "@/assets/data.json";
import { UnitsColumns } from "@/components/units/columns";
import { DataTable } from "@/components/data-table/data-table";
import { UnitsCostFilter } from "./cost-filter";

export function UnitsTable() {
  const data = fake_data.units;

  return (
    <DataTable
      columns={UnitsColumns}
      data={data}
      getRowId={(row) => row.unit}
      defaultSortId="unit"
      searchPlaceholder="Search units..."
      customToolbar={<UnitsCostFilter />}
    />
  );
}