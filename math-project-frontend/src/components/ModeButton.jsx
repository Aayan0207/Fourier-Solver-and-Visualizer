import react from "react";

function ModeButton({ name, onClick }) {
  return (
    <>
      <div className="mode_button" onClick={onClick}>
        {name}
      </div>
    </>
  );
}

export default ModeButton;
