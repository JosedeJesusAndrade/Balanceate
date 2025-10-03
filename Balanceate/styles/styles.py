from enum import Enum
import reflex as rx
from .colors import Colors
from .fonts import Font, FontWeight


#Constants for styles
class Size(Enum):
    ZERO = "0px"
    SMALL = "0.5em"
    DEFAULT = "1em"
    MEDIUM = "1.5em"
    LARGE = "2em"
    BIG = "3em"
    VERY_BIG = "4em"

MAX_WIDTH = "600px"

#STYLESHEETS
STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap",
    "https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&display=swap",
    "https://fonts.googleapis.com/css2?family=Inter:wght@500&display=swap"
]


#Styles
BASE_STYLE = {
    "font_family": Font.DEFAULT.value,
    "font_weight": FontWeight.LIGHT.value,
    "background_color": Colors.SECONDARY.value,

}