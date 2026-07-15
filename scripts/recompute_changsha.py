#!/usr/bin/env python3
"""Recompute the Changsha/CZT population-weighted kilometre ranking."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from urban_rail_centrality.centrality import compute_closeness, dense_ranks
from urban_rail_centrality.io import graph_from_csv


def main() -> None:
    data_dir = ROOT / "data" / "changsha"
    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)

    graph, stations, _ = graph_from_csv(
        data_dir / "stations.csv",
        data_dir / "edges_km.csv",
        active_column="current_active",
    )
    population = pd.read_csv(
        data_dir / "station_population_worldpop2027.csv",
        encoding="utf-8-sig",
    )
    population_by_node = dict(
        zip(
            population["node_id"].astype(str),
            population["service_population"],
        )
    )

    results = compute_closeness(
        graph,
        node_weights=population_by_node,
        edge_weight="distance_km",
    )
    ordinary_scores = {row.node: row.closeness for row in results}
    weighted_scores = {row.node: row.weighted_closeness for row in results}
    ordinary_ranks = dense_ranks(ordinary_scores)
    weighted_ranks = dense_ranks(weighted_scores)
    station_info = stations.set_index(
        stations["node_id"].astype(str)
    ).to_dict("index")

    rows = []
    for row in sorted(
        results,
        key=lambda item: (weighted_ranks[item.node], str(item.node)),
    ):
        info = station_info[str(row.node)]
        rows.append(
            {
                "weighted_rank": weighted_ranks[row.node],
                "ordinary_rank": ordinary_ranks[row.node],
                "rank_change": ordinary_ranks[row.node]
                - weighted_ranks[row.node],
                "node_id": row.node,
                "station_name": info.get("station_name"),
                "mode": info.get("mode"),
                "city": info.get("city"),
                "lines": info.get("lines"),
                "service_population": population_by_node.get(
                    str(row.node), 0.0
                ),
                "ordinary_average_km": row.average_distance,
                "ordinary_closeness_km": row.closeness,
                "population_weighted_mean_km": row.weighted_average_distance,
                "population_weighted_closeness_km": row.weighted_closeness,
            }
        )

    output = output_dir / "czt_population_weighted_km_results.csv"
    pd.DataFrame(rows).to_csv(output, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(rows)} rows to {output}")


if __name__ == "__main__":
    main()
