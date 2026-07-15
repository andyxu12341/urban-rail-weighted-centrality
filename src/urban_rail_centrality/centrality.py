"""Reusable closeness and demand-weighted closeness algorithms."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Mapping

import networkx as nx


@dataclass(frozen=True)
class CentralityResult:
    node: Hashable
    average_distance: float
    closeness: float
    weighted_average_distance: float
    weighted_closeness: float


def dense_ranks(scores: Mapping[Hashable, float], tolerance: float = 1e-12) -> dict[Hashable, int]:
    """Rank descending scores; values equal within tolerance share a dense rank."""
    ordered = sorted(scores, key=lambda node: (-scores[node], str(node)))
    ranks: dict[Hashable, int] = {}
    previous: float | None = None
    rank = 0
    for node in ordered:
        value = float(scores[node])
        if previous is None or abs(value - previous) > tolerance:
            rank += 1
            previous = value
        ranks[node] = rank
    return ranks


def compute_closeness(
    graph: nx.Graph,
    *,
    node_weights: Mapping[Hashable, float] | None = None,
    edge_weight: str | None = None,
) -> list[CentralityResult]:
    """Compute ordinary and destination-weighted closeness for a connected graph.

    ``edge_weight=None`` gives unit-hop distance. Otherwise Dijkstra uses the
    named non-negative edge attribute. Missing node weights default to zero
    when a weight mapping is supplied, and to one when no mapping is supplied.
    """
    if graph.number_of_nodes() < 2:
        raise ValueError("The graph must contain at least two nodes.")
    if not nx.is_connected(graph):
        raise ValueError("The graph must be connected.")

    nodes = list(graph.nodes)
    weights = {
        node: (
            float(node_weights.get(node, 0.0))
            if node_weights is not None
            else 1.0
        )
        for node in nodes
    }
    if any(value < 0 for value in weights.values()):
        raise ValueError("Node weights must be non-negative.")
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("At least one node weight must be positive.")

    if edge_weight is None:
        all_distances = dict(nx.all_pairs_shortest_path_length(graph))
    else:
        all_distances = {
            source: dict(lengths)
            for source, lengths in nx.all_pairs_dijkstra_path_length(
                graph, weight=edge_weight
            )
        }

    n = len(nodes)
    results: list[CentralityResult] = []
    for source in nodes:
        distances = all_distances[source]
        total_distance = sum(
            float(distances[target]) for target in nodes if target != source
        )
        average_distance = total_distance / (n - 1)
        closeness = 1.0 / average_distance

        weighted_distance = sum(
            weights[target] * float(distances[target]) for target in nodes
        )
        weighted_average = weighted_distance / total_weight
        weighted_closeness = (
            1.0 / weighted_average if weighted_average > 0 else float("inf")
        )

        results.append(
            CentralityResult(
                node=source,
                average_distance=average_distance,
                closeness=closeness,
                weighted_average_distance=weighted_average,
                weighted_closeness=weighted_closeness,
            )
        )
    return results
