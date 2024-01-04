# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_extras.row import row  # type: ignore

from .loader import CsvFileUploader


class DataParser:
    # pylint: disable=too-few-public-methods

    SAMPLE_DTYPE: dict[str, type] = {"Year": str}

    DIMENSION: str = "Category"
    MEASURE: str = "Value"

    def __init__(self, csv_file: Path | None) -> None:
        self._df: pd.DataFrame = pd.DataFrame()

        if csv_file is None:
            return

        self._add_title()
        self._read_csv_file(csv_file)
        self._process_df()

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def _add_title(self) -> None:
        st.subheader("Step 2: Configure Data")

        st.write(
            """
            Specify which columns should be treated as values and which ones should
            be treated as categories, and optionally filter the data.
            """
        )

    def _read_csv_file(self, csv_file: Path) -> None:
        dtype = {}
        if csv_file == Path(CsvFileUploader.SAMPLE_FILE):
            dtype = self.SAMPLE_DTYPE
        self._df = pd.read_csv(csv_file, dtype=dtype)

    def _process_df(self) -> None:
        types_container = st.empty()
        self._add_type_buttons()
        self._add_types(types_container)
        self._add_data()

    def _add_types(self, types_container) -> None:  # type: ignore
        types = [
            DataParser.DIMENSION
            if self._df[col].dtype == object
            else DataParser.MEASURE
            for col in self._df.columns
        ]
        types_df = pd.DataFrame([types], columns=self._df.columns)
        types_df = types_df.set_index(pd.Index(["Type"]))
        types_container.write(types_df.head(1))

    def _add_type_buttons(self) -> None:
        rows = row(4)
        column_names = self._df.columns
        for column_name in column_names:
            if not self._is_column_convertible_to_float(column_name):
                continue
            index = (
                1 if pd.api.types.is_numeric_dtype(self._df[column_name].dtype) else 0
            )
            selected_type = rows.selectbox(
                f"Type for {column_name}",
                [DataParser.DIMENSION, DataParser.MEASURE],
                index=index,
            )
            self._convert_column(column_name, selected_type)

    def _add_data(self) -> None:
        with st.expander("Show Data"):
            max_rows = len(self._df)
            num_rows = st.slider(
                "Number of rows to show",
                min_value=0,
                max_value=max_rows,
                value=min(10, max_rows),
            )
            st.write(self._df.head(num_rows))

    def _is_column_convertible_to_float(self, column_name: str) -> bool:
        try:
            self._df[column_name].astype(float)
            return True
        except ValueError:
            return False

    def _convert_column(self, column_name: str, selected_type: str) -> None:
        if selected_type == DataParser.DIMENSION:
            self._df[column_name] = self._df[column_name].astype(str)
        else:
            self._df[column_name] = self._df[column_name].astype(float)
