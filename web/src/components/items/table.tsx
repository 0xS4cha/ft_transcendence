import { ItemsColumns } from "@/components/items/columns";
import { DataTable } from "@/components/data-table/data-table";
import { ItemsTypeFilter } from "@/components/items/type_filter";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { toast } from "@/components/ui/toast";
import { type ItemRow } from "@/components/items/schema";
import { getItemsStats } from "@/services/statsService";
import { type FilterType } from "@/types/stats";

export function ItemsTable() {
  const [filter, setFilter] = useState<FilterType>({
      queue: "1100",
    ranked: "PLATINUM",
    server: "EUW1"
  });
  const [data, setData] = useState<ItemRow[]>([]);
  const [searchParams] = useSearchParams();
  const initialSearchQuery = searchParams.get("q")?.trim() ?? "";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getItemsStats(filter.queue, filter.ranked, filter.server);
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
      setFilter={setFilter}
      filter={filter}
      getRowId={(row) => row.id}
      defaultSortId="id"
      searchPlaceholder="Search items..."
      initialSearchQuery={initialSearchQuery}
      customToolbar={<ItemsTypeFilter />}
    />
  );
}