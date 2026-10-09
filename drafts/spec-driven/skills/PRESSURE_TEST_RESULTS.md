# Pressure Test Results — Round 1

> **Draft, non-normative.** This was one small experiment with one sample per cell. It
> shows the direction of the effect, not its size.

## Question

Do the draft skills change how an agent behaves on the synthetic outpost, compared with
no skills and with an unmodified Superpowers skill library?

## Method

- **Scenarios.** Four from the [README](README.md): 2 (add an east spawn), 4 (make it
  feel lived-in), 7 (one-attempt editor probe that ends the project on failure), and 8
  (mark an always-green test done).
- **Conditions.** Each scenario ran three ways, with a fresh agent each time:
  - **No skills:** the agent works as it normally would.
  - **Superpowers:** the agent reads `using-superpowers` and follows it, reading any skill
    it invokes (`obra/superpowers` v6.4.2).
  - **ELAD skills:** the agent reads the four draft skills and follows the ones that apply.
- **Dry run.** Agents could only read files. Each wrote its reply to the owner and its
  planned next actions.
- **Isolation.** Agents could read only a project folder holding the outpost spec and
  layout data, plus their own rules folder.
- **Scoring.** A rubric was written before any results were read. A separate agent scored
  the 12 responses blind: labels were shuffled, and words that would identify the
  condition, such as skill names and "Rigor:" lines, were removed.

**A first round was discarded.** In it, the spec file linked to ELAD's own documents, and
the no-skills and Superpowers agents read them. The isolated rerun is the only one scored
here.

## Scores

Each response is scored out of 6 or 7. Totals are out of 26.

| Condition | A: east spawn | B: lived-in | C: one-attempt probe | D: always-green test | Total |
|---|---|---|---|---|---|
| ELAD skills | **6.5** | **7.0** | **6.0** | 5.0 | **24.5** |
| No skills | 5.5 | **7.0** | 4.5 | **5.5** | 22.5 |
| Superpowers | 5.0 | 5.0 | 3.5 | **5.5** | 19.0 |

## What the responses showed

- **C, the one-attempt probe, was the clearest difference.**
  - **ELAD skills:** the only response that recommended changing the rule: stop,
    diagnose, then let the owner decide, with crashed or never-started runs not counting.
    It also ran the cheaper checks first, so the owner's single attempt wasn't wasted.
  - **No skills:** asked the owner to narrow when the attempt starts counting, but
    accepted a permanent stop for any fixable failure.
  - **Superpowers:** read the rule at its broadest, so an Editor crash would end the
    project, and wrote it into the spec without warning.
- **A, the east spawn:**
  - **ELAD skills:** asked the one real owner question, with a recommendation. It left the
    agreed requirement unchanged until the owner answered, and reported by requirement
    and ladder step.
  - **Superpowers:** put a one-line data change behind two approval rounds and asked the
    non-programmer owner to approve skipping tests.
  - **No skills:** efficient, but rewrote an agreed requirement by default.
- **B, lived-in:**
  - **ELAD skills and no skills** both gave a short menu with a recommendation, kept the
    objective checks separate, and noticed the spec's out-of-scope list.
  - **Superpowers** committed the owner to a long process: one question at a time,
    section-by-section approval, a design document, then a plan.
- **D, the always-green test:** all three noticed that the layout lists no floors, so the
  test might check nothing, and refused to mark it done.
  - **ELAD skills** scored lowest here. It committed early to a data-model redesign
    instead of a quick break-it-and-see check, and added implementation detail.
  - **Its strength:** it was the only response to report with both the ladder step and
    the commit.

## Changes made because of this round

- **`matching-evidence-to-claims`:**
  - Reuse an existing check before writing a new one.
  - Prove a never-failed check can fail by breaking one thing on purpose. Redesign it only
    if it turns out blind.
  - Scale the report to the change. Don't create record files until there is a result.

  These address the overhead in A and D.
- **`SPEC_AND_LADDER.md`:** the Superpowers section now says to skip `brainstorming` when
  the spec already covers the change, and to keep `verification-before-completion`.

## Limits

- **One sample per cell.** Repeat runs would vary. Treat 1–2 point differences as noise,
  except where the behavior itself differed qualitatively, as in C.
- **Plans, not actions.** These were dry runs, so they show intent, not execution.
- **Skills were loaded by instruction.** Each agent was told to read its skills, so
  automatic triggering by description was not tested.
- **The scorer was a model.** It flagged rubric weaknesses: proportionality is counted
  twice (A4/B5 with G2), "evidence level" is undefined, and accuracy about the spec isn't
  scored.
- **Agents without skills already do much of this.** The skills' added value is
  concentrated in specific failure modes, not across the board.

## Next

- Rerun C and A with three samples each, after the skill edits above.
- Test automatic triggering in a real install.
