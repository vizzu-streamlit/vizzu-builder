# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

from pathlib import Path
import streamlit as st


class CsvFileUploader:
    # pylint: disable=too-few-public-methods

    SAMPLE_FILE: str = "sample/sales.csv"

    def __init__(self) -> None:
        self._csv_file: str | None = None

        self._add_title()
        self._add_upload_button()

    @property
    def csv_file(self) -> Path | None:
        if self._csv_file:
            if isinstance(self._csv_file, str):
                return Path(self.SAMPLE_FILE)
            return self._csv_file
        return None

    def _add_title(self) -> None:
        st.subheader("Step 1: Upload Data")

        st.write(
            "Upload a CSV under 5MB that you would like to use to build charts and stories, or use "
            "sample data."
        )

    def _add_upload_button(self) -> None:
        self._csv_file = st.file_uploader("Upload a CSV file", type=["csv"])  # type: ignore
        if not self._csv_file:
            self._add_sample_data()

    def _add_sample_data(self) -> None:
        if st.toggle("Use sample data"):
            self._csv_file = self.SAMPLE_FILE
