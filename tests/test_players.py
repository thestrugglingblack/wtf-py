from pathlib import Path

from wtfpy.players import (
    Players,
    load_players,
)


def test_players_load_without_season_filter(
    processed_data_dir: Path,
) -> None:
    df = Players().load()

    assert set(
        df["player_id"].to_list()
    ) == {
        "p1",
        "p2",
        "p3",
    }


def test_players_load_season_uses_rosters(
    processed_data_dir: Path,
) -> None:
    df = Players().load(
        seasons=2025,
        league="wfa",
    )

    assert (
        df["player_id"].to_list()
        == ["p2"]
    )


def test_load_players_function(
    processed_data_dir: Path,
) -> None:
    df = load_players(
        seasons=2025,
        league="wnfc",
    )

    assert (
        df["player_id"].to_list()
        == ["p3"]
    )


def test_players_game_stats(
    processed_data_dir: Path,
) -> None:
    df = Players().game_stats(
        league="wfa",
    )

    assert (
        df["player_id"].to_list()
        == ["p2"]
    )


def test_players_season_stats(
    processed_data_dir: Path,
) -> None:
    df = Players().season_stats(
        league="wnfc",
    )

    assert (
        df["player_id"].to_list()
        == ["p3"]
    )


def test_players_available_seasons_uses_rosters(
    processed_data_dir: Path,
) -> None:
    assert (
        Players().available_seasons()
        == [2024, 2025]
    )