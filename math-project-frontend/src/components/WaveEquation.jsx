import { useState } from "react";
import Condition from "./Conditon";

function WaveEquation() {
  const [boundary_0, setBoundary_0] = useState(0);
  return (
    <>
      <div className="wave_conditions">
        <Condition left="u(0,t)"></Condition>
        <input type = "text" className="condition_input" placeholder="Boundary condition at left margin"/>
        <Condition left="u(L,t)"></Condition>
        <input type = "text" className="condition_input" placeholder="Boundary Condition at right margin"/>
        <Condition left="u(x,0)"></Condition>
        <input type = "text" className="condition_input" placeholder="Initial Displacement Condition"/>
        <Condition left="u_t(x,0)"></Condition>
        <input type = "text" className="condition_input" placeholder="Initial Velocity Condition"/>
      </div>
    </>
  );
}

export default WaveEquation;
