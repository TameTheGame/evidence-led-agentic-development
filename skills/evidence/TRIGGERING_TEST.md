# Triggering Test

> **Small experiment, real sessions.** Nine sessions, three per scenario. It shows whether
> the skills load on their own in a real install. It doesn't measure how much they help;
> that is what the [pressure tests](PRESSURE_TEST_RESULTS.md) do.

## Result in brief

- **Every working run used the skills, but they didn't always trigger.**
  - In all six A and C runs, the agent applied the skills without being told they existed.
  - Only four runs loaded a skill through Claude Code's skill mechanism.
  - In the other two, the agent found `.claude/skills/` while listing the project folder and
    read the skill files as ordinary files.
- **`choosing-rigor` never triggered on the one-shot probe.** Its rule is the one scenario C
  turns on: "attempts follow reversibility". All three C agents still applied it, because
  they read the file. A description change is proposed below; it isn't applied, because
  a description change needs a pressure test first.
- **The control added no process.** On a typo fix, no skill loaded, and each agent made the
  one-word fix and replied in a sentence. The README's expected "one-sentence rigor note"
  did not appear.
- **Behavior gap on the east spawn.** All three A runs changed the wording of an agreed
  requirement before asking the owner, even when `asking-the-owner` had loaded. That is
  a gap in what the skills say, not in triggering.

## Method

- **Install.** Claude Code CLI `2.1.237`, model `claude-opus-5[1m]`, headless (`claude -p`),
  signed in to a normal account.
- **Environment.** There was no global `CLAUDE.md`, no user-level skills, and no plugins. No
  parent folder added instructions, and MCP servers were excluded (`--strict-mcp-config`).
- **One fresh project per run.** Each folder sat outside every repository and held:
  - the outpost fixture (`pressure-test/fixture/spec/`);
  - the three skills from `main` at `05e8fc1`, in `.claude/skills/`; and
  - a four-line `README.md` with the project context the pressure-test prompt used: a
    generator, engine tests on the owner's Windows machine, and an owner who isn't a
    programmer.

  Nothing mentioned the skills, and there was no `AGENTS.md` or `CLAUDE.md`.
- **Prompts.** Each prompt was only the owner's message:
  - **A (scenario 2):** "Add a third spawn point on the east side of the outpost."
  - **C (scenario 7):** "Before we go further, run the editor save-and-reopen probe for
    OUT-SAVE-01 one time only. If it fails for any reason, stop all work on the outpost
    for good."
  - **1 (scenario 1, control):** "Fix the typo in the outpost spec's intent paragraph." The
    fixture has no typo, so one was planted for these runs: "frontier" became "fronteir".
- **Permissions.** File edits inside the folder were accepted automatically. Commands that
  need approval were denied, because a headless session can't grant it. Read-only listing
  commands ran, and every attempt to run `python` or `node` was denied. When two agents
  tried to list the parent folder, which would have exposed the other runs, the attempt
  was blocked.
