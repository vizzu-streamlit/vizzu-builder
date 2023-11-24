# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,R0801

from __future__ import annotations

from .style import Style


class D1M2:
    # pylint: disable=too-few-public-methods

    @staticmethod
    def get(dimension1: str, measure1: str, measure2: str) -> list:
        return [
            {
                "config": {
                    "coordSystem": "cartesian",
                    "geometry": "circle",
                    "x": measure2,
                    "y": {"set": measure1, "range": {"min": None, "max": "110%"}},
                    "color": None,
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
                    "y": {"set": measure1, "range": {"min": None, "max": "110%"}},
                    "color": None,
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
                    "y": {"set": measure1, "range": {"min": None, "max": "110%"}},
                    "color": None,
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
                    "coordSystem": "polar",
                    "geometry": "circle",
                    "x": measure2,
                    "y": {"set": measure1, "range": {"min": None, "max": "110%"}},
                    "color": None,
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
            {
                "config": {
                    "coordSystem": "polar",
                    "geometry": "rectangle",
                    "x": [dimension1, measure2],
                    "y": {"set": measure1, "range": {"min": None, "max": None}},
                    "color": dimension1,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                },
                "style": Style.style(),
                "chart": "Variable Radius Pie Chart",
            },
            {
                "config": {
                    "coordSystem": "cartesian",
                    "geometry": "rectangle",
                    "x": [dimension1, measure2],
                    "y": {"set": measure1, "range": {"min": None, "max": None}},
                    "color": dimension1,
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                },
                "style": Style.style(),
                "chart": "Mekko",
            },
        ]
