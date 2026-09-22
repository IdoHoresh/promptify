# promptify rules for Opus 4.8

Source: Anthropic's *Prompting Claude Opus 4.8* guide (read September 2026); 4.8 runs well on
Opus 4.7 prompts. Behaviorally it sits closer to Sonnet 5 than to Opus 5 — literal,
effort-strict, conservative about tools and subagents — so the first bullet reuses Sonnet 5
material (in `sonnet-5.md`), and Opus 5's "constrain delegation" and "set narration
cadence" bullets must NOT be carried over.

- **Reuse three Sonnet 5 bullets (in `sonnet-5.md`) as written:** the think-this-through nudge when effort must
  stay `low`/`medium` (4.8's own wording: "This task involves multistep reasoning. Think
  carefully through the problem before responding." — but raise effort first; Anthropic's
  starting point for coding and agentic work on 4.8 is `xhigh`, minimum `high` for anything
  intelligence-sensitive); strip progress-update scaffolding (4.8 already gives regular,
  high-quality updates — if miscalibrated, describe the shape and give an example); and state
  tone only when the task needs a voice other than the default (4.8's baseline is direct and
  opinionated, minimal validation, sparing emoji; for warmer: "Use a warm, collaborative tone.
  Acknowledge the user's framing before answering.").
- **State length only when overriding its default — and show, don't forbid.** 4.8 calibrates
  length to how complex it judges the task: short on lookups, long on open-ended analysis. If
  the draft wants shorter, add "Provide concise, focused responses. Skip non-essential
  context, and keep examples minimal." For a recurring pattern like over-explaining, a
  positive example of the wanted concision beats telling it what not to do.
- **Name a tool, and why, when the task depends on one.** 4.8 favors reasoning over tool
  calls — usually better, but it under-triggers search and retrieval in knowledge work.
  Effort is the first lever (`high`/`xhigh` show substantially more tool use); if a tool the
  task depends on is still skipped, describe clearly why and how to use it.
- **Scope explicitly — it won't generalize for you.** 4.8 reads instructions literally,
  especially at lower effort: it neither extends an instruction from one item to the next nor
  infers requests you didn't make. The universal scope bullet is load-bearing here ("apply
  this to every section, not just the first one").
- **Say when to fan out — the inverse of Opus 5.** 4.8 spawns fewer subagents by default. For
  a wide, parallelizable task say: "Spawn multiple subagents in the same turn when fanning out
  across items or reading multiple files; don't spawn one for work you can complete directly
  in a single response."
- **Design/frontend: a concrete visual spec, or directions first.** 4.8 has a persistent
  house style (warm cream ~#F4F1EA, serif display type, italic word-accents, terracotta/amber)
  that suits editorial and hospitality briefs and reads wrong for dashboards, dev tools,
  fintech, healthcare, and enterprise UI. Generic negations ("don't use cream," "clean and
  minimal") only move it to another fixed palette. Either (1) specify the alternative
  concretely — palette hexes, type family, radii, spacing, section order — or (2) say "before
  building, propose 4 distinct visual directions (bg hex / accent hex / typeface — one-line
  rationale), ask me to pick one, then implement only that" — this replaces `temperature` as
  the variety lever. 4.8 needs less anti-"AI slop" prompting than earlier models: the short
  `<frontend_aesthetics>` snippet (no Inter/Roboto/Arial/system fonts, no purple-gradient
  clichés, no cookie-cutter layouts; unique fonts, cohesive themes, micro-interactions)
  suffices; the long frontend-design skill prompt was written for earlier models.
- **Front-load the whole spec in interactive coding.** 4.8 reasons more after each user turn
  in interactive sessions, so ambiguity dribbled across turns costs tokens and performance —
  the universal "full spec up front" bullet matters most on this model.
- **Code review: coverage language plus per-finding confidence and severity.** 4.8 finds more
  bugs than prior models but follows "only high-severity" or "don't nitpick" more faithfully,
  so it investigates as deeply and reports less. Use the universal coverage rephrase and add
  "include your confidence and an estimated severity for each finding so a downstream filter
  can rank them." The universal bullet's concrete-bar phrasing is the alternative when
  one-pass self-filtering is wanted.

Deliberately not touched, because they're session, API, or harness settings rather than something a task-level rewrite fixes: effort-level tuning and `thinking:
adaptive` (off by default on 4.8 — API/session settings), the thinking-trigger steering line
and the 64k `max_tokens` note at `xhigh`/`max` (API-level), the "auto mode" harness setting,
and computer-use toolsets and screenshot resolution (harness capability).
