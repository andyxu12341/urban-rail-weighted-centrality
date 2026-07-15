import networkx as nx

from urban_rail_centrality.centrality import compute_closeness, dense_ranks


def test_path_graph_closeness():
    graph = nx.path_graph(["a", "b", "c"])
    results = {row.node: row for row in compute_closeness(graph)}
    assert results["b"].average_distance == 1.0
    assert results["b"].closeness == 1.0
    assert results["a"].average_distance == 1.5


def test_weighted_destination_pull():
    graph = nx.path_graph(["a", "b", "c"])
    results = {
        row.node: row
        for row in compute_closeness(
            graph, node_weights={"a": 1, "b": 1, "c": 10}
        )
    }
    assert results["c"].weighted_closeness > results["a"].weighted_closeness


def test_dense_ties():
    ranks = dense_ranks({"a": 1.0, "b": 1.0, "c": 0.5})
    assert ranks == {"a": 1, "b": 1, "c": 2}
