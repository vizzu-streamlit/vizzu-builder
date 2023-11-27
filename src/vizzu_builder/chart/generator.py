# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import black
import streamlit as st

import streamlit_vizzu  # type: ignore

from ..config.presets import Preset, Presets
from ..data.generator import DataGenerator
from ..data.parser import DataParser
from ..story.generator import StoryGenerator


class ChartGenerator:
    # pylint: disable=too-few-public-methods

    def __init__(self, story_generator: StoryGenerator) -> None:
        self._data = st.session_state.get("BuilderData", None)
        self._config = st.session_state.get("BuilderConfig", None)
        self._story_generator = story_generator

        if self._data is not None and self._config is not None:
            self._add_charts()

    def _add_charts(self) -> None:
        presets = Presets(self._config)
        charts = presets.charts
        self._add_title()
        if not charts:
            st.warning(
                f"Please select at least one {DataParser.DIMENSION} and one {DataParser.MEASURE}",
                icon="⚠️",
            )
        else:
            data = streamlit_vizzu.Data()
            data.add_df(self._data.df)
            data.set_filter(self._data.filters)
            for index in range(0, len(charts), 3):
                col0, col1, col2 = st.columns(3)

                index0 = index
                with col0:
                    preset0 = Preset(data, charts, index0)
                    self._add_chart(preset0)

                index1 = index + 1
                if index1 < len(charts):
                    with col1:
                        preset1 = Preset(data, charts, index1)
                        self._add_chart(preset1)

                index2 = index + 2
                if index2 < len(charts):
                    with col2:
                        preset2 = Preset(data, charts, index2)
                        self._add_chart(preset2)
        st.divider()

    def _add_title(self) -> None:
        st.subheader("Charts")

    def _add_chart(self, preset: Preset) -> None:
        self._add_chart_title(preset)
        self._add_chart_animation(preset)
        self._add_chart_code(preset)
        self._add_save_button(preset)

    def _add_chart_title(self, preset: Preset) -> None:
        st.subheader(preset.chart)

    def _add_chart_animation(self, preset: Preset) -> None:
        preset_type = f"d{len(self._config.dimensions)}m{len(self._config.measures)}"
        chart = streamlit_vizzu.VizzuChart(
            height=300,
            key=f"chart_{preset_type}_{preset.index}",
            use_container_width=True,
        )
        chart.animate(
            preset.data,
            streamlit_vizzu.Config(preset.config),
            streamlit_vizzu.Style(preset.style),
        )
        chart.feature("tooltip", self._config.tooltip)
        chart.show()

    def _add_chart_code(self, preset: Preset) -> None:
        show_code = st.expander("Show code")
        with show_code:
            code = []
            code.append("from streamlit_vizzu import VizzuChart, Data, Config, Style")
            code.append("import pandas as pd")
            code += DataGenerator.get(self._data)
            code.append("chart = VizzuChart()")
            if self._config.tooltip:
                code.append('chart.feature("tooltip", True)')
            code.append("chart.animate(data)\n")
            filters = f'"{self._data.filters}"' if self._data.filters else None
            animation = f"Data.filter({filters}), Config({preset.config}), Style({preset.style})"
            code.append(f"chart.animate({animation})\n")
            code.append("chart.show()")
            unformatted_code = "\n".join(code)
            formatted_code = black.format_str(unformatted_code, mode=black.FileMode())
            st.code(
                formatted_code,
                language="python",
            )

    def _add_save_button(self, preset: Preset) -> None:
        preset_type = f"d{len(self._config.dimensions)}m{len(self._config.measures)}"
        button = st.button(
            "Add Chart to Story",
            key=f"save_{preset_type}_{preset.index}",
            use_container_width=True,
        )
        if button:
            self._story_generator.add_slide(preset)

    def _add_story(self) -> None:
        self._story_generator.play()
