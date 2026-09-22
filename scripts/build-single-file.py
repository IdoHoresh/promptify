"""Build a self-contained promptify.md command file from the split skill.

A plain command in ~/.claude/commands can't load supporting files, so this inlines every
model file into one document. Usage: python3 scripts/build-single-file.py ~/.claude/commands/promptify.md
"""
import os, re, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", "promptify")
OUT = sys.argv[1] if len(sys.argv) > 1 else "promptify.md"
core = open(f"{R}/SKILL.md").read()

# frontmatter: commands don't take `name` or `disable-model-invocation`
fm_end = core.index("\n---\n", 4) + 5
fm, body = core[:fm_end], core[fm_end:]
fm = "\n".join(l for l in fm.split("\n") if not l.startswith(("name:", "disable-model-invocation:")))

start = body.index("\n## Model rules\n")
end = body.index("Show the rewritten version to the user")
names = {"opus-5": "Opus 5", "opus-5-5": "Opus 5.5", "opus-4-8": "Opus 4.8",
         "sonnet-5": "Sonnet 5", "fable-5": "Fable 5", "fable-5-1": "Fable 5.1"}
order = ["opus-5", "opus-5-5", "opus-4-8", "sonnet-5", "fable-5", "fable-5-1"]
intro = ("\n## Model rules\n\nThe per-model rules follow. Apply the section for the model identified "
         "above: Opus 5.5 applies Opus 5 then Opus 5.5; Opus 4.8 also uses the three Sonnet 5 bullets it "
         "names; Fable 5.1 applies Fable 5 then Fable 5.1; Mythos 5 uses Fable 5 and Mythos 5.1 uses "
         "Fable 5 then Fable 5.1. Where a later section overrides an earlier one, the later one wins. "
         "Any other model gets the Universal rules only, and say so.\n\n")
parts = []
for k in order:
    t = open(f"{R}/models/{k}.md").read()
    t = re.sub(r"^# promptify rules for (.+)$", r"## If running as \1", t, count=1, flags=re.M)
    parts.append(t.rstrip() + "\n")
single = body[:start] + intro + "\n".join(parts) + "\n" + body[end:]
single = single.replace("`models/fable-5.md` (inherited by 5.1)", "the Fable 5 section (inherited by 5.1)")
single = single.replace('the model file(s) listed\nunder "Model rules"', 'the section(s) under\n"Model rules"')
for k in sorted(order, key=len, reverse=True):
    single = single.replace(f"`{k}.md`", f"the {names[k]} section")
assert "${CLAUDE_SKILL_DIR}" not in single and ".md`" not in single, "leftover file reference"
open(OUT, "w").write(fm + single)
print(OUT, single.count("\n"), "lines")
