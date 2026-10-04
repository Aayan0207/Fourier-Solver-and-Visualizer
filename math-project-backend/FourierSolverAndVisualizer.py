import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

C1, C2, C3, C4, x, y, p, c, t, a, L, lam, b, h = sp.symbols(
    "C1 C2 C3 C4 x y p c t a L lambda b h"
)
n = sp.symbols("n", integer=True, positive=True)

transformations = standard_transformations + (implicit_multiplication_application,)


def generate_condition(expr):
    if not expr:
        return 0
    if not isinstance(expr, str):
        return sp.sympify(expr)
    if expr.startswith("Which"):
        expr = create_piecewise(expr)
    expressions = {
        "np.arcsin": "asin",
        "np.arccos": "acos",
        "np.arctan": "atan",
        "np.sinh": "sinh",
        "np.cosh": "cosh",
        "np.tanh": "tanh",
        "np.log": "log",
        "np.exp": "exp",
        "np.sin": "sin",
        "np.cos": "cos",
        "np.tan": "tan",
        "np.sqrt": "sqrt",
        "np.pi": "pi",
    }
    for key, value in expressions.items():
        expr = expr.replace(key, value)

    return sp.sympify(
        expr,
        locals={
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "sinh": sp.sinh,
            "cosh": sp.cosh,
            "tanh": sp.tanh,
            "log": sp.log,
            "exp": sp.exp,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "sqrt": sp.sqrt,
            "pi": sp.pi,
        },
    )


def create_piecewise(expr):
    expr = expr.removeprefix("Which(").removesuffix(")")
    parts = [p.strip() for p in expr.split(",")]
    cases = []
    for i in range(0, len(parts), 2):
        condition = parse_expr(parts[i], transformations=transformations)
        expression = parse_expr(parts[i + 1], transformations=transformations)
        cases.append((expression, condition))
    return str(sp.Piecewise(*cases))


class Heat_Equation:
    X = C1 * sp.cos(p * x) + C2 * sp.sin(p * x)
    T = C3 * sp.exp(-(c**2) * p**2 * t)
    general_solution = X * T

    def __init__(
        self,
        boundary_conditions=None,
        initial_conditions=None,
        lower=0,
        upper=L,
    ):
        self.length = upper - lower
        self.boundary_conditions = []
        if boundary_conditions:
            self.boundary_conditions = boundary_conditions
        self.initial_conditions = []
        if initial_conditions:
            self.initial_conditions = initial_conditions
        self.X = Heat_Equation.X
        self.T = Heat_Equation.T
        self.general_solution = Heat_Equation.general_solution

    def solve_boundary_conditions(self):
        for cond in self.boundary_conditions:
            sub = cond.x
            value = cond.value
            expression = self.X.subs(x, sub)
            condition = sp.Eq(expression, value)

            if expression.has(C1):
                solution = sp.solve(condition, C1)
                if solution:
                    self.X = self.X.subs(C1, solution[0])

            elif expression.has(p) and expression.has(C2):
                p_value = n * sp.pi / self.length
                self.X = self.X.subs(p, p_value)
                self.T = self.T.subs(p, p_value)

            elif expression.has(C2):
                solution = sp.solve(condition, C2)
                if solution:
                    self.X = self.X.subs(C2, solution[0])

        self.general_solution = self.X * self.T

    def solve_initial_conditions(self):
        temperature = 0

        for cond in self.initial_conditions:
            if cond.type.lower() == "temperature":
                temperature = cond.value

        b_n = self.b_n(temperature)

        self.X = self.X.subs(C2, 1)
        self.T = self.T.subs(C3, b_n)

        self.general_solution = self.X * self.T

    def b_n(self, temperature):
        b_n = (
            2
            / self.length
            * sp.integrate(
                temperature * sp.sin(n * sp.pi * x / self.length),
                (x, 0, self.length),
            )
        )
        return sp.simplify(b_n)

    def solve(self):
        self.solve_boundary_conditions()
        self.solve_initial_conditions()
        return sp.latex(self.general_solution)


