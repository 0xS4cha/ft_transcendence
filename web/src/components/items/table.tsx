import { ItemsColumns } from "@/components/items/columns";
import { DataTable } from "@/components/data-table/data-table";
import { ItemsTypeFilter } from "@/components/items/type_filter";
import { useEffect, useState } from "react";
import { toast } from "@/components/ui/toast";
import { type ItemRow } from "@/components/items/schema";
import { getItemsStats } from "@/services/statsService";

export function ItemsTable() {
  const [data, setData] = useState<ItemRow[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getItemsStats();
        setData(result);
      } catch (error) {
        toast.add({
          type: "error",
          title: `Fetch failed: ${error}`,
        });
      }
    };

    fetchData();
  }, []);

  return (
    <DataTable
      columns={ItemsColumns}
      data={data}
      getRowId={(row) => row.id}
      defaultSortId="id"
      searchPlaceholder="Search items..."
      customToolbar={<ItemsTypeFilter />}
    />
  );
}