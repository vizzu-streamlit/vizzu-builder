# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

from dataclasses import dataclass, field

from ipyvizzustory.env.st.story import Story

from ..data.configurator import DataConfig


@dataclass
class StoryConfig:
    data: DataConfig | None = None
    colors: dict[str, int] = field(default_factory=lambda: {})
    code: list[str] = field(default_factory=list)
    story: Story | None = None
