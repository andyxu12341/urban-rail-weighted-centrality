---
name: rail-network-construction
description: Convert audited station and route sequences into reproducible urban rail graphs. Use when building nodes, adjacent-stop edges, transfer edges, service scenarios, GraphML/GeoJSON files, or shortest-path matrices for later centrality analysis.
---

# Urban Rail Network Construction

## Goal

Transform audited public-source station and route data into one or more explicit graph scenarios whose topology and edge weights can be reproduced and inspected.

## Inputs

Required:

- canonical station table;
- ordered route sequences;
- explicit transfer pairs;
- analysis date and service scenario;
- node and transfer policy.

Optional:

- exact track geometry;
- timetable or travel-time data;
- fare-gate/paid-area transfer constraints;
- express/local stopping patterns.

## Core graph model

Use an undirected graph for ordinary bidirectional passenger rail unless direction-specific operation matters. Use a directed graph only when service direction, one-way loops, or timetable accessibility requires it.

### Node policy

Support three explicit policies:

1. `physical_complex`
   - merge all platforms/modes within one passenger interchange into one node;
2. `same_system_merged_cross_mode_separate`
   - merge same-system transfer stations;
   - keep metro, intercity, maglev, tram, etc. as separate nodes;
   - connect them with transfer edges;
3. `platform_level`
   - preserve each platform/service group and model all transfers explicitly.

Never mix policies inside a scenario without documenting exceptions.

### Edge types

Use at least:

- `service`: consecutive passenger stops on one route;
- `transfer`: passenger connection between nodes;
- `walk_link`: optional out-of-station transfer;
- `virtual`: scenario-specific connector that must be clearly flagged.

## Edge-weight models

Create separate edge columns rather than overwriting one cost:

```text
station_hops
distance_km
in_vehicle_minutes
transfer_minutes
generalized_minutes
```

Recommended defaults:

- adjacent service edge: `station_hops = 1`;
- same-complex cross-mode transfer: `station_hops = 0` when the user wants station-count equivalence without node merging;
- same-complex cross-mode transfer: `distance_km = 0` for physical-complex distance analysis;
- realistic time analysis: use positive walking, waiting, and interchange time.

A zero-cost transfer means two nodes have identical shortest-path closeness values, although they remain distinct records.

## Workflow

### 1. Create nodes

Minimum schema:

```text
node_id
station_name
mode
city
operator
lines
lat
lon
status
current_active
physical_complex_id
coordinate_quality
notes
```

Use stable IDs. Display names are not IDs.

### 2. Create service edges

For each ordered route sequence, connect only consecutive active stops.

For sequence:

```text
A, B, C, D
```

create:

```text
A-B, B-C, C-D
```

Do not create `A-C` unless an express service actually stops at A and C while bypassing B under the selected service model.

When multiple routes share an edge, combine route labels while preserving one graph edge unless a multigraph is required.

### 3. Create transfer edges

Use the explicit transfer table. Do not infer a transfer solely from geographic proximity.

Recommended schema:

```text
from_id
to_id
transfer_type
station_hops
distance_km
transfer_minutes
paid_area
source
notes
```

### 4. Calculate distance

Preferred order:

1. official track/route distance;
2. OSM rail geometry length;
3. geodesic distance between adjacent stations as a disclosed proxy.

Use WGS84 coordinates and a geodesic or suitable projected CRS. Do not calculate kilometres directly from raw longitude/latitude degrees.

### 5. Build scenarios

Common scenarios:

- `base_current`: currently operating metro/urban rail;
- `multimodal_current`: base plus current regional/intercity services;
- `full_infrastructure`: includes temporarily closed or reconstructed stations;
- `planned`: future network, clearly separated from current results.

Keep scenario-specific node/edge activation fields instead of deleting source records.

### 6. Validate graph integrity

Check:

- node IDs are unique;
- every edge endpoint exists;
- no accidental self-loops;
- no duplicate edges with conflicting weights;
- active network connectivity or documented components;
- branch terminals and transfer hubs;
- zero-cost transfer pairs behave as intended;
- distance values are non-negative;
- implausibly long adjacent segments are flagged;
- current-service exclusions are documented.

### 7. Export

Required outputs:

```text
data/network/<scenario>_nodes.csv
data/network/<scenario>_edges.csv
data/network/<scenario>.graphml
data/network/<scenario>.geojson
data/network/<scenario>_shortest_hops.csv
data/network/<scenario>_shortest_km.csv
```

Optional:

- shortest-time matrix;
- route-specific graph;
- physical-complex contraction map;
- diagnostic map.

## Quality report

Produce a summary containing:

```text
node_count
edge_count
connected_components
network_diameter_by_metric
mean_shortest_path_by_metric
zero_weight_transfer_count
approximate_coordinate_count
inactive_station_count
```

## Handoff

Pass nodes, edges, shortest-path matrices, physical-complex mapping, and scenario metadata to `rail-centrality-analysis`.
