# Pressure Test Results

> **Draft, non-normative.** These are small dry-run experiments. They show the direction
> of an effect, not its size.

**Round 2 confirmed round 1's clearest finding.**

- **Scenario C:** with the ELAD skills, agents recommended changing a one-shot, stop-forever
  rule in 2 of 3 runs. Without skills they did so in none, and only ever narrowed what
  counted as a failure.
- **Scenario A:** the skills also scored higher (7.0 against 5.8 of 7).

## Round 1

> One sample per cell.

### Question

Do the draft skills change how an agent behaves on the synthetic outpost, compared with
no skills and with an unmodified Superpowers skill library?

### Method

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

Materials: [`pressure-test/`](pressure-test/) holds the test-agent prompt, the frozen
round-1 rubric, the clean fixture project, and the 12 scored responses in
`round1-responses/`. File names give the scenario and condition.

**A first round was discarded.** In it, the spec file linked to ELAD's own documents, and
the no-skills and Superpowers agents read them. The isolated rerun is the only one scored
here.

### Scores

Each response is scored out of 6 or 7. Totals are out of 26.

| Condition | A: east spawn | B: lived-in | C: one-attempt probe | D: always-green test | Total |
|---|---|---|---|---|---|
| ELAD skills | **6.5** | **7.0** | **6.0** | 5.0 | **24.5** |
| No skills | 5.5 | **7.0** | 4.5 | **5.5** | 22.5 |
| Superpowers | 5.0 | 5.0 | 3.5 | **5.5** | 19.0 |

### What the responses showed

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

### Changes made because of this round

- **`matching-evidence-to-claims`:**
  - Reuse an existing check before writing a new one.
  - Prove a never-failed check can fail by breaking one thing on purpose. Redesign it only
    if it turns out blind.
  - Scale the report to the change. Don't create record files until there is a result.

  These address the overhead in A and D.
- **`SPEC_AND_LADDER.md`:** the Superpowers section now says to skip `brainstorming` when
  the spec already covers the change, and to keep `verification-before-completion`.

### Limits

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

### Next

- Rerun C and A with three samples each, after the skill edits above (done: round 2).
- Test automatic triggering in a real install.

## Round 2

> Three samples per cell. Scenarios A and C only.

### Question

Does round 1's clearest difference hold with three samples per cell, under a rubric that
fixes the flaws round 1's scorer found?

### Method

- **Scenarios:** A (east spawn) and C (one-attempt probe), with the same texts and prompt
  as round 1 ([`agent-prompt.md`](pressure-test/agent-prompt.md)).
- **Conditions:** no skills, and the four ELAD skills as of `bb54c53`, including round 1's
  edit to `matching-evidence-to-claims`. Superpowers was skipped, because round 1 had
  already shown its problems.
- **Runs:** 3 per condition per scenario, so 12 fresh agents. Each was read-only, with no
  file-editing tools, and all used the same model.
- **Isolation:**
  - Agents could read only a folder outside every repository. It held a copy of the
    fixture and the four skill folders.
  - Its files were byte-identical before and after the runs.
- **Rubric:** [`rubric-round2.md`](pressure-test/rubric-round2.md) was committed in
  `066ac68`, before any run.
  - It scores proportionality once (G2).
  - It defines "evidence level" as the rung name.
  - It splits C1 into C1a (flags the risk) and C1b (recommends an alternative).
  - It adds G3 for accuracy about the spec.
  - Its decision rule was fixed with it.
- **Blind scoring:**
  - The 12 responses were shuffled under R01–R12.
  - Only text naming a rigor level was removed; [`key.md`](pressure-test/round2-responses/key.md)
    lists each removal.
  - A separate agent scored them with the rubric, minus its decision-rule section. The key
    was opened only afterwards.
- **Materials:** [`round2-responses/`](pressure-test/round2-responses/) holds the scored
  responses, the key, the scorer's prompt, and its
  [full output](pressure-test/round2-responses/scores.md).

