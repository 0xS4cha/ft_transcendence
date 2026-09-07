import fake_data from "@/assets/data.json";
import { UnitsColumns } from "@/components/units/columns";
import { DataTable } from "@/components/data-table/data-table";
import { UnitsCostFilter } from "@/components/units/cost_filter";
import { UnitsExpand } from "@/components/units/expand";

export function UnitsTable() {
  const data = fake_data.units;

  function onExpand(unit, columns) {
    return <UnitsExpand unit={unit} columns={columns}/>
  };

  return (
    <DataTable
      columns={UnitsColumns}
      data={data}
      getRowId={(row) => row.unit}
      defaultSortId="unit"
      searchPlaceholder="Search units..."
      customToolbar={<UnitsCostFilter />}
      onExpand={onExpand}
    />
  );
}