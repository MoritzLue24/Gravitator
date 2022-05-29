

def constrain(value: float | int, min_val: float | int, max_val: float | int) -> float | int:
    '''
    Constrains a value between a minimum and maximum value.
    '''
    
    return min(max_val, max(min_val, value))
