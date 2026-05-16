import test from "node:test";
import assert from "node:assert/strict";

import { buildResultViewModel, formatConfidencePercent } from "./app.mjs";

test("formatConfidencePercent converts decimal confidence to percentage", () => {
  assert.equal(formatConfidencePercent(0.928), 93);
});

test("buildResultViewModel maps backend response into UI friendly fields", () => {
  const viewModel = buildResultViewModel({
    filename: "sample.jpg",
    prediction: {
      label: "bawang putih",
      confidence: 0.928083,
    },
    recommendation: {
      text: "Bawang putih cocok untuk tumisan dan sup.",
      source: "gemini",
    },
  });

  assert.equal(viewModel.label, "bawang putih");
  assert.equal(viewModel.confidencePercent, 93);
  assert.equal(viewModel.recommendationSourceLabel, "Gemini AI");
  assert.match(viewModel.summary, /bawang putih/i);
});
