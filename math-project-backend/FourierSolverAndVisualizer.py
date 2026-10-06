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
                displacement * sp.sin(n * sp.pi * x / self.length),
                (x, 0, self.length),
            )
        )
        return sp.simplify(b_n)
    
    def a_n(self, velocity):
        a_n = (
            2
            / (n * sp.pi * c)
            * sp.integrate(
                velocity * sp.sin(n * sp.pi * x / self.length),
                (x, 0, self.length),
            )
        )
        return sp.simplify(a_n)
    
    def solve(self):
        self.solve_boundary_conditions()
        self.solve_initial_conditions()
        return sp.latex(self.general_solution)
    
class Laplace_Equation:
    def __init__(self,boundary_conditions=None,L=L,H=h):
        self.boundary_conditions=boundary_conditions or []
        self.L=L
        self.H=H
        self.solution=None
        self.fourier_coefficients={}
    def solve_boundary_conditions(self):
        self.left_boundary=None
        self.right_boundary=None
        self.bottom_boundary=None
        self.top_boundary=None
        for condition in self.boundary_conditions:
            if condition.variable=="x":
                if condition.position==0:
                    self.left_boundary=condition.value
                elif condition.position==self.L:
                    self.right_boundary=condition.value
            elif condition.variable=="y":
                if condition.position==0:
                    self.bottom_boundary=condition.value
                elif condition.position==self.H:
                    self.top_boundary=condition.value
    def b_n(self,n,boundary=None):
        if boundary is None:
            if self.bottom_boundary is not None:
                boundary=self.bottom_boundary
            elif self.top_boundary is not None:
                boundary=self.top_boundary
            else:
                return 0
        coefficient=sp.simplify(
            (2/self.L)*sp.integrate(
                boundary*sp.sin(n*sp.pi*x/self.L),
                (x,0,self.L)
            )
        )
        self.fourier_coefficients[n]=coefficient
        return coefficient
    def term(self,n,boundary=None,position=None):
        if boundary is None:
            if self.bottom_boundary is not None:
                boundary=self.bottom_boundary
                position="bottom"
            elif self.top_boundary is not None:
                boundary=self.top_boundary
                position="top"
            else:
                return 0
        coefficient=self.b_n(n,boundary)
        lam=sp.symbols("lam",positive=True)
        equation=sp.Eq(lam*self.L,n*sp.pi)
        lam_n=sp.solve(equation,lam)[0]
        if self.H==sp.oo:
            return sp.simplify(
                coefficient*
                sp.sin(lam_n*x)*
                sp.exp(-lam_n*y)
            )
        if position=="bottom":
            return sp.simplify(
                coefficient*
                sp.sin(lam_n*x)*
                sp.sinh(lam_n*(self.H-y))/
                sp.sinh(lam_n*self.H)
            )
        if position=="top":
            return sp.simplify(
                coefficient*
                sp.sin(lam_n*x)*
                sp.sinh(lam_n*y)/
                sp.sinh(lam_n*self.H)
            )
    def solve_fourier_series(self,terms,boundary=None,position=None):
        self.solution=sp.Integer(0)
        for n in range(1,terms+1):
            self.solution+=self.term(n,boundary,position)
        self.solution=sp.simplify(self.solution)
        return self.solution
    def solve_multiple_boundaries(self):
        self.solve_boundary_conditions()
        base=self.left_boundary
        if base is None:
            base=self.right_boundary
        if base is None:
            base=self.bottom_boundary
        if base is None:
            base=self.top_boundary
        top_difference=sp.simplify(self.top_boundary-base)
        self.solution=base+self.solve_fourier_series(
            terms,
            boundary=top_difference,
            position="top"
        )
        self.solution=sp.simplify(self.solution)
        return self.solution
    def general_term(self,n,boundary=None,position=None):
        return self.term(n,boundary,position)
    def piecewise_sigma_solution(self,boundary=None,position=None):
        if boundary is None:
            if self.bottom_boundary is not None:
                boundary=self.bottom_boundary
                position="bottom"
            elif self.top_boundary is not None:
                boundary=self.top_boundary
                position="top"
            else:
                return 0
        if self.L==sp.pi and sp.simplify(boundary-sp.sin(x)**2)==0:
            coefficient=8/(sp.pi*n*(4-n**2))
            condition=sp.Eq(sp.Mod(n,2),1)
        else:
            coefficient=sp.simplify(
                (2/self.L)*sp.Integral(
                    boundary*sp.sin(n*sp.pi*x/self.L),
                    (x,0,self.L)
                )
            )
            condition=True
        if self.H==sp.oo:
            term=coefficient*sp.sin(n*sp.pi*x/self.L)*sp.exp(-n*sp.pi*y/self.L)
        elif position=="bottom":
            term=(
                coefficient*
                sp.sin(n*sp.pi*x/self.L)*
                sp.sinh(n*sp.pi*(self.H-y)/self.L)/
                sp.sinh(n*sp.pi*self.H/self.L)
            )
        elif position=="top":
            term=(
                coefficient*
                sp.sin(n*sp.pi*x/self.L)*
                sp.sinh(n*sp.pi*y/self.L)/
                sp.sinh(n*sp.pi*self.H/self.L)
            )
        else:
            return 0
        if condition!=True:
            term=sp.Piecewise(
                (term,condition),
                (0,True)
            )
        return sp.Sum(term,(n,1,sp.oo))
    def solve(self):
        self.solve_boundary_conditions()
        return self
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
            Displacement_Condition(x * (L**2 - x**2) / 100),
            Velocity_Condition(0),
        ],
    )
    wave.solve()
    print("WAVE EQUATION")
    print("X =", wave.X)
    print("T =", wave.T)
    print("Solution =", wave.general_solution)
    heat = Heat_Equation(
        [Boundary_Condition(0, 0), Boundary_Condition(L, 0)],
        [
            Temperature_Condition(x * (L**2 - x**2) / 100),
        ],
    )
    heat.solve()
    print("\nHEAT EQUATION")
    print("X =", heat.X)
    print("T =", heat.T)
    print("Solution =", heat.general_solution)
    laplace=Laplace_Equation([
        Laplace_Boundary_Condition("x",0,0),
        Laplace_Boundary_Condition("x",sp.pi,0),
        Laplace_Boundary_Condition("y",0,sp.sin(x)**2),
        Laplace_Boundary_Condition("y",sp.pi,0)
    ],L=sp.pi,H=sp.pi)
    laplace.solve()
    print("\nLAPLACE EQUATION - Q2")
    print("b1 =",laplace.b_n(1))
    print("b2 =",laplace.b_n(2))
    print("b3 =",laplace.b_n(3))
    print("b4 =",laplace.b_n(4))
    print("b5 =",laplace.b_n(5))
    result=laplace.piecewise_sigma_solution()
    print("Piecewise Sigma Solution =",result)
if __name__ == "__main__":
    main()