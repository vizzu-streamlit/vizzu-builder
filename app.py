from __future__ import annotations

import streamlit as st
import pandas as pd
import json
import streamlit_vizzu
from filter_data import filter_dataframe

from streamlit_extras.row import row


class DataFrameParser:
    DIMENSION = "Category"
    MEASURE = "Value"

    def __init__(self, df):
        self._df = df
        self.rows = row(3)

    def process_dataframe(self):
        self._add_column_types()

    def _add_column_types(self):
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

    def _is_column_convertible_to_float(self, column_name):
        try:
            self._df[column_name].astype(float)
            return True
        except ValueError:
            return False

    def _convert_column(self, column_name, selected_type):
        if selected_type == DataFrameParser.DIMENSION:
            self._df[column_name] = self._df[column_name].astype(str)
        else:
            self._df[column_name] = self._df[column_name].astype(float)


class CsvFileUploader:
    SAMPLE_DATA = "music_data.csv"

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
                return self.SAMPLE_DATA
            return self._csv_file.name
        return None

    def _add_title(self):
        st.subheader("Create Data")

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


class ChartBuilder:
    KEYS = [
        "Cat1, Value1",
        "Cat1, Value1, Value2",
        "Cat1, Cat2, Value1",
        "Cat1, Cat2, Value1, Value2",
    ]

    def __init__(self, file_name, df, filters: str | None):
        self._file_name = file_name
        self._df = df
        self._cat1, self._cat2 = None, None
        self._selected_cat1, self._selected_cat2 = None, None
        self._value1, self._value2 = None, None
        self._selected_value1, self._selected_value2 = None, None
        self._label = None
        self._key = None
        self._presets = self._parse_presets_file()
        self._filters = filters
        if self._df is not None:
            self._categories, self._values = self._get_columns()
            self._add_title()
            self.select_rows = row(3)
            self._add_select_buttons()
            self._set_key()
            self._add_show_button()

    def _add_title(self):
        st.subheader("Create Chart")

    def _get_columns(self):
        categories = []
        values = []
        for column_name in self._df.columns:
            if self._df[column_name].dtype == object:
                categories.append(column_name)
            else:
                values.append(column_name)
        return categories, values

    def _add_select_buttons(self):
        self._tooltips = st.toggle("Show tooltips", value=True)
        (
            self._cat1,
            self._selected_cat1,
            self._cat2,
            self._selected_cat2,
        ) = self._add_select_buttons_by_type(DataFrameParser.DIMENSION)
        (
            self._value1,
            self._selected_value1,
            self._value2,
            self._selected_value2,
        ) = self._add_select_buttons_by_type(DataFrameParser.MEASURE)
        self._label = self._add_label_button()

    def _add_select_buttons_by_type(self, type):
        items1 = self._categories
        if type == DataFrameParser.MEASURE:
            items1 = self._values
        button1 = self.select_rows.selectbox(f"Select {type} 1 (mandatory)", items1)
        items2 = [c for c in items1 if c != button1]
        items2.insert(0, None)
        button2 = self.select_rows.selectbox(f"Select {type} 2 (optional)", items2)
        return items1, button1, items2, button2

    def _add_label_button(self):
        labels = [None]
        for item in [
            self._selected_cat1,
            self._selected_cat2,
            self._selected_value1,
            self._selected_value2,
        ]:
            if item is not None:
                labels.append(item)
        return self.select_rows.selectbox("Select Label (optional)", labels)

    def _set_key(self):
        contains = {"Cat1": False, "Cat2": False, "Value1": False, "Value2": False}
        if self._selected_cat1 is not None:
            contains["Cat1"] = True
        if self._selected_cat2 is not None:
            contains["Cat2"] = True
        if self._selected_value1 is not None:
            contains["Value1"] = True
        if self._selected_value2 is not None:
            contains["Value2"] = True
        self._key = ", ".join(key for key, value in contains.items() if value)
        if self._key not in self.KEYS:
            st.warning("Please select both a category and a value for the chart!")

    def _parse_presets_file(self):
        with open("presets/presets.json", "r") as json_file:
            return json.load(json_file)

    def _add_show_button(self):
        if self._presets and self._key:
            if self._key in self._presets:
                self._add_charts()

    def _add_charts(self):
        data = streamlit_vizzu.Data()
        data.add_df(self._df)

        for index in range(0, len(self._presets[self._key]), 2):
            col1, col2 = st.columns(2)
            self._add_chart(data, index, col1, self._filters)
            next_index = index + 1
            if next_index < len(self._presets[self._key]):
                self._add_chart(data, next_index, col2, self._filters)

    def _add_chart(self, data, index, col, filters):
        raw_config = self._presets[self._key][index]
        config = self._process_raw_config(raw_config)
        with col:
            self._add_chart_title(raw_config)
            self._add_chart_animation(index, data, config, filters)
            self._add_chart_code(config)

    def _add_chart_title(self, raw_config):
        st.caption(raw_config["chart"])

    def _add_chart_animation(self, index, data, config, filters):
        chart = streamlit_vizzu.VizzuChart(
            height=300, key=f"vizzu_{self._key}_{index}", use_container_width=True
        )
        chart.animate(data, streamlit_vizzu.Config(config))
        chart.animate(streamlit_vizzu.Data.filter(filters))
        chart.feature("tooltip", self._tooltips)
        chart.show()

    def _add_chart_code(self, config):
        show_code = st.expander("Show code")
        with show_code:
            code_import = "from streamlit_vizzu import VizzuChart, Data, Config\nimport pandas as pd\n\n"
            d_types = []
            for column in self._df.columns:
                if self._df[column].dtype == object:
                    d_types.append(f"'{column}': str")
                else:
                    d_types.append(f"'{column}': float")
            code_data = f"d_types={{{', '.join(d_types)}}}\ndf = pd.read_csv('{self._file_name}', dtype=d_types)\ndata = Data()\ndata.add_df(df)\n\n"
            code_chart = "chart = VizzuChart()\n\n"
            code_animate = f"chart.animate(data, Config({config}))\n\n"
            if self._filters:
                code_animate += f"chart.animate(Data.filter('{self._filters}'))\n\n"
            if self._tooltips:
                code_animate += "chart.feature('tooltip', True)\n\n"
            code_show = "chart.show()\n\n"
            st.code(
                code_import + code_data + code_chart + code_animate + code_show,
                language="python",
            )

    def _process_raw_config(self, raw_config):
        config = {}
        for key, value in raw_config.items():
            if key not in ["chart", "y_range_min", "y_range_max"] and value is not None:
                if isinstance(value, list):
                    value = [self._replace_config(v) for v in value]
                else:
                    value = self._replace_config(value)
                config[key] = value
        if "y" in config:
            config["y"] = {"set": config["y"]}
        if "y_range_min" in raw_config:
            config["y"] = config.get("y", {})
            config["y"]["range"] = config["y"].get("range", {})
            config["y"]["range"]["min"] = raw_config["y_range_min"]
        if "y_range_max" in raw_config:
            config["y"] = config.get("y", {})
            config["y"]["range"] = config["y"].get("range", {})
            config["y"]["range"]["max"] = raw_config["y_range_max"]
        if self._label is not None:
            config["label"] = self._label
        return config

    def _replace_config(self, value):
        if isinstance(value, str):
            value = value.replace("Cat1", self._selected_cat1 or "")
            value = value.replace("Cat2", self._selected_cat2 or "")
            value = value.replace("Value1", self._selected_value1 or "")
            value = value.replace("Value2", self._selected_value2 or "")
        return value


class App:
    def __init__(self):
        self._df = None
        self._file_name = None
        self._filters = None
        st.set_page_config(page_title="Vizzu Chart Builder", page_icon="🏗️")
        self._add_title()
        self._init_csv_file_loader()
        self._init_chart_builder()

    def _add_title(self):
        st.title("🏗️ Vizzu Chart Builder")

    def _init_csv_file_loader(self):
        csv_file_uploader = CsvFileUploader()
        self._df = csv_file_uploader.df
        self._file_name = csv_file_uploader.file_name
        if self._df is not None:
            self._filters = filter_dataframe(self._df)

    def _init_chart_builder(self):
        ChartBuilder(self._file_name, self._df, self._filters)


App()
