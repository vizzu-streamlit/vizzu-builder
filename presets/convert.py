import pandas as pd
import json

df = pd.read_csv("presets.csv")

keys = [
    "Cat1, Value1",
    "Cat1, Value1, Value2",
    "Cat1, Cat2, Value1",
    "Cat1, Cat2, Value1, Value2",
]

json_data = {str(key): [] for key in keys}

for _, row in df.iterrows():
    contains = {"Cat1": False, "Cat2": False, "Value1": False, "Value2": False}
    data = {}
    for col in row.index:
        original_value = row[col] if not pd.isna(row[col]) else None
        value = original_value
        if isinstance(original_value, str):
            original_values = original_value.split(",")
            if len(original_values) > 1:
                value = original_values
        data[col] = value
        cell = str(original_value)
        if "Cat1" in cell:
            contains["Cat1"] = True
        if "Cat2" in cell:
            contains["Cat2"] = True
        if "Value1" in cell:
            contains["Value1"] = True
        if "Value2" in cell:
            contains["Value2"] = True
    key = ", ".join(key for key, value in contains.items() if value)
    json_data[key].append(data)

json_str = json.dumps(json_data, indent=4)

with open("presets.json", "w") as json_file:
    json_file.write(json_str)
