from pathlib import Path

from wtfpy.teams import (
    Teams,
    load_teams,
)


def test_teams_load(
    processed_data_dir: Path,
) -> None:
    df = Teams().load(
        seasons=2025,
        league="wnfc",
    )

    assert (
        df["team_id"].to_list()
        == ["t3"]
    )


def test_load_teams_function(
    processed_data_dir: Path,
) -> None:
    df = load_teams(
        seasons=2025,
        league="wfa",
    )

    assert (
        df["team_id"].to_list()
        == ["t2"]
    )


def test_team_season_stats(
    processed_data_dir: Path,
) -> None:
    df = Teams().season_stats(
        league="wfa",
    )

    assert (
        df["team_id"].to_list()
        == ["t2"]
    )


def test_team_standings(
    processed_data_dir: Path,
) -> None:
    df = Teams().standings(
        league="wnfc",
    )

    assert (
        df["team_name"].to_list()
        == ["Rebellion"]
    )

    assert (
        df["wins"].to_list()
        == [7]
    )