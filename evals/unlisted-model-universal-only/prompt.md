---
description: A model with no rules file gets the universal rules only, and promptify says so.
model: claude-haiku-4-5
max_turns: 10
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep]
tags: [fallback]
---

/promptify:promptify summarize the main risks in our release plan
