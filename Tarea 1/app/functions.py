import re
import os
import pandas as pd

KEYS = ["OUTLOOK", "TEMPERATURE", "HUMIDITY", "WINDY", "PLAY"]

PATTERNS = [
    r"^[a-zA-Z0-9\s.-]+$",  # OUTLOOK
    r"^\d{1,3}$",           # TEMPERATURE
    r"^\d{1,3}$"            # HUMIDITY
    r"^\d{1,1}$",           # WINDY
    r"^\d{1,3}$"            # 
]

DEFAULT_VALUES = [
    "Sunny...",        # OUTLOOK
    "0",            # TEMPERATURE
    "0",            # HUMIDITY
    "0, 1",         # WINDY
    "0"             # 
]

DESCRIPTIONS = [
    "Outlook",
    "Temperature",
    "Humidity",
    "Windy",
    "Play"
]

WIDTHS = [10, 10, 10, 10, 10]


def get_Keys() -> list:
    return KEYS

def get_Parameter_DV(Parameter : str) -> str:
    return dict(zip(KEYS, DEFAULT_VALUES))[Parameter]

def get_Parameter_Des(Parameter : str) -> str:
    return dict(zip(KEYS, DESCRIPTIONS))[Parameter]

def get_Parameter_Width(Parameter : str) -> int:
    return dict(zip(KEYS, WIDTHS))[Parameter]

def is_Valid_Code(code : str) -> bool:
    return re.match(PATTERNS[0], str(code))

def Verify_Data(entry : dict) -> tuple:
    errors_in_fields = []
    check_dict = dict(zip(KEYS[:-1], PATTERNS))
    for key in KEYS[:-1]:
        if not re.match(check_dict[key], entry[key].get()):
            errors_in_fields.append(key)

    return len(errors_in_fields) == 0, errors_in_fields

def isValid_CSV(csv_path : str) -> bool:
    return csv_path == None or not os.path.isfile(csv_path)