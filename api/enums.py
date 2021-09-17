# Constants for color
from enum import Enum

class RouteColors(Enum):
    WHITE = "#EEEEEE"
    BLACK = "#9E9E9E"
    RED = "#EF5350"
    BLUE = "#42a5f5"
    GREEN = "#9CCC65"
    DEEP_GREEN = "#1B5E20"
    YELLOW = "#FDD835"
    BROWN = "#a1887f"


    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]