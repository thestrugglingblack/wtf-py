"""
Analytics data accessors for wtfpy.

Analytics datasets are published beside the canonical datasets.

Expected layout:

<release>/
├── datasets/
│   ├── games.parquet
│   └── ...
└── analytics/
    ├── mart_players.parquet
    ├── mart_player_game_logs.parquet
    ├── mart_player_season_stats.parquet
    ├── mart_qb_season_stats.parquet
    ├── mart_player_career_stats.parquet
    └── mart_team_season_summary.parquet

WTF_DATA_PATH should continue pointing to the canonical
datasets directory.
"""

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
    get_data_path,
    unique_sorted_leagues,
    unique_sorted_seasons,
)


SUPPORTED_ANALYTICS_DATASETS = {
    "mart_players",
    "mart_player_game_logs",
    "mart_player_season_stats",
    "mart_qb_season_stats",
    "mart_player_career_stats",
    "mart_team_season_summary",
}


class AnalyticsLoader:
    """
    Loader for a published WTF analytics mart.
    """

    def __init__(
        self,
        dataset: str,
    ) -> None:
        if dataset not in SUPPORTED_ANALYTICS_DATASETS:
            raise InvalidDatasetError(
                f"Unsupported analytics dataset: {dataset}"
            )

        self.dataset = dataset

    @property
    def analytics_path(self) -> Path:
        """
        Return the analytics directory associated with WTF_DATA_PATH.

        Normal layout:

        release/
        ├── datasets/   <- WTF_DATA_PATH
        └── analytics/
        """

        data_path = get_data_path()

        sibling_path = (
            data_path.parent
            / "analytics"
        )

        nested_path = (
            data_path
            / "analytics"
        )

        if sibling_path.exists():
            return sibling_path

        if nested_path.exists():
            return nested_path

        raise DatasetNotFoundError(
            "Could not find the published analytics directory. "
            f"Expected {sibling_path}."
        )

    @property
    def file_path(self) -> Path:
        """
        Return the Parquet path for the requested analytics mart.
        """

        path = (
            self.analytics_path
            / f"{self.dataset}.parquet"
        )

        if not path.exists():
            raise DatasetNotFoundError(
                "Could not find analytics dataset "
                f"'{self.dataset}'. Expected {path}."
            )

        return path

    def read(self) -> pl.DataFrame:
        """
        Read the complete analytics mart.
        """

        return pl.read_parquet(
            self.file_path
        )

    def load(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """
        Load an analytics mart with optional filters.
        """

        dataframe = self.read()

        return filter_dataframe(
            dataframe,
            seasons=seasons,
            league=league,
        )

    def available_seasons(
        self,
        *,
        league: LeagueInput = None,
    ) -> list[int]:
        """
        Return seasons represented in this mart.
        """

        dataframe = self.read()

        if league is not None:
            dataframe = filter_dataframe(
                dataframe,
                league=league,
            )

        return unique_sorted_seasons(
            dataframe
        )

    def available_leagues(
        self,
        *,
        seasons: SeasonInput = None,
    ) -> list[str]:
        """
        Return leagues represented in this mart.
        """

        dataframe = self.read()

        if seasons is not None:
            dataframe = filter_dataframe(
                dataframe,
                seasons=seasons,
            )

        return unique_sorted_leagues(
            dataframe
        )


class Analytics:
    """
    Access WTF analytical datasets.
    """

    def __init__(self) -> None:
        self._players = AnalyticsLoader(
            "mart_players"
        )

        self._player_game_logs = AnalyticsLoader(
            "mart_player_game_logs"
        )

        self._player_season_stats = AnalyticsLoader(
            "mart_player_season_stats"
        )

        self._qb_season_stats = AnalyticsLoader(
            "mart_qb_season_stats"
        )

        self._player_career_stats = AnalyticsLoader(
            "mart_player_career_stats"
        )

        self._team_season_summary = AnalyticsLoader(
            "mart_team_season_summary"
        )

    def players(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """
        Load the historical analytical player directory.
        """

        return self._players.load(
            seasons=seasons,
            league=league,
        )

    def player_game_logs(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """
        Load enriched player game logs.
        """

        return self._player_game_logs.load(
            seasons=seasons,
            league=league,
        )

    def player_season_stats(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """
        Load analytical player season statistics.
        """

        return self._player_season_stats.load(
            seasons=seasons,
            league=league,
        )

    def qb_season_stats(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """
        Load quarterback season analytics.
        """

        return self._qb_season_stats.load(
            seasons=seasons,
            league=league,
        )

    def player_career_stats(
        self,
        *,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """
        Load player career analytics.

        Career records do not contain a single season,
        so only league filtering is supported.
        """

        return self._player_career_stats.load(
            league=league,
        )

    def team_season_summary(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """
        Load team season summaries.
        """

        return self._team_season_summary.load(
            seasons=seasons,
            league=league,
        )


def load_analytics_players(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load the analytical historical player directory.
    """

    return AnalyticsLoader(
        "mart_players"
    ).load(
        seasons=seasons,
        league=league,
    )


def load_analytics_player_game_logs(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load enriched player game logs.
    """

    return AnalyticsLoader(
        "mart_player_game_logs"
    ).load(
        seasons=seasons,
        league=league,
    )


def load_analytics_player_season_stats(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load analytical player season statistics.
    """

    return AnalyticsLoader(
        "mart_player_season_stats"
    ).load(
        seasons=seasons,
        league=league,
    )


def load_qb_season_stats(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load quarterback season analytics.
    """

    return AnalyticsLoader(
        "mart_qb_season_stats"
    ).load(
        seasons=seasons,
        league=league,
    )


def load_player_career_stats(
    *,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load player career analytics.
    """

    return AnalyticsLoader(
        "mart_player_career_stats"
    ).load(
        league=league,
    )


def load_team_season_summary(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load analytical team season summaries.
    """

    return AnalyticsLoader(
        "mart_team_season_summary"
    ).load(
        seasons=seasons,
        league=league,
    )


def available_analytics_seasons(
    *,
    league: LeagueInput = None,
    dataset: str = "mart_player_season_stats",
) -> list[int]:
    """
    Return seasons available in an analytical dataset.
    """

    return AnalyticsLoader(
        dataset
    ).available_seasons(
        league=league,
    )


def available_analytics_leagues(
    *,
    seasons: SeasonInput = None,
    dataset: str = "mart_player_season_stats",
) -> list[str]:
    """
    Return leagues available in an analytical dataset.
    """

    return AnalyticsLoader(
        dataset
    ).available_leagues(
        seasons=seasons,
    )