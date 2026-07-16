---
name: rail-centrality-analysis
description: Calculate, compare, validate, and interpret ordinary and demand-weighted rail-network centrality using station hops, kilometres, or travel time. Use when ranking stations, adding ridership or population weights, testing transfer assumptions, or exporting full centrality results.
---

# Rail Network Centrality Analysis

## Goal

Calculate reproducible station rankings while keeping the graph definition, distance metric, destination weight, transfer rule, and scenario explicit.

## Required inputs

- node table;
- edge table or all-pairs shortest-path matrix;
- selected scenario;
- selected distance metric;
- optional destination-demand weights;
- physical-complex/transfer mapping.

## Distance metrics

Treat each metric as a separate model:

- `hops`: number of service edges or weighted station intervals;
- `km`: cumulative network distance;
- `in_vehicle_time`: scheduled or estimated running time;
- `generalized_time`: running + waiting + transfer + walking penalties.

Never compare raw centrality values from different metrics as though they share one unit. Compare rankings or normalized values instead.

## Ordinary closeness

For connected graph with \(N\) nodes:

\[
C_i=\frac{N-1}{\sum_{j\ne i}d_{ij}}=\frac{1}{\bar d_i}
\]

Report both:

- average shortest distance \(\bar d_i\), which is easier to interpret;
- closeness \(C_i\), which is easier to rank.

For disconnected graphs, either:

- use harmonic centrality;
- calculate each connected component separately;
- or explicitly restrict the scenario to the connected passenger network.

Do not silently replace the formula.

## Demand-weighted closeness

For destination demand \(W_j\):

\[
\bar d_i^W=\frac{\sum_j W_jd_{ij}}{\sum_jW_j}
\]

\[
C_i^W=\frac{\sum_jW_j}{\sum_jW_jd_{ij}}=\frac{1}{\bar d_i^W}
\]

Examples of \(W_j\):

- station entries/ridership;
- service population;
- employment;
- activity intensity;
- a composite demand index.

Interpret this as proximity to high-demand destinations, not as predicted ridership at origin station \(i\).

## Population assignment

When weights come from a population raster:

1. group co-located transfer nodes into a physical complex for catchment assignment;
2. assign every raster cell or subcell to at most one complex;
3. use a maximum catchment distance;
4. split complex population among member nodes when nodes remain separate;
5. record raster year, resolution, unit, CRS, and whether data are observed or projected.

Recommended default for coarse 1 km data:

- split each raster cell into a 10×10 subgrid;
- assign subcells to the nearest physical complex within 1000 m;
- sum population fractions;
- disclose this as area-proportional approximation.

Do not sum overlapping circular buffers independently because this double-counts population.

## Ridership assignment

When weights come from station ridership:

- use one consistent time period;
- aggregate platforms to the graph node definition;
- distinguish entries, exits, linked trips, and total station usage;
- document missing or imputed stations;
- avoid combining incomparable pandemic and normal-service periods without adjustment.

## Zero-cost transfers

When separate nodes are connected by a zero-cost transfer edge:

- their shortest distances to every other node are identical;
- their closeness values are identical;
- report them as tied;
- preserve separate rows only for mode-level metadata or later flow analysis.

Do not use standard weighted betweenness with zero-weight cycles without checking algorithm assumptions. For betweenness, prefer:

- node contraction;
- a small positive transfer cost;
- or an unweighted structural reference clearly labelled as such.

## Workflow

### 1. Validate matrices

Confirm:

- row and column node order is identical;
- diagonal values are zero;
- matrix is symmetric for an undirected graph;
- no negative values;
- no unreachable values unless intentionally handled;
- zero-cost transfer pairs have identical distance rows.

### 2. Calculate ordinary centrality

For every metric, output:

```text
ordinary_rank
node_id
station_name
average_shortest_<metric>
closeness_<metric>
```

Use dense or minimum ranking consistently and state how ties are handled.

### 3. Calculate weighted centrality

Output:

```text
weighted_rank
ordinary_rank
rank_change
node_id
station_name
mode
city
lines
destination_weight
weighted_average_<metric>
weighted_closeness_<metric>
```

Define:

```text
rank_change = ordinary_rank - weighted_rank
```

A positive value means the station rises after demand weighting.

### 4. Compare scenarios

At minimum compare:

- base network versus multimodal extension;
- ordinary versus weighted;
- hops versus kilometres;
- optional time model;
- transfer cost sensitivity;
- catchment distance sensitivity.

### 5. Sensitivity analysis

Recommended tests:

- catchment: 500, 800, 1000 m;
- transfer: 0 hops, 1 hop, realistic minutes;
- distance: geodesic proxy versus track geometry;
- demand: equal station weight versus population/ridership;
- current passenger network versus full infrastructure.

A robust central station should remain near the top across several plausible assumptions.

### 6. Interpret results

Use distinctions such as:

- topological interchange centre;
- geometric distance centre;
- travel-time centre;
- population-oriented accessibility centre;
- ridership-oriented accessibility centre.

Avoid saying a station is “the city centre” solely from one centrality model.

## Required outputs

```text
results/<scenario>_ordinary_hops.csv
results/<scenario>_ordinary_km.csv
results/<scenario>_weighted_hops.csv
results/<scenario>_weighted_km.csv
results/<scenario>_comparison.xlsx
results/<scenario>_method.json
```

Include full rankings, not only top 10.

## Validation

Before delivery:

- weighted closeness equals inverse weighted mean distance within tolerance;
- sorted rank matches score order;
- tie groups have equal scores;
- all nodes appear exactly once;
- total assigned demand matches the catchment allocation output;
- formula errors and missing values are absent;
- results can be regenerated from repository inputs.

## Reporting template

Summarize:

1. data and scenario;
2. graph construction rule;
3. distance metric;
4. demand-weight method;
5. top results;
6. ranking changes;
7. sensitivity and limitations;
8. links to full machine-readable tables.
