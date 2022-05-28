import math
import sys
from VectorUtils import Vector2


def constrain(value: float | int, min_val: float | int, max_val: float | int) -> float | int:
    """
    Constrains a value between a minimum and maximum value.
    """
    
    return min(max_val, max(min_val, value))


def raiseError(error_message: str):
    """
    Raises an error with the specified error message.
    """

    print(error_message)
    sys.exit(-1)
