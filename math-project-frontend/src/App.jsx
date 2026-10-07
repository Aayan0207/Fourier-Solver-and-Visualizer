import { useState } from "react";
import "./App.css";
import ModeButton from "./components/ModeButton";
import WaveEquation from "./components/WaveEquation";
import HeatEquation from "./components/HeatEquation";
import LaplaceEquation from "./components/LaplaceEquation";
function App() {
  const [page, setPage] = useState("wave");
  const pages = {
    wave: () => {
      return <WaveEquation />;
    },
    heat: () => {
      return <HeatEquation />;
    },
    laplace: () => {
      return <LaplaceEquation />;
    },
  };
  return (
    <>
      <h1 id="project_title">PDE Lab</h1>
      <div className="mode_buttons">
        <ModeButton
          name="Wave Equation (1-D)"
          key="wave"
          onClick={() => setPage("wave")}
          value={
            "\\frac{\\partial^2 u}{\\partial t^2} = c^2\\frac{\\partial^2 u}{\\partial x^2}"
          }
        ></ModeButton>
        <ModeButton
          name="Heat Equation (1-D)"
          key="heat"
          onClick={() => setPage("heat")}
          value={
            "\\frac{\\partial u}{\\partial t} = c^2\\frac{\\partial^2 u}{\\partial x^2}"
          }
        ></ModeButton>
        <ModeButton
          name="Laplace Equation"
          key="laplace"
          onClick={() => setPage("laplace")}
          value={
            "\\frac{\\partial^2 u}{\\partial x^2} + \\frac{\\partial^2 u}{\\partial y^2} = 0"
          }
        ></ModeButton>
      </div>
      <div className="page">{pages[page]?.()}</div>
    </>
  );
}

export default App;
