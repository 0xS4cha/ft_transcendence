// {
//   "meta": {
//     "total": 1000,
//     "offset": 0,
//     "limit": 50
//   },
//   "data": [
//     {
//       "player_id": "142782300",
//       "summoner_region": "la2",
//       "riot_id": "MJS Leofloresdc#Chemb",
//       "puuid": "lxwsxKT_X60rbb3-Vwvwggpv-4OybAQ13ulw8TcXi--6o1Ga-csL85S8v83Yu4r3LIitiJIHz0e8_g",
//       "rating": "CHALLENGER I 2408 LP",
//       "rating_numeric": 5208,
//       "num_played": 565,
//       "rank": 1,
//       "stats": {
//         "num_played": 565,
//         "place_sum": 1713,
//         "wins": 162,
//         "appMatches": false
//       }
//     },

export interface rankingMeta {
    total: number;
    offset: number;
    limit: number;
}

interface Dictionary {
  [key: string]: string;
}

export interface rankingPlayerStatRecentResult {
    ItemData: Dictionary;
    topCarries: [],
    damage_percentile_sum: number;
    board_strength_percentile_sum: number;
    percentile_count: number;
    num_played: number;
    wins: number;
    place_sum: number;
    avg_similarity: number;
    lpChange: number
}


export interface rankingPlayerStats {
    num_played: number;
    place_sum: number;
    wins: number;
    appMatches: boolean;
    RecentResult: rankingPlayerStatRecentResult;
    currentPatchResult: rankingPlayerStatRecentResult;
}

export interface rankingPlayer {
    player_id: string;
    summoner_region: string,
    riot_id: string,
    puuid: string;
    rating: string;
    rating_numeric: number;
    num_played: number;
    rank: number;
    stats: rankingPlayerStats
}

export interface rankingApi {
    meta: rankingMeta
    data: rankingPlayer[]
}
