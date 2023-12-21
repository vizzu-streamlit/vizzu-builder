# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

import streamlit as st

from .chart.configurator import SelectedChartConfig, ChartConfigurator
from .chart.generator import ChartGenerator
from .chart.updater import ChartUpdater
from .data.configurator import DataConfig, DataConfigurator
from .story.generator import StoryGenerator


class App:
    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        self._builder_data = DataConfig()
        self._builder_config = SelectedChartConfig()

        self._init_page()
        self._add_data_configurator()
        self._add_chart_configurator()
        self._add_chart_updater()
        self._add_generators()

    def _init_page(self) -> None:
        st.set_page_config(page_title="Vizzu Builder", page_icon="🏗️", layout="wide")
        col3,col4 = st.columns([4, 1])
        col3.header("🏗️ Vizzu Streamlit Builder App - No-Code Data Animation")
        col3.subheader("Welcome! 🤩")
        col4.image("https://github.com/vizzuhq/vizzu-workshops/blob/main/2023-11-20-Budapest_BI_Forum/assets/Vizzu_Logo2.png?raw=true")
        col1, col2 = st.columns(2)
        col1.markdown('''- Create stunning Vizzu charts and animated data stories without writing a single line of code.
- Quickly and easily create and iterate on your charts.
- Access the Python code of the generated charts and fine-tune them in a notebook or another Streamlit app if needed.''')
        col2.markdown('''- Learn to use our open-source Python tool, [ipyvizzu](https://ipyvizzu.com), via the code automatically generated for all charts and stories.
- Need help? Join our community [Slack](https://join.slack.com/t/vizzu-community/shared_invite/zt-w2nqhq44-2CCWL4o7qn2Ns1EFSf9kEg) or contact us at hello@vizzuhq.com.
- Explore the code for this app and report bugs at our [GitHub repository](https://github.com/vizzu-streamlit/vizzu-builder). You can also create a screencast by clicking on the three dots in the top right corner to help us understand your issue. We’d appreciate your help and feedback.
		''')

    def _add_data_configurator(self) -> None:
        data_configurator = DataConfigurator()
        self._builder_data = data_configurator.data

    def _add_chart_configurator(self) -> None:
        chart_configurator = ChartConfigurator(self._builder_data)
        self._builder_config = chart_configurator.config

    def _add_chart_updater(self) -> None:
        ChartUpdater(self._builder_data, self._builder_config)

    def _add_generators(self) -> None:
        story_generator = StoryGenerator()
        ChartGenerator(story_generator)
        story_generator.play()
