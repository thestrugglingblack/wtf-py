"""Player-focused accessors for wtfpy."""

from __future__ import annotations

import polars as pl

from .loaders import BaseLoader
from .utils import LeagueInput, SeasonInput


class Players:
    """Access player-centric WTF datasets."""

    def __init__(self) -> None:
        self._players = BaseLoader("players")
        self._game_stats = BaseLoader("player_game_stats")
        self._season_stats = BaseLoader("player_season_stats")

    def load(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """Load canonical player records."""
        return self._players.load(
            seasons=seasons,
            league=league,
        )

    def game_stats(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """Load player game statistics."""
        return self._game_stats.load(
            seasons=seasons,
            league=league,
        )

    def season_stats(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """Load player season statistics."""
        return self._season_stats.load(
            seasons=seasons,
            league=league,
        )

    def available_seasons(
        self,
        *,
        league: LeagueInput = None,
    ) -> list[int]:
        """Return seasons available in the player dataset."""
        return self._players.available_seasons(
            league=league,
        )

    def available_leagues(
        self,
        *,
        seasons: SeasonInput = None,
    ) -> list[str]:
        """Return leagues available in the player dataset."""
        return self._players.available_leagues(
            seasons=seasons,
        )


def load_players(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """Load canonical player records."""
    return Players().load(
        seasons=seasons,
        league=league,
    )
