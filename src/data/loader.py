from pathlib import Path
import pandas as pd
import streamlit as st
from src.data.parser import DataFrameParser


class CsvFileUploader:
    SAMPLE_DATA = "sample/music_data.csv"

    def __init__(self):
        self._csv_file = None
        self._df = None

        self._add_title()
        self._add_upload_button()
        self._parse_csv_file()
        self._init_data_frame_parser()

    @property
    def df(self):
        return self._df

    @property
    def file_name(self):
        if self._csv_file:
            if isinstance(self._csv_file, str):
                return Path(self.SAMPLE_DATA).name
            return self._csv_file.name
        return None

    def _add_title(self):
        st.subheader("Upload Data")

    def _add_upload_button(self):
        self._csv_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if not self._csv_file:
            if st.toggle("Use sample data"):
                self._csv_file = self.SAMPLE_DATA

    def _parse_csv_file(self):
        if self._csv_file is not None:
            self._df = pd.read_csv(self._csv_file)

    def _init_data_frame_parser(self):
        if self._df is not None:
            DataFrameParser(self._df).process_dataframe()
            with st.expander("Show data"):
                self._show_data()

    def _show_data(self):
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
