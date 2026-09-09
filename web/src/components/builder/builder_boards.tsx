import { cn } from "@/lib/utils";

const ROWS = 4;
const COLS = 7;
const HEX_SIZE = 30; // TAILLE QUI M'A L'AIR RAISONNABLE
const HEX_GAP = 5;

const HEX_WIDTH = Math.sqrt(3) * HEX_SIZE; // FORMULE MATHEMATIQUE DE LA LARGEUR TOTALE D'UN HEXAGONE
const HEX_HEIGHT = 2 * HEX_SIZE;
const ROW_HEIGHT = 1.5 * HEX_SIZE;


export default function BuilderBoard()
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

			hexes.push(
				<polygon
				  key={`${row}-${col}`}
				  points={getHexagonPoints(cx, cy)}
				  className={cn(
            "fill-[#2A2A2A] stroke-[grey]/75 stroke-[2px]",
				  )}
        />
      );
		}
	}

	const boardWidth = COLS * HEX_WIDTH + (HEX_WIDTH / 2);
  const boardHeight = (ROWS - 1) * ROW_HEIGHT + HEX_HEIGHT;

  // ON RECUPERE LA HAUTEUR ET LA LARGEUR DU SVG
  // REACT S'OCCUPE NATIVEMENT DE TRAITER LE CONTENU JS ET DE L'AFFICHER A L'INTERIEUR DE LA BALISE SVG (SCALABLE VECTOR GRAPHIQUE)
  // PAS DE PIXEL C'EST DES MATHS
	return (
    <div className="flex h-full w-full items-center justify-center p-4">
      <svg
        viewBox={`0 0 ${boardWidth} ${boardHeight}`}
        className="max-h-full max-w-full drop-shadow-xl">
        {hexes}
      </svg>
    </div>
	)
}