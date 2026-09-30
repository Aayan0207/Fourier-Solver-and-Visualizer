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
  console.log(page);
  return (
    <>
      <ModeButton
        name="Wave Equation (1-D)"
        onClick={() => setPage("wave")}
        value={
          "\\frac{\\partial^2 u}{\\partial t^2} = c^2\\frac{\\partial^2 u}{\\partial x^2}"
        }
      ></ModeButton>
      <ModeButton
        name="Heat Equation"
        onClick={() => setPage("heat")}
        value={
          "\\frac{\\partial u}{\\partial t} = c^2\\frac{\\partial^2 u}{\\partial x^2}"
        }
      ></ModeButton>
      <ModeButton
        name="Laplace Equation"
        onClick={() => setPage("laplace")}
        value={
          "\\frac{\\partial^2 u}{\\partial x^2} + \\frac{\\partial^2 u}{\\partial y^2} = 0"
        }
      ></ModeButton>
      <div className="page">{pages[page]?.()}</div>
    </>
  );
}

export default App;
