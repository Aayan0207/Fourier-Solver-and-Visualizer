import {
  ComputeEngine,
  PythonTarget,
  compile,
} from "@cortex-js/compute-engine";
const engine = new ComputeEngine();
engine._registerCompilationTarget(
  "python",
  new PythonTarget({ includeImports: false }),
);

function getExpression(value) {
  if (!value) {
    return 0;
  }
  const expr = engine.parse(value);
  if (expr.has("Which")) {
    const val = expr.toString();
    return val;
  }
  const result = compile(expr, { to: "python" });
  return result.code;
}

export default getExpression;
