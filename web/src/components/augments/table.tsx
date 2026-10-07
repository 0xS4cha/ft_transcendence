import { AugmentsColumns } from "@/components/augments/columns";
import { DataTable } from "@/components/data-table/data-table";
import { useEffect, useState, useImperativeHandle } from "react";
import { useSearchParams } from "react-router-dom";
import { toast } from "@/components/ui/toast";
import { type AugmentRow } from "@/components/augments/schema";
import { getAugmentsStats } from "@/services/statsService";
import { type FilterType } from "@/types/stats";
import { downloadJson, downloadXml } from "@/lib/utils";


export function AugmentsTable({ ref }: any) {
  const [filter, setFilter] = useState<FilterType>({
    queue: "1100",
    ranked: "PLATINUM",
    server: "EUW1"
  });
  const [data, setData] = useState<AugmentRow[]>([]);
  const [searchParams] = useSearchParams();
  const initialSearchQuery = searchParams.get("q")?.trim() ?? "";

  useImperativeHandle(ref, () => ({
    exportJson() {
      downloadJson(data, "units.json")
    },
    exportXml() {
      downloadXml(data, "units.xml")
    }
  }));

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getAugmentsStats(filter.queue, filter.ranked, filter.server);
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
      columns={AugmentsColumns}
      data={data}
      getRowId={(row) => row.id}
      defaultSortId="name"
      searchPlaceholder="Search augments..."
      initialSearchQuery={initialSearchQuery}
    />
  );
}