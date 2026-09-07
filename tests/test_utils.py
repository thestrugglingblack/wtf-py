from pathlib import Path

import pytest

from wtfpy.exceptions import (
    EnvironmentVariableError,
    InvalidFilterError,
)
from wtfpy.utils import (
    get_data_path,
    normalize_leagues,
    normalize_seasons,
)


def test_get_data_path_from_environment(
    processed_data_dir: Path,
) -> None:
    assert (
        get_data_path()
        == processed_data_dir.resolve()
    )


def test_missing_environment_variable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(
        "WTF_DATA_PATH",
        raising=False,
    )

    with pytest.raises(
        EnvironmentVariableError
    ):
        get_data_path()


def test_normalize_seasons() -> None:
    assert (
        normalize_seasons(2025)
        == [2025]
    )

    assert (
        normalize_seasons(
            [2025, 2024, 2025]
        )
        == [2024, 2025]
    )


def test_invalid_seasons() -> None:
    with pytest.raises(
        InvalidFilterError
    ):
        normalize_seasons(
            ["2025"]  # type: ignore[list-item]
        )


def test_normalize_leagues() -> None:
    assert (
        normalize_leagues("WNFC")
        == ["wnfc"]
    )

    assert (
        normalize_leagues(
            ["WFA", "wnfc", "WFA"]
        )
        == ["wfa", "wnfc"]
    )


def test_invalid_leagues() -> None:
    with pytest.raises(
        InvalidFilterError
    ):
        normalize_leagues(
            [2025]  # type: ignore[list-item]
        )