import { BlockMath } from "react-katex";

function ModeButton({ name, onClick, value }) {
  return (
    <>
      <div className="mode_button" onClick={onClick}>
        {name}
        <BlockMath math={value} />
      </div>
    </>
  );
}

export default ModeButton;
