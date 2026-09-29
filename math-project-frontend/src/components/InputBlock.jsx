import "mathlive";
import { useState } from "react";
import Piecewise from "./PiecewiseBlock";
function InputBlock({ value, setValue }) {
  const [piecewise, setPiecewise] = useState(false);
  return (
    <div className="input_block">
      <math-field
        onChange={(e) => setValue(e.target.value)}
        value={value}
      ></math-field>
      <button onClick={() => setPiecewise((prev) => !prev)}>
        Piecewise Input
      </button>
      {piecewise ? <Piecewise setter = {setValue}/> : ""}
    </div>
  );
}

export default InputBlock;
