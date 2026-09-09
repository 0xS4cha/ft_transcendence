export interface HistoryChartProps {
  date: string;
  gold_wasted_avg: number;
  time_elapsed_avg: number;
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