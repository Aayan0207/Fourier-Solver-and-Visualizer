import "mathlive";
import { useState, useEffect, useRef } from "react";
import Piecewise from "./PiecewiseBlock";
function InputBlock({ value, setValue }) {
  const [piecewise, setPiecewise] = useState(false);
  const mfRef = useRef(null);

  useEffect(() => {
    if (mfRef.current) {
      mfRef.current.mathVirtualKeyboardPolicy = "manual";
    }
    window.mathVirtualKeyboard.layouts = [
      "alphabetic",
      "numeric",
      "symbols",
      "greek",
    ];
  }, []);

  useEffect(() => {
    if (!piecewise) {
      setValue(0);
    }
  }, [piecewise, setValue]);

  function handleFocus() {
    if (window.matchMedia("(pointer: coarse)").matches) {
      window.mathVirtualKeyboard.show();
    }
  }

  return (
    <div
      className="input_block"
      onBlur={() => {
        window.mathVirtualKeyboard.hide();
      }}
    >
      <math-field
        onChange={(e) => setValue(e.target.value)}
        value={value}
        ref={mfRef}
        onFocus={handleFocus}
      ></math-field>
      <button
        onClick={() => setPiecewise((prev) => !prev)}
        className="piecewise_input_button"
      >
        Piecewise Input
      </button>
      {piecewise ? <Piecewise setter={setValue} /> : ""}
    </div>
  );
}

export default InputBlock;
