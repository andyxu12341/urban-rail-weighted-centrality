---
name: osm-wiki-source-collection
description: Collect, reconcile, and audit urban rail station and route data from OpenStreetMap, Wikipedia/Wikidata, operator pages, and GTFS. Use when a user asks to build a rail network from public sources, verify station order/status, or prepare node and route tables for centrality analysis.
---

# OSM + Wiki Urban Rail Source Collection

## Goal

Build an auditable, current station-and-route source table that can be passed directly to the network-construction skill.

## Required inputs

- Study area: city, metropolitan region, or corridor.
- Included modes: metro, subway, suburban rail, intercity rail, tram, light rail, monorail, maglev, automated people mover, etc.
- Analysis date.
- Scenario:
  - `current_passenger_service`
  - `full_infrastructure`
  - `planned_network`
- Preferred node granularity:
  - physical station complex
  - mode/platform-level node
- Output language and station-name convention.

When an input is missing, infer the most conservative current-passenger-service scope and record the assumption.

## Source priority

Use sources in this order:

1. Operator GTFS, official route maps, station lists, timetables, or government open data.
2. OpenStreetMap route relations and station geometries.
3. Wikidata for stable identifiers and aliases.
4. Wikipedia for chronology, opening/closure notes, and readable station order.
5. Other public sources only as supporting evidence.

Never treat a single Wikipedia table as the sole source of current operational status.

## Workflow

### 1. Define scope and date

Create a scope record containing:

```yaml
study_area: Changsha-Zhuzhou-Xiangtan
analysis_date: 2026-07-16
modes: [metro, maglev, intercity_rail]
scenario: current_passenger_service
node_granularity: separate_modes_same_complex
```

### 2. Query OSM

Retrieve:

- route relations for relevant rail modes;
- ordered members where available;
- station/stop/platform objects;
- coordinates and names;
- operator, network, line/ref, opening/status tags;
- transfer complexes and shared station areas.

Prefer relation membership and stop order over spatial nearest-neighbour inference.

Record the OSM object ID and retrieval timestamp for every source row.

### 3. Cross-check with Wiki/Wikidata

For every line and station, verify:

- official/current name;
- aliases and former names;
- opening date;
- closure, suspension, reconstruction, or temporary non-service status;
- branch structure and terminal stations;
- whether the page describes infrastructure or current passenger service.

Use Wikidata QIDs when available to stabilize identity across language variants.

### 4. Normalize station identity

Create a canonical station key independent of display name.

Recommended fields:

```text
source_station_id
canonical_station_id
station_name
station_name_local
station_name_en
mode
city
operator
network
lines
lat
lon
status
current_active
osm_type
osm_id
wikidata_qid
source_urls
coordinate_quality
source_confidence
notes
```

Rules:

- Normalize punctuation, spaces, full-width characters, and suffixes such as “站” or “Station”.
- Do not merge stations only because their names are similar.
- Use coordinates, operator, line membership, transfer evidence, and identifiers together.
- Keep mode-specific nodes separate when the analysis requires explicit transfer edges.

### 5. Reconstruct line order

For each route, produce an ordered stop sequence:

```text
route_id, route_name, direction_or_branch, sequence, canonical_station_id
```

Handle:

- branches;
- loops;
- short-turn services;
- express/local stopping patterns;
- shared track segments;
- suspended or non-passenger stations.

Do not connect two stations merely because they are geographically close.

### 6. Assign confidence

Use:

- `A`: official source and OSM/Wiki agree;
- `B`: two independent public sources agree;
- `C`: one source or approximate coordinate;
- `D`: inferred and requires manual review.

Any `C` or `D` coordinate must be flagged before distance-based analysis.

## Required outputs

Write:

```text
data/source/stations_raw.csv
data/source/route_sequences_raw.csv
data/source/source_audit.csv
data/source/unresolved_items.csv
```

`source_audit.csv` should include the claim, source, retrieval date, and confidence.

## Validation checklist

Before handoff:

- every route has at least two active stops;
- station coordinates fall inside the study area;
- no duplicate canonical IDs;
- terminal and branch order matches at least two sources;
- closed/suspended stations are scenario-specific rather than silently deleted;
- transfer pairs are explicitly listed;
- all approximate coordinates are disclosed.

## Handoff

Pass the canonical station table, ordered route table, explicit transfer-pair table, scenario definition, and unresolved-items list to `rail-network-construction`.
