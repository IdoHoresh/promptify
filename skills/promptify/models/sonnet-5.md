# promptify rules for Sonnet 5

- **Add a "think this through" nudge on genuinely multistep tasks** if effort is set to low or
  medium. Sonnet 5 scopes tightly to what's literally asked at those levels and can under-think
  a complex problem rather than expanding beyond the ask; a short line like "this involves
  multistep reasoning, think it through carefully" closes that gap. But state the better fix
  first: raising effort to `high`/`xhigh` beats prompting around low effort, so only reach for
  the nudge when latency forces effort to stay down.
- **State length explicitly only when you want shorter than the task's natural complexity
  suggests.** Sonnet 5 already scales response length to complexity by default, so this is a
  lighter touch than the Opus 5 version — only add it when overriding that default, not as a
  standing habit.
- **Name a tool only when it's observably going unused.** Sonnet 5 is more agentic than its
  predecessors by default; under-triggering is mainly a thinking-disabled artifact. Don't
  pre-name tools as a standing habit — but if the task depends on one that's
  being skipped (search never invoked, files never read), say when and why to use it.
- **State tone explicitly when this task needs a voice different from your default.** If the
  draft calls for a specific register (warmer, more formal, more terse) beyond your standing
  style config, say so for this task rather than assuming the baseline carries it.
- **Don't add progress-update scaffolding — remove it.** The inverse of the Opus 5 narration
  bullet: Sonnet 5 already gives well-calibrated updates through long agentic runs. Forced
  interim status ("summarize every 3 tool calls") is scaffolding to strip, not add. If the
  updates are miscalibrated, describe what they should look like instead of mandating a cadence.
- **Design/frontend: a concrete visual spec, or directions first** — the same rule promptify
  applies on Opus 4.8, and it does not depend on a design skill being installed. Sonnet 5 settles
  into a default house style on open-ended briefs, which reads wrong for dashboards, dev
  tools, fintech, healthcare, and enterprise UI, and generic negations ("don't use that
  color," "clean and minimal") only move it to another fixed palette. Either specify the
  alternative concretely — palette hexes, type family, radii, spacing, section order — or
  say "before building, propose 4 distinct visual directions (bg hex / accent hex / typeface
  — one-line rationale), ask me to pick one, then implement only that." Because `temperature`
  is rejected on Sonnet 5, the propose-first form is Anthropic's recommended way to get
  variety across runs. Add the short `<frontend_aesthetics>` snippet (no Inter/Roboto/Arial/
  system fonts, no purple-gradient clichés, no cookie-cutter layouts; unique fonts, cohesive
  themes, micro-interactions) to steer off the "AI slop" default. If a design skill *is*
  installed and enabled, invoke it instead of hand-rolling all of this.

Deliberately not touched, because they're session, API, or harness settings rather than something a task-level rewrite fixes: effort-level tuning, tool-triggering-with-
thinking-off (only relevant in sessions that run with thinking disabled), `temperature`/`top_p`/
`top_k` (API-only parameters, not prompt edits), the "auto mode" interactive-coding harness
setting (session-level, not a per-prompt edit), and computer-use tool resolution (a harness
capability, not something a prompt rewrite fixes).
