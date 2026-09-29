import { TraitsColumns } from "@/components/traits/columns";
import { DataTable } from "@/components/data-table/data-table";
import { useEffect, useState } from "react";
import { toast } from "@/components/ui/toast";
import { type TraitRow } from "@/components/traits/schema";
import { getTraitsStats } from "@/services/statsService";

export function TraitsTable() {
  const [data, setData] = useState<TraitRow[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getTraitsStats();
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
      columns={TraitsColumns}
      data={data}
      getRowId={(row) => row.id}
      defaultSortId="id"
      searchPlaceholder="Search trait..."
    />
  );
}