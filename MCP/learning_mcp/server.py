from mcp.server import MCPServer

mcp=MCPServer("hello_mcp")

@mcp.tool()
def add(a: int | float, b: int | float) -> int | float:
    """Add two numbers.

    Args:
        a (int | float): First number.
        b (int | float): Second number.

    Returns:
        int | float: Sum of a and b.
    """
    return a + b

@mcp.tool()
def sub(a: int | float, b: int | float) -> int | float:
    """Subtract the second number from the first.

    Args:
        a (int | float): First number.
        b (int | float): Second number.

    Returns:
        int | float: Difference between a and b.
    """
    return a - b

@mcp.tool()
def multiply(a: int | float, b: int | float) -> int | float:
    """Multiply two numbers.

    Args:
        a (int | float): First number.
        b (int | float): Second number.

    Returns:
        int | float: Product of a and b.
    """
    return a * b

@mcp.tool()
def divide(a: int | float, b: int | float) -> float:
    """Divide the first number by the second.

    Args:
        a (int | float): Numerator.
        b (int | float): Denominator.

    Returns:
        float: Division result.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")

    return a / b

@mcp.tool()
def modulus(a: int | float, b: int | float) -> int | float:
    """Return the remainder after division.

    Args:
        a (int | float): First number.
        b (int | float): Second number.

    Returns:
        int | float: Remainder of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot calculate modulus with zero.")

    return a % b