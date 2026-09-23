import { cn } from "@/lib/utils";
import { getChampionById } from '@/lib/champion';
import { useDroppable, useDraggable } from "@dnd-kit/core";

const ROWS = 4;
const COLS = 7;
const HEX_SIZE = 24; // TAILLE QUI M'A L'AIR RAISONNABLE
const HEX_GAP = 4;

const HEX_WIDTH = Math.sqrt(3) * HEX_SIZE; // FORMULE MATHEMATIQUE DE LA LARGEUR TOTALE D'UN HEXAGONE
const HEX_HEIGHT = 2 * HEX_SIZE;
const ROW_HEIGHT = 1.5 * HEX_SIZE;


function HexagonCell({ id, cx, cy, points, championId, onRemove }: {id: string, cx: number, cy: number, points: string, championId?: string, onRemove: (id: string) => void}){
  const {isOver, setNodeRef} = useDroppable( {id} );

  const { attributes, listeners, setNodeRef: setDraggableRef, isDragging } = useDraggable({ 
    id: id,
    disabled: !championId
  });

  const champion = championId ? getChampionById(championId) : null;
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
        "stroke-[grey]/75 stroke-[1px] transition-colors",
        isOver ? "fill-[grey]/75" : "fill-[#2A2A2A]"
      )}/>
      {champion && (
        <g
        ref={setDraggableRef as any}
        {...listeners}
        {...attributes}
        onClick={() => onRemove(id)}
        className={cn("cursor-grab hover:opacity-70 transition focus:outline-none stroke-[1px]", 
                  isDragging && "opacity-30")}
        >
        <polygon points={points} fill="transparent" />
          <image
            href={champion.imageUrl}
            x={cx - 20}
            y={cy - 20}
            width={40}
            height={40}
            clipPath={`url(#${clipPathId})`}
            preserveAspectRatio="xMidYMid"
            className="pointer-events-none"
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

export default function BuilderBoard({ boardState, onRemoveChampion }: { boardState: Record<string, string>, onRemoveChampion: (id: string) => void })
{
  // UN CERCLE COMPLET FAIT 360 DEGREE IL Y A 6 POINTS A DESSINER POUR L'HEXAGONE
  // ON RECUPERE LE RADIAN AU LIEU DE L'ANGLE (-30 POUR LA ROTATION EN HAUT)
  // ON TROUVE LE CENTRE DE L'HEXAGONE (X ET Y QUE L'ON RAJOUTE DANS LE TABLEAU POINTS POUR CHACUN DES 6 POINTS
  // 6 PAIRES DE COORDONNEES SEPARER PAR ESPACE
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

  // ON REMPLIT LE TABLEAU D'HEXAGONE AVEC LES VALEURS ET ON CALCUL L'OFFSET SUR LES IMPAIRE (1,3) SINON (0,2)
  // ON RECUPERE LA TAILLE DE L'HEXAGONE PAR RAPPORT A SA POSITION X - Y (LIGNE ET COLONE)
  // ON MULTIPLIE SA POSITION PAR SA LARGEUR ET SA HAUTEUR EN RAJOUTANT L'OFFSET
  // ON PUSH UN COMPOSANT VIRTUEL REACT (POLYGONE) AVEC SES POINTS ET SA CLASS (LES TRAITS DE BORDURE)
  // KEY EST OBLIGATOIRE POUR NE PAS QUE REACT CONFONDE LES POLYGONE
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
			hexes.push(
				<HexagonCell
          key={hexId}
          id={hexId}
          cx={cx}
          cy={cy}
          points={getHexagonPoints(cx, cy)}
          championId={boardState[hexId]}
          onRemove={onRemoveChampion}
        />
      );
		}
	}

	const boardWidth = (COLS * HEX_WIDTH + (HEX_WIDTH / 2));
  const boardHeight = ((ROWS - 1) * ROW_HEIGHT + HEX_HEIGHT );

  // ON RECUPERE LA HAUTEUR ET LA LARGEUR DU SVG
  // REACT S'OCCUPE NATIVEMENT DE TRAITER LE CONTENU JS ET DE L'AFFICHER A L'INTERIEUR DE LA BALISE SVG (SCALABLE VECTOR GRAPHIQUE)
  // PAS DE PIXEL C'EST DES MATHS
	return (
    <div className="flex h-full w-full items-center justify-center p-4 bg-[#202020] rounded-xl">
      <svg
        viewBox={`0 0 ${boardWidth} ${boardHeight}`}
        className="w-full max-h-full drop-shadow-xl md:w-[85%] lg:w-[85%]">
        {hexes}
      </svg>
    </div>
	)
}