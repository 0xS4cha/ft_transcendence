import { TraitsColumns } from "@/components/traits/columns";
import { DataTable } from "@/components/data-table/data-table";
import { useEffect, useState, useImperativeHandle, type Ref } from "react";
import { useSearchParams } from "react-router-dom";
import { toast } from "@/components/ui/toast";
import { type TraitRow } from "@/components/traits/schema";
import { getTraitsStats } from "@/services/statsService";
import { type FilterType, type exportRef } from "@/types/stats";
import { downloadJson, downloadXml } from "@/lib/utils";

export function TraitsTable({ ref }: { ref?: Ref<exportRef> }) {
  const [filter, setFilter] = useState<FilterType>({
    queue: "Ranked",
    ranked: "PLATINUM",
    server: "EUW1"
  });
  const [data, setData] = useState<TraitRow[]>([]);
  const [searchParams] = useSearchParams();
  const initialSearchQuery = searchParams.get("q")?.trim() ?? "";

  useImperativeHandle(ref, () => ({
    exportJson() {
      downloadJson(data, "traits.json")
    },
    exportXml() {
      downloadXml(data, "traits.xml")
    }
  }));

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
  }, [filter]);

  return (
    <DataTable
      setFilter={setFilter}
      filter={filter}
      columns={TraitsColumns}
      data={data}
      getRowId={(row) => row.id}
      defaultSortId="name"
      searchPlaceholder="Search trait..."
      addAvgSort={true}
      initialSearchQuery={initialSearchQuery}
    />
  );
}