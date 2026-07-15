"""CSV input helpers."""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import pandas as pd


def graph_from_csv(
    stations_path: str | Path,
    edges_path: str | Path,
    *,
    node_id: str = "node_id",
    from_id: str = "from_id",
    to_id: str = "to_id",
    active_column: str | None = None,
) -> tuple[nx.Graph, pd.DataFrame, pd.DataFrame]:
    stations = pd.read_csv(stations_path, encoding="utf-8-sig")
    edges = pd.read_csv(edges_path, encoding="utf-8-sig")
    if active_column and active_column in stations.columns:
        active = stations[active_column].astype(str).str.lower().isin(
            {"true", "1", "yes", "y"}
        )
        stations = stations.loc[active].copy()

    graph = nx.Graph()
    for record in stations.to_dict("records"):
        graph.add_node(str(record[node_id]), **record)
    for record in edges.to_dict("records"):
        u, v = str(record[from_id]), str(record[to_id])
        if u not in graph or v not in graph:
            continue
        graph.add_edge(u, v, **record)
    return graph, stations, edges
