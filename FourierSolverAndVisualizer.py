import sympy as sp
C1,C2,C3,C4,x,y,p,c,t,a,L = sp.symbols("C1 C2 C3 C4 x y p c t a L")
n = sp.symbols("n", integer=True, positive=True)
def fourier_coefficient(f):
    b_n = 2/L * sp.integrate(f * sp.sin(n*sp.pi*x/L), (x,0,L))
    return sp.simplify(b_n)

class Wave_Equation:
    X = C1*sp.cos(p*x) + C2*sp.sin(p*x)
    T = C3*sp.cos(p*c*t) + C4 * sp.sin(p*c*t)
    general_solution = X*T
    def __init__(self, boundary_conditions = [], initial_conditions = [], derivative_conditions = []):
        self.boundary_conditions = boundary_conditions
        self.initial_conditions = initial_conditions
        self.derivative_conditions = derivative_conditions
        self.X = C1*sp.cos(p*x) + C2*sp.sin(p*x)
        self.T = C3*sp.cos(p*c*t) + C4 * sp.sin(p*c*t)
        self.general_solution = self.X * self.T
        self.unknowns = {C1,C2,C3,C4,p}
        self.found = set()
        
    def solve_boundary_conditions(self):
        for sub,value in self.boundary_conditions:
            expression = self.X.subs(x, sub)
            condition = sp.Eq(expression, value)
            involved = self.unknowns.intersection(expression.free_symbols)
            for variable in involved:
                solution = sp.solve(condition, variable)
                if solution:
                    self.found.add(variable)
                    self.unknowns.remove(variable)
                    if variable == C1 and solution[0] == 0:
                        self.unknowns.remove(C2)
                        self.found.add(C2)
                    elif variable == C2 and solution[0] == 0:
                        self.unknowns.remove(C1)
                        self.found.add(C1)
                    if variable == p:
                        self.X = self.X.subs(variable, n*solution[1])
                        self.T = self.T.subs(variable, n*solution[1])
                    else:
                        self.X = self.X.subs(variable, solution[0])
        self.general_solution  = self.X * self.T
        
    def solve_initial_conditions(self):
        for condition,value in self.initial_conditions:
            value = fourier_coefficient(value)
            if condition == "displacement":
                self.X = self.X.subs(C2, 1)
                self.T = self.T.subs(C2, 1)
                self.general_solution = self.X * self.T
                expression = self.general_solution.subs(t, 0)
                coefficient = expression.coeff(sp.sin(n*sp.pi*x/L))
                equation = sp.Eq(coefficient, value)
                solution = sp.solve(equation, C3)
                if solution:
                    self.T = self.T.subs(C3, solution[0])
                self.general_solution  = self.X * self.T
            else:
                derivative = sp.diff(self.general_solution,t)
                expression = sp.expand(derivative.subs(t, 0))
                coefficient = expression.coeff(sp.sin(n*sp.pi*x/L))
                equation = sp.Eq(coefficient, value)    
                solution = sp.solve(equation, C4)
                if solution:
                    self.T = self.T.subs(C4, solution[0])
                self.general_solution  = self.X * self.T
    
    def solve(self):
        self.solve_boundary_conditions()
        self.solve_initial_conditions()
        sp.pprint(self.general_solution)         
        
def main():
    wave = Wave_Equation(boundary_conditions=[(0,0),(L,0)], initial_conditions=[("displacement",a*sp.sin(3*sp.pi*x/L)*sp.cos(5*sp.pi*x/L)),("velocity", 0)])
    wave.solve()
    

if __name__ == "__main__":
    main()