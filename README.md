# Urban Rail Weighted Centrality

A reproducible comparison of demand-weighted closeness centrality for two urban rail systems:

1. **New York City Subway** — station-hop distance weighted by average monthly ridership.
2. **Changsha / Changsha–Zhuzhou–Xiangtan rail network** — network-kilometre distance weighted by WorldPop 2027 station-service population.

本仓库整理纽约地铁与长沙—长株潭轨道网络的接近中心性计算方法、可运行算法和完整结果。

## Core formula

Ordinary closeness centrality:

\[
C_i=\frac{N-1}{\sum_{j\ne i}d_{ij}}=\frac{1}{\bar d_i}
\]

Demand-weighted closeness centrality:

\[
C_i^W=\frac{\sum_j W_j}{\sum_j W_j d_{ij}}=\frac{1}{\bar d_i^W}
\]

- \(d_{ij}\): shortest network distance from station \(i\) to destination station \(j\).
- \(W_j\): destination demand weight, such as ridership or service population.
- A larger score means a station is, on average, closer to high-demand destinations.

## Headline results

### New York City Subway — passenger-weighted station-hop centrality

| Rank | Station complex | Weighted average stops | Weighted closeness |
|---:|---|---:|---:|
| 1 | Grand Central–42 St | 5.162 | 0.193727 |
| 2 | 14 St–Union Sq | 5.247 | 0.190574 |
| 3 | Times Sq–42 St / Bryant Park / 5 Av complex | 5.302 | 0.188598 |
| 4 | Lexington Av–53 St / 51 St | 5.447 | 0.183579 |
| 5 | 34 St–Herald Sq | 5.449 | 0.183504 |

Full result: [`results/new_york/nyc_full_closeness_and_ridership_results.csv`](results/new_york/nyc_full_closeness_and_ridership_results.csv)

### Changsha–Zhuzhou–Xiangtan — population-weighted kilometre centrality

| Rank | Station node | Mode | Weighted average km | Weighted closeness |
|---:|---|---|---:|---:|
| 1 | 五一广场 | Metro | 9.807 | 0.101965 |
| 2 | 迎宾路口 | Metro | 9.950 | 0.100504 |
| 3 | 芙蓉广场 | Metro | 9.965 | 0.100347 |
| 4 | 黄兴广场 | Metro | 10.011 | 0.099885 |
| 5 | 长沙火车站 | Metro | 10.084 | 0.099171 |

Full result: [`results/changsha/czt_population_weighted_km_results.csv`](results/changsha/czt_population_weighted_km_results.csv)

## Repository layout

```text
.
├── docs/                       Methodology and source notes
├── src/urban_rail_centrality/  Reusable Python algorithms
├── scripts/                    Recompute and verification commands
├── data/changsha/              Reproducible Changsha/CZT inputs
├── data/new_york/              NYC source instructions
├── results/                    Machine-readable complete rankings
└── artifacts/                  Excel deliverables
```

## Recompute the Changsha/CZT result

```bash
python -m pip install -r requirements.txt
python scripts/recompute_changsha.py
```

The regenerated file is written to:

```text
outputs/czt_population_weighted_km_results.csv
```

## Verify the NYC published result

The repository contains the complete 423-complex result table but not redistributed MTA source extracts. You can verify ranking and inverse-distance identities with:

```bash
python scripts/verify_nyc_results.py
```

See [`docs/new_york_method.md`](docs/new_york_method.md) for full reconstruction sources.

## Interpretation

This metric is **destination-weighted accessibility**, not observed origin–destination travel time and not a forecast of ridership at the candidate station. Results depend on:

- graph node and transfer definitions;
- edge-cost choice: stops, kilometres or time;
- destination-weight definition;
- temporal scope and spatial resolution of demand data.

## Licensing

- Code: MIT License.
- Derived result tables: CC BY 4.0, subject to attribution of the original public data providers.
- Source datasets retain their original terms; large raw WorldPop and MTA source files are not redistributed here.
