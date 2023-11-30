# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import streamlit as st

from .loader import CsvFileUploader
from .parser import DataParser
from .filter import DataFilter


@dataclass
class DataConfig:
    df: pd.DataFrame = field(default_factory=pd.DataFrame)
    filters: str | None = None
    csv_file: Path | None = None


class DataConfigurator:
    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        self._data = DataConfig()
        if "BuilderData" not in st.session_state:
            st.session_state["BuilderData"] = self._data

        self._add_loader()
        self._add_parser()
        self._add_filter()
        st.divider()

    @property
    def data(self) -> DataConfig:
        return self._data

    def _add_loader(self) -> None:
        csv_file_uploader = CsvFileUploader()
        self._data.csv_file = csv_file_uploader.csv_file

    def _add_parser(self) -> None:
        parser = DataParser(self._data.csv_file)
        self._data.df = parser.df

    def _add_filter(self) -> None:
        data_filter = DataFilter(self._data.df)
        self._data.filters = data_filter.filters
