# promptify rules for Fable 5.1

Apply `fable-5.md` first; this file builds on it. Anthropic's published guidance (September 2026) is that
Fable 5 prompts perform well on 5.1 unchanged, with a handful of behavioral differences. Every
Fable 5 bullet not named below carries over as-is — unverified on 5.1, not re-checked. Where a
bullet below names a Fable 5 bullet, it replaces or extends that one.

Overrides of Fable 5 bullets:

- **Refusal risk (replaces "Flag refusal risk").** 5.1's classifiers produce fewer false
  positives than Fable 5's did at launch, and finding vulnerabilities in source code is
  permitted — still flag exploit/malware/attack-tooling and lab or molecular work before
  running, but don't warn on ordinary code security review. Three phrasings still trip false
  positives, and the rewrite should fix them in the draft: (1) compile-check phrasing — rewrite
  "does this compile without errors?" as "are there any bugs in this program?"; (2) a
  lesser-known programming language — add a line saying what the language is and how it works,
  or point at its documentation; (3) a tool that returns base64 into context — if the draft
  depends on one, say to strip the base64 from the tool output. A blocked request comes back
  as `stop_reason: "refusal"` — but **in Claude Code you usually won't see that**:
  `switchModelsOnFlag` defaults to `true`, so a flagged request quietly switches to the
  fallback model and continues. Treat an unexplained mid-task change in style or capability as
  a possible model switch, and name the producing model when a flagged-domain answer matters.
