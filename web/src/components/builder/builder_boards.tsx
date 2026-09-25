import { cn } from "@/lib/utils";
import { useDroppable, useDraggable } from "@dnd-kit/core";
import type { Unit } from "@/types/unit"; // 👈 Nouvel import du type de ton ami

const ROWS = 4;
const COLS = 7;
const HEX_SIZE = 24; 
const HEX_GAP = 4;

const HEX_WIDTH = Math.sqrt(3) * HEX_SIZE;
const HEX_HEIGHT = 2 * HEX_SIZE;
const ROW_HEIGHT = 1.5 * HEX_SIZE;

function HexagonCell({ id, cx, cy, points, champion, onRemove }: {id: string, cx: number, cy: number, points: string, champion?: Unit | null, onRemove: (id: string) => void}){
  const {isOver, setNodeRef} = useDroppable( {id} );

  const { attributes, listeners, setNodeRef: setDraggableRef, isDragging } = useDraggable({ 
    id: id,
    disabled: !champion
  });

  const clipPathId = `clip-${id}`;
  
  return (
    <g ref={setNodeRef as any}>
      <defs>
        <clipPath id={clipPathId}>
          <polygon points={points}/>
        </clipPath>
      </defs>
      <polygon
        points={points}
        className={cn(
          "stroke-[grey]/75 transition-colors",
          isOver ? "fill-[grey]/75" : "fill-[#2A2A2A]"
        )}
      />
      
      {champion && (
        <g
          ref={setDraggableRef as any}
          {...listeners}
          {...attributes}
          onClick={() => onRemove(id)}
          className={cn("cursor-grab hover:opacity-70 transition focus:outline-none", 
                    isDragging && "opacity-30")}
        >
          <polygon points={points} fill="transparent" />
          <image
            href={champion.icon}
            x={cx - 21}
            y={cy - 21}
            width={42}
            height={42}
            clipPath={`url(#${clipPathId})`}
            preserveAspectRatio="xMidYMid"
            className="pointer-events-none"
          />
          <polygon 
            points={points} 
            className="fill-none stroke-[grey]/75 stroke-[1px] pointer-events-none" 
          />
          <text 
            x={cx} 
            y={cy + 10} 
            textAnchor="middle" 
            alignmentBaseline="middle" 
            fill="white" 
            fontSize="5px"
            fontWeight="bold"
            stroke="black"
            strokeWidth="1px"
            paintOrder="stroke fill"
            className="pointer-events-none" 
          >
            {champion.name}
          </text>
        </g>
      )}
    </g>
  )
}

export default function BuilderBoard({ boardState, champions, onRemoveChampion, boardItems }: { boardState: Record<string, string>, champions: Unit[], onRemoveChampion: (id: string) => void , boardItems: })
{
  const getHexagonPoints = (cx: number, cy: number) =>
  {
    const points = [];
    for (let i = 0; i < 6; i++)
    {
      const angle_deg = 60 * i - 30;
      const angle_rad = (Math.PI / 180) * angle_deg;

      const x = cx + (HEX_SIZE - HEX_GAP) * Math.cos(angle_rad);
      const y = cy + (HEX_SIZE - HEX_GAP) * Math.sin(angle_rad);

      points.push(`${x},${y}`);
    }
    return points.join(" ");
  };

  const hexes = [];
  for (let row = 0; row < ROWS; row++)
  {
    for(let col = 0; col < COLS; col++)
    {
      const OddRow= row % 2 !== 0;
      const xOffSet = OddRow ? HEX_WIDTH / 2 : 0;

      const cx = (col * HEX_WIDTH) + xOffSet + (HEX_WIDTH / 2);
      const cy =(row * ROW_HEIGHT) + (HEX_HEIGHT / 2);

      const hexId = `hex-${row}-${col}`;
      const champId = boardState[hexId];
      const championOnCell = champId ? champions.find((c) => c.id === champId) : null;

      hexes.push(
        <HexagonCell
          key={hexId}
          id={hexId}
          cx={cx}
          cy={cy}
          points={getHexagonPoints(cx, cy)}
          champion={championOnCell}
          onRemove={onRemoveChampion}
        />
      );
    }
  }
  const boardWidth = (COLS * HEX_WIDTH + (HEX_WIDTH / 2));
  const boardHeight = ((ROWS - 1) * ROW_HEIGHT + HEX_HEIGHT );

  return (
    <div className="h-full w-full p-2">
      <svg
        viewBox={`0 0 ${boardWidth} ${boardHeight}`}
        className="w-full h-full drop-shadow-xl"
      >
        {hexes}
      </svg>
    </div>
  )
}