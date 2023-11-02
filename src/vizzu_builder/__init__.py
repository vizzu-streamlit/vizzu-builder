# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations
import streamlit as st

from .data.loader import CsvFileUploader
from .data.filter import filter_dataframe
from .chart import ChartBuilder

if "filters" not in st.session_state:
    st.session_state["filters"] = None


class App:
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self._file_name = None
        self._df = None
        self._init_page()
        self._init_csv_file_loader()
        self._init_builders()

    def _init_page(self):
        st.set_page_config(page_title="Vizzu Builder", page_icon="🏗️")
        st.title("🏗️ Vizzu Builder")

    def _init_csv_file_loader(self):
        csv_file_uploader = CsvFileUploader()
        self._file_name = csv_file_uploader.file_name
        self._df = csv_file_uploader.df
        if self._df is not None:
            filter_dataframe(self._df)

    def _init_builders(self):
        ChartBuilder(self._file_name, self._df)
