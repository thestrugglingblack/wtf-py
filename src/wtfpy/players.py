"""Player-focused data access for wtfpy."""

from __future__ import annotations

import polars as pl

from .exceptions import (
    DataRelationshipError,
    DatasetSchemaError,
)
from .loaders import BaseLoader
from .utils import (
    LeagueInput,
    SeasonInput,
    normalize_leagues,
    normalize_seasons,
)


class Players:
    """
    Access player-related WTF datasets.

    The canonical players dataset is treated as an identity table.

    Season and league membership are determined through the rosters
    dataset rather than assuming those columns exist in players.csv.
    """

    def __init__(self) -> None:
        self._players = BaseLoader(
            "players"
        )

        self._rosters = BaseLoader(
            "rosters"
        )

        self._game_stats = BaseLoader(
            "player_game_stats"
        )

        self._season_stats = BaseLoader(
            "player_season_stats"
        )

    def load(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """
        Load canonical player records.

        If no filters are provided, the canonical players table is
        returned directly.

        If season or league filtering is requested, roster membership is
        used to determine which player IDs belong to the requested scope.
        """
        players = self._players.read()

        if seasons is None and league is None:
            return players

        if "player_id" not in players.columns:
            raise DatasetSchemaError(
                "players dataset does not contain 'player_id'."
            )

        rosters = self._rosters.read()

        required_columns = {
            "player_id",
        }

        if seasons is not None:
            required_columns.add(
                "season"
            )

        if league is not None:
            required_columns.add(
                "league"
            )

        missing_columns = (
            required_columns
            - set(rosters.columns)
        )

        if missing_columns:
            raise DataRelationshipError(
                "Cannot filter players because rosters is missing required "
                "columns: "
                + ", ".join(
                    sorted(
                        missing_columns
                    )
                )
            )

        roster_membership = rosters

        season_values = normalize_seasons(
            seasons
        )

        league_values = normalize_leagues(
            league
        )

        if season_values is not None:
            roster_membership = (
                roster_membership.filter(
                    pl.col("season")
                    .cast(
                        pl.Int64,
                        strict=False,
                    )
                    .is_in(
                        season_values
                    )
                )
            )

        if league_values is not None:
            roster_membership = (
                roster_membership.filter(
                    pl.col("league")
                    .cast(pl.String)
                    .str.strip_chars()
                    .str.to_lowercase()
                    .is_in(
                        league_values
                    )
                )
            )

        eligible_players = (
            roster_membership
            .select(
                "player_id"
            )
            .drop_nulls()
            .unique()
        )

        return players.join(
            eligible_players,
            on="player_id",
            how="semi",
        )

    def game_stats(
        self,
        *,
        seasons: SeasonInput = None,
        league: LeagueInput = None,
    ) -> pl.DataFrame:
        """
        Load player game statistics.
        """
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
        """
        Load player season statistics.
        """
        return self._season_stats.load(
            seasons=seasons,
            league=league,
        )

    def available_seasons(
        self,
        *,
        league: LeagueInput = None,
    ) -> list[int]:
        """
        Return seasons with player roster membership.

        Rosters are used because the canonical players table does not
        contain season information.
        """
        return self._rosters.available_seasons(
            league=league,
        )

    def available_leagues(
        self,
        *,
        seasons: SeasonInput = None,
    ) -> list[str]:
        """
        Return leagues with player roster membership.

        Rosters are used because the canonical players table does not
        contain league membership.
        """
        return self._rosters.available_leagues(
            seasons=seasons,
        )


def load_players(
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Load canonical player records.

    Season and league filters are resolved through roster membership.
    """
    return Players().load(
        seasons=seasons,
        league=league,
    )