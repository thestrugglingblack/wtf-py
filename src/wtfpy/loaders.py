"""Core dataset loading functionality for wtfpy."""

from __future__ import annotations

from pathlib import Path

import polars as pl

try:
    from .exceptions import (
        DatasetNotFoundError,
        InvalidDatasetError,
    )
except ImportError:  # pragma: no cover - fallback for some tooling setups
    from wtfpy.exceptions import (
        DatasetNotFoundError,
        InvalidDatasetError,
    )
from .utils import (
    LeagueInput,
    SeasonInput,
    filter_dataframe,
    get_data_path,
    unique_sorted_leagues,
    unique_sorted_seasons,
)

SUPPORTED_DATASETS = {
    "teams",
    "players",
    "rosters",
    "games",
    "player_game_stats",
    "player_season_stats",
    "team_season_stats",
    "standings",
}


class BaseLoader:
    """
    Base class for loading processed WTF datasets.

    Dataset location always comes from the WTF_DATA_PATH environment variable.
    """

    def __init__(
        self,
        dataset: str,
    ) -> None:
        if dataset not in SUPPORTED_DATASETS:
            raise InvalidDatasetError(
                f"Unsupported dataset: {dataset}"
            )

        self.dataset = dataset

    @property
    def data_path(self) -> Path:
        """Return the configured processed-data directory."""
        return get_data_path()

    @property
    def file_path(self) -> Path:
        """
        Return the dataset file path.

        Parquet is preferred when both Parquet and CSV are available.
        """
        parquet_path = self.data_path / f"{self.dataset}.parquet"
        csv_path = self.data_path / f"{self.dataset}.csv"

        if parquet_path.exists():
            return parquet_path

        if csv_path.exists():
            return csv_path

        raise DatasetNotFoundError(
            f"Could not find dataset '{self.dataset}' in {self.data_path}. "
            f"Expected {parquet_path.name} or {csv_path.name}."
        )

    def read(self) -> pl.DataFrame:
        """Read the full dataset without applying filters."""
        path = self.file_path

        if path.suffix.lower() == ".parquet":
            return pl.read_parquet(path)

        return pl.read_csv(
            path,
            infer_schema_length=10_000,
            null_values=[
                "",
                "null",
                "NULL",
                "None",
                "NA",
                "N/A",
            ],
        )

    def load(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """Load the dataset and optionally filter by season and league."""
        return filter_dataframe(
            self.read(),
            seasons=seasons,
            league=league,
        )

    def available_seasons(
        self,
        *,
        league: LeagueInput = None,
    ) -> list[int]:
        """Return seasons available in this dataset."""
        df = filter_dataframe(
            self.read(),
            league=league,
        )

        return unique_sorted_seasons(df)

    def available_leagues(
        self,
        *,
        seasons: SeasonInput = None,
    ) -> list[str]:
        """Return leagues available in this dataset."""
        df = filter_dataframe(
            self.read(),
            seasons=seasons,
        )

        return unique_sorted_leagues(df)


def _load_dataset(
    dataset: str,
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    return BaseLoader(dataset).load(
        seasons=seasons,
        league=league,
    )


def load_rosters(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """Load processed roster data."""
    return _load_dataset(
        "rosters",
        seasons=seasons,
        league=league,
    )


def load_games(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """Load processed game data."""
    return _load_dataset(
        "games",
        seasons=seasons,
        league=league,
    )


def load_player_game_stats(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """Load processed player game statistics."""
    return _load_dataset(
        "player_game_stats",
        seasons=seasons,
        league=league,
    )


def load_player_season_stats(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """Load processed player season statistics."""
    return _load_dataset(
        "player_season_stats",
        seasons=seasons,
        league=league,
    )


def load_team_season_stats(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """Load processed team season statistics."""
    return _load_dataset(
        "team_season_stats",
        seasons=seasons,
        league=league,
    )


def load_standings(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """Load processed standings."""
    return _load_dataset(
        "standings",
        seasons=seasons,
        league=league,
    )


def available_seasons(
    *,
    league: LeagueInput = None,
    dataset: str = "games",
) -> list[int]:
    """Return seasons available in a dataset."""
    return BaseLoader(dataset).available_seasons(
        league=league,
    )


def available_leagues(
    *,
    seasons: SeasonInput = None,
    dataset: str = "games",
) -> list[str]:
    """Return leagues available in a dataset."""
    return BaseLoader(dataset).available_leagues(
        seasons=seasons,
    )
