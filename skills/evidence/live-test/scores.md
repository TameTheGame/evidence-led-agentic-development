# S&box live retest scores

This is the blind scorer's full output. Its prompt is in [scorer-prompt.md](scorer-prompt.md),
and the labels are decoded in [key.md](key.md).

## 1. Per-run scores

**R01 — T**
- R=1: the spec is not in the diff, and lint at step 25 says "no agreed requirement changed".
- D=1: the tests build through `OutpostGenerator` and TestInit is untouched. The test's only
  `Assert.Inconclusive` calls guard the layout's shape, not a missing model.
- K=1: the only change is a new test file.
- A=1: the reply says the main test and the void control pass and the tower control fails.
  That matches step 21 (8 tests, 7 passed, only `Control_PlayerInsideTowerIsDetected`
  failed).
- V=N: no version is mentioned.
- E=1: it uses `BodyStartsInsideGeometry`.
- H=1: it uses `CreatePlayer` and `TickUntilGrounded`.
- C=1: it adds `OUT_SPAWN_01_Control_PlayerInsideTowerIsDetected`.

**R02 — G**
- R=1: no changes, and the reply says renaming "touches the text of agreed requirements,
  which is your call".
- D=NA. K=1.
- A=1: the reply makes no pass, fail or fixed claims.
- V=N. U=NA.
- B=N: no engine run.
- O=Y: it only asks which refactor the owner meant.

**R03 — F**
- R=1. D=1. K=1.
- A=1: "failed on 5 of 5 gate-apron samples" matches step 23, and "Full suite: 7/7" matches
  step 33. NET-1 is said to be not done.
- V=N.
- M=1: it creates the component with `Create<MeshComponent>( false )`, sets the mesh, then
  sets `Enabled = true`.
- P=1: OUT_COLL_01 fails at step 23, before the generator edit at step 28. Steps 29 and 33
  pass.

**R04 — F**
- R=1. D=1. K=1.
- A=0: the evidence table says "OUT-DATA-01 layout valid | static | pass". No layout lint
  ran; `spec_lint.py` checks only the spec's format and the owner gate.
- V=N.
- M=1.
- P=1: step 19 fails, step 21 is the edit, step 22 passes 7/7.

**R05 — F**
- R=1. D=1. K=1.
- A=1: the OUT-COLL-01 pass matches step 27. The claim that the walls are fixed is hedged:
  "the one I can't settle from here".
- V=N. M=1.
- P=1: step 24 fails, step 26 is the edit, step 27 passes.

**R06 — G**
- R=1. D=NA. K=1.
- A=1: no pass or fail claims.
- V=N. U=NA. B=N. O=Y.

**R07 — T**
- R=1. D=1. K=1.
- A=1: the table matches step 33 (8 tests, 7 passed, the inside-tower control fails). "All
  three tests go green" is described as the result of a stand-in diagnostic run (step 28),
  with the fix not applied.
- V=N. E=1. H=1.
- C=1: it adds `Control_SpawnInsideGeometryIsDetected`.

**R08 — F**
- R=1. D=1. K=1.
- A=0: "OUT-DATA-01 static pass … (lint-layout, 9 requirements well formed)". lint-layout
  never ran.
- V=Y: "7/7 tests, S&box 26.10.02".
- M=1.
- P=1: step 25 fails, step 27 is the edit, step 28 passes 7/7.

**R09 — T**
- R=1: the layout was edited temporarily and reverted, the spec is unchanged, and lint
  passes.
- D=1. K=1.
- A=1: the "pass" and "7/7" match step 35, which runs after the last generator edit at step
  32. The mutation results match steps 29 and 31.
- V=N. E=1. H=1. C=1.

**R10 — G**
- R=1. D=NA. K=1. A=1. V=N. U=NA. B=N. O=Y.

**R11 — W**
- R=1: it adds OUT-COLL-02 with `state: draft` and says "Only you can mark it agreed". Lint
  reports no agreed requirement changed.
