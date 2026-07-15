# Changsha / Changsha–Zhuzhou–Xiangtan case

## Network scope

The current passenger-service extended network includes:

- Changsha Metro Lines 1–6;
- Changsha Maglev S2;
- active Changsha–Zhuzhou–Xiangtan intercity railway stations.

## Kilometre impedance

For adjacent service stations, edge cost is the WGS84 great-circle distance between station coordinates. This is a reproducible spatial proxy rather than exact rail alignment length.

Intermodal transfer edges cost 0 km. Nodes remain separate, so mode and station-level attributes can still be retained.

## Population weight

- Product: WorldPop China 2027 constrained population count, R2025A.
- Resolution: 1 km.
- Maximum service distance: 1,000 m.
- Allocation: nearest physical station complex, using a 10 × 10 subgrid per raster pixel.
- Colocated nodes: service population divided across member nodes.

## Formula

\[
C_i^{POP,D}=\frac{\sum_jR_j}{\sum_jR_jD_{ij}}
\]

where \(D_{ij}\) is the shortest cumulative network distance in kilometres and \(R_j\) is station-service population.

## Main result

The population-weighted kilometre centre remains in central Changsha. Wuyi Square ranks first, followed by Yingbin Road, Furong Square, Huangxing Square and Changsha Railway Station.
