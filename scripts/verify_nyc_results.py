#!/usr/bin/env python3
"""Validate formula identities and ranking fields in the NYC result table."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "results" / "new_york" / "nyc_full_closeness_and_ridership_results.csv"


def main() -> None:
    frame = pd.read_csv(PATH)
    assert len(frame) == 423, f"Expected 423 station complexes, found {len(frame)}"
    assert np.allclose(frame["closeness_centrality"], 1 / frame["average_stops"])
    assert np.allclose(
        frame["passenger_weighted_closeness"],
        1 / frame["passenger_weighted_average_stops"],
    )
    assert np.array_equal(
        frame["rank_change"].to_numpy(),
        (frame["ordinary_rank"] - frame["weighted_rank"]).to_numpy(),
    )
    top = frame.sort_values(["weighted_rank", "station_complex_id"]).iloc[0]
    assert top["station_complex_id"] == "R238"
    print("NYC result table passed all checks.")


if __name__ == "__main__":
    main()
