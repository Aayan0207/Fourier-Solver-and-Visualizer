import { useState } from "react";
import Condition from "./Conditon";
import OutputBlock from "./OutputBlock";
import InputBlock from "./InputBlock";
import getExpression from "../assets/ComputeEngine";
import InputBlockRegular from "./InputBlockRegular";
import Spinner from "./Spinner";

function WaveEquation() {
  const [boundary_0, setBoundary_0] = useState(0);
  const [boundary_L, setBoundary_L] = useState(0);
  const [displacement, setDisplacement] = useState(0);
  const [velocity, setVelocity] = useState(0);
  const [upper, setUpper] = useState("L");
  const [answer, setAnswer] = useState(null);
  const [showSpinner, setShowSpinner] = useState(false);
  function solveWave() {
    setAnswer(null);
    setShowSpinner(true);
    fetch("http://127.0.0.1:5000/solve_wave", {
      method: "POST",
      body: JSON.stringify({
        left_boundary: getExpression(boundary_0),
        right_boundary: getExpression(boundary_L),
        displacement: getExpression(displacement),
        velocity: getExpression(velocity),
        upper: getExpression(upper),
      }),
      headers: {
        "content-type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setTimeout(() => {
          setShowSpinner(false);
          setAnswer(data);
        }, 500);
      })
      .catch((e) => {
        console.log(e);
      });
  }
  return (
    <>
      <div className="wave_conditions">
        <h3>Wave Equation</h3>
        <Condition left="L"></Condition>
        <InputBlockRegular value={upper} setValue={setUpper} />
        <Condition left="u(0,t)"></Condition>
        <InputBlock value={boundary_0} setValue={setBoundary_0} />
        <Condition left="u(L,t)"></Condition>
        <InputBlock value={boundary_L} setValue={setBoundary_L} />
        <Condition left="u(x,0)"></Condition>
        <InputBlock value={displacement} setValue={setDisplacement} />
        <Condition left="u_t(x,0)"></Condition>
        <InputBlock value={velocity} setValue={setVelocity} />
        <button
          className="solve_button"
          id="wave_solve"
          onClick={() => solveWave()}
        >
          Solve
        </button>
        {showSpinner ? <Spinner /> : ""}
        {answer != null ? <OutputBlock value={answer} /> : ""}
      </div>
    </>
  );
}

export default WaveEquation;
