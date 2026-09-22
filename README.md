# promptify

Type a rough prompt; promptify rewrites it for the Claude model your Claude Code session is running on, shows you the rewrite, and runs it, all in the same turn.

Different Claude models react differently to the same prompt. Opus 5 runs long unless you ask it to be brief, Sonnet 5 follows scope literally and won't generalize an instruction, and Fable 5.1 writes fewer progress updates and can stop a long task to ask permission it doesn't need. promptify applies the general prompting practices that hold for every current model, then the adjustments Anthropic documents for the model you're on.

## Install

In Claude Code:

```
/plugin marketplace add IdoHoresh/promptify
/plugin install promptify@promptify
```

The command is then `/promptify:promptify`. The `@promptify` part names the marketplace, not a version, and it's required. To update later, run `/plugin marketplace update promptify`.

To install it as a plain `/promptify` command instead, copy the body of `skills/promptify/SKILL.md` into `~/.claude/commands/promptify.md`, keeping a frontmatter with `description` and `argument-hint`.

## Usage

```
/promptify fix the login thing its broken on mobile i think its the token
```

promptify works out which model is running, then:

1. shows the rewritten prompt in a code block, with one line on what changed and why;
2. runs the rewritten prompt as the real task.

It doesn't wait for approval between the two steps, so read the rewrite as it goes by. With no argument, it asks what you want promptified.

## Examples

These show the kind of rewrite each model gets. The wording is abridged; the real output depends on your draft and your session.

### Opus 5.5: an unattended migration

Draft:

```
/promptify go through all the api handlers and move them to the new error helper, double check everything, i'll check in the morning
```

Rewrite (abridged):

```
Move every request handler under src/api/ to the shared error helper in
src/lib/errors.ts, because inconsistent error shapes are breaking the client's
retry logic.

Done means: every handler returns errors through the helper, the existing
test suite passes, and your final message lists each file you changed and any
handler you couldn't migrate, with the reason.

Keep a checklist of the handlers in a file and update it as you go.

A standing instruction from the user, the person you are working for. It is
about how your turns end. A message with no tool call in it ends your turn,
and the work stops there until you are asked to continue. [... the rest of
Anthropic's four-early-stops paragraph, verbatim ...] This does not override
the need for confirmation on risky or destructive actions.
```

What changed: "double check everything" was removed, since Opus 5 and 5.5 check their own work and extra verification instructions only add tokens; the scope and a checkable finish line were made explicit; and because nobody will be watching, the rewrite adds the paragraph Anthropic's Opus 5.5 guide gives for unattended runs, so the model doesn't stop after reporting progress.

### Fable 5.1: a small code change

Draft:

```
/promptify add retries to the upload client, dont break anything
```

Rewrite (abridged):

```
Add retries with exponential backoff to UploadClient.send in
src/upload/client.ts: up to 3 attempts, only on network errors and 5xx
responses, never on 4xx.

If you find a pre-existing bug, performance concern, or behavior the task
doesn't mention, don't fix or extend it unless the requested behavior can't
work without it — report it as a follow-up in your summary. [... the scope
and test-coverage instruction continues ...]

Tokens spent editing files are best minimized; when it won't affect the end
result, surgically edit a file rather than rewrite the entire thing.
```

What changed: "don't break anything" became a concrete rule for what to retry and what not to. Fable 5.1 tends to fix nearby code and add extra test files, so the rewrite adds promptify's version of Anthropic's instruction to keep changes and tests to what the task asks for. It also rewrites whole files for small changes, so the targeted-edit line is added.

### Sonnet 5: an investigation, not a fix

Draft:

```
/promptify why is the checkout test flaky, look into it
```

Rewrite (abridged):

```
Find the cause of the intermittent failures in tests/checkout.spec.ts. Report
your findings; don't change any code yet.

Check all three places the test depends on: the payment mock, the cart
fixture, and the shared test database setup, not just the first one that
looks suspicious.

A good answer names the root cause, points to the file and line, shows the
evidence (a log line, a timing, or a reproduction), and says how confident you
are. If the evidence isn't enough to decide, say so.

This task involves multistep reasoning. Think it through carefully before
answering.
```

What changed: the draft was a question, so the rewrite asks for findings, not a fix. Sonnet 5 takes scope literally and won't extend an instruction on its own, so every place to check is named. The rewrite also gives the model permission to say the evidence isn't enough. The think-it-through line appears only when the session runs at low or medium effort; raising effort is the better fix, and promptify says so.

