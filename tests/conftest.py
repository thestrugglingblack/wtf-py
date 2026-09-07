from pathlib import Path

import polars as pl
import pytest


@pytest.fixture(autouse=True)
def isolate_wtf_data_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """
    Make every test use isolated fixture data.

    This prevents the developer's real WTF_DATA_PATH from leaking
    into the unit tests.
    """
    datasets = {
        "teams": pl.DataFrame(
            {
                "league": ["wfa", "wfa", "wnfc"],
                "season": [2024, 2025, 2025],
                "team_id": ["t1", "t2", "t3"],
                "team_name": [
                    "Chaos",
                    "Prodigy",
                    "Rebellion",
                ],
            }
        ),
        "players": pl.DataFrame(
            {
                "player_id": [
                    "p1",
                    "p2",
                    "p3",
                ],
                "player_name": [
                    "Alpha One",
                    "Beta Two",
                    "Gamma Three",
                ],
            }
        ),
        "rosters": pl.DataFrame(
            {
                "league": [
                    "wfa",
                    "wfa",
                    "wnfc",
                ],
                "season": [
                    2024,
                    2025,
                    2025,
                ],
                "team_id": [
                    "t1",
                    "t2",
                    "t3",
                ],
                "player_id": [
                    "p1",
                    "p2",
                    "p3",
                ],
            }
        ),
        "games": pl.DataFrame(
            {
                "league": [
                    "wfa",
                    "wfa",
                    "wnfc",
                    "wnfc",
                ],
                "season": [
                    2024,
                    2025,
                    2025,
                    2026,
                ],
                "game_id": [
                    "g1",
                    "g2",
                    "g3",
                    "g4",
                ],
            }
        ),
        "player_game_stats": pl.DataFrame(
            {
                "league": [
                    "wfa",
                    "wnfc",
                ],
                "season": [
                    2025,
                    2025,
                ],
                "game_id": [
                    "g2",
                    "g3",
                ],
                "player_id": [
                    "p2",
                    "p3",
                ],
            }
        ),
        "player_season_stats": pl.DataFrame(
            {
                "league": [
                    "wfa",
                    "wnfc",
                ],
                "season": [
                    2025,
                    2025,
                ],
                "player_id": [
                    "p2",
                    "p3",
                ],
            }
        ),
        "team_season_stats": pl.DataFrame(
            {
                "league": [
                    "wfa",
                    "wnfc",
                ],
                "season": [
                    2025,
                    2025,
                ],
                "team_id": [
                    "t2",
                    "t3",
                ],
            }
        ),
        "standings": pl.DataFrame(
            {
                "league": [
                    "wfa",
                    "wnfc",
                ],
                "season": [
                    2025,
                    2025,
                ],
                "team_name": [
                    "Prodigy",
                    "Rebellion",
                ],
                "wins": [
                    8,
                    7,
                ],
            }
        ),
    }

    for name, frame in datasets.items():
        frame.write_csv(
            tmp_path / f"{name}.csv"
        )

    monkeypatch.setenv(
        "WTF_DATA_PATH",
        str(tmp_path),
    )

    return tmp_path


@pytest.fixture
def processed_data_dir(
    isolate_wtf_data_path: Path,
) -> Path:
    return isolate_wtf_data_path