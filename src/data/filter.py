from __future__ import annotations

import streamlit as st
import pandas as pd
from pandas.api.types import (
    CategoricalDtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from streamlit_extras.row import row

if "filters" not in st.session_state:
    st.session_state["filters"] = None


def filter_dataframe(df: pd.DataFrame) -> str | None:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.toggle("Add filters")

    if not modify:
        return None

    filters: list[str] = []

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        rows = row(2)
        for column in to_filter_columns:
            # Treat columns with < 10 unique values as categorical
            if (
                isinstance(df[column].dtype, CategoricalDtype)
                or df[column].nunique() < 10
            ):
                user_cat_input = rows.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                filters.append(
                    "||".join(
                        [f"record['{column}'] == '{cat}'" for cat in user_cat_input]
                    )
                )
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = rows.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                filters.append(
                    f"record['{column}'] >= {user_num_input[0]} "
                    f"&& record['{column}'] <= {user_num_input[1]}"
                )
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = rows.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    # df = df.loc[df[column].between(start_date, end_date)]
                    filters.append(
                        f"record['{column}'] <= '{end_date}' "
                        f"&& record['{column}'] >= '{start_date}'"
                    )
            else:
                user_text_input = rows.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    filters.append(f"record['{column}'].includes('{user_text_input}')")
                    # df = df[df[column].astype(str).str.contains(user_text_input)]

                # raise NotImplementedError("Cannot filter on this column currently")

    filters_wrapped = [f"({_f})" for _f in filters]

    filters = " && ".join(filters_wrapped) if filters_wrapped else None

    if st.button("Update data"):
        st.session_state["filters"] = filters
