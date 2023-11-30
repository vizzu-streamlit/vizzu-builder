# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

import streamlit as st
import streamlit_vizzu  # type: ignore

from .d1m1 import D1M1
from .d1m2 import D1M2
from .d2m1 import D2M1
from .d2m2 import D2M2
from .palettes import DEFAULT, PALETTES
from ..unset import UNSET
from ...data.parser import DataParser
from ...chart.configurator import SelectedChartConfig


class Preset:
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        data: streamlit_vizzu.Data,
        colors: dict[str, int],
        preset: dict,
        index: int,
    ) -> None:
        self._colors: dict[str, int] = colors
        self.index: int = index
        self.data: streamlit_vizzu.Data = data
        self.types: dict = preset["types"]
        self.chart: str = preset["chart"]
        self.config: dict = preset["config"]
        self.style: dict = preset["style"]
        self._set_color_palette()

    def _set_color_palette(self) -> None:
        color = self.config["color"]
        if color is None or self.types[color] != DataParser.DIMENSION:
            self.style["plot"]["marker"]["colorPalette"] = DEFAULT
        else:
            if color not in self._colors:
                self._colors[color] = len(self._colors) % len(PALETTES)
            self.style["plot"]["marker"]["colorPalette"] = " ".join(
                PALETTES[self._colors[color]]
            )


class Presets:
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        config: SelectedChartConfig,
    ) -> None:
        self._config = config
        self._charts: list = []
        self._set_charts()

    @property
    def charts(self) -> list:
        return self._charts

    def _set_charts(self) -> None:
        if len(self._config.dimensions) == 1 and len(self._config.measures) == 1:
            dimension1 = self._config.dimensions[0]
            measure1 = Presets._set_aggregator(
                self._config.measures[0], self._config.aggregators[0]
            )
            self._charts = D1M1.get(dimension1, measure1)
        elif len(self._config.dimensions) == 1 and len(self._config.measures) == 2:
            dimension1 = self._config.dimensions[0]
            measure1 = Presets._set_aggregator(
                self._config.measures[0], self._config.aggregators[0]
            )
            measure2 = Presets._set_aggregator(
                self._config.measures[1], self._config.aggregators[1]
            )
            self._charts = D1M2.get(dimension1, measure1, measure2)
        elif len(self._config.dimensions) == 2 and len(self._config.measures) == 1:
            dimension1 = self._config.dimensions[0]
            dimension2 = self._config.dimensions[1]
            measure1 = Presets._set_aggregator(
                self._config.measures[0], self._config.aggregators[0]
            )
            self._charts = D2M1.get(dimension1, dimension2, measure1)
        elif len(self._config.dimensions) == 2 and len(self._config.measures) == 2:
            dimension1 = self._config.dimensions[0]
            dimension2 = self._config.dimensions[1]
            measure1 = Presets._set_aggregator(
                self._config.measures[0], self._config.aggregators[0]
            )
            measure2 = Presets._set_aggregator(
                self._config.measures[1], self._config.aggregators[1]
            )
            self._charts = D2M2.get(dimension1, dimension2, measure1, measure2)

        self._set_labels()
        self._set_sorts()

    def _set_labels(self) -> None:
        label = self._get_label()
        for index, _ in enumerate(self._charts):
            self._charts[index]["config"]["label"] = label

    def _get_label(self) -> str | None:
        new_label: str | None = self._config.label
        if new_label == UNSET:
            new_label = None
        elif len(self._config.measures) > 0 and new_label == self._config.measures[0]:
            new_label = Presets._set_aggregator(new_label, self._config.aggregators[0])
        elif len(self._config.measures) > 1 and new_label == self._config.measures[1]:
            new_label = Presets._set_aggregator(new_label, self._config.aggregators[1])
        return new_label

    def _set_sorts(self) -> None:
        sort = self._get_sort()
        for index, _ in enumerate(self._charts):
            self._charts[index]["config"]["sort"] = sort

    def _get_sort(self) -> str:
        if self._config.sort:
            return "byValue"
        return "none"

    @staticmethod
    def _set_aggregator(measure: str, aggregator: str) -> str:
        new_measure: str = measure
        if aggregator not in [UNSET, "Sum"]:
            new_measure = f"{aggregator.lower()}({measure})"
        if measure == "Count":
            new_measure = f"{measure.lower()}()"
        return new_measure
