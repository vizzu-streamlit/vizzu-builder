import json
import streamlit_vizzu
import streamlit as st
from streamlit_extras.row import row

from src.data.parser import DataFrameParser
from src.story import StoryBuilder


class ChartBuilder:
    KEYS = [
        "Cat1, Value1",
        "Cat1, Value1, Value2",
        "Cat1, Cat2, Value1",
        "Cat1, Cat2, Value1, Value2",
    ]

    def __init__(self, file_name, df, filters):
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
        self._story_builder = StoryBuilder(self._df)
        if self._df is not None:
            self._categories, self._values = self._get_columns()
            self._add_title()
            self.select_rows = row(2)
            self._add_select_buttons()
            self._set_key()
            self._add_charts()
            self._add_story()

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
        self._add_tooltip_button()
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
        self._add_label_button()

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
        self._label = self.select_rows.selectbox("Select Label (optional)", labels)

    def _add_tooltip_button(self):
        self._tooltips = st.toggle("Show tooltips", value=True)
        self._story_builder.set_tooltip(self._tooltips)

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
            st.warning("Please select at least one category and one value!")

    def _parse_presets_file(self):
        with open("src/config/presets.json", "r") as json_file:
            return json.load(json_file)

    def _add_charts(self):
        if self._presets and self._key:
            if self._key in self._presets:
                data = streamlit_vizzu.Data()
                data.add_df(self._df)
                data.set_filter(self._filters)

                for index in range(0, len(self._presets[self._key]), 2):
                    col1, col2 = st.columns(2)
                    self._add_chart(data, index, col1)
                    next_index = index + 1
                    if next_index < len(self._presets[self._key]):
                        self._add_chart(data, next_index, col2)

    def _add_chart(self, data, index, col):
        raw_config = self._presets[self._key][index]
        config = self._process_raw_config(raw_config)
        with col:
            self._add_chart_title(raw_config)
            self._add_chart_animation(index, data, config)
            self._add_chart_code(config)
            self._add_save_button(config)

    def _add_chart_title(self, raw_config):
        st.subheader(raw_config["chart"])

    def _add_chart_animation(self, index, data, config):
        chart = streamlit_vizzu.VizzuChart(
            height=300, key=f"vizzu_{self._key}_{index}", use_container_width=True
        )
        chart.animate(data, streamlit_vizzu.Config(config))
        chart.feature("tooltip", self._tooltips)
        chart.show()

    def _add_chart_code(self, config):
        show_code = st.expander("Show code")
        with show_code:
            code = "from streamlit_vizzu import VizzuChart, Data, Config\nimport pandas as pd\n\n"
            d_types = []
            for column in self._df.columns:
                if self._df[column].dtype == object:
                    d_types.append(f'"{column}": str')
                else:
                    d_types.append(f'"{column}": float')
            code += f'd_types={{{", ".join(d_types)}}}\ndf = pd.read_csv("{self._file_name}", dtype=d_types)\ndata = Data()\ndata.add_df(df)\n'
            code += "\n"
            code += "chart = VizzuChart()\n"
            if self._tooltips:
                code += 'chart.feature("tooltip", True)\n'
            code += f"chart.animate(data)\n"
            filters = f'Data.filter("{self._filters}"), ' if self._filters else ""
            code += f"chart.animate({filters}Config({config}))\n"
            code += "chart.show()\n\n"
            st.code(
                code,
                language="python",
            )

    def _add_save_button(self, config):
        button = st.button("Add Chart to Story", key=config, use_container_width=True)
        if button:
            self._story_builder.add_slide(self._filters, config)

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

    def _add_story(self):
        self._story_builder.play()
