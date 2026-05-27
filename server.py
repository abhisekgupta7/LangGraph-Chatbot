from __future__ import annotations
from fastmcp import FastMCP

mcp=FastMCP("arith")

def __as_number(x):
    """
    Accept ints/floats or numeric strings;raise clear errors otherwise 
    """
    if isinstance(x,(int,float)):
        return float(x)
    if isinstance(x,str):
        return float(x.strip())
    raise TypeError(f"Invalid a number(int/float or numeric string)")

@mcp.tool()
async def add(a:float,b:float)->float:
    """
    Return the sum of a and b.
"""
    return __as_number(a)+__as_number(b)

@mcp.tool()
async def subtract(a:float,b:float)->float:
    """
    Return the difference of a and b.
    """
    return __as_number(a)-__as_number(b)

@mcp.tool()
async def multiply(a:float,b:float)->float:
    """
    Return the product of a and b.
    """
    return __as_number(a)*__as_number(b)    

@mcp.tool()
async def divide(a:float,b:float)->float:
    """
    Return the quotient of a and b.Raises an error if b is zero.
    """
    a=__as_number(a)
    b=__as_number(b)

    if b==0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a/b

@mcp.tool()
async def power(a:float,b:float)->float:
    """
    Return a raised to the power of b.
    """
    return __as_number(a)**__as_number(b)

@mcp.tool()
async def modulus(a:float,b:float)->float:
    """
    Return the modulus of a and b(a % b).Raises an error if b is zero.
    """
    a=__as_number(a)
    b=__as_number(b)

    if b==0:
        raise ZeroDivisionError("Modulus by zero is not allowed.")
    return a%b  

def main():
    mcp.run()


if __name__ == "__main__":
    main()

