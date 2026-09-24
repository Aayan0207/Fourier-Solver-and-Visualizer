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
        boundary_conditions=[],
        initial_conditions=[],
        lower=0,
        upper=L,
    ):
        self.length = upper - lower
        self.boundary_conditions = boundary_conditions
        self.initial_conditions = initial_conditions
        self.X = Wave_Equation.X
        self.T = Wave_Equation.T
        self.general_solution = Wave_Equation.general_solution
        self.unknowns = {C1, C2, C3, C4, p}

    def solve_boundary_conditions(self):
        for cond in self.boundary_conditions:
            sub = cond.x
            value = cond.value
            expression = self.X.subs(x, sub)
            condition = sp.Eq(expression, value)
            involved = self.unknowns.intersection(expression.free_symbols)
            for variable in involved:
                solution = sp.solve(condition, variable)
                if solution:
                    self.unknowns.remove(variable)
                    if variable == C1 and solution[0] == 0:
                        self.unknowns.remove(C2)
                    elif variable == C2 and solution[0] == 0:
                        self.unknowns.remove(C1)
                    if variable == p:
                        self.X = self.X.subs(variable, n * solution[1])
                        self.T = self.T.subs(variable, n * solution[1])
                    else:
                        self.X = self.X.subs(variable, solution[0])
        self.general_solution = self.X * self.T

    def solve_initial_conditions(self):
        displacement = 0
        velocity = 0
        for cond in self.initial_conditions:
            if cond.type.lower() == "displacement":
                displacement = cond.value
            elif cond.type.lower() == "velocity":
                velocity = cond.value

        a_n = self.a_n(displacement)
        b_n = self.b_n(velocity)

        self.X = self.X.subs(C2, 1)

        self.T = self.T.subs(C3, a_n)
        self.T = self.T.subs(C4, b_n)

        self.general_solution = self.X * self.T

    def a_n(self, displacement):
        a_n = (
            2
            / self.length
            * sp.integrate(
                displacement * sp.sin(n * sp.pi * x / self.length), (x, 0, self.length)
            )
        )
        return sp.simplify(a_n)

    def b_n(self, velocity):
        b_n = (
            2
            / (n * sp.pi * c)
            * sp.integrate(
                velocity * sp.sin(n * sp.pi * x / self.length), (x, 0, self.length)
            )
        )
        return sp.simplify(b_n)

    def solve(self):
        self.solve_boundary_conditions()
        self.solve_initial_conditions()
        sp.pprint(self.general_solution)


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
                     Displacement_Condition(sp.Function("f")(x)),
                     Velocity_Condition(0),
                 ],
    )
    wave.solve()


if __name__ == "__main__":
    main()
