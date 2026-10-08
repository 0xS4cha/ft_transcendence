import { ItemsColumns } from "@/components/items/columns";
import { DataTable } from "@/components/data-table/data-table";
import { useEffect, useState, useImperativeHandle } from "react";
import { useSearchParams } from "react-router-dom";
import { toast } from "@/components/ui/toast";
import { type ItemRow } from "@/components/items/schema";
import { getItemsStats } from "@/services/statsService";
import { type FilterType } from "@/types/stats";
import { downloadJson, downloadXml } from "@/lib/utils";

export function ItemsTable({ ref }: any) {
  const [filter, setFilter] = useState<FilterType>({
    queue: "1100",
    ranked: "PLATINUM",
    server: "EUW1"
  });
  const [data, setData] = useState<ItemRow[]>([]);
  const [searchParams] = useSearchParams();
  const initialSearchQuery = searchParams.get("q")?.trim() ?? "";

  useImperativeHandle(ref, () => ({
    exportJson() {
      downloadJson(data, "items.json")
    },
    exportXml() {
      downloadXml(data, "items.xml")
    }
  }));

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
  }, [filter]);

  return (
    <DataTable
      columns={ItemsColumns}
      data={data}
      setFilter={setFilter}
      filter={filter}
      getRowId={(row) => row.id}
      defaultSortId="name"
      addAvgSort={true}
      searchPlaceholder="Search items..."
      initialSearchQuery={initialSearchQuery}
    />
  );
}