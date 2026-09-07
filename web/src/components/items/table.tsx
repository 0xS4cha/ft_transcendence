import fake_data from "@/assets/data.json";
import { ItemsColumns } from "@/components/items/columns";
import { DataTable } from "@/components/data-table/data-table";
import { ItemsTypeFilter } from "@/components/items/type_filter";

export function ItemsTable() {
  const data = fake_data.itemNames;

  return (
    <DataTable
      columns={ItemsColumns}
      data={data}
      getRowId={(row) => row.itemName}
      defaultSortId="itemName"
      searchPlaceholder="Search items..."
      customToolbar={<ItemsTypeFilter />}
    />
  );
}