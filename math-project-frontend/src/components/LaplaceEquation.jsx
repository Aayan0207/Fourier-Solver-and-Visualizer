import { useState } from "react";
import getExpression from "../assets/ComputeEngine";
import Condition from "./Conditon";
import InputBlock from "./InputBlock";
import OutputBlock from "./OutputBlock";
import Spinner from "./Spinner";
import InputBlockRegular from "./InputBlockRegular";
import { BlockMath } from "react-katex";

function LaplaceEquation() {
  const [leftBoundary, setLeftBoundary] = useState(0);
  const [rightBoundary, setRightBoundary] = useState(0);
  const [bottomBoundary, setBottomBoundary] = useState(0);
  const [topBoundary, setTopBoundary] = useState(0);
  const [upper, setUpper] = useState("H");
  const [right, setRight] = useState("L");
  const [answer, setAnswer] = useState(null);
  const [showSpinner, setShowSpinner] = useState(false);
  function solveLaplace() {
    setAnswer(null);
    setShowSpinner(true);
    fetch("https://pdelab-api.vercel.app/solve_laplace", {
      method: "POST",
      body: JSON.stringify({
        left_boundary: getExpression(leftBoundary),
        right_boundary: getExpression(rightBoundary),
        top_boundary: getExpression(topBoundary),
        bottom_boundary: getExpression(bottomBoundary),
        upper: getExpression(upper),
        right: getExpression(right),
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
      <div className="laplace_conditions">
        <h3>Laplace Equation</h3>
        <div className="regular_conditions_container">
          <Condition left="L"></Condition>
          <InputBlockRegular value={right} setValue={setRight} />
          <Condition left="H"></Condition>
          <InputBlockRegular value={upper} setValue={setUpper} />
          <button
            className="infinity_button"
            onClick={() => {
              setUpper((prev) => {
                if (prev !== "\\infty") {
                  return "\\infty";
                }
                return "H";
              });
            }}
          >
            <BlockMath>{"\\infty"}</BlockMath>
          </button>
        </div>
        <Condition left="u(0,y)"></Condition>
        <InputBlock value={leftBoundary} setValue={setLeftBoundary} />
        <Condition left="u(L,y)"></Condition>
        <InputBlock value={rightBoundary} setValue={setRightBoundary} />
        <Condition left="u(x,0)"></Condition>
        <InputBlock value={bottomBoundary} setValue={setBottomBoundary} />
        <Condition left="u(x,H)"></Condition>
        <InputBlock value={topBoundary} setValue={setTopBoundary} />
        <button
          className="solve_button"
          id="laplace_solve"
          onClick={() => solveLaplace()}
        >
          Solve
        </button>
        {showSpinner ? <Spinner /> : ""}
        {answer != null ? <OutputBlock value={answer} /> : ""}
      </div>
    </>
  );
}

export default LaplaceEquation;
