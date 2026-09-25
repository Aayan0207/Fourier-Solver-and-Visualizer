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
  console.log(page)
  return (
    <>
      <ModeButton
        name="Wave Equation Solver"
        onClick={() => setPage("wave")}
      ></ModeButton>
      <ModeButton
        name="Heat Equation Solver"
        onClick={() => setPage("heat")}
      ></ModeButton>
      <ModeButton
        name="Laplace Equation Solver"
        onClick={() => setPage("laplace")}
      ></ModeButton>
      <div className="page">
        {pages[page]?.()}
      </div>
    </>
  );
}

export default App;
