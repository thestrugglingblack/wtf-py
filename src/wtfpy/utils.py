"""Shared utility helpers for wtfpy."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import TypeAlias

import polars as pl

from .config import get_wtf_data_path
from .exceptions import (
    DatasetSchemaError,
    EnvironmentVariableError,
    InvalidFilterError,
)

SeasonInput: TypeAlias = int | Iterable[int] | None
LeagueInput: TypeAlias = str | Iterable[str] | None


def get_data_path() -> Path:
    """
    Return the processed-data directory from WTF_DATA_PATH.

    The environment variable is read every time this function is called.
    Nothing is cached at import time.
    """
    raw_path = get_wtf_data_path()

    if raw_path is None or not raw_path.strip():
        raise EnvironmentVariableError(
            "WTF_DATA_PATH is not set. Set it to the directory containing "
            "the processed WTF datasets."
        )

    path = Path(raw_path).expanduser().resolve()

    if not path.exists():
        raise EnvironmentVariableError(
            f"WTF_DATA_PATH does not exist: {path}"
        )

    if not path.is_dir():
        raise EnvironmentVariableError(
            f"WTF_DATA_PATH is not a directory: {path}"
        )

    return path


def normalize_seasons(
    seasons: SeasonInput,
) -> list[int] | None:
    """
    Normalize a season filter to a sorted unique list of integers.
    """
    if seasons is None:
        return None

    if isinstance(seasons, bool):
        raise InvalidFilterError(
            "seasons must be an integer, iterable of integers, or None."
        )

    if isinstance(seasons, int):
        return [seasons]

    try:
        values = list(seasons)
    except TypeError as exc:
        raise InvalidFilterError(
            "seasons must be an integer, iterable of integers, or None."
        ) from exc

    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in values
    ):
        raise InvalidFilterError(
            "Every season value must be an integer."
        )

    return sorted(set(values))


def normalize_leagues(
    league: LeagueInput,
) -> list[str] | None:
    """
    Normalize league filters to lowercase sorted unique strings.
    """
    if league is None:
        return None

    if isinstance(league, str):
        values = [league]
    else:
        try:
            values = list(league)
        except TypeError as exc:
            raise InvalidFilterError(
                "league must be a string, iterable of strings, or None."
            ) from exc

    normalized: list[str] = []

    for value in values:
        if not isinstance(value, str):
            raise InvalidFilterError(
                "Every league value must be a string."
            )

        cleaned = value.strip().lower()

        if cleaned:
            normalized.append(cleaned)

    return sorted(set(normalized))


def filter_dataframe(
    df: pl.DataFrame,
    *,
    seasons: SeasonInput = None,
    league: LeagueInput = None,
) -> pl.DataFrame:
    """
    Apply optional season and league filters to a dataframe.

    The dataframe must contain the relevant filter column if that
    filter is requested.
    """
    season_values = normalize_seasons(
        seasons
    )

    league_values = normalize_leagues(
        league
    )

    result = df

    if season_values is not None:
        if "season" not in result.columns:
            raise DatasetSchemaError(
                "Dataset does not contain a 'season' column."
            )

        result = result.filter(
            pl.col("season")
            .cast(
                pl.Int64,
                strict=False,
            )
            .is_in(
                season_values
            )
        )

    if league_values is not None:
        if "league" not in result.columns:
            raise DatasetSchemaError(
                "Dataset does not contain a 'league' column."
            )

        result = result.filter(
            pl.col("league")
            .cast(pl.String)
            .str.strip_chars()
            .str.to_lowercase()
            .is_in(
                league_values
            )
        )

    return result


def unique_sorted_seasons(
    df: pl.DataFrame,
) -> list[int]:
    """
    Return sorted unique season values from a dataframe.
    """
    if "season" not in df.columns:
        raise DatasetSchemaError(
            "Dataset does not contain a 'season' column."
        )

    return (
        df.select(
            pl.col("season")
            .cast(
                pl.Int64,
                strict=False,
            )
            .drop_nulls()
            .unique()
            .sort()
        )
        .to_series()
        .to_list()
    )


def unique_sorted_leagues(
    df: pl.DataFrame,
) -> list[str]:
    """
    Return sorted unique lowercase league values from a dataframe.
    """
    if "league" not in df.columns:
        raise DatasetSchemaError(
            "Dataset does not contain a 'league' column."
        )

    return (
        df.select(
            pl.col("league")
            .cast(pl.String)
            .str.strip_chars()
            .str.to_lowercase()
            .drop_nulls()
            .unique()
            .sort()
        )
        .to_series()
        .to_list()
    )