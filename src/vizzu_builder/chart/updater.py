# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

import streamlit as st

from .configurator import SelectedChartConfig
from ..data.configurator import DataConfig


class ChartUpdater:
    # pylint: disable=too-few-public-methods

    def __init__(self, data: DataConfig, config: SelectedChartConfig) -> None:
        button_label = (
            "Create Charts"
            if "BuilderConfig" not in st.session_state
            else "Update Charts"
        )
        if not data.df.empty:
            if st.button(button_label):
                st.session_state["BuilderData"] = data
                st.session_state["BuilderConfig"] = config
            st.divider()
