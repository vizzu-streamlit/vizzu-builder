# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

import pandas as pd


class DataCodeGenerator:
    # pylint: disable=too-few-public-methods

    @staticmethod
    def get_data_code(file_name: str | None, df: pd.DataFrame | None) -> list[str]:
        code = []
        if file_name is not None and df is not None:
            d_types = []
            for column in df.columns:
                if df[column].dtype == object:
                    d_types.append(f'"{column}": str')
                else:
                    d_types.append(f'"{column}": float')
            code.append(f'd_types={{{", ".join(d_types)}}}')
            code.append(f'df = pd.read_csv("{file_name}", dtype=d_types)')
            code.append("data = Data()")
            code.append("data.add_df(df)\n")
        return code
