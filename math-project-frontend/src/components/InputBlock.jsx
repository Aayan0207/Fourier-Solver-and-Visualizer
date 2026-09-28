import "mathlive";
function InputBlock({ value, setValue }) {
  return (
    <div className="input_block">
      <math-field
        onChange={(e) => setValue(e.target.value)}
        value={value}
      ></math-field>
    </div>
  );
}

export default InputBlock;
