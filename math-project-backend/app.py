from flask import Flask, session, jsonify, request
from flask_cors import CORS
from FourierSolverAndVisualizer import *
import secrets
import os
import sympy as sp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(16))
CORS(app, origins=["https://pdelab.vercel.app"])


@app.route("/solve_wave", methods=["POST"])
def solve_wave():
    body = request.get_json()
    session["left_boundary"] = body.get("left_boundary")
    session["right_boundary"] = body.get("right_boundary")
    session["displacement"] = body.get("displacement")
    session["velocity"] = body.get("velocity")
    session["upper"] = body.get("upper")
    try:
        session["wave"] = Wave_Equation(
            boundary_conditions=[
                Boundary_Condition(0, generate_condition(session["left_boundary"])),
                Boundary_Condition(
                    generate_condition(session["upper"]),
                    generate_condition(session["right_boundary"]),
                ),
            ],
            initial_conditions=[
                Displacement_Condition(generate_condition(session["displacement"])),
                Velocity_Condition(generate_condition(session["velocity"])),
            ],
            upper=generate_condition(session["upper"]),
        ).solve()
    except (ValueError, AttributeError):
        session["wave"] = r"\text{Unable to solve this equation.}"
    return jsonify(session["wave"])


@app.route("/solve_heat", methods=["POST"])
def solve_heat():
    body = request.get_json()
    session["left_boundary"] = body.get("left_boundary")
    session["right_boundary"] = body.get("right_boundary")
    session["temperature"] = body.get("temperature")
    session["upper"] = body.get("upper")
    try:
        session["heat"] = Heat_Equation(
            boundary_conditions=[
                Boundary_Condition(0, generate_condition(session["left_boundary"])),
                Boundary_Condition(
                    generate_condition(session["upper"]),
                    generate_condition(session["right_boundary"]),
                ),
            ],
            initial_conditions=[
                Temperature_Condition(generate_condition(session["temperature"])),
            ],
            upper=(generate_condition(session["upper"])),
        ).solve()
    except (ValueError, AttributeError):
        session["heat"] = r"\text{Unable to solve this equation.}"
    return jsonify(session["heat"])


@app.route("/solve_laplace", methods=["POST"])
def solve_laplace():
    body = request.get_json()
    session["left_boundary"] = body.get("left_boundary")
    session["right_boundary"] = body.get("right_boundary")
    session["bottom_boundary"] = body.get("bottom_boundary")
    session["top_boundary"] = body.get("top_boundary")
    session["upper"] = body.get("upper")
    session["right"] = body.get("right")
    try:
        session["laplace"] = Laplace_Equation(
            boundary_conditions=[
                Laplace_Boundary_Condition(
                    "x", 0, generate_condition(session["left_boundary"])
                ),
                Laplace_Boundary_Condition(
                    "x",
                    generate_condition(session["right"]),
                    generate_condition(session["right_boundary"]),
                ),
                Laplace_Boundary_Condition(
                    "y", 0, generate_condition(session["bottom_boundary"])
                ),
                Laplace_Boundary_Condition(
                    "y",
                    generate_condition(session["upper"]),
                    generate_condition(session["top_boundary"]),
                ),
            ],
            H=generate_condition(session["upper"]),
            L=generate_condition(session["right"]),
        ).solve()
    except (ValueError, AttributeError):
        session["laplace"] = r"\text{Unable to solve this equation.}"
    return jsonify(session["laplace"])
