#!/usr/bin/env python3
"""Validate the three published NYC passenger-weighted ranking tables."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "results" / "new_york"
FILES = [
    RESULT_DIR / "nyc_passenger_weighted_ranking_001_150.csv",
    RESULT_DIR / "nyc_passenger_weighted_ranking_151_300.csv",
    RESULT_DIR / "nyc_passenger_weighted_ranking_301_423.csv",
]


def main() -> None:
    frame = pd.concat((pd.read_csv(path) for path in FILES), ignore_index=True)

    assert len(frame) == 423, f"Expected 423 station complexes, found {len(frame)}"
    assert frame["station_complex_id"].is_unique
    assert frame["weighted_rank"].tolist() == list(range(1, 424))
    assert np.allclose(
        frame["passenger_weighted_closeness"],
        1 / frame["passenger_weighted_average_stops"],
    )

    top = frame.sort_values(["weighted_rank", "station_complex_id"]).iloc[0]
    assert top["station_complex_id"] == "R238"
    assert top["station"].startswith("Grand Central-42 St")
    print("NYC 423-complex ranking passed all checks.")


if __name__ == "__main__":
    main()
