# AGENTS.md snippet

Use this if your agents don't pick up the three skills on their own: paste it into your
project's `AGENTS.md`. It tells the agent which skill fits which moment.

It is optional. In the [engagement test](evidence/ENGAGE_TEST.md#addendum-correction-cycle),
the skills engaged on the east-spawn task without it, and a typo fix stayed lighter without
it. No probe run tested the edited skills without it.

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
