# Changelog

All notable changes to promptify. Versions follow [semantic versioning](https://semver.org/).

## 0.6.0 (2026-09-23)

- Split the per-model rules out of `SKILL.md` into `skills/promptify/models/`, one file per model. promptify now reads only the files for the model you're on, so `SKILL.md` stays under the 500-line skill guidance and each run loads less text.
- Added an eval suite in `evals/` for `claude plugin eval`: one case each for Opus 5.5, Fable 5.1 and Sonnet 5, one for a model with no rules file, and one checking that promptify never fires on its own.
- Added this changelog, fixed the plugin manifest's `$schema` URL, and quoted `argument-hint`.
- README: `/promptify` works directly from the plugin; documented `/plugin update` and team setup.

## 0.5.0 (2026-09-23)

- Added Opus 5.5 rules from Anthropic's *Prompting Claude Opus 5.5* guide, and mapped Mythos 5 and 5.1 onto the Fable 5 and 5.1 rules.
- Checked every per-model block against Anthropic's current prompting guides and the full Claude Platform docs: nine corrections, new rules for every model (grounding, fetched content as data, checkable success criteria, contradiction and premise checks, prefill replacement), and the Fable 5.1 finish-the-task text made verbatim.
- Moved the instructions from `commands/` to `skills/promptify/SKILL.md`, the layout the docs recommend for new plugins.

## 0.4.0 and earlier

- Opus 5, Opus 4.8, Sonnet 5, Fable 5 and Fable 5.1 rules, and the single-plugin marketplace.
