import "mathlive";
import { useEffect, useRef } from "react";
function InputBlockRegular({ value, setValue }) {
  const mfRef = useRef(null);

  useEffect(() => {
    if (mfRef.current) {
      mfRef.current.mathVirtualKeyboardPolicy = "hide";
    }
  }, []);

  return (
    <div
      className="input_block input_block_regular"
      onBlur={() => {
        window.mathVirtualKeyboard.hide();
      }}
    >
      <math-field
        onChange={(e) => setValue(e.target.value)}
        value={value}
        ref={mfRef}
      ></math-field>
    </div>
  );
}

export default InputBlockRegular;
