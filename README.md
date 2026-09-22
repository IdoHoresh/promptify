# promptify

Rewrite a rough prompt into a structure tuned for the Claude model actually running your
session — then run the improved version, in the same turn.

You type the lazy version; the command applies Anthropic-style prompt patterns (action verbs,
explicit scope, anchored references, success criteria, positive framing over prohibitions,
XML structure and long-context ordering when warranted) plus a block of model-specific
adjustments for the model you're on, shows you the rewrite in a fenced block, and executes it.

## Install

In Claude Code:

```
/plugin marketplace add IdoHoresh/promptify
/plugin install promptify@promptify
```

The `@promptify` suffix names the marketplace, not a version — it is required.

## Usage

```
/promptify fix the login thing its broken on mobile i think its the token
```

With no arguments it asks what you want promptified.

## What it adjusts per model

- **Opus 5** — constrains unneeded subagent delegation, sets explicit length and narration
  cadence, adds document/style specs and iterative visual verification where relevant.
- **Opus 5.5** — inherits the Opus 5 block, then: re-tests crop/zoom and cadence scaffolding
  instead of assuming it, removes prompts that make it reproduce its internal reasoning (the
  `reasoning_extraction` refusal) and chat-style "think carefully" lines, flags biology and
  high-risk cyber refusal risk, and adds the guide's verbatim four-early-stops paragraph for
  unattended runs, explore-first for multi-app tasks, a "time matters" line for fan-outs,
  pasted-text markers, and a named-patterns avoid list for frontend.
- **Opus 4.8** — closer to Sonnet 5 than Opus 5: reuses the think-through nudge, scaffolding
  strip, and tone bullets; adds explicit fan-out for parallel work (the inverse of Opus 5),
  tool-naming when a tool is skipped, a concrete visual spec or "propose directions first" for
  frontend work, and per-finding confidence/severity on code review.
- **Sonnet 5** — adds a think-it-through nudge on multistep work at low effort, strips
  progress-update scaffolding, defers design work to a design skill when one is installed.
- **Fable 5** — flags refusal-risk phrasing, pins scope, adds grounding and fresh-subagent
  self-verification on long runs, sets pause boundaries for unattended work.
- **Fable 5.1** — inherits the Fable 5 block, then: relaxes the refusal flag (fewer false
  positives; rewrites compile-check phrasing), adds the "check your last paragraph" finish rule
  and test-file scope guard, strips narration-suppressing and anti-formatting lines instead of
  adding them, adds mannered-prose and surgical-edit lines, a quoting `<example>` for
  summarize-sources tasks, and effort-conditional nudges for low-effort search and
  xhigh/max long outputs.
- **Mythos 5 / 5.1** — use the Fable 5 / Fable 5.1 blocks; Anthropic's Fable guides cover both.
- **Any other model** (Haiku, 4.x, or newer than this file) — applies only the universal
  block and says so, rather than guessing which per-model block fits.

## Calibration and staleness

The Opus 5, Sonnet 5, and Fable 5 heuristics are community-observed behaviors, calibrated
August 2026 against `claude-opus-5`, `claude-sonnet-5`, and `claude-fable-5`. The Fable 5.1
and Opus 5.5 deltas and the Opus 4.8 block come from Anthropic's published guides *Prompting
Claude Fable 5.1*, *Prompting Claude Opus 5.5*, and *Prompting Claude Opus 4.8* (all read
September 2026; `claude-fable-5-1`, `claude-opus-5-5`, `claude-opus-4-8`); Fable 5 and Opus 5
bullets the newer guides don't mention carry over to 5.1 and 5.5 unverified. Model updates
will invalidate some of these; treat the per-model blocks as dated observations, not
documentation.

## Cost

Invoke-only: nothing loads into standing context. Each invocation injects ~52KB (the full
instruction set) into that turn.

## Maintenance notes

Kept as a single file deliberately: it is an invoke-only command, so progressive disclosure's
standing-context rationale doesn't apply, and sub-file paths have broken across machines
before. Re-litigate only if this ever becomes auto-invoked or grows past readability.
Checked 2026-09-23 against the skill-authoring guidance (SKILL.md under 500 lines / ~5k
tokens): that budget targets auto-loaded skills, this file is invoke-only, and splitting it
would multiply the copies that must stay in sync, so the single file stands. No evals yet —
the docs suggest 3+ cases per model, including should-not-trigger ones.

In this plugin the instructions live in `skills/promptify/SKILL.md`, which the docs recommend
for new plugins over a flat `commands/` file. `disable-model-invocation: true` keeps it
invoke-only (`/promptify:promptify`). A personal copy at `~/.claude/commands/promptify.md`
(the plain `/promptify` command) has the same body under a shorter frontmatter. Edit the
body in one, carry it to the other, and diff the bodies (everything after the frontmatter)
to confirm.
