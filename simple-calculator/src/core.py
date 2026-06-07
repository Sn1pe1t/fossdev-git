def add(a: float, b: float) -> float:
    """Return sum of a and b."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Return difference a - b."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Return product of a and b."""
    return a * b

def divide(a: float, b: float) -> float:
    """Return quotient of a divided by b. Raises ValueError if b == 0."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b