class Wave_Equation:
    X = C1 * sp.cos(p * x) + C2 * sp.sin(p * x)
    T = C3 * sp.cos(p * c * t) + C4 * sp.sin(p * c * t)
    general_solution = X * T

    def __init__(
        self,
        boundary_conditions=None,
        initial_conditions=None,
        lower=0,
        upper=L,
    ):
        self.length = upper - lower
        self.boundary_conditions = []
        if boundary_conditions:
            self.boundary_conditions = boundary_conditions
        self.initial_conditions = []
        if initial_conditions:
            self.initial_conditions = initial_conditions
        self.X = Wave_Equation.X
        self.T = Wave_Equation.T
        self.general_solution = Wave_Equation.general_solution

    def solve_boundary_conditions(self):
        for cond in self.boundary_conditions:
            sub = cond.x
            value = cond.value
            expression = self.X.subs(x, sub)
            condition = sp.Eq(expression, value)
            if expression.has(C1):
                solution = sp.solve(condition, C1)
                if solution:
                    self.X = self.X.subs(C1, solution[0])
            elif expression.has(p) and expression.has(C2):
                p_value = n * sp.pi / self.length
                self.X = self.X.subs(p, p_value)
                self.T = self.T.subs(p, p_value)
            elif expression.has(C2):
                solution = sp.solve(condition, C2)
                if solution:
                    self.X = self.X.subs(C2, solution[0])
        self.general_solution = self.X * self.T

    def solve_initial_conditions(self):
        displacement = 0
        velocity = 0
        for cond in self.initial_conditions:
            if cond.type.lower() == "displacement":
                displacement = cond.value
            elif cond.type.lower() == "velocity":
                velocity = cond.value

        a_n = self.a_n(velocity)
        b_n = self.b_n(displacement)

        self.X = self.X.subs(C2, 1)

        self.T = self.T.subs(C3, a_n)
        self.T = self.T.subs(C4, b_n)

        self.general_solution = self.X * self.T

    def b_n(self, displacement):
        b_n = (
            2
            / self.length
            * sp.integrate(
                displacement * sp.sin(n * sp.pi * x / self.length), (x, 0, self.length)
            )
        )
        return sp.simplify(b_n)

    def a_n(self, velocity):
        a_n = (
            2
            / (n * sp.pi * c)
            * sp.integrate(
                velocity * sp.sin(n * sp.pi * x / self.length), (x, 0, self.length)
            )
        )
        return sp.simplify(a_n)

    def solve(self):
        self.solve_boundary_conditions()
        self.solve_initial_conditions()
        return sp.latex(self.general_solution)

class Laplace_Equation:
    X = C1 * sp.sin(p*x) + C2 * sp.cos(p*x)
    Y = C3 * sp.exp(p*y) + C4 * sp.exp(-p*y)
    general_solution = X * Y

    def __init__(self,boundary_conditions=None,lower=0,upper=L):
        self.length=upper-lower
        self.lower=lower
        self.upper=upper
        self.boundary_conditions=boundary_conditions or []
        self.general_solution=Laplace_Equation.general_solution
        self.boundary_equations=[]
        self.solution=None

    def solve(self):
        self.boundary_equations=[]

        for cond in self.boundary_conditions:
            if cond.variable=="x":
                expression=self.general_solution.subs(x,cond.position)
            elif cond.variable=="y":
                expression=self.general_solution.subs(y,cond.position)
            else:
                raise ValueError("Variable must be x or y")

            self.boundary_equations.append(
                sp.Eq(expression,cond.value,evaluate=False)
            )

        if len(self.boundary_conditions)!=4:
            raise ValueError("Four boundary conditions are required")

        if all(sp.simplify(cond.value)==0 for cond in self.boundary_conditions):
            self.solution=sp.Integer(0)
            return sp.latex(self.solution)

        raise NotImplementedError(
            "Nonzero boundary conditions require a Fourier series solution."
        )
class Condition:
    def __init__(self, condition_type):
        self.type = condition_type


class Boundary_Condition(Condition):
    def __init__(self, x, value):
        super().__init__("boundary")
        self.x = x
        self.value = value


class Initial_Condition(Condition):
    def __init__(self, type):
        super().__init__("initial")
        self.type = type


class Displacement_Condition(Initial_Condition):
    def __init__(self, value):
        super().__init__("Displacement")
        self.value = value


class Velocity_Condition(Initial_Condition):
    def __init__(self, value):
        super().__init__("Velocity")
        self.value = value


class Temperature_Condition(Initial_Condition):
    def __init__(self, value):
        super().__init__("Temperature")
        self.value = value

class Laplace_Boundary_Condition(Condition):
    def __init__(self,variable,position,value):
        super().__init__("Laplace_Boundary")
        self.variable=variable
        self.position=position
        self.value=value
        
def main():
    wave = Wave_Equation(
        [Boundary_Condition(0, 0), Boundary_Condition(L, 0)],
        [
            Displacement_Condition(
                sp.Piecewise(
                    (3 * h * x / L, x <= L / 3),
                    (3 * h * (L - x) / (2 * L), x <= L),
                )
            ),
            Velocity_Condition(0),
        ],
    )
    # sp.pprint(wave.solve())
    heat = Heat_Equation(
        [Boundary_Condition(0, 0), Boundary_Condition(L, 0)],
        [
            Temperature_Condition(x * (L**2 - x**2) / 100),
        ],
    )
    # sp.pprint(heat.solve())
    laplace=Laplace_Equation([
        Laplace_Boundary_Condition("x",0,0),
        Laplace_Boundary_Condition("x",L,0),
        Laplace_Boundary_Condition("y",0,0),
        Laplace_Boundary_Condition("y",L,0)
    ])
    sp.pprint(laplace.solve())

if __name__ == "__main__":
    main()
