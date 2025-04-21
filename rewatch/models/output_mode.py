from enum import StrEnum


class OutputMode(StrEnum):
    PRETTY = "pretty"
    BARS = "bars"
    DOTS = "dots"
    RAW = "raw"
    JSON = "json"
    NONE = "none"
