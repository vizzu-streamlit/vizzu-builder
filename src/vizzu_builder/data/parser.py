# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import pandas as pd
from streamlit_extras.row import row  # type: ignore


class DataFrameParser:
    # pylint: disable=too-few-public-methods

    DIMENSION: str = "Category"
    MEASURE: str = "Value"

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df
        self.rows = row(3)

    def process_dataframe(self) -> None:
        self._add_column_types()

    def _add_column_types(self) -> None:
        column_names = self._df.columns
        for column_name in column_names:
            if not self._is_column_convertible_to_float(column_name):
                continue
            index = (
                1 if pd.api.types.is_numeric_dtype(self._df[column_name].dtype) else 0
            )
            selected_type = self.rows.selectbox(
                f"Set type for {column_name}",
                [DataFrameParser.DIMENSION, DataFrameParser.MEASURE],
                index=index,
            )
            self._convert_column(column_name, selected_type)

    def _is_column_convertible_to_float(self, column_name: str) -> bool:
        try:
            self._df[column_name].astype(float)
            return True
        except ValueError:
            return False

    def _convert_column(self, column_name: str, selected_type: str) -> None:
        if selected_type == DataFrameParser.DIMENSION:
            self._df[column_name] = self._df[column_name].astype(str)
        else:
            self._df[column_name] = self._df[column_name].astype(float)
