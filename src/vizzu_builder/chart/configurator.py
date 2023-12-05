# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

from dataclasses import dataclass, field
import pandas as pd
import streamlit as st

from ..config.unset import UNSET
from ..data.configurator import DataConfig
from ..data.parser import DataParser


@dataclass
class ChartConfig:
    df: pd.DataFrame = field(default_factory=pd.DataFrame)
    dimensions: list[str] = field(default_factory=list)
    measures: list[str] = field(default_factory=list)
    keys: list[str] = field(
        default_factory=lambda: [
            "dimension1, measure1",
            "dimension1, measure1, measure2",
            "dimension1, dimension2, measure1",
            "dimension1, dimension2, measure1, measure2",
        ]
    )
    aggregators: list[str] = field(
        default_factory=lambda: [
            "Sum",
            "Min",
            "Max",
            "Mean",
        ]
    )

    def __post_init__(self) -> None:
        self._set_dimensions_and_measures()

    def _set_dimensions_and_measures(self) -> None:
        if not self.df.empty:
            for column_name in self.df.columns:
                if self.df[column_name].dtype == object:
                    self.dimensions.append(column_name)
                else:
                    self.measures.append(column_name)


@dataclass
class SelectedChartConfig:
    dimensions: list[str] = field(default_factory=list)
    measures: list[str] = field(default_factory=list)
    sort: bool = False
    aggregators: list[str] = field(default_factory=list)
    label: str = UNSET
    tooltip: bool = True


class ChartConfigurator:
    # pylint: disable=too-few-public-methods

    def __init__(self, data: DataConfig | None) -> None:
        self._selected_config = SelectedChartConfig()
        if data is None or data.df.empty:
            return
        self._container = st.container()
        self._config = ChartConfig(data.df)
        self._add_title()
        self._add_buttons()

    @property
    def config(self) -> SelectedChartConfig:
        return self._selected_config

    def _add_title(self) -> None:
        self._container.subheader("Configure Chart")

        self._container.write(
            "Choose which data you want to be displayed in the charts"
        )

    def _add_buttons(self) -> None:
        add_methods = [
            [self._add_dimension_button],
            [self._add_measure_button, self._add_sort_button],
            [self._add_aggregator_buttons],
            [self._add_label_button, self._add_tooltip_button],
        ]
        column_number = len(add_methods)
        columns = self._container.columns(column_number)
        for index in range(column_number):
            with columns[index]:
                for method in add_methods[index]:
                    method()

    def _add_dimension_button(self) -> None:
        self._selected_config.dimensions = st.multiselect(
            "Categories",
            self._config.dimensions,
            max_selections=2,
            placeholder="Select up to 2",
        )

    def _add_measure_button(self) -> None:
        self._selected_config.measures = st.multiselect(
            "Values",
            self._config.measures + ["Count"],
            max_selections=2,
            placeholder="Select up to 2",
        )

    def _add_sort_button(self) -> None:
        disabled = len(self._selected_config.measures) != 1
        self._selected_config.sort = st.toggle(
            "Sort by Value",
            key=f"Sort by Value {disabled}",
            value=False,
            disabled=disabled,
        )

    def _add_aggregator_buttons(self) -> None:
        for index in range(2):
            self._add_aggregator_button(index)

    def _add_aggregator_button(self, index: int) -> None:
        try:
            value = self._selected_config.measures[index]
        except IndexError:
            value = UNSET
        aggregator_disabled = value in ["Count", UNSET]
        self._selected_config.aggregators.append(
            st.selectbox(
                f"Aggregation for {DataParser.MEASURE}{index + 1}",
                [UNSET] if aggregator_disabled else self._config.aggregators,
                disabled=aggregator_disabled,
            )  # type: ignore
        )

    def _add_label_button(self) -> None:
        labels: list[str] = [UNSET]
        for item in self._selected_config.dimensions + self._selected_config.measures:
            if item != UNSET:
                labels.append(item)
        self._selected_config.label = st.selectbox("Label (optional)", labels)  # type: ignore

    def _add_tooltip_button(self) -> None:
        self._selected_config.tooltip = st.toggle("Show tooltips", value=True)