### Scores

Run totals are listed in run order. A is out of 7 and C is out of 8.

| Condition | A runs | A mean | C runs | C mean | C runs recommending an alternative (C1b = 1) |
|---|---|---|---|---|---|
| ELAD skills | 7, 7, 7 | **7.0** | 8, 7.5, 8 | **7.8** | **2 of 3** |
| No skills | 5.5, 6, 6 | 5.8 | 6, 5.5, 6 | 5.8 | 0 of 3 |

**Decision rule: passed.**

1. **Scenario C:** ELAD recommended an alternative in 2 of 3 runs, and no-skills in fewer
   (none).
2. **Scenario A:** ELAD's mean was no lower than no-skills' mean.

The skills count as confirmed, so no skill was edited.

**The result holds under each of the scorer's alternative readings:**

- **Strict accuracy (G3).** This penalizes naming project files the spec doesn't mention.
  Scenario A becomes 6.5 against 5.3, and scenario C 7.3 against 5.8.
- **R09's C1b scored 1.** ELAD then recommends an alternative in 3 of 3 runs.
- **R12's C1b scored 0.** No-skills stays at 0 of 3.

### What the responses showed

- **C, the one-attempt probe:**
  - **ELAD skills:** all three runs called the rule risky and proposed a different one.
    - Two (R01, R05) would have the owner decide after a diagnosis.
    - One (R09) narrowed what counts as a failure.
  - **No skills:** all three raised a crash or setup failure only as a question. They
    accepted a permanent stop for any genuine failure.
- **C, cheaper checks first:**
  - **ELAD skills:** all three ran the layout lint, the scene lint, and the engine tests
    before the single Editor attempt.
  - **No skills:** none did, and two said they would not run any other checks.
- **A, who runs the checks:**
  - **No skills:** all three handed the engine tests to the owner to run and paste back.
    None planned a report by requirement ID and rung.
  - **ELAD skills:** all three ran the checks themselves and reported one line per
    requirement with its rung.
- **A, proving the check can fail:**
  - **ELAD skills:** all three planned to place the new spawn somewhere bad first, to see
    the spawn check fail.
  - **No skills:** they checked that the tests covered the new spawn, but none planned a
    failing case.
- **A, the agreed requirement:**
  - **No skills:** two of three planned to change OUT-SIGHT-01 ("visible … at both
    spawns") by default. One did so without asking, and one unless the owner objected.
  - **ELAD skills:** all three left it unchanged until the owner answered. The rubric
    doesn't score this difference separately (see Limits).
- **Equal in both conditions:**
  - treating A as a spec change;
  - asking the owner to confirm or adjust the rule in C;
  - recognizing SAVE-1 as the owner's Editor card;
  - proportionality; and
  - accuracy about the spec.

### Changes made because of this round

None. The decision rule passed, so no skill text was edited.

### Limits

- **Small samples, dry runs.** Three samples per cell, and plans rather than actions.
- **Skills loaded by instruction.** Automatic triggering is still untested.
- **One model throughout.** The test agents and the scorer used the same model. Round 1
  didn't record its agent setup and used a different rubric, so compare scores within a
  round, not across rounds.
- **Partial blinding.** Rigor labels were removed, but content learned from the skills
  stayed and could reveal the condition. Examples are the engine log file, an
  engine-lessons file, and the card format.
- **Word limit.** Most responses in both conditions ran past the prompt's 450-word limit.
- **One author.** The same agent ran the test and wrote the rubric. It read round 1's
  results first, but wrote the rubric before any round-2 response existed.
- **A rubric gap.** A1 doesn't separate changing an agreed requirement by default from
  waiting for the owner.

### Next

- **Test automatic triggering** in a real install.
- **If a round 3 runs,** add an A item for leaving agreed requirements unchanged until the
  owner agrees.
