from sympy import simplify

def do_calculation(number1, number2):
    return number1 + number2

def symplify_bool(eq1, eq2):
    return simplify(eq1-eq2) == 0