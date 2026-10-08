export interface HistoryChartProps {
  date: string;
  value: number;
}

export interface HomeDataProps {
  visitsCount: number;
  goldCount: number;
  matchCount: number;
  history: HistoryChartProps[];
}

export interface ChartProps {
    data: HistoryChartProps[]
}