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
  const { unit: name, avg, pick, count, items } = unit.original;
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
            <div>
              <h3 className="font-semibold text-base leading-none">{name}</h3>
              <p className="mt-1 text-muted-foreground text-xs">
                {count} game{count > 1 ? "s" : ""} played{count > 1 ? "s" : ""}
              </p>
            </div>

            <div className="grid grid-cols-3 gap-4 border-y py-3">
              <div className="grid gap-0.5">
                <span className="font-medium text-base leading-none tabular-nums">
                  {avg}%
                </span>
                <span className="text-muted-foreground text-xs">
                  Avg place
                </span>
              </div>
              <div className="grid gap-0.5">
                <span className="font-medium text-base leading-none tabular-nums">
                  {pick}%
                </span>
                <span className="text-muted-foreground text-xs">
                  Pick rate
                </span>
              </div>
              <div className="grid gap-0.5">
                <span className="font-medium text-base leading-none tabular-nums">
                  {count}
                </span>
                <span className="text-muted-foreground text-xs">Games</span>
              </div>
            </div>

            <div className="grid gap-2">
              <span className="text-muted-foreground text-xs">
                Popular items
              </span>
              {items.length ? (
                <div className="flex flex-wrap gap-1.5">
                  {items.map((item, index) => (
                    <span
                      key={`${item.itemName}-${index}`}
                      className="rounded-md border bg-background px-2 py-1 text-xs"
                    >
                      {item.itemName}
                    </span>
                  ))}
                </div>
              ) : (
                <span className="text-muted-foreground text-xs">
                  No popular items
                </span>
              )}
            </div>
          </div>
        </div>
      </TableCell>
    </TableRow>
  );
}