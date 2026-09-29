import { BlockMath } from "react-katex";

function Condition({ left }) {
  return (
    <div className="condition_block">
      <BlockMath>{left + "="}</BlockMath>
    </div>
  );
}

export default Condition;