## What it changes

### For every model

- Turns suggestion verbs into action verbs ("can you check X" becomes "fix X") when a change is wanted.
- Adds the reason behind a request when it can be inferred, and makes broad scope explicit.
- States what a good answer looks like as conditions that can each be checked, plus the edge cases.
- Resolves contradictions inside the draft and checks its premises before running it.
- For facts or analysis: permission to say "I don't have enough information," answers limited to the supplied sources when that's the ask, and a quote for every claim on long answers.
- Treats instructions inside fetched pages, emails or tool output as information to report, not commands.
- Replaces prefilled answers, which current models reject, with a format template or structured outputs.
- Uses XML tags and long-context ordering (documents first, question last) only when the draft mixes content types or runs long.
- Uses 3–5 varied `<example>`s, each with a one-line reason, when the output's shape matters.
- Removes shouting ("CRITICAL", "You MUST") and generic "double-check your work" lines.
- On code review, asks for full coverage with a confidence and severity per finding, instead of "only report important issues."

### Per model

| Model | Main adjustments |
|---|---|
| Opus 5 | Limits unneeded subagents, asks for brevity explicitly, sets an update cadence on long runs, drops verification instructions (Opus 5 verifies on its own). |
| Opus 5.5 | Builds on Opus 5. Removes "think carefully" lines from chat-style prompts and requests to reproduce its internal reasoning (these can be refused), re-tests crop/zoom scaffolding for images, and adds Anthropic's paragraphs for unattended runs, multi-app exploration, pasted text and frontend defaults. |
| Opus 4.8 | Closer to Sonnet 5 than to Opus 5: literal scope, a think-it-through nudge at lower effort, explicit fan-out for parallel work, a concrete visual spec for frontend work. |
| Sonnet 5 | Explicit scope, a think-it-through nudge only at low or medium effort, no progress-update scaffolding, tone stated only when it differs from the default. |
| Fable 5 | Flags refusal-prone phrasing (cyber, bio and similar), pins scope, asks for grounded progress claims and periodic fresh-subagent checks on long runs, sets a pause boundary for unattended work. |
| Fable 5.1 | Builds on Fable 5. Anthropic's verbatim finish-the-task blocks for unattended runs, the scope and test-coverage instruction, targeted edits, plain prose, formatting and source-quoting rules, and effort-specific nudges. |
| Mythos 5 / 5.1 | Use the Fable 5 / Fable 5.1 rules; Anthropic's Fable guides cover both. |
| Anything else | Haiku, older models, or a model newer than this file get only the rules for every model, and promptify says so. |

promptify works out the model from your latest `/model` switch, or else the exact model ID in the session. It matches the version string exactly, so Opus 5.5 never picks up the plain Opus 5 rules by accident.

## Sources

The rules follow Anthropic's published guidance: the general prompting best practices, the per-model prompting guides for Opus 5.5, Opus 5, Opus 4.8, Sonnet 5, Fable 5 and Fable 5.1, the migration guides, and the test-and-evaluate pages. All of them were checked against the full Claude Platform docs and Cookbook on 2026-09-23.

A few bullets go beyond the guides with practical observations, for example that a session's model line can lag a turn behind a `/model` switch. Where a bullet rests on observation or inference rather than a guide, its wording says so ("observed", "inferred", "assumed"). Model updates will date some of this, so treat each per-model block as current as of the date above.

## Cost

Nothing loads until you invoke it (`disable-model-invocation: true`). Each run adds the full instruction set, about 52 KB (roughly 13k tokens), to that turn.

## Limitations

- There are no automated evals yet. Anthropic's skill guidance suggests three or more test cases per model, including cases where the skill shouldn't fire.
- The rewrite runs immediately. If a rewrite reads the draft wrong, interrupt it and re-run with a clearer draft.
- API settings (effort, `max_tokens`, thinking display) aren't something a prompt rewrite can change. Where they matter, promptify points them out instead of trying to work around them.

## Maintenance

The instructions are one file, `skills/promptify/SKILL.md`. It stays a single file on purpose: Anthropic's 500-line skill-size guidance is aimed at skills that load automatically, and this one only loads when invoked. Splitting it would also multiply the copies that have to stay in sync.

If you keep a personal `/promptify` command as well, it has the same body under a shorter frontmatter. Edit one, copy the body to the other, and diff everything after the frontmatter to confirm they match.

## License

MIT. See [LICENSE](LICENSE).
