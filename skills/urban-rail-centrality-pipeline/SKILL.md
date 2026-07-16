---
name: urban-rail-centrality-pipeline
description: Orchestrate the complete public-data urban rail analysis workflow from OSM/Wikipedia source collection through graph construction to ordinary and demand-weighted centrality results. Use when a user asks to analyse a city's metro/rail network end to end.
---

# Urban Rail Centrality Pipeline

## Purpose

Run an end-to-end, auditable workflow:

```text
OSM / operator / Wiki sources
        ↓
station and route reconciliation
        ↓
rail graph construction
        ↓
shortest-path matrices
        ↓
ordinary centrality
        ↓
population/ridership-weighted centrality
        ↓
full rankings, workbook, maps, and method record
```

This skill coordinates:

1. `osm-wiki-source-collection`
2. `rail-network-construction`
3. `rail-centrality-analysis`

## Trigger examples

Use this skill when the user asks:

- “分析某城市轨道交通线网接近中心性”；
- “从OSM和维基建立地铁线网”；
- “加入城际铁路、磁浮、有轨电车后重新排名”；
- “用人口或客流对中心度加权”；
- “比较站数、公里、时间三种中心性”；
- “生成完整站点排名和可复现代码”。

## Initial specification

Resolve or infer:

```yaml
study_area:
analysis_date:
modes:
base_scenario:
extended_scenario:
node_policy:
transfer_policy:
distance_metrics:
demand_weight:
catchment_method:
output_formats:
```

Recommended defaults:

```yaml
base_scenario: current urban rail passenger service
extended_scenario: base plus current regional/intercity passenger service
node_policy: same-system merged, cross-mode separate
transfer_policy:
  hops: 0
  km: 0
  time: positive transfer penalty
distance_metrics: [hops, km]
demand_weight: none first, then population or ridership
output_formats: [csv, xlsx, graphml, geojson]
```

State all assumptions before interpreting results.

## Pipeline

### Stage 1 — Source collection

Invoke `osm-wiki-source-collection`.

Deliverables required before continuing:

- canonical stations;
- ordered route sequences;
- transfer pairs;
- current/inactive status;
- source audit;
- coordinate-quality flags;
- unresolved items.

Stop and flag the issue when route order or transfer identity cannot be established reliably.

### Stage 2 — Graph construction

Invoke `rail-network-construction`.

Construct at least:

- base current network;
- extended current network when regional modes are included.

Calculate separate edge weights for:

- station hops;
- kilometres;
- time when available.

Export graph files and shortest-path matrices.

### Stage 3 — Ordinary centrality

Invoke `rail-centrality-analysis` without demand weights.

Calculate full rankings for each scenario and metric.

Explain structural differences before adding demand weights. In particular:

- hop models favour routes that cover large areas with few stops;
- kilometre models favour spatially central locations;
- time models may restore advantages of faster regional rail;
- dense station areas receive more destination-node weight in an equal-node model.

### Stage 4 — Demand weights

Select one or more:

- station ridership;
- population raster;
- employment;
- activity/POI index.

For population:

- avoid overlapping-buffer double counting;
- assign cells/subcells to one physical complex;
- state raster year and resolution;
- identify projected versus observed population.

For ridership:

- match the graph node definition;
- use a consistent period;
- retain missing-data diagnostics.

### Stage 5 — Weighted centrality

Calculate:

- population/ridership-weighted hops;
- population/ridership-weighted kilometres;
- weighted time when possible.

Compare ordinary and weighted rank changes.

### Stage 6 — Validation

Required checks:

```text
[ ] every active node is in each matrix
[ ] matrix row and column order matches
[ ] diagonal is zero
[ ] zero-cost transfer pairs have identical distance rows
[ ] weighted score = 1 / weighted mean distance
[ ] all scores are finite
[ ] tie handling is consistent
[ ] demand is not duplicated
[ ] approximate coordinates are disclosed
[ ] complete rankings are exported
```

### Stage 7 — Deliverables

Create:

```text
README.md
METHOD.md
SOURCES.md
ASSUMPTIONS.md

data/source/
data/network/
data/demand/

results/base/
results/extended/

scripts/
artifacts/
```

Minimum result package:

- node and edge tables;
- source audit;
- GraphML and GeoJSON;
- shortest-hop and shortest-km matrices;
- ordinary rankings;
- demand-weighted rankings;
- one comparison workbook;
- one machine-readable method JSON;
- full reproduction script.

## Interpretation framework

Use this sequence:

1. **Topology:** Which station reaches the largest number of station nodes in fewest intervals?
2. **Geometry:** Which station minimizes cumulative network kilometres?
3. **Demand:** Which station is closest to high-population or high-ridership destinations?
4. **Multimodality:** How does adding regional/intercity rail change the centre?
5. **Sensitivity:** Which results remain stable under alternate assumptions?

Do not collapse these into one claim of absolute centrality.

## Common decision rules

### Same physical station, different modes

Default:

- preserve separate nodes;
- connect with explicit transfer edge;
- use zero hops/zero km only when modelling the interchange as one physical location;
- use positive time for realistic accessibility.

### Temporarily closed stations

- exclude from `current_passenger_service`;
- retain in `full_infrastructure`;
- document how adjacent active stations are connected in each scenario.

### Approximate coordinates

- acceptable for hop centrality;
- not acceptable for final fine-scale distance or catchment analysis without sensitivity disclosure.

### Disconnected graph

Do not calculate ordinary closeness across unreachable nodes without stating a method. Use component analysis or harmonic centrality.

## Final response pattern

Report:

- scope and date;
- network node/edge counts;
- ordinary hop centre;
- ordinary kilometre centre;
- weighted centres;
- notable rank changes;
- effect of adding modes;
- data limitations;
- links to complete files and repository.

The final result must remain understandable without opening the workbook, while the repository must contain enough detail to reproduce every ranking.
