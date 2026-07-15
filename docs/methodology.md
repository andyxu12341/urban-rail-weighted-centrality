# Methodology

## 1. Network representation

The urban rail system is represented as an undirected graph \(G=(V,E)\).

- **Node**: a station or station complex.
- **Edge**: service adjacency between consecutive stops, or a transfer connection.
- **Cost**: station hops, kilometres or another non-negative impedance.

For zero-cost intermodal transfers, the two nodes remain distinct but their transfer edge has cost zero. They therefore have identical shortest-distance profiles when no other asymmetric attributes are introduced.

## 2. Ordinary closeness

\[
C_i=\frac{N-1}{\sum_{j\ne i}d_{ij}}
\]

Equivalent average distance:

\[
\bar d_i=\frac{1}{N-1}\sum_{j\ne i}d_{ij},\qquad C_i=\frac{1}{\bar d_i}
\]

## 3. Demand-weighted closeness

\[
C_i^W=\frac{\sum_jW_j}{\sum_jW_jd_{ij}}
\]

Equivalent weighted average distance:

\[
\bar d_i^W=\frac{\sum_jW_jd_{ij}}{\sum_jW_j},\qquad C_i^W=\frac{1}{\bar d_i^W}
\]

The self-distance \(d_{ii}=0\), so the candidate station's own demand enters naturally without a separately invented bonus coefficient.

## 4. Ranking

Dense ranking is used. Numerically equal scores within a small tolerance share the same rank.

```text
rank_change = ordinary_rank - weighted_rank
```

A positive value means that the station rises after demand weighting.

## 5. New York case

- Nodes: 423 MTA station complexes; Staten Island Railway excluded.
- Edges: 513 undirected adjacency links.
- Impedance: shortest number of stop-to-stop edges.
- Weight: average monthly ridership by station complex.
- Ridership period: monthly averages derived from February 2022 through October 2023.

## 6. Changsha / CZT case

- Nodes: Changsha Metro Lines 1–6, Maglev S2 and active Changsha–Zhuzhou–Xiangtan intercity stations.
- Impedance: cumulative adjacent-station geodesic kilometres.
- Transfer convention: intermodal transfer edges cost 0 km while nodes remain separate.
- Weight: WorldPop 2027 constrained population assigned to station-service areas.

### Population allocation

1. Use the WorldPop China 2027 1 km constrained population-count raster.
2. Split every 1 km pixel into a 10 × 10 subgrid for area-proportional approximation.
3. Assign each subcell to the nearest physical station complex within 1,000 m.
4. Count each subcell once; exclude population outside the maximum service distance.
5. For colocated intermodal nodes, divide complex population equally among member nodes to prevent double counting.

## 7. Limitations

- Station-hop distance ignores running speed, waiting and transfer time.
- Geodesic segment length is a spatial proxy, not engineering track mileage.
- WorldPop 2027 is a modelled projection, not observed 2027 census population.
- A 1 km grid supports metropolitan-scale comparison, not entrance-level catchment analysis.
- Weighted closeness measures access to weighted destinations, not causal ridership generation.
