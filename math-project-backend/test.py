import sympy as sp
import pytest
from FourierSolverAndVisualizer import *

questions_wave = [
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(a * sp.sin(sp.pi * x / L)),
            Velocity_Condition(0),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(a * sp.sin(3 * sp.pi * x / L)),
            Velocity_Condition(0),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(K * (L * x - x**2)),
            Velocity_Condition(0),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(0),
            Velocity_Condition(b * x / L * sp.sin(sp.pi * x / L)),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(0),
            Velocity_Condition(lam * x * (L - x)),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
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
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(
                sp.Piecewise(
                    (2 * k * x / L, x <= L / 2),
                    (2 * k * (L - x) / L, x <= L),
                )
            ),
            Velocity_Condition(0),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(
                sp.Piecewise(
                    (h * x / (L / 3), x <= L / 3),
                    (h * (L - x) / (2 * L / 3), x <= L),
                )
            ),
            Velocity_Condition(0),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(
                sp.Piecewise(
                    (k * x**2, x <= L / 2),
                    (k * (L - x) ** 2, x <= L),
                )
            ),
            Velocity_Condition(0),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(sp.Function("f")(x)),
            Velocity_Condition(0),
        ],
    ),
    (
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Displacement_Condition(0),
            Velocity_Condition(sp.Function("g")(x)),
        ],
    ),
]

questions_heat = [
    [
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Temperature_Condition(sp.sin(sp.pi * x / L)),
        ],
    ],
    [
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Temperature_Condition(sp.sin(sp.pi * x / L) + sp.sin(5 * sp.pi * x / L)),
        ],
    ],
    [
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Temperature_Condition(50),
        ],
    ],
    [
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Temperature_Condition(50 * sp.sin(sp.pi * x / 100)),
        ],
    ],
    [
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Temperature_Condition(x * (L - x)),
        ],
    ],
    [
        [
            Boundary_Condition(0, 0),
            Boundary_Condition(L, 0),
        ],
        [
            Temperature_Condition(
                sp.Piecewise(
                    (x, x < L / 2),
                    (L - x, x >= L / 2),
                )
            ),
        ],
    ],
]

questions_laplace = [
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", 8, 0),
            Laplace_Boundary_Condition("y", 0, 100 * sp.sin(sp.pi * x / 8)),
        ],
        8,
        sp.oo,
    ),
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", sp.pi, 0),
            Laplace_Boundary_Condition("y", 0, sp.sin(x) ** 2),
        ],
        sp.pi,
        sp.oo,
    ),
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", 10, 0),
            Laplace_Boundary_Condition(
                "y", 0, sp.Piecewise((20 * x, x <= 5), (20 * (10 - x), x <= 10))
            ),
        ],
        10,
        sp.oo,
    ),
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", sp.pi, 0),
            Laplace_Boundary_Condition("y", 0, x**2),
        ],
        sp.pi,
        sp.oo,
    ),
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", 10, 0),
            Laplace_Boundary_Condition("y", 0, x * (10 - x)),
        ],
        10,
        sp.oo,
    ),
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", 10, 0),
            Laplace_Boundary_Condition("y", 5, 50),
        ],
        10,
        5,
    ),
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", 10, 0),
            Laplace_Boundary_Condition("y", 0, 0),
            Laplace_Boundary_Condition("y", 5, 100),
        ],
        10,
        5,
    ),
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", sp.pi, 0),
            Laplace_Boundary_Condition("y", 0, sp.sin(x)),
            Laplace_Boundary_Condition("y", sp.pi, 0),
        ],
        sp.pi,
        sp.pi,
    ),
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", 10, 0),
            Laplace_Boundary_Condition("y", 0, x),
            Laplace_Boundary_Condition("y", 5, 0),
        ],
        10,
        5,
    ),
    (
        [
            Laplace_Boundary_Condition("x", 0, 0),
            Laplace_Boundary_Condition("x", 20, 0),
            Laplace_Boundary_Condition("y", 10, 20 * x - x**2),
            Laplace_Boundary_Condition("y", 0, 0),
        ],
        20,
        10,
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


@pytest.mark.parametrize("boundary_conditions, L, H", questions_laplace)
def test_laplace_equation(boundary_conditions, L, H):
    laplace = Laplace_Equation(
        boundary_conditions=boundary_conditions,
        L=L,
        H=H,
    )

    laplace.solve()

    u = laplace.solution
    u_yy = sp.diff(u, y, 2)
    u_xx = sp.diff(u, x, 2)

    assert sp.simplify(u_xx + u_yy) == 0 and u_yy != 0 and u_xx != 0


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
