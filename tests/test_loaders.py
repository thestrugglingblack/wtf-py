from pathlib import Path

import polars as pl
import pytest

import wtfpy
from wtfpy.exceptions import (
    DatasetNotFoundError,
    InvalidDatasetError,
)
from wtfpy.loaders import BaseLoader


def test_public_api_exports() -> None:
    assert callable(wtfpy.load_games)
    assert callable(wtfpy.available_seasons)
    assert callable(wtfpy.available_leagues)


def test_base_loader_reads_csv(
    processed_data_dir: Path,
) -> None:
    df = BaseLoader("games").read()

    assert isinstance(df, pl.DataFrame)
    assert df.height == 4


def test_invalid_dataset() -> None:
    with pytest.raises(InvalidDatasetError):
        BaseLoader("not_a_dataset")


def test_missing_dataset(
    processed_data_dir: Path,
) -> None:
    (
        processed_data_dir
        / "games.csv"
    ).unlink()

    with pytest.raises(
        DatasetNotFoundError
    ):
        BaseLoader("games").read()


def test_parquet_preferred(
    processed_data_dir: Path,
) -> None:
    pl.DataFrame(
        {
            "league": ["wnfc"],
            "season": [2030],
            "game_id": ["parquet-game"],
        }
    ).write_parquet(
        processed_data_dir
        / "games.parquet"
    )

    df = BaseLoader("games").read()

    assert (
        df["game_id"].to_list()
        == ["parquet-game"]
    )


def test_load_games_filters(
    processed_data_dir: Path,
) -> None:
    df = wtfpy.load_games(
        seasons=2025,
        league="WNFC",
    )

    assert (
        df["game_id"].to_list()
        == ["g3"]
    )


def test_empty_filter_result(
    processed_data_dir: Path,
) -> None:
    df = wtfpy.load_games(
        seasons=1999,
    )

    assert df.is_empty()


def test_available_seasons(
    processed_data_dir: Path,
) -> None:
    assert (
        wtfpy.available_seasons()
        == [2024, 2025, 2026]
    )


def test_available_leagues(
    processed_data_dir: Path,
) -> None:
    assert (
        wtfpy.available_leagues()
        == ["wfa", "wnfc"]
    )