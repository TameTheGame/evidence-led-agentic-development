# AGENTS.md snippet

Paste this into your project's `AGENTS.md`, after installing the three skills. It tells the
agent which skill fits which moment, so the skills engage even when nothing in the request
names them.

```markdown
## Skills

Use these skills at these moments:

- Before planning or editing, or when a request sets an attempt limit or a stop rule: use `choosing-rigor`.
- Before choosing or running checks for a requirement, and before reporting a requirement as done: use `matching-evidence-to-claims`.
- Before changing any agreed requirement, or deciding feel, scope, merging, or releasing: use `asking-the-owner`.
```

The idea of a short note that routes moments to skills comes from Superpowers'
session-start hook in [obra/superpowers](https://github.com/obra/superpowers). It is
paraphrased here, not copied. Evidence for the snippet's effect is in
[`evidence/`](evidence/).