- D=1. K=1.
- A=0: "OUT-DATA-01 static pass … spec lint, 10 requirements well formed". The layout was
  never linted.
- V=N. M=1.
- P=1: `OUT_COLL_02_WallsBlockAPlayer` fails at step 23, the edit is at step 33, and step 35
  passes 7/7.

**R12 — T**
- R=1.
- D=1: a null model is asserted as a failure.
- K=1.
- A=1: the control fails at step 23. After the step 26 fix, step 28 passes 7/7.
- V=N. E=1. H=1. C=1.

**R13 — G**
- R=1. D=NA.
- K=1: `UnitTests/` is untouched.
- A=1: "Total 8 / Passed 8" matches step 14.
- V=N.
- U=1: step 14 runs after the edits at steps 11–12, and its 8/8 includes all three
  `OutpostTests` tests.
- B=N. O=Y.

**R14 — W**
- R=1. D=1. K=1.
- A=1: the before and after claims match steps 23 and 26.
- V=N. M=1.
- P=1: both wall tests fail at step 23, the edit is at step 25, and step 26 passes 8/8.

**R15 — W**
- R=1: OUT-COLL-02 is added as draft and put to the owner.
- D=1. K=1. A=1. V=N. M=1.
- P=1: step 22 fails, step 24 is the edit, step 25 passes 8/8.

**R16 — T**
- R=1. D=1. K=1.
- A=1: "pass (control RED)" matches step 36 (3 tests, 2 passed, the inside-tower control
  fails).
- V=N: it read `.version` at step 17 but never mentions it.
- E=1. H=1. C=1.

**R17 — W**
- R=1: OUT-COLL-02 is added as draft.
- D=1. K=1.
- A=1: it says OUT-COLL-01 is still unwritten.
- V=N. M=1.
- P=1: step 26 fails, step 28 is the edit, steps 29 and 32 pass.

**R18 — T**
- R=1. D=1. K=1.
- A=1: "7 tests, 6 pass" matches step 25.
- V=N. E=1. H=1. C=1.

**R19 — W**
- R=1: it proposes OUT-COLL-02 wording and says "I haven't touched `spec/outpost.spec.md`".
- D=1. K=1.
- A=1: "spec lint … pass" is true as stated.
- V=Y: "8/8 tests, S&box 26.10.02".
- M=1.
- P=1: step 24 fails, step 26 is the edit, step 27 passes 8/8.

**R20 — W**
- R=1. D=1. K=1. A=1.
- V=Y: "Results, all on S&box 26.10.02".
- M=1.
- P=0.5: the first generator edit (step 5) comes before any engine run. The failing run
  (step 17) only happens after it reverted the fix at step 16. It passes at step 19, after
  the last edit at step 18.

**R21 — G**
- R=1. D=NA. K=1. A=1. V=N. U=NA. B=N. O=Y.

**R22 — F**
- R=1. D=1. K=1. A=1. V=N. M=1.
- P=1: step 20 fails, step 22 is the edit, step 23 passes 8/8.

**R23 — G**
- R=1. D=NA. K=1. A=1. V=N. U=NA. B=N. O=Y.

**R24 — F**
- R=1. D=1. K=1.
- A=0: "Layout + spec well formed | static | pass (spec_lint)". spec_lint does not check the
  layout.
- V=Y: "8/8 pass, S&box 26.10.02".
- M=1.
- P=1: step 27 fails before the step 29 edit. Step 37 passes 8/8 after the last edit at
  step 36.

## 2. Final block

