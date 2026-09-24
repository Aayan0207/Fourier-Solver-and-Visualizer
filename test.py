import sympy as sp
import pytest
from FourierSolverAndVisualizer import *

questions = [
    (
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
    ),
    (
        [Boundary_Condition(0, 0), Boundary_Condition(L, 0)],
        [
            Displacement_Condition(sp.Function("f")(x)),
            Velocity_Condition(0),
        ],
    ),
    (
        [Boundary_Condition(0, 0), Boundary_Condition(L, 0)],
        [
            Displacement_Condition(0),
            Velocity_Condition(sp.Function("f")(x)),
        ],
    ),
    (
        [Boundary_Condition(0, 0), Boundary_Condition(L, 0)],
        [
            Displacement_Condition(0),
            Velocity_Condition(lam * x * (L - x)),
        ],
    ),
    (
        [Boundary_Condition(0, 0), Boundary_Condition(L, 0)],
        [
            Displacement_Condition(
                sp.Piecewise(
                    (2 * b * x / L, x <= L / 2),
                    (2 * b * (L - x) / L, x <= L),
                )
            ),
            Velocity_Condition(0),
        ],
    ),
    (
        [Boundary_Condition(0, 0), Boundary_Condition(L, 0)],
        [
            Displacement_Condition(x * (L**2 - x**2) / 100),
            Velocity_Condition(0),
        ],
    ),
    (
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
    ),
    (
        [Boundary_Condition(0, 0), Boundary_Condition(1, 0)],
        [
            Displacement_Condition(
                sp.Piecewise(
                    (x, x <= sp.Rational(1, 2)),
                    (1 - x, x <= 1),
                )
            ),
            Velocity_Condition(a),
        ],
    ),
]


@pytest.mark.parametrize("boundary_conditions, initial_conditions", questions)
def test_wave_equation(boundary_conditions, initial_conditions):
    wave = Wave_Equation(
        boundary_conditions=boundary_conditions,
        initial_conditions=initial_conditions,
    )

    wave.solve()

    u = wave.general_solution
    u_tt = sp.diff(u, t, 2)
    u_xx = sp.diff(u, x, 2)

    assert sp.simplify(u_tt - c**2 * u_xx) == 0 and u_tt != 0 and u_xx != 0
