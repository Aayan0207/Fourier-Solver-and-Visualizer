import "katex/dist/katex.min.css";
import { BlockMath } from "react-katex";
function OutputBlock({ value }) {
  return (
    <div className="output_block">
      <BlockMath math={value} />
    </div>
  );
}

export default OutputBlock;
