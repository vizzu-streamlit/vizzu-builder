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

    def set_size(self, width, height):
        if "story" in st.session_state:
            st.session_state.story.set_size(width, height)

    def set_tooltip(self, tooltip):
        if "story" in st.session_state:
            st.session_state.story.set_feature("tooltip", tooltip)

    def add_slide(self, filters, config):
        if "story" in st.session_state:
            st.session_state.story.add_slide(
                Slide(Step(Data.filter(filters), Config(config)))
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
