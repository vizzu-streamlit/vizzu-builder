import streamlit as st
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

    def play(self):
        if "story" in st.session_state:
            st.session_state.story.play()
