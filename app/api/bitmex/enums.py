from enum import Enum


class OrderState(str, Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"