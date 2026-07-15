"""WorldPop raster allocation helpers used by the Changsha/CZT case."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from rasterio.windows import Window, from_bounds
from scipy.spatial import cKDTree


def allocate_population_to_nearest_station(
    raster_path: str | Path,
    complexes: pd.DataFrame,
    *,
    max_distance_m: float = 1000.0,
    subgrid: int = 10,
    projected_crs: str = "EPSG:32649",
) -> pd.Series:
    """Allocate population raster cells to the nearest station complex.

    Each raster cell is represented by a ``subgrid × subgrid`` lattice. Every
    subcell is assigned once to its nearest physical station complex when that
    complex is no farther than ``max_distance_m``. Population beyond the
    catchment limit is excluded.
    """
    required = {"complex_id", "lon", "lat"}
    missing = required - set(complexes.columns)
    if missing:
        raise ValueError(f"Missing complex columns: {sorted(missing)}")
    if subgrid < 1:
        raise ValueError("subgrid must be at least 1")

    to_projected = Transformer.from_crs(
        "EPSG:4326", projected_crs, always_xy=True
    )
    sx, sy = to_projected.transform(complexes["lon"], complexes["lat"])
    tree = cKDTree(np.column_stack([sx, sy]))
    totals = np.zeros(len(complexes), dtype=float)

    offsets = (np.arange(subgrid) + 0.5) / subgrid
    row_offsets, col_offsets = np.meshgrid(offsets, offsets, indexing="ij")
    row_offsets = row_offsets.ravel()
    col_offsets = col_offsets.ravel()
    divisor = float(subgrid * subgrid)

    with rasterio.open(raster_path) as source:
        margin_deg = 0.04
        window = from_bounds(
            complexes["lon"].min() - margin_deg,
            complexes["lat"].min() - margin_deg,
            complexes["lon"].max() + margin_deg,
            complexes["lat"].max() + margin_deg,
            source.transform,
        ).round_offsets().round_lengths()
        window = Window(
            max(0, int(window.col_off)),
            max(0, int(window.row_off)),
            min(source.width - max(0, int(window.col_off)), int(window.width)),
            min(source.height - max(0, int(window.row_off)), int(window.height)),
        )
        raster = source.read(1, window=window, masked=True)
        transform = source.window_transform(window)
        values = raster.filled(np.nan)
        valid = (
            np.isfinite(values)
            & (~np.ma.getmaskarray(raster))
            & (values > 0)
        )

        for row, col in zip(*np.where(valid)):
            population = float(values[row, col])
            xs = (
                transform.c
                + (col + col_offsets) * transform.a
                + (row + row_offsets) * transform.b
            )
            ys = (
                transform.f
                + (col + col_offsets) * transform.d
                + (row + row_offsets) * transform.e
            )
            px, py = to_projected.transform(xs, ys)
            distances, nearest = tree.query(np.column_stack([px, py]), k=1)
            accepted = distances <= max_distance_m
            np.add.at(totals, nearest[accepted], population / divisor)

    return pd.Series(
        totals,
        index=complexes["complex_id"],
        name="service_population",
    )


def split_complex_population(
    node_to_complex: dict[str, str], complex_population: pd.Series
) -> dict[str, float]:
    """Split each physical complex's population across retained graph nodes."""
    members: dict[str, list[str]] = defaultdict(list)
    for node, complex_id in node_to_complex.items():
        members[complex_id].append(node)
    return {
        node: float(complex_population.get(complex_id, 0.0))
        / len(members[complex_id])
        for node, complex_id in node_to_complex.items()
    }
