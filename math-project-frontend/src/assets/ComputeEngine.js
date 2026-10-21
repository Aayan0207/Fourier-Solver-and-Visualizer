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
const variables = ["x", "t", "y", "c", "L", "l", "p", "h", "k", "b", "a","m","n"];
for (const variable of variables) {
  engine.declare(variable, "real");
}

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
