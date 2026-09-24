import sympy as sp

C1, C2, C3, C4, x, y, p, c, t, a, L, lam, b, h = sp.symbols(
    "C1 C2 C3 C4 x y p c t a L lambda b h"
)
n = sp.symbols("n", integer=True, positive=True)


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


def main():
    wave = Wave_Equation(
        [Boundary_Condition(0, 0), Boundary_Condition(L, 0)],
        [
            Displacement_Condition(x * (L**2 - x**2) / 100),
            Velocity_Condition(0),
        ],
    )
    wave.solve()


if __name__ == "__main__":
    main()
