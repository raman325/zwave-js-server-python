"""Provide a model for Z-Wave JS Duration."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from ..const import USE_TYPING_EXTENSIONS

if USE_TYPING_EXTENSIONS:
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


class DurationDataType(TypedDict, total=False):
    """Represent a Duration data dict type."""

    # https://github.com/zwave-js/node-zwave-js/blob/v11-dev/packages/core/src/values/Duration.ts#L11
    unit: Literal["seconds", "minutes", "unknown", "default"]  # required
    value: int | float


@dataclass
class Duration:
    """Duration class."""

    data: DurationDataType
    unit: Literal["seconds", "minutes", "unknown", "default"] = field(init=False)
    value: int | float | None = field(init=False)

    def __post_init__(self) -> None:
        """Post init."""
        self.unit = self.data["unit"]
        self.value = self.data.get("value")

    def __repr__(self) -> str:
        """Return the representation."""
        if self.value:
            return f"{self.value} {self.unit}"
        return f"{self.unit} duration"
