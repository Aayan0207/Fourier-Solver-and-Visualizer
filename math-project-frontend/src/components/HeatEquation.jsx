import { useState } from "react";
import getExpression from "../assets/ComputeEngine";
import Condition from "./Conditon";
import InputBlock from "./InputBlock";
import OutputBlock from "./OutputBlock";

function HeatEquation() {
  const [boundary_0, setBoundary_0] = useState(0);
  const [boundary_L, setBoundary_L] = useState(0);
  const [temperature, setTemperature] = useState(0);
  const [answer, setAnswer] = useState(null);
  function solveHeat() {
    fetch("http://127.0.0.1:5000/solve_heat", {
      method: "POST",
      body: JSON.stringify({
        left_boundary: getExpression(boundary_0),
        right_boundary: getExpression(boundary_L),
        temperature: getExpression(temperature),
      }),
      headers: {
        "content-type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setAnswer(data);
      })
      .catch((e) => {
        console.log(e);
      });
  }
  return (
    <>
      <div className="heat_conditions">
        <h3>Heat Equation</h3>
        <Condition left="u(0,t)"></Condition>
        <InputBlock value={boundary_0} setValue={setBoundary_0} />
        <Condition left="u(L,t)"></Condition>
        <InputBlock value={boundary_L} setValue={setBoundary_L} />
        <Condition left="u(x,0)"></Condition>
        <InputBlock value={temperature} setValue={setTemperature} />
        <button
          className="solve_button"
          id="wave_solve"
          onClick={() => solveHeat()}
        >
          Solve
        </button>
        {answer != null ? <OutputBlock value={answer} /> : ""}
      </div>
    </>
  );
}

export default HeatEquation;
