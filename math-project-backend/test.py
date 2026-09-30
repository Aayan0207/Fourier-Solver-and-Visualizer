import sympy as sp
import pytest
from FourierSolverAndVisualizer import *

questions_wave = [
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

questions_heat = [
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Temperature_Condition(
                sp.sin(sp.pi * x / L)
            ),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(2, 0),
        ],
        [
            Temperature_Condition(
                sp.sin(sp.pi * x / 2)
                + 3 * sp.sin(5 * sp.pi * x / 2)
            ),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Temperature_Condition(a),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(100, 0),
        ],
        [
            Temperature_Condition(
                50 * sp.sin(sp.pi * x / 100)
            ),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Temperature_Condition(
                sp.sin(sp.pi * x / L)
            ),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(10, 0),
        ],
        [
            Temperature_Condition(
                sp.Piecewise(
                    (40 * x, (x > 0) & (x < 5)),
                    (40 * (10 - x), (x > 5) & (x < 10)),
                )
            ),
        ],
    ),
]

@pytest.mark.parametrize("boundary_conditions, initial_conditions", questions_wave)
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


@pytest.mark.parametrize("boundary_conditions, initial_conditions", questions_heat)
def test_heat_equation(boundary_conditions, initial_conditions):
    heat = Heat_Equation(
        boundary_conditions=boundary_conditions,
        initial_conditions=initial_conditions,
    )

    heat.solve()

    u = heat.general_solution
    u_t = sp.diff(u, t, 1)
    u_xx = sp.diff(u, x, 2)

    assert sp.simplify(u_t - c**2 * u_xx) == 0 and u_t != 0 and u_xx != 0
