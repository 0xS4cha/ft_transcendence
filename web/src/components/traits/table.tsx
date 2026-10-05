import { TraitsColumns } from "@/components/traits/columns";
import { DataTable } from "@/components/data-table/data-table";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { toast } from "@/components/ui/toast";
import { type TraitRow } from "@/components/traits/schema";
import { getTraitsStats } from "@/services/statsService";
import { type FilterType } from "@/types/stats";

export function TraitsTable() {
  const [filter, setFilter] = useState<FilterType>({
    queue: "1100",
    ranked: "PLATINUM",
    server: "EUW1"
  });
  const [data, setData] = useState<TraitRow[]>([]);
  const [searchParams] = useSearchParams();
  const initialSearchQuery = searchParams.get("q")?.trim() ?? "";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getTraitsStats(filter.queue, filter.ranked, filter.server);
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
      setFilter={setFilter}
      filter={filter}
      columns={TraitsColumns}
      data={data}
      getRowId={(row) => row.id}
      defaultSortId="id"
      searchPlaceholder="Search trait..."
      initialSearchQuery={initialSearchQuery}
    />
  );
}