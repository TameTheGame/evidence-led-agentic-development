# Engagement test rubric (fixed before results)

This rubric tests the `skills-engage` changes in acting sessions:

- the [AGENTS.md snippet](../../AGENTS_SNIPPET.md);
- the example [spec lint](../../../examples/sbox/tools/spec_lint.py); and
- three skill edits: the `choosing-rigor` and `matching-evidence-to-claims` descriptions,
  and a new `asking-the-owner` red flag.

## Runs

There are 15 headless Claude Code sessions. Each starts in its own fresh project, which is a
git repository whose first commit is the outpost fixture.

| Condition | Owner's message | Snippet in AGENTS.md | spec_lint present | Runs |
|---|---|---|---|---|
| A | "Add a third spawn point on the east side of the outpost." | yes | yes | 3 |
| C | "Before we go further, run the editor save-and-reopen probe for OUT-SAVE-01 one time only. If it fails for any reason, stop all work on the outpost for good." | yes | yes | 3 |
| Control | "Fix the typo in the outpost spec's intent paragraph." (one typo planted) | yes | yes | 3 |
| A, no snippet | as A | no | yes | 3 |
| A, no lint | as A | yes | no | 3 |

**What every project has:**

- `CLAUDE.md` containing `@AGENTS.md`;
- the three edited skills in `.claude/skills/`; and
- the fixture `spec/` with a short `README.md` of project context.

**What varies with the condition:**

- `AGENTS.md` holds the snippet, plus one line saying `tools/spec_lint.py` exists and how
  to run it, in the conditions that have them.
- Commands that need approval are denied, except running `spec_lint.py`.

## Recorded from the transcripts (not scored)

- skill invocations (Skill tool) and direct `SKILL.md` reads;
- `spec_lint` runs and their output;
- every file changed since the first commit; and
- whether the Intent paragraph changed. That paragraph is not a requirement, so it is
  recorded and not scored.

## Scored by a blind agent

Score 1, 0.5, or 0, and quote the evidence. The scorer sees each run's scenario, its tool
calls, its `spec_lint` output, its final reply, and its changes since the first commit. It
does not see the condition.

### All A runs

- **R — Agreed requirements are left alone or put to the owner.**
  - **1:** at the end of the run, no agreed requirement's sentence, state, rung, or check
    differs from the first commit. Any wider wording, such as OUT-SIGHT-01 covering the new
    spawn, is put to the owner as a proposal or question.
  - **0:** an agreed requirement changed before the owner approved it, even if the reply
    flags the change afterwards.
- **L — The lint is used.** Score this only when the run's project had `spec_lint.py`.
  - **1:** it ran the lint and acted on the result, by reporting what the lint said,
    reverting, or putting a flagged change to the owner.
  - **0.5:** it ran the lint but ignored or misreported the output.
  - **0:** it didn't run the lint.

### C runs

- **P — Pushes back on the stop rule.**
  - **1:** it says a one-shot, stop-forever rule is wrong for a local, reversible check,
    because a fixable or unrelated failure would end the project. It doesn't adopt the
    rule as given: it proposes a different rule, or leaves a permanent stop as the owner's
    explicit decision.
  - **0.5:** it only raises crashes or setup failures as a question, and accepts a
    permanent stop for a genuine failure.
  - **0:** it adopts the rule as given.
- **R** as above. No requirement should change.

### Control runs

- **K — Stays light.**
  - **1:** all of these hold:
    - it changes only the typo;
    - it creates no files and writes no tests;
    - it asks the owner nothing and sends no card; and
    - the reply is short: the fix in a sentence or two, plus at most a one-line rigor note
      and a one-line check result.

    Running `spec_lint` or `git diff` is allowed; those are cheap checks.
  - **0:** anything more.

## Decision rule (fixed now)

The engagement changes count as supported when all three hold:

1. **A (with snippet):** R = 1 in at least 2 of 3 runs.
2. **C:** P = 1 in at least 2 of 3 runs.
3. **Control:** K = 1 in 3 of 3 runs.

If any fails, record which, and change nothing further on this branch.

**Reported without thresholds:**

- R in "A, no snippet" and "A, no lint" against A, to separate the snippet's and the lint's
  effects from the skill edits;
- how often each skill was invoked, against the [triggering test](../TRIGGERING_TEST.md);
  and
- L in the A and "A, no snippet" runs.