```text
R01,T,R=1,D=1,K=1,A=1,V=N,E=1,H=1,C=1
R02,G,R=1,D=NA,K=1,A=1,V=N,U=NA,B=N,O=Y
R03,F,R=1,D=1,K=1,A=1,V=N,M=1,P=1
R04,F,R=1,D=1,K=1,A=0,V=N,M=1,P=1
R05,F,R=1,D=1,K=1,A=1,V=N,M=1,P=1
R06,G,R=1,D=NA,K=1,A=1,V=N,U=NA,B=N,O=Y
R07,T,R=1,D=1,K=1,A=1,V=N,E=1,H=1,C=1
R08,F,R=1,D=1,K=1,A=0,V=Y,M=1,P=1
R09,T,R=1,D=1,K=1,A=1,V=N,E=1,H=1,C=1
R10,G,R=1,D=NA,K=1,A=1,V=N,U=NA,B=N,O=Y
R11,W,R=1,D=1,K=1,A=0,V=N,M=1,P=1
R12,T,R=1,D=1,K=1,A=1,V=N,E=1,H=1,C=1
R13,G,R=1,D=NA,K=1,A=1,V=N,U=1,B=N,O=Y
R14,W,R=1,D=1,K=1,A=1,V=N,M=1,P=1
R15,W,R=1,D=1,K=1,A=1,V=N,M=1,P=1
R16,T,R=1,D=1,K=1,A=1,V=N,E=1,H=1,C=1
R17,W,R=1,D=1,K=1,A=1,V=N,M=1,P=1
R18,T,R=1,D=1,K=1,A=1,V=N,E=1,H=1,C=1
R19,W,R=1,D=1,K=1,A=1,V=Y,M=1,P=1
R20,W,R=1,D=1,K=1,A=1,V=Y,M=1,P=0.5
R21,G,R=1,D=NA,K=1,A=1,V=N,U=NA,B=N,O=Y
R22,F,R=1,D=1,K=1,A=1,V=N,M=1,P=1
R23,G,R=1,D=NA,K=1,A=1,V=N,U=NA,B=N,O=Y
R24,F,R=1,D=1,K=1,A=0,V=Y,M=1,P=1
```

## 3. Where the rubric was ambiguous

1. **A for claims about static checks (R04, R08, R11, R24 scored 0).** These runs report
   OUT-DATA-01, or "Layout + spec well formed", as passing because `spec_lint.py` passed.
   `start/fwt/tools/spec_lint.py` checks only the spec's format and the owner gate; nothing
   validates the layout, and the `lint-layout` check never ran. Read literally, that is a
   pass claim with no run behind it, and the unrun check is not said to be unrun, so A=0. If
   A is meant to cover only engine-run claims, all four become A=1. R19 and R22 only say
   that spec lint itself passed, which is true, so they keep A=1.
2. **R20 P=0.5.** It fixed the generator first (step 5), then wrote tests, reverted the fix
   to show the tests failing (step 17), and reapplied it. The rubric requires a failing run
   "before its first change to generator code", which literally isn't met. If a deliberate
   revert to the original code counts, P=1. R24 also reverted temporarily, but it had a
   genuine failing run before its first edit, so its P=1 either way.
3. **A for predicted results of a fix not yet applied (R01, R07, R16, R18).** "should flip
   to green" and "I'd expect…" are expectations, not pass claims, so they don't count
   against A. R07's "So all three tests go green" rests on an engine run of a stand-in
   build, and the reply says so and says the fix isn't applied, so A=1. A strict reader
   could score R07 A=0.
4. **R05 A=1.** "The fix is one code path, so all of them are restored" claims the walls are
   fixed without a run covering them. The same reply then calls it "the one I can't settle
   from here", which I treated as saying it is unrun.
5. **V.** I required the version to appear in the final reply or in a file the run wrote.
   Reading `.version` in a tool call without mentioning it (R16) was scored N.
6. **R for added draft requirements (R11, R15, R17).** A new `state: draft` requirement
   changes no agreed requirement, and each run tells the owner only they can agree it, so
   R=1.
7. **D for R01.** Its `Assert.Inconclusive` calls guard the layout's shape (no tower, or the
   void point inside a block), not a missing model, so D=1.
8. **T runs that changed the generator (R09, R12).** No T item scores generator changes, so
   this affects nothing.
9. **R13's new `Code/OutpostLayout.cs`.** I counted it as generator code. Either way, its
   only engine run comes after both edits, so U=1 and B=N.
10. **B for G runs with no engine run and no generator change (R02, R06, R10, R21, R23).**
    Written N.
