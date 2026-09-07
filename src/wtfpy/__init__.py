"""Public API for wtfpy."""

from .exceptions import (
    DataRelationshipError,
    DatasetNotFoundError,
    DatasetSchemaError,
    EnvironmentVariableError,
    InvalidDatasetError,
    InvalidFilterError,
    WTFPyError,
)
from .loaders import (
    BaseLoader,
    available_leagues,
    available_seasons,
    load_games,
    load_player_game_stats,
    load_player_season_stats,
    load_rosters,
    load_standings,
    load_team_season_stats,
)
from .players import (
    Players,
    load_players,
)
from .teams import (
    Teams,
    load_teams,
)

__version__ = "0.1.0"


__all__ = [
    "WTFPyError",
    "EnvironmentVariableError",
    "DatasetNotFoundError",
    "InvalidDatasetError",
    "InvalidFilterError",
    "DatasetSchemaError",
    "DataRelationshipError",
    "BaseLoader",
    "Players",
    "Teams",
    "load_teams",
    "load_players",
    "load_rosters",
    "load_games",
    "load_player_game_stats",
    "load_player_season_stats",
    "load_team_season_stats",
    "load_standings",
    "available_seasons",
    "available_leagues",
]