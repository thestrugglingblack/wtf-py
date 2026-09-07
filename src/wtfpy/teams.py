"""Team-focused accessors for wtfpy."""

from __future__ import annotations

import polars as pl

from .loaders import BaseLoader
from .utils import LeagueInput, SeasonInput


class Teams:
    """Access team-centric WTF datasets."""

    def __init__(self) -> None:
        self._teams = BaseLoader("teams")
        self._season_stats = BaseLoader("team_season_stats")
        self._standings = BaseLoader("standings")

    def load(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """Load canonical team records."""
        return self._teams.load(
            seasons=seasons,
            league=league,
        )

    def season_stats(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """Load team season statistics."""
        return self._season_stats.load(
            seasons=seasons,
            league=league,
        )

    def standings(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """Load standings."""
        return self._standings.load(
            seasons=seasons,
            league=league,
        )

    def available_seasons(
        self,
        *,
        league: LeagueInput = None,
    ) -> list[int]:
        """Return seasons available in the team dataset."""
        return self._teams.available_seasons(
            league=league,
        )

    def available_leagues(
        self,
        *,
        seasons: SeasonInput = None,
    ) -> list[str]:
        """Return leagues available in the team dataset."""
        return self._teams.available_leagues(
            seasons=seasons,
        )


def load_teams(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """Load canonical team records."""
    return Teams().load(
        seasons=seasons,
        league=league,
    )
