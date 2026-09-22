# promptify rules for Opus 5

- **Constrain subagent delegation explicitly** when the task is a small, single-track job (a
  handful of tool calls). Opus 5 delegates to subagents more readily than the task size
  justifies; state that direct work is fine here rather than leaving it to default, and that
  subagents aren't for verifying or double-checking its own work.
- **State length explicitly when this one answer should be short.** Opus 5's default responses
  run long, and effort doesn't control length — only an explicit instruction does. If the draft
  is a question or explanation that wants a brief answer, say so in the rewrite: "answer in
  N sentences" or "give a high-level summary, not an in-depth one."
- **Specify style or template for office/document output.** If the ask is to produce a
  spreadsheet, slide deck, or formatted document, state the format, template, or style
  constraints explicitly — Opus 5 needs them stated rather than inferred.
- **Ask for iterative visual verification on vision-heavy tasks.** If the task involves
  analyzing or replicating an image, UI, chart, or diagram, and a crop/screenshot tool is
  available, tell it to use the tool to zoom in and verify rather than reasoning from a single
  look — this outperforms reasoning alone on Opus 5.
- **Set the narration cadence on long agentic runs.** Opus 5 narrates what it is about to do,
  and its per-message output during agentic work runs longer than prior models'. It responds
  better to guidance on *how* to communicate than on *how much*, so say what earns an update:
  "one line before the first tool call, then updates only when you find something load-bearing
  or change direction — save the rest for the final summary." Skip this when the session's
  output-style config already sets a cadence, and never carry it over to Sonnet 5 (see `sonnet-5.md`).
- **Add explicit length calibration when writing a deliverable file** (a report, a doc, a
  summary saved to disk). Say "cover the substance, don't pad with filler sections or
  boilerplate" — Opus 5's written files run long by default the same way its chat responses do.

Deliberately not touched by this command, because they're session-level settings or already
governed by standing config rather than something a task-level rewrite fixes: effort-level
tuning, self-correction narration, and thinking-disabled artifacts (only relevant in sessions
that run with thinking disabled).
