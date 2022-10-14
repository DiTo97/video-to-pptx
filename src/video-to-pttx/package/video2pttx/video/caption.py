import enum
from enum import auto


class CaptionType(enum.Enum):
    """A class that wraps the caption type: XML or SRT"""
    xml = auto()
    srt = auto()
