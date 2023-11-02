# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import pandas as pd
import streamlit as st

from .data.loader import CsvFileUploader
from .data.filter import DataFrameFilter
from .chart import ChartBuilder


class App:
    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        self._file_name: str | None = None
        self._df: pd.DataFrame | None = None
        self._init_page()
        self._init_csv_file_loader()
        self._init_builders()

    def _init_page(self) -> None:
        st.set_page_config(page_title="Vizzu Builder", page_icon="🏗️")
        st.title("🏗️ Vizzu Builder")

    def _init_csv_file_loader(self) -> None:
        csv_file_uploader = CsvFileUploader()
        self._file_name = csv_file_uploader.file_name
        self._df = csv_file_uploader.df
        if self._df is not None:
            DataFrameFilter(self._df)

    def _init_builders(self) -> None:
        ChartBuilder(self._file_name, self._df)
