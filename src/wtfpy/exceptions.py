"""Custom exceptions for wtfpy."""


class WTFPyError(Exception):
    """Base exception for all wtfpy errors."""


class EnvironmentVariableError(WTFPyError):
    """Raised when WTF_DATA_PATH is missing or invalid."""


class DatasetNotFoundError(WTFPyError):
    """Raised when a requested processed dataset cannot be found."""


class InvalidDatasetError(WTFPyError):
    """Raised when a dataset name is not supported."""


class InvalidFilterError(WTFPyError):
    """Raised when a league or season filter is invalid."""


class DatasetSchemaError(WTFPyError):
    """Raised when a dataset is missing a required column."""
