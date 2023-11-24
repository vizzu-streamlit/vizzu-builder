# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import copy


class Style:
    @staticmethod
    def style() -> dict:
        return {
            "plot": {
                "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                "marker": {
                    "label": {
                        "numberFormat": "prefixed",
                        "maxFractionDigits": "1",
                        "numberScale": "shortScaleSymbolUS",
                    },
                    "rectangleSpacing": None,
                    "circleMinRadius": 0.005,
                    "borderOpacity": 1,
                },
            },
        }

    @staticmethod
    def style_lollipop() -> dict:
        style = copy.deepcopy(Style.style())
        style["plot"]["marker"]["rectangleSpacing"] = 0
        style["plot"]["marker"]["circleMinRadius"] = 0.02
        return style

    @staticmethod
    def style_bubbleplot_scatterplot() -> dict:
        style = copy.deepcopy(Style.style())
        style["plot"]["marker"]["rectangleSpacing"] = 0
        style["plot"]["marker"]["circleMinRadius"] = 0.015
        return style

    @staticmethod
    def style_polarscatter() -> dict:
        style = copy.deepcopy(Style.style())
        style["plot"]["marker"]["rectangleSpacing"] = 0
        style["plot"]["marker"]["circleMinRadius"] = 0.025
        return style

    @staticmethod
    def style_nesteddonut() -> dict:
        style = copy.deepcopy(Style.style())
        style["plot"]["marker"]["rectangleSpacing"] = 0
        style["plot"]["marker"]["circleMinRadius"] = 0.015
        style["plot"]["marker"]["borderOpacity"] = 0
        return style

    @staticmethod
    def style_heatmap() -> dict:
        style = copy.deepcopy(Style.style())
        style["plot"]["marker"]["rectangleSpacing"] = 0
        return style
