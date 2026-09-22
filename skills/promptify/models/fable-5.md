# promptify rules for Fable 5

- **Flag refusal risk on cybersecurity or life-sciences work.** If the draft touches exploit
  development, malware, attack tooling, lab methods, or molecular mechanisms — even benign,
  authorized work in those areas — say so before running it: Fable 5 runs dedicated safety
  classifiers here and can decline what Sonnet 5 or Opus 4.8 would handle normally (Opus 5 and
  Opus 5.5 run classifiers too). Categories: `cyber`, `bio`, `frontier_llm` (work that could
  help build competing AI models), `general_harms`, and `reasoning_extraction`. **In Claude
  Code a refusal is usually invisible:** `switchModelsOnFlag` defaults to `true`, so a flagged
  request switches to the fallback model and continues rather than surfacing
  `stop_reason: "refusal"`. If the answer to a flagged-domain task matters, say which model
  produced it, and know that an unexplained shift in style or capability mid-task may be that
  switch rather than the model you asked for.
- **Don't ask it to reproduce its internal reasoning in the response** ("explain your
  reasoning," "show your thinking"). That phrasing risks a `reasoning_extraction` refusal. If
  reasoning visibility is actually needed, ask for a plain restatement of conclusions and the
  evidence behind them, not a transcript of the thinking process; a reason-then-answer grader
  structure is not what the category names, but it is redundant because Fable always thinks.
- **State "assessment only" explicitly when the draft is a question, not a change request.**
  Fable 5 can occasionally take unrequested action (applying a fix, creating a backup branch)
  when the user was actually just asking or thinking out loud. If the draft is exploratory, say
  "report findings, don't apply a fix" rather than leaving it to be inferred. Pair it with the
  evidence check when the task can change system state: "before running a command that
  restarts, deletes, or edits config, confirm the evidence supports that specific action — a
  signal that pattern-matches a known failure may have a different cause."
- **Add "when you have enough information to act, act" on ambiguous tasks.** Fable 5 can
  overplan — re-deriving established facts, re-litigating settled decisions, narrating options
  it won't pursue. One line telling it to act on sufficient information closes that.
- **Pin scope at higher effort: no unrequested refactors.** At high effort Fable 5 can tidy
  beyond the ask. Say: "don't add features, refactor, or introduce abstractions beyond what
  the task requires; no error handling for scenarios that can't happen — the simplest thing
  that works." Pick one scope guard per rewrite — this, the universal scope bullet, or
  "assessment only," whichever fits the draft — don't stack all three.
- **Lean into parallel subagent delegation for genuinely independent work** — the opposite
  instinct from Opus 5. Parallel subagents are dependable on Fable 5, so prior-model
  guardrails suppressing delegation don't apply; for a wide, parallelizable task, explicitly
  say to delegate and keep working async rather than blocking on each one.
- **Add periodic subagent-based self-verification on long-running tasks.** This is the one
  place this command adds verification instead of removing it: for a task that will run long
  and autonomous, say "check your own work against the spec at regular intervals using a fresh
  subagent" — fresh-context verification outperforms self-critique on Fable 5's long runs.
- **State the pause boundary for unattended, multi-hour work.** If the task is meant to run
  without you watching, say so explicitly ("you won't be available to answer mid-task, proceed
  on reversible actions without asking") — otherwise Fable 5 can pause to ask permission it
  doesn't need, stalling an unattended run.
- **Context-countdown reassurance, only if the harness shows one.** Fable 5 can offer to hand
  off, summarize, or trim its work when it sees a remaining-token countdown. Claude Code
  compacts instead and says so, so skip this there; where a raw countdown is shown, add the
  guide's line: "You have ample context remaining. Do not stop, summarize, or suggest a new
  session on account of context limits. Continue the work."
- **Ask for a lessons file on multi-session work.** If the task will span more than this
  session, ask it to record corrections and confirmed approaches to a plain note file as it
  goes — distinct from Claude Code's own cross-session memory, this is a scratch file scoped to
  one task's long run.
- **Ground progress claims against tool results on long runs.** Fable 5 can report status it
  hasn't verified. For any long or unattended run, say: "before reporting progress, audit each
  claim against a tool result from this session; report only what you can point to evidence for,
  and say so explicitly when something is unverified."
- **Ask for lead-with-outcome output.** Un-steered at higher effort, Fable 5 elaborates beyond
  need — alternatives not chosen, heavy structure. Say: "first sentence answers what happened
  or what you found; keep it short by dropping details that don't change what the reader does
  next, not by compressing into fragments or jargon." Skip if the session's output style
  already sets response shape.
- **On long runs, ask for a re-grounding final summary.** Deep into a session Fable 5's text
  can go dense — arrow chains, invented labels, references to thinking the reader never saw.
  Say the final message is for someone who watched none of it: complete sentences, terms
  spelled out, working shorthand left behind. Skip if the output style already covers it.
- **Ask for iterative visual verification and document/style specs.** If the task analyzes or
  replicates an image, UI, chart, or diagram and a crop or screenshot tool is available, tell it
  to zoom in and verify rather than reason from a single look. If it produces a spreadsheet,
  slide deck, or formatted document, state the format, template, or style constraints
  explicitly rather than leaving them to be inferred.

Deliberately not touched, because they're session, API, or harness settings rather than something a task-level rewrite fixes: effort-level tuning, the API-only thinking
parameters (adaptive-only, summarized thinking output, no budget_tokens), and the `send_to_user`
tool pattern (a client-side tool for custom integrations — not something exposed in a Claude
Code slash command). Also not touched: one-time meta-advice about auditing which older-model
instructions and skills to prune when adopting Fable 5 — that's a standing-config review, not
something a single task-level rewrite fixes.
