import { useEffect, useState } from "react";

function Piecewise({ setter }) {
  const [cases, setCases] = useState(2);
  const block = "▢ & ▢ \\\\";
  const latex = `\\begin{cases} ${block.repeat(cases)} \\end{cases}`;
  useEffect(() => {
    setter(latex);
  }, [latex, setter]);
  return (
    <div className="piecewise_block">
      <p>Number of cases: </p>
      <input
        type="number"
        value={cases}
        onChange={(e) => setCases(e.target.value)}
      />
    </div>
  );
}

export default Piecewise;
