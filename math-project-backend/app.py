from flask import Flask, session, jsonify, request
from flask_cors import CORS
from FourierSolverAndVisualizer import *
import secrets
import os
import sympy as sp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(16))
CORS(app, origins=["http://localhost:5173"])


@app.route("/solve_wave", methods=["POST"])
def solve_wave():
    body = request.get_json()
    session["left_boundary"] = body.get("left_boundary")
    session["right_boundary"] = body.get("right_boundary")
    session["displacement"] = body.get("displacement")
    session["velocity"] = body.get("velocity")
    try:
        session["wave"] = Wave_Equation(
            boundary_conditions=[
                Boundary_Condition(0, generate_condition(session["left_boundary"])),
                Boundary_Condition(L, generate_condition(session["right_boundary"])),
            ],
            initial_conditions=[
                Displacement_Condition(generate_condition(session["displacement"])),
                Velocity_Condition(generate_condition(session["velocity"])),
            ],
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
    # try:
    session["heat"] = Heat_Equation(
        boundary_conditions=[
            Boundary_Condition(0, generate_condition(session["left_boundary"])),
            Boundary_Condition(L, generate_condition(session["right_boundary"])),
        ],
        initial_conditions=[
            Temperature_Condition(generate_condition(session["temperature"])),
        ],
    ).solve()
    # except (ValueError, AttributeError):
    #     session["heat"] = r"\text{Unable to solve this equation.}"
    return jsonify(session["heat"])
