# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

import pandas as pd
import black
import streamlit as st
from streamlit_extras.row import row  # type: ignore
from ipyvizzustory.env.st.story import Story
from ipyvizzustory import Slide, Step
from ipyvizzu import Config, Data

from .data.generator import DataCodeGenerator


if "story_code" not in st.session_state:
    st.session_state["story_code"] = []


class StoryBuilder:
    def __init__(self, file_name: str | None, df: pd.DataFrame | None) -> None:
        self._file_name = file_name
        self._df = df
        self._width = 640
        self._height = 320
        self._start_slide = -1
        self._tooltip = True
        if self._df is not None:
            if "df" not in st.session_state:
                st.session_state.df = self._df
            if "story" not in st.session_state or not st.session_state.df.equals(
                self._df
            ):
                st.session_state.df = self._df
                data = Data()
                data.add_df(self._df)
                st.session_state.story = Story(data=data)
                self.set_size(self._width, self._height)
                self.set_start_slide(self._start_slide)
                st.session_state.story_code = []

    def set_start_slide(self, index: int) -> None:
        if "story" in st.session_state:
            st.session_state.story.start_slide = index

    def set_size(self, width: int, height: int) -> None:
        if "story" in st.session_state:
            st.session_state.story.set_size(width, height)

    def set_tooltip(self, tooltip: bool) -> None:
        if "story" in st.session_state:
            st.session_state.story.set_feature("tooltip", tooltip)
            self._tooltip = tooltip

    def add_slide(self, filters: str | None, config: dict) -> None:
        if "story" in st.session_state:
            st.session_state.story.add_slide(
                Slide(Step(Data.filter(filters), Config(config)))
            )
            filters = f'"{filters}"' if filters else None
            st.session_state.story_code.append(
                f"story.add_slide(Slide(Step(Data.filter({filters}), Config({config}))))"
            )

    @staticmethod
    def delete_last_slide() -> None:
        if (
            "story" in st.session_state
            and st.session_state.story["slides"]
            and st.session_state.story_code
        ):
            st.session_state.story["slides"].pop()
            st.session_state.story_code.pop()

    def play(self) -> None:
        if "story" in st.session_state and st.session_state.story["slides"]:
            st.subheader("Create Story")
            st.session_state.story.play()
            rows = row(2)
            self._add_delete_button(rows)
            self._add_download_button(rows)
            self._add_show_code_button()

    def _add_delete_button(self, rows) -> None:  # type: ignore
        if "story" in st.session_state and st.session_state.story["slides"]:
            rows.button(
                "Delete last Slide",
                use_container_width=True,
                on_click=StoryBuilder.delete_last_slide,
            )

    def _add_download_button(self, rows) -> None:  # type: ignore
        if "story" in st.session_state:
            self.set_start_slide(0)
            rows.download_button(
                label="Download Story",
                data=st.session_state.story.to_html(),
                file_name="story.html",
                mime="text/html",
                use_container_width=True,
            )
            self.set_start_slide(self._start_slide)

    def _add_show_code_button(self) -> None:
        if "story" in st.session_state and st.session_state.story_code:
            show_code = st.expander("Show code")
            with show_code:
                st.code(
                    self._get_code(),
                    language="python",
                )

    def _get_code(self) -> str:
        if "story" in st.session_state and st.session_state.story_code:
            code = []
            code.append("import pandas as pd")
            code.append("from ipyvizzu import Config, Data")
            code.append("from ipyvizzustory import Story, Slide, Step")
            code += DataCodeGenerator.get_data_code(self._file_name, self._df)
            code.append("story = Story(data)")
            code.append(f"story.set_size({self._width}, {self._height})")
            code.append(f'story.set_feature("tooltip", {self._tooltip})\n')
            unformatted_code = "\n".join(
                code + st.session_state.story_code + ["\nstory.play()"]
            )
            formatted_code = black.format_str(unformatted_code, mode=black.FileMode())
            return formatted_code
        return ""
