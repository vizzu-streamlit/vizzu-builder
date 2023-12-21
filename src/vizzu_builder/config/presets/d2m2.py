# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,R0801

from __future__ import annotations

from .style import Style
from ...data.parser import DataParser


class D2M2:
    # pylint: disable=too-few-public-methods

    @staticmethod
    def get(dimension1: str, dimension2: str, measure1: str, measure2: str) -> list:
        charts: list[dict] = [
            {
                "config": {
                    "coordSystem": "cartesian",
                    "geometry": "circle",
                    "x": measure2,
                    "y": {"set": measure1, "range": {"min": "auto", "max": "110%"}},
                    "color": dimension2,
                    "lightness": None,
                    "size": None,
                    "noop": dimension1,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                },
                "style": Style.style_bubbleplot_scatterplot(),
                "chart": "Scatter Plot",
            },
            {
                "config": {
                    "coordSystem": "cartesian",
                    "geometry": "circle",
                    "x": measure2,
                    "y": {"set": measure1, "range": {"min": "auto", "max": "110%"}},
                    "color": dimension2,
                    "lightness": None,
                    "size": measure1,
                    "noop": dimension1,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                },
                "style": Style.style(),
                "chart": "Bubble Plot",
            },
            {
                "config": {
                    "coordSystem": "cartesian",
                    "geometry": "circle",
                    "x": measure2,
                    "y": {"set": measure1, "range": {"min": "auto", "max": "110%"}},
                    "color": dimension2,
                    "lightness": None,
                    "size": measure2,
                    "noop": dimension1,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                },
                "style": Style.style(),
                "chart": "Bubble Plot V2",
            },
            {
                "config": {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": None,
                    "y": {"set": None, "range": {"min": "auto", "max": "auto"}},
                    "color": dimension2,
                    "lightness": measure2,
                    "size": [dimension1, measure1],
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                },
                "style": Style.style(),
                "chart": "Stacked Treemap",
            },
            {
                "config": {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": [dimension2, measure2],
                    "y": {
                        "set": [dimension1, measure1],
                        "range": {"min": "auto", "max": "auto"},
                    },
                    "color": dimension2,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                },
                "style": Style.style(),
                "chart": "Stacked Mekko Chart",
            },
            {
                "config": {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": [dimension2, measure2],
                    "y": {
                        "set": [dimension1, measure1],
                        "range": {"min": "auto", "max": "auto"},
                    },
                    "color": dimension2,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "stretch",
                    "orientation": "horizontal",
                },
                "style": Style.style(),
                "chart": "Marimekko Chart",
            },
            {
                "config": {
                    "coordSystem": "polar",
                    "geometry": "circle",
                    "x": measure2,
                    "y": {"set": measure1, "range": {"min": "auto", "max": "110%"}},
                    "color": dimension2,
                    "lightness": None,
                    "size": None,
                    "noop": dimension1,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                },
                "style": Style.style_polarscatter(),
                "chart": "Polar Scatter",
            },
        ]
        for chart in charts:
            chart["types"] = {}
            chart["types"][dimension1] = DataParser.DIMENSION
            chart["types"][dimension2] = DataParser.DIMENSION
            chart["types"][measure1] = DataParser.MEASURE
            chart["types"][measure2] = DataParser.MEASURE
        return charts
