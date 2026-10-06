import { useMemo } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";

const KATEX_OPTIONS = {
  displayMode: true,
  throwOnError: false,
  macros: { "\\arraystretch": "1.6" },
};

function OutputBlock({ value }) {
  const html = useMemo(
    () => katex.renderToString(value, KATEX_OPTIONS),
    [value],
  );
  return (
    <div className="output_block">
      {!value.includes("Unable") ? <h3>Solution: </h3> : ""}
      <div className="output_math" dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
}

export default OutputBlock;