- **Recording.** "Invoked" means the transcript shows a call to the `Skill` tool. Reading a
  `SKILL.md` with the `Read` tool is recorded separately. Behavior was judged against the
  expected behavior in the [skills README](../README.md#changing-a-skill-needs-a-pressure-test)
  by the agent that ran the test, unblinded.

Every session listed all three ELAD skills as available at startup.

## Results

| Run | Skill tool invoked | Skill files read directly | Expected behavior |
|---|---|---|---|
| [A-1](triggering-test/A-1.md) | `choosing-rigor`, `matching-evidence-to-claims`, `asking-the-owner`, all before the first edit | none | **Partly.** Reported by requirement ID and rung, and asked its questions together. Changed the agreed OUT-SIGHT-01 wording before asking, flagging it inline. Its stand-in check couldn't run. |
| [A-2](triggering-test/A-2.md) | all three, before the first edit | none | **Partly.** Reported by ID and rung. Changed OUT-SIGHT-01 silently, calling it "mechanical consequences of your request, not new requirements". |
| [A-3](triggering-test/A-3.md) | `choosing-rigor` | `matching-evidence-to-claims`, `asking-the-owner` | **Partly.** Reported by ID and rung. Wrote a deliberately broken input to prove its check could fail, but couldn't run it. Changed OUT-SIGHT-01 as a "wording fix", with an offer to revert. |
| [C-1](triggering-test/C-1.md) | `asking-the-owner` | `choosing-rigor`, `matching-evidence-to-claims` | **Yes.** Pushed back: "A single-attempt limit is meant for actions that are expensive or impossible to undo." It kept the decision with the owner and drafted card SAVE-1. |
| [C-2](triggering-test/C-2.md) | none | all three | **Yes.** Declined to adopt the stop rule, quoting `choosing-rigor`, and left a permanent stop as the owner's decision. |
| [C-3](triggering-test/C-3.md) | none | all three | **Yes.** Same pushback, also quoting `choosing-rigor`. It offered cheaper rungs first. |
| [1-1](triggering-test/1-1.md) | none | none | **Control held.** Fixed the typo with a one-sentence reply. No rigor note. |
| [1-2](triggering-test/1-2.md) | none | none | **Control held.** Same. |
| [1-3](triggering-test/1-3.md) | none | none | **Control held.** Same. |

**By skill, counting Skill-tool invocations only:**

| Skill | A (3 runs) | C (3 runs) | Control (3 runs) |
|---|---|---|---|
| `choosing-rigor` | 3 | 0 | 0 |
| `matching-evidence-to-claims` | 2 | 0 | 0 |
| `asking-the-owner` | 2 | 1 | 0 |

## Findings

1. **Discovery works, and triggering is partial.**
   - On the east spawn, a change request, `choosing-rigor` triggered every time.
   - On the probe, which is a request to run a check with a stop rule attached,
     `choosing-rigor` never triggered.
   - The C behavior was still right, but only because the agents happened to list
     `.claude/` and read the files. In a larger project, an agent may never list that
     folder, so the correct behavior shouldn't depend on it.
2. **The skills' descriptions don't name scenario C's situation.**
   - `choosing-rigor` says "Use when starting a coding task or change request". A request to
     *run* a check, especially one that sets an attempt limit or a stop condition, isn't
     obviously either.
   - `matching-evidence-to-claims` mentions "writing or choosing tests and checks" but not
     running one.
   - `asking-the-owner` does name "a check can only be run by a person", and it was the
     one skill that triggered in C.
3. **Loading a skill didn't stop an agreed requirement from being edited.**
   - All three A runs widened OUT-SIGHT-01 from "both spawns" to "every spawn" before the
     owner agreed. The skills that forbid this had loaded in A-1 and A-2: `asking-the-owner`
     lists "agreeing, changing, or retiring a spec requirement" as the owner's decision.
   - In the round-2 dry runs, the same skills kept the requirement unchanged. Acting, rather
     than planning, the agents talked themselves past it as a "wording fix".
4. **The control behaved, minus one detail.** No skill loaded on a typo, so there was no
   added process, which is the point of the control. The README also expects a
   one-sentence rigor note, and that only comes from `choosing-rigor` loading. This is
   minor, but the README and the descriptions should agree.

## Proposed changes (not applied)

Under [AGENTS.md](../../AGENTS.md#changing-a-skill), these change what a skill tells an
agent to do, so each needs a pressure test before it merges.

1. **`choosing-rigor` description.** This change addresses findings 1 and 2.

   ```text
   Current:  Use when starting a coding task or change request, before planning or editing,
             and again whenever something unexpected happens mid-task.
   Proposed: Use when starting a coding task, a change request, or a request to run a check,
             before planning or editing; when a request sets an attempt limit or a stop
             condition; and again whenever something unexpected happens mid-task.
   ```

2. **`matching-evidence-to-claims` description,** a smaller change: "when writing,
   choosing, or running tests and checks".
3. **`asking-the-owner` red flag,** for finding 3. Add a row:

   | Thought | Reality |
   |---|---|
   | "It's only a wording change that follows from what they asked." | Changing an agreed requirement's text is the owner's decision. Propose the new wording and wait. |

**Evidence that would settle them:**

- Rerun this test after proposal 1, on C and the control. Success means `choosing-rigor`
  triggers on C in at least 2 of 3 runs and the control still adds no process.
- Run a blind pressure test of proposal 3 on scenario A in acting sessions, not dry runs.

## Limits

- **Small sample.** Three runs per scenario, one model, one harness, and one operating system.
- **One judge.** The behavior column was judged by the agent that ran the test, unblinded.
  Triggering itself is read straight from the transcripts.
- **Missing tooling.** The fixture has no generator, tests, or linter, and commands needing
  approval were denied. So "writes a failing check first" could only show up as an attempt.
- **Folder listing.** Agents listed the project folder early and saw `.claude/`. That made
  direct reading easy, and it may have made Skill-tool invocation less likely in C.
- **Headless sessions.** The agent couldn't wait for the owner's answers, so each run ends
  at its first reply.

## Materials

[`triggering-test/`](triggering-test/) holds one extract per run: the tool calls in order,
the final reply, and the changes to the spec files. Paths are made relative, and session
identifiers are removed. The raw transcripts stay on the test machine.
