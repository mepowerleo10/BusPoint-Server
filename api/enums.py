# Constants for color
from enum import Enum

class RouteColors(Enum):
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    RED = "#E53935"
    LIGHT_BLUE = "#4FC3F7"
    BLUE = "#1E88E5"
    DARK_BLUE = "#01579B"
    GREEN = "#4CAF50"
    DEEP_GREEN = "#1B5E20"
    YELLOW = "#FDD835"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]