# New York City Subway case

## Scope

- 423 station complexes.
- Staten Island Railway excluded.
- Same-complex free-transfer stations merged into one node.
- Consecutive scheduled stops connected by undirected edges.

## Data sources used in the original calculation

- MTA hourly ridership dataset: `https://data.ny.gov/resource/wujg-7c2s`
- Public route-stop sequence used to derive the graph: `https://github.com/acouch/transit-viz/blob/master/data/nyc_subway/routes_stops.csv`
- Public cleaned station-average table used in the original workflow: `https://github.com/sreejeetsreenivasan/PIC16B-Project/blob/master/TestingWorkplace/MTA%20Ridership%20and%20Density/MTA%20Average%20Monthly%20Ridership%20By%20Station.csv`

## Weighting

Hourly observations were aggregated by month and averaged over February 2022–October 2023. Destination station-complex average monthly ridership is \(P_j\):

\[
C_i^P=\frac{\sum_jP_j}{\sum_jP_jd_{ij}}
\]

where \(d_{ij}\) is the fewest stop-to-stop edges.

## Result table

The complete 423-complex result includes ordinary and passenger-weighted ranks, average stop distances, centrality values, station-complex ridership and coordinates.
