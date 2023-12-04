# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations


from .configurator import DataConfig


class DataGenerator:
    # pylint: disable=too-few-public-methods

    @staticmethod
    def get(config: DataConfig) -> list[str]:
        code: list[str] = []
        if config.csv_file is None or config.df.empty:
            return code
        d_types = []
        for column in config.df.columns:
            if config.df[column].dtype == object:
                d_types.append(f'"{column}": str')
            else:
                d_types.append(f'"{column}": float')
        code.append(f'd_types={{{", ".join(d_types)}}}')
        code.append(f'df = pd.read_csv("{config.csv_file.name}", dtype=d_types)')
        code.append("data = Data()")
        code.append("data.add_df(df)\n")
        return code
