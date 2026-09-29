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
    session["left_boundary"] = (
        body.get("left_boundary") if body.get("left_boundary") else 0
    )
    session["right_boundary"] = (
        body.get("right_boundary") if body.get("right_boundary") else 0
    )
    session["displacement"] = (
        body.get("displacement") if body.get("displacement") else 0
    )
    if session["displacement"] and session["displacement"].startswith("Which"):
        session["displacement"] = create_piecewise(session["displacement"])
    session["velocity"] = body.get("velocity") if body.get("velocity") else 0
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
