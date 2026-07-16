# Reusable Skills

This directory packages the complete urban-rail centrality workflow as four composable skills.

## 1. OSM + Wiki source collection

[`osm-wiki-source-collection/SKILL.md`](osm-wiki-source-collection/SKILL.md)

Collects and reconciles station names, coordinates, route order, service status, transfer identity, OSM IDs, Wikidata QIDs, and source confidence.

**Input:** city/region, included modes, analysis date and service scenario.  
**Output:** canonical stations, route sequences, transfer pairs, source audit and unresolved items.

## 2. Rail network construction

[`rail-network-construction/SKILL.md`](rail-network-construction/SKILL.md)

Converts audited route sequences into explicit graph scenarios with service edges, transfer edges, station-hop, kilometre and optional time costs.

**Input:** canonical stations, route sequences and transfer policy.  
**Output:** nodes, edges, GraphML, GeoJSON and shortest-path matrices.

## 3. Rail centrality analysis

[`rail-centrality-analysis/SKILL.md`](rail-centrality-analysis/SKILL.md)

Calculates ordinary and demand-weighted closeness using station hops, kilometres or time. Includes population/ridership assignment, tie handling, sensitivity analysis and validation.

**Input:** graph/matrices and optional demand weights.  
**Output:** complete rankings, rank changes, comparison workbook and method record.

## 4. End-to-end pipeline

[`urban-rail-centrality-pipeline/SKILL.md`](urban-rail-centrality-pipeline/SKILL.md)

Orchestrates the full sequence:

```text
OSM / Wiki / official data
→ source reconciliation
→ rail graph
→ shortest paths
→ ordinary centrality
→ demand weighting
→ full reproducible results
```

Use this when starting from only a city name and a requested set of rail modes.

## Recommended invocation order

```text
urban-rail-centrality-pipeline
  ├─ osm-wiki-source-collection
  ├─ rail-network-construction
  └─ rail-centrality-analysis
```

Each skill is deliberately independent so that a verified station/route dataset or an existing graph can enter the workflow at the appropriate stage.
