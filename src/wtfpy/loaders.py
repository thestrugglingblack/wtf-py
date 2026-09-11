"""Core dataset loading functionality for wtfpy."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from .exceptions import (
    DatasetNotFoundError,
    InvalidDatasetError,
)
from .utils import (
    LeagueInput,
    SeasonInput,
    filter_dataframe,
    get_layer_path,
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
    Base loader for a single canonical WTF dataset.
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
        """
        Return the published canonical dataset directory.
        """
        return get_layer_path("canonical")

    @property
    def file_path(self) -> Path:
        """
        Return the path to the requested dataset.

        Parquet is preferred when both Parquet and CSV files exist.
        """
        data_path = self.data_path

        parquet_path = (
            data_path
            / f"{self.dataset}.parquet"
        )

        csv_path = (
            data_path
            / f"{self.dataset}.csv"
        )

        if parquet_path.exists():
            return parquet_path

        if csv_path.exists():
            return csv_path

        raise DatasetNotFoundError(
            f"Could not find dataset '{self.dataset}' in {data_path}. "
            f"Expected {parquet_path.name} or {csv_path.name}."
        )

    def read(self) -> pl.DataFrame:
        """
        Read the complete dataset without applying filters.
        """
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
        """
        Read the dataset and apply optional season and league filters.
        """
        df = self.read()

        return filter_dataframe(
            df,
            seasons=seasons,
            league=league,
        )

    def available_seasons(
        self,
        *,
        league: LeagueInput = None,
    ) -> list[int]:
        """
        Return sorted seasons available in this dataset.
        """
        df = self.read()

        if league is not None:
            df = filter_dataframe(
                df,
                league=league,
            )

        return unique_sorted_seasons(df)

    def available_leagues(
        self,
        *,
        seasons: SeasonInput = None,
    ) -> list[str]:
        """
        Return sorted leagues available in this dataset.
        """
        df = self.read()

        if seasons is not None:
            df = filter_dataframe(
                df,
                seasons=seasons,
            )

        return unique_sorted_leagues(df)


def load_rosters(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load processed roster data.
    """
    return BaseLoader(
        "rosters"
    ).load(
        seasons=seasons,
        league=league,
    )


def load_games(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load processed game data.
    """
    return BaseLoader(
        "games"
    ).load(
        seasons=seasons,
        league=league,
    )


def load_player_game_stats(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load processed player game statistics.
    """
    return BaseLoader(
        "player_game_stats"
    ).load(
        seasons=seasons,
        league=league,
    )


def load_player_season_stats(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load processed player season statistics.
    """
    return BaseLoader(
        "player_season_stats"
    ).load(
        seasons=seasons,
        league=league,
    )


def load_team_season_stats(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load processed team season statistics.
    """
    return BaseLoader(
        "team_season_stats"
    ).load(
        seasons=seasons,
        league=league,
    )


def load_standings(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load processed standings data.
    """
    return BaseLoader(
        "standings"
    ).load(
        seasons=seasons,
        league=league,
    )


def available_seasons(
    *,
    league: LeagueInput = None,
    dataset: str = "games",
) -> list[int]:
    """
    Return sorted seasons available in a dataset.

    Games are used by default because they are the best general source
    of competition-season availability.
    """
    loader = BaseLoader(dataset)

    return loader.available_seasons(
        league=league,
    )


def available_leagues(
    *,
    seasons: SeasonInput = None,
    dataset: str = "games",
) -> list[str]:
    """
    Return sorted leagues available in a dataset.
    """
    loader = BaseLoader(dataset)

    return loader.available_leagues(
        seasons=seasons,
    )