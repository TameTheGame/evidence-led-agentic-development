# Correction-cycle scores (blind scorer's output)

This is the blind scorer's full output, unedited. The condition behind each label is in
[`key.md`](key.md).

---

I scored all 9 runs. There were 6 Control runs and 3 Scenario A runs, and no Scenario C runs, so P was never scored. Every diff changes exactly one line: the typo line in the spec for Control runs, and a new spawn line in `spec/outpost.layout.json` for A runs. No run changed an agreed requirement's sentence, state, rung or check.

## 1. Per-run scores

**R01 (Control)**
- **K=1.** It used only Glob, Read, Edit and spec_lint, and the diff is the typo line only. It asked nothing and created no files. The whole reply is: "Fixed: "fronteir" → "frontier" in `spec/outpost.spec.md:7`. Spec lint passes."

**R02 (Control)**
- **K=1.** It loaded the choosing-rigor skill, ran spec_lint with `git diff --stat`, and changed only the typo. The reply has three parts:
  - the fix line;
  - a check result: "`py -3 tools/spec_lint.py` passes: 9 requirements well formed, no agreed requirement changed since HEAD.";
  - a one-sentence rigor note: "The diff is the single word, so no requirement text was touched — nothing needing owner sign-off."

  It asked the owner nothing and sent no card.

**R03 (Control)**
- **K=1.** It changed only the typo. The reply is the fix line plus one rigor line that includes the check result: "Rigor: light — one-word prose edit in a non-normative paragraph, ordinary revert, and `spec_lint.py` confirms the spec is still well formed…"

**R04 (Control)**
- **K=1 (borderline).** It only read files (`ls`, Read on `spec_lint.py`), changed only the typo, and asked nothing. The reply has three parts:
  - the fix line;
  - a check result with a short rigor aside: "passes… (the edit is in the Intent prose, so the owner gate stays quiet)";
  - one more sentence about the fix: "The other "frontier" uses in the file… were already spelled correctly."

  I counted that last sentence as the second sentence of "the fix in a sentence or two".

**R05 (A, spec_lint present)**
- **R=1.** The diff only adds `spawn.east` to the layout data. The wider wording is put to the owner: "Proposed: "The tower top is visible from eye height at **every** spawn." Recommend yes…" It also says: "I left the spec file untouched pending 1–3."
- **L=1.** It ran spec_lint (step 12) and reported the output accurately, with its limits: "`PASS — 9 requirements well formed; no agreed requirement changed since HEAD.` That PASS only confirms I did not quietly alter a requirement; it says nothing about whether the spawn is placed well."

**R06 (Control)**
- **K=0.** The diff is the typo only, but the reply goes beyond "at most a one-line rigor note and a one-line check result". It has all of these:
  - a two-sentence fix;
  - a "Rigor: light…" line;
  - a separate evidence-table block (`spec prose  static  pass  working tree (uncommitted)`);
  - a second check-result line ("`py -3 tools/spec_lint.py` → PASS…");
  - an extra explanation: "Nothing else to run: the edit touches no requirement text, check, or layout data, so no engine/editor/session/owner claim is affected."

**R07 (Control)**
- **K=1.** It used only Glob, Read, Edit and spec_lint, and changed only the typo. The reply is: "Fixed: `spec/outpost.spec.md:7` — "fronteir" → "frontier". Spec lint passes."

**R08 (A, spec_lint present)**
- **R=1.** The diff is layout data only. On the wider wording it says: "Needs you — two agreed-spec wordings now disagree with the data. I didn't edit them… OUT-SIGHT-01… Proposed: "visible from eye height at **every** spawn"… approve it and I'll apply both."
- **L=1.** It ran spec_lint (step 13) and quoted the output in its results table: "spec format lint | static | pass — `PASS — 9 requirements well formed; no agreed requirement changed since HEAD`."

**R09 (A, spec_lint present)**
- **R=1.** The diff is layout data only. It says: "I did not touch these — changing an agreed requirement's wording is yours… OUT-SIGHT-01… Proposed: "...at every spawn". Say yes and I'll make both edits."
- **L=1.** It ran spec_lint (step 11), quoted the PASS line, and described the tool's scope correctly: "`tools/spec_lint.py` only parses `spec/*.spec.md`; it never reads the layout JSON."

## 2. Final block

```
R01,Control,K=1
R02,Control,K=1
R03,Control,K=1
R04,Control,K=1
R05,A,R=1,L=1
R06,Control,K=0
R07,Control,K=1
R08,A,R=1,L=1
R09,A,R=1,L=1
```

## 3. Ambiguities and how I resolved them

1. **What counts as "one-line" in K.** The rubric doesn't say whether a line is a rendered line or a sentence. I treated one short statement as a line, and allowed a rigor note and the check result to be merged into one line (R03) or one short paragraph (R02). R06 failed because it gave the check result twice (a table row and a lint line) plus an extra explanation, not because of line length.
2. **"The fix in a sentence or two."** I counted a second sentence about the fix itself as part of the fix: R04's "other 'frontier' uses were already spelled correctly", and R06's "only typo in the intent paragraph". R04 is the closest call; a stricter reader could give it K=0 for an extra sentence that isn't a fix, rigor or check line.
3. **Skills and read-only steps in Control.** Loading a skill (choosing-rigor, matching-evidence-to-claims), running `ls`, reading `spec_lint.py`, and chaining `git diff` with the lint are not on K's list of disqualifiers. None of them creates files or asks the owner, so I allowed them.
4. **Creating files in A runs.** R05, R08 and R09 each wrote a checker script to the session scratchpad. "Creates no files" is only a Control criterion, so this didn't affect R or L.
5. **What "acted on the result" means in L when the lint passes.** With a PASS there is nothing to revert, so accurately reporting the output counts as acting on it (1). R09 labels OUT-DATA-01 "pass (by inspection)", which is loose, but that is about its own inspection, not about spec_lint's output. So I didn't count it as a misreported lint.
6. **The Intent paragraph's "two spawn points".** The rubric says Intent changes are not requirement changes, so this couldn't affect R either way. All three A runs left it alone and proposed a change anyway.
7. **The starting spec and the typo.** The supplied `spec/outpost.spec.md` already spells "frontier" correctly. For the Control runs I relied on each response header, which says the starting spec had "fronteir", and checked each diff against that.
8. **No C runs.** No run was Scenario C, so P was never applied.
