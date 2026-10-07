import "mathlive";
import { useEffect, useRef } from "react";
function InputBlockRegular({ value, setValue }) {
  const mfRef = useRef(null);

  useEffect(() => {
    if (mfRef.current) {
      mfRef.current.mathVirtualKeyboardPolicy = "manual";
    }
    window.mathVirtualKeyboard.layouts = ["alphabetic", "numeric", "greek"];
  }, []);

  function handleBlur() {
    window.mathVirtualKeyboard.hide();
  }

  function handleFocus() {
    if (window.matchMedia("(pointer: coarse)").matches) {
      window.mathVirtualKeyboard.show();
    }
  }

  return (
    <div className="input_block input_block_regular" onBlur={handleBlur}>
      <math-field
        onChange={(e) => setValue(e.target.value)}
        onFocus={handleFocus}
        value={value}
        ref={mfRef}
      ></math-field>
    </div>
  );
}

export default InputBlockRegular;
