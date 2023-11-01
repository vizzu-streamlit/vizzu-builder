import streamlit as st
from streamlit_extras.row import row
from ipyvizzustory.env.st.story import Story
from ipyvizzustory import Slide, Step
from ipyvizzu.animation import Config, Data


class StoryBuilder:
    def __init__(self, df):
        if df is not None:
            if "df" not in st.session_state:
                st.session_state.df = df
            if "story" not in st.session_state or not st.session_state.df.equals(df):
                data = Data()
                data.add_df(df)
                st.session_state.story = Story(data=data)
                self.set_size(640, 320)
                self.set_start_slide(-2)

    def set_start_slide(self, index):
        if "story" in st.session_state:
            st.session_state.story.start_slide = index

    def set_size(self, width, height):
        if "story" in st.session_state:
            st.session_state.story.set_size(width, height)

    def set_tooltip(self, tooltip):
        if "story" in st.session_state:
            st.session_state.story.set_feature("tooltip", tooltip)

    def add_slide(self, filters, config):
        if "story" in st.session_state:
            normalized_config = self._normalize_config(config)
            st.session_state.story.add_slide(
                Slide(Step(Data.filter(filters), Config(normalized_config)))
            )

    def play(self):
        if "story" in st.session_state and st.session_state.story["slides"]:
            st.session_state.story.play()
            rows = row(2)
            self._add_delete_button(rows)
            self._add_download_button(rows)

    def _add_delete_button(self, rows):
        if "story" in st.session_state and st.session_state.story["slides"]:
            delete = rows.button("Delete last Slide", use_container_width=True)
            if delete:
                st.session_state.story["slides"].pop()

    def _add_download_button(self, rows):
        if "story" in st.session_state:
            rows.download_button(
                label="Download Story",
                data=st.session_state.story.to_html(),
                file_name="story.html",
                mime="text/html",
                use_container_width=True,
            )

    def _normalize_config(self, config):
        normalized_config = {}
        normalized_config["x"] = None if "x" not in config else config["x"]

        y_set = config.get("y", {}).get("set", None)
        y_range_min = config.get("y", {}).get("range", {}).get("min", "auto")
        y_range_max = config.get("y", {}).get("range", {}).get("max", "auto")
        normalized_config["y"] = {
            "set": y_set,
            "range": {"min": y_range_min, "max": y_range_max},
        }

        normalized_config["color"] = None if "color" not in config else config["color"]
        normalized_config["lightness"] = (
            None if "lightness" not in config else config["lightness"]
        )
        normalized_config["size"] = None if "size" not in config else config["size"]
        normalized_config["noop"] = None if "noop" not in config else config["noop"]

        normalized_config["split"] = False if "split" not in config else config["split"]
        normalized_config["align"] = (
            "none" if "align" not in config else config["align"]
        )

        normalized_config["coordSystem"] = config["coordSystem"]
        normalized_config["geometry"] = config["geometry"]
        normalized_config["orientation"] = (
            "horizontal" if "orientation" not in config else config["orientation"]
        )

        return normalized_config
