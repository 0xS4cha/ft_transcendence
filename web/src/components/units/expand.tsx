import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import { OrbitControls, Center } from "@react-three/drei";
import { TableRow, TableCell } from "@/components/ui/table";
import { Model } from "@/components/models/model";
import type { Row } from "@tanstack/react-table";
import type { dataTableFeatures } from "@/lib/data-table-features";
import type { UnitRow } from "@/components/units/schema";

interface UnitsExpandProps {
  unit: Row<typeof dataTableFeatures, UnitRow>;
  columns: unknown[];
}

export function UnitsExpand({ unit, columns }: UnitsExpandProps) {
  const { id: name, avg_place, frequency, winrate } = unit.original;
  const colSpan = unit.getVisibleCells?.().length ?? columns.length;

  return (
    <TableRow className="hover:bg-transparent">
      <TableCell colSpan={colSpan} className="bg-muted/30 p-0">
        <div className="grid grid-cols-[220px_1fr] gap-6 p-5">
          <div className="relative aspect-square overflow-hidden">
            <Canvas dpr={[1, 2]} camera={{ position: [0, 1, 3], fov: 50 }}>
              <Suspense fallback={null}>
                <ambientLight intensity={0.5} />
                <directionalLight position={[5, 5, 5]} intensity={1} />
                <Center disableX disableZ>
                  <Model url="/ahri.glb" />
                </Center>
                <OrbitControls
                  enableZoom={false}
                  autoRotate
                  autoRotateSpeed={2}
                />
              </Suspense>
            </Canvas>
          </div>
          <div className="flex flex-col gap-5">
            <h3 className="font-semibold text-base leading-none">{name}</h3>

            <div className="grid grid-cols-3 gap-4 border-y py-3">
              <div className="grid gap-0.5">
                <span className="font-medium text-base leading-none tabular-nums">
                  {avg_place.toFixed(2)}%
                </span>
                <span className="text-muted-foreground text-xs">
                  Avg place
                </span>
              </div>
              <div className="grid gap-0.5">
                <span className="font-medium text-base leading-none tabular-nums">
                  {frequency.toFixed(2)}%
                </span>
                <span className="text-muted-foreground text-xs">
                  Pick rate
                </span>
              </div>
              <div className="grid gap-0.5">
                <span className="font-medium text-base leading-none tabular-nums">
                  {winrate.toFixed(2)}%
                </span>
                <span className="text-muted-foreground text-xs">Winrate</span>
              </div>
            </div>
          </div>
        </div>
      </TableCell>
    </TableRow>
  );
}