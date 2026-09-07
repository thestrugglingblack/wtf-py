"""Configuration helpers for wtfpy."""

from __future__ import annotations

import os

WTF_DATA_PATH_ENV = "WTF_DATA_PATH"


def get_wtf_data_path() -> str | None:
    """
    Return the current WTF_DATA_PATH environment variable.

    The environment variable is read at call time rather than when
    the module is imported. This allows pytest monkeypatching and
    other runtime environment changes to work correctly.
    """
    return os.environ.get(WTF_DATA_PATH_ENV)