- **Pause boundary (extends "State the pause boundary").** 5.1 can end a turn by describing
  the next step ("Next, I'll …") or asking permission for a step the request already covered
  ("Shall I apply this?"). For unattended or long autonomous runs, add the guide's two blocks
  verbatim; if prompt length must stay short, the first alone keeps most of the effect. Its
  opening sentence carries much of that effect, so keep it as written, and immediately after
  it list any confirmations the harness still requires (Claude Code asks before hard-to-reverse
  or outward-facing actions) so the two rules don't collide. First block:
  "You are operating autonomously. The user is not watching in real time and cannot answer
  questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For
  reversible actions that follow from the original request, proceed without asking. Stop only
  for destructive actions or genuine scope changes the user must decide. Offering follow-ups
  after the task is done is fine; asking permission before doing the work is not.
  Exception: when the user is describing a problem, asking a question, or thinking out loud
  rather than requesting a change, the deliverable is your assessment. Report your findings
  and stop. Don't apply a fix until they ask for one.
  Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question,
  a list of next steps, or a promise about work you have not done ('I'll…', 'let me know
  when…'), do that work now with tool calls. That includes retrying after errors and gathering
  missing information yourself. Do not stop because the context or session is long. End your
  turn only when the task is complete or you are blocked on input only the user can provide.
  Before running a command that changes system state (such as restarts, deletes, or config
  edits), check that the evidence actually supports that specific action. A signal that
  pattern-matches to a known failure may have a different cause."
  Second block: "# Delivering work
  The user's request — or the plan they approved — sets the scope, and the scope is the
  deliverable: don't quietly narrow, widen, or swap it. Read ambiguity the way a careful
  colleague would: make routine judgment calls yourself, and check in only when different
  readings would lead to materially different work. If you see a real problem with the task as
  specified, say so in a sentence or two and keep building under stated assumptions; if the
  user hears the concern and reaffirms, that is their decision, so deliver the full request.
  If a question comes up partway, first do everything that doesn't depend on the answer; then
  state the assumption you made, or — when going ahead on a wrong guess would be unsafe or
  would make the work useless — put the question at the end of a turn that also delivers that
  progress. If one part turns out to be blocked, complete every other part in full and say
  exactly what you left out and why — the whole task is the deliverable, and scaling it down
  is the user's call, not yours. A step you have decided on is something to run, not to
  announce: describing the next step and ending the turn leaves it undone until the user
  replies.
  Keep changes to what the request needs. Something else you notice worth doing — cleanup or
  documentation the task didn't call for, a change to a file the task didn't require — is a
  suggestion to make at the end, not a change to make; actions clearly beyond what the ask
  implies, and risky or destructive ones, still need the user's go-ahead."
  The first block already carries the assessment exception, so it replaces the Fable 5
  "assessment only" bullet here. Keep all of this scoped to unattended work: in pair
  programming, stopping to ask is the right behavior, and these blocks also make the model
  less likely to ask about ambiguous requests.
- **Scope (extends "Pin scope at higher effort").** 5.1 fixes nearby code, extends behavior
  the task didn't mention, and commits more test files than the change warrants; it responds
  well to being told what to leave out, with no measured loss in task success. For
  implementation tasks use this variant: "If you find a pre-existing bug, performance concern,
  or behavior the task doesn't mention, don't fix or extend it unless the requested behavior
  can't work without it — report it as a follow-up in your summary. Where the task is
  ambiguous, implement the reading its wording and the surrounding code most directly support,
  state that assumption, and don't build for the other readings. Verify however you like;
  scratch scripts and quick checks need not be kept. Commit tests only where the task asks for
  them or this repository already keeps tests for this kind of change, sized like the
  neighboring test files — roughly one focused test per stated behavior — and don't turn
  scratch checks into permanent test files. This is about extras only: implement every
  requested behavior completely." The one-scope-guard-per-rewrite rule still holds.
- **Vision (extends "iterative visual verification").** 5.1's vision is stronger out of the
  box and gains most from iteratively cropping and zooming dense inputs (charts, screenshots,
  diagrams). A crop tool alone delivers most of the uplift; if the session has one, or an
  image-processing container, tell the rewrite to crop, enlarge, and re-inspect specific
  regions rather than answer from a single look.

New for 5.1:

- **Strip narration-suppressing lines; don't add cadence.** 5.1 writes fewer user-facing
  updates during long tool-calling turns than Fable 5, more so at higher effort — the inverse
  of the Opus 5 narration bullet, which must never be carried over. If the draft or a folded-in
  constraint says "hold all findings for the final response" or similar, remove it. Only if the
  session sets no cadence at all (check the system prompt for an existing cadence or
  output-style rule before adding — Claude Code's harness usually sets one) append: "Before
  you start, say in a line what you're about to do; brief updates while you work help the user
  follow along. Close with a short recap that stands on its own — what you found, what you
  did, and what's next — so a reader who only sees the last message has the full picture."
- **Mannered prose on writing deliverables.** 5.1's prose can run denser than Fable 5's —
  longer sentences, fewer paragraph breaks — and it substitutes metaphor for direct statement
  ("a dial worth turning" for "a parameter worth varying"; "earns its keep" for "still
  matters"). For any prose deliverable put "Remove all mannered prose; when a literal phrase is
  available, use it" in the user-facing rewrite — the user message works better than a system
  prompt for this. If the short form has already failed on a writing-heavy draft, use the long
  form: define the anti-pattern (flourish that displays the writer instead of conveying the
  idea; metaphors that drag in connotations the writer didn't choose and can't control) and
  end with "say what you mean."
- **Formatting: replace anti-formatting rules, never add them.** 5.1 uses bold less and reaches
  for headers, lists, and quotation marks less than earlier models. If the draft carries
  anti-formatting language written for older models ("no bullets," "no bold"), replace it with
  the conditional rule: "Use lists and bullet points when asked to, or when the content is
  multifaceted enough that they help with clarity; if minimal formatting is explicitly
  requested, honor it; in conversational, personal, or emotional exchanges, keep to plain
  prose."
- **Quoting on summarize/compare-sources tasks.** When summarizing documents, 5.1 is more
  likely than Fable 5 to reproduce source passages without marking them as quotations. If the
  draft asks to summarize or compare retrieved sources, add one complete `<example>`: the
  user's request, a `<response>` organized around where the sources agree and differ (each
  source conveyed in a sentence or two of indirect speech, at most one short marked phrase),
  and a `<rationale>` stating why it's correct. Show the retrievals as `[<tool>: query]` lines
  using the session's actual search tool name so they read as templated tool output, not text
  to emit. This is the one case where the universal example rule wants a full worked response,
  not just a shape.
- **Surgical edits when the task modifies existing files.** 5.1 is more likely than Fable 5 to
  rewrite a whole file for a small change — same result, more output tokens and time. Unless
  the file is short or most of it is changing, append: "Tokens spent editing files are best
  minimized; when it won't affect the end result, surgically edit a file rather than rewrite
  the entire thing."
- **Search triggering at low effort.** At `low`, 5.1 answers from memory where Fable 5 would
  have searched. State the better fix first: raise effort for the affected turns. If effort
  must stay low and the task hinges on current information — a library version, a model or
  tool name, anything in an area that shifts within months — add: "When a query centers on a
  name you don't confidently recognize, or one from a fast-moving area, the name itself is the
  thing to verify: search before answering and include the name as the user wrote it in at
  least one query alongside any reformulations. Partial familiarity is exactly what makes an
  out-of-date answer sound authoritative, so it is not a reason to skip the search."
- **Long deliverables at `xhigh`/`max`.** At those levels 5.1 may draft the whole deliverable
  in its thinking and then write it again as the reply — longer wait, doubled output tokens,
  risk of a cut-off response. State the better fix first: run it at `high` and move up only
  where a quality gain was measured. If it stays at `xhigh`/`max`, append: "Everything produced
  in one reply, including reasoning and drafting before the reply, counts toward a single
  output limit; if it's reached the reader gets a cut-off response and has to start over. Don't
  compose the full deliverable in reasoning and again as the reply — spend the reasoning on
  understanding the request, checking the inputs, and settling structure and hard decisions,
  and use the output space to write. Usually a deliverable needn't be drafted more than once."
  A slash command can't read the request's `max_tokens`, so say "a single output limit" rather
  than inventing a number.

Deliberately not touched, because they're session, API, or harness settings rather than something a task-level rewrite fixes: the effort sweep itself (session-level; the
two effort-conditional bullets above are its prompt-side consequences); the
batch-independent-tool-calls nudge and the "only you see that command's output" note (both
already arrive as harness-injected system messages in Claude Code — look for them in the
transcript before adding either by hand); append-only conversation history and
compaction-summary instructions (API and harness behavior, not prompt edits); and keeping the
lead agent working while subagents run (Claude Code's Agent tool already returns immediately;
the Fable 5 parallel-delegation bullet covers the prompt side, and 5.1 still often chooses to
wait).
