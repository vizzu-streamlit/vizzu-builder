# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st
from .parser import DataFrameParser


class CsvFileUploader:
    SAMPLE_DATA: str = "sample/music_data.csv"

    def __init__(self) -> None:
        self._csv_file: str | None = None
        self._df: pd.DataFrame | None = None

        self._add_title()
        self._add_upload_button()
        self._parse_csv_file()
        self._init_data_frame_parser()

    @property
    def df(self) -> pd.DataFrame | None:
        return self._df

    @property
    def file_name(self) -> str | None:
        if self._csv_file:
            if isinstance(self._csv_file, str):
                return Path(self.SAMPLE_DATA).name
            return self._csv_file.name
        return None

    def _add_title(self) -> None:
        st.subheader("Upload Data")

    def _add_upload_button(self) -> None:
        self._csv_file = st.file_uploader("Upload a CSV file", type=["csv"])  # type: ignore
        if not self._csv_file:
            self._add_sample_data()

    def _add_sample_data(self) -> None:
        if st.toggle("Use sample data"):
            self._csv_file = self.SAMPLE_DATA
            st.download_button(
                label="Download CSV",
                data=self._read_sample_data(),
                file_name=Path(self.SAMPLE_DATA).name,
                mime="text/csv",
            )

    def _read_sample_data(self) -> str:
        with open(
            self.SAMPLE_DATA,
            "r",
            encoding="utf8",
        ) as csv:
            return csv.read()

    def _parse_csv_file(self) -> None:
        if self._csv_file is not None:
            self._df = pd.read_csv(self._csv_file)

    def _init_data_frame_parser(self) -> None:
        if self._df is not None:
            DataFrameParser(self._df).process_dataframe()
            with st.expander("Show data"):
                self._show_data()

    def _show_data(self) -> None:
        if self._df is not None:
            types = [
                DataFrameParser.DIMENSION
                if self._df[col].dtype == object
                else DataFrameParser.MEASURE
                for col in self._df.columns
            ]
            types_df = pd.DataFrame([types], columns=self._df.columns)
            types_df = types_df.set_index(pd.Index(["Type"]))
            max_rows = len(self._df)
            num_rows = st.slider(
                "Number of rows to show",
                min_value=0,
                max_value=max_rows,
                value=min(10, max_rows),
            )
            st.write(types_df.head(1))
            st.write(self._df.head(num_rows))
