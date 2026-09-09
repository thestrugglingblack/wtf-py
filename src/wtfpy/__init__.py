"""Public API for wtfpy."""

from .analytics import (
    Analytics,
    AnalyticsLoader,
    available_analytics_leagues,
    available_analytics_seasons,
    load_analytics_player_game_logs,
    load_analytics_player_season_stats,
    load_analytics_players,
    load_player_career_stats,
    load_qb_season_stats,
    load_team_season_summary,
)
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


__version__ = "0.2.0"


__all__ = [
    "WTFPyError",
    "EnvironmentVariableError",
    "DatasetNotFoundError",
    "InvalidDatasetError",
    "InvalidFilterError",
    "DatasetSchemaError",
    "DataRelationshipError",
    "BaseLoader",
    "AnalyticsLoader",
    "Players",
    "Teams",
    "Analytics",
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
    "load_analytics_players",
    "load_analytics_player_game_logs",
    "load_analytics_player_season_stats",
    "load_qb_season_stats",
    "load_player_career_stats",
    "load_team_season_summary",
    "available_analytics_seasons",
    "available_analytics_leagues",
]