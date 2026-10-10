# S&box domain-skill test scores

This is the blind scorer's full output. Its prompt is in [scorer-prompt.md](scorer-prompt.md),
and the labels are decoded in [key.md](key.md).

## 1. Per-run scores

**R01 (T)**
- R=1: the spec is untouched. The reply says "I didn't touch the spec", and lint reports
  "no agreed requirement changed".
- D=0: the test calls `OutpostGenerator.Build`, but the run never mentions a `default`
  surface.
- G=0: it asks the owner to run `dotnet test`, but names no engine log.
- V=N.
- E=0: the room-to-stand check is a zero-length `Trace.Box` using `Hit || StartedSolid`, and
  the run doesn't say this misses bodies inside mesh collision.
- H=0: no player is simulated.
- C=1: card step 3 says to set "spawn.south… [400, 0, 8]" and "Expect: RED… (that spot is
  inside the tower)".

**R02 (F)**
- R=1: the spec is unchanged and lint passes.
- D=0.5: it says "no `default` physics surface is loaded in tests… needs the spike kit's
  `TestSurfaces.cs`", but adds no setup code.
- G=1: "`logs/testhost.log` in the S&box install folder has the engine's own errors."
- V=N.
- M=1: it changes the code to `Create<MeshComponent>( startEnabled: false )` …
  `block.Enabled = true;`, with the correct diagnosis.
- X=1: `CollisionTests.cs` is written at step 16, before the generator is edited at step 17.

**R03 (F)**
- R=1: the spec is unchanged.
- D=0: it adds an engine test that builds the generator's geometry, with no mention of a
  surface.
- G=0: it asks the owner to run the tests, but names no log.
- V=N.
- M=0: its suspect is "`Collision` *before* `Mesh`", with the fix "Reordering those two
  lines". It never identifies enable order.
- X=1: "I deliberately left `OutpostGenerator.cs` untouched" and it asks the owner to run
  the test first.

**R04 (F)**
- R=1: it only adds OUT-COLL-02 as `draft` ("stays `draft` until you agree it"). The layout
  data change touches no requirement.
- D=0: it proposes "With that I can write `OUT_COLL_01_EveryFloorHasCollision`", but
  doesn't mention a surface.
- G=NA: the only card is an in-game walk, not an engine test run.
- V=N.
- M=0: it offers the Collision-before-Mesh hypothesis, and its fix is a layout overlap.
- X=0: it adds no engine test.

**R05 (W)**
- R=1: the new requirement OUT-WALL-01 is `draft`.
- D=0: no surface mention.
- G=0: the card says "dotnet test", with no log.
- V=N.
- M=0.5: it applies the workaround, "each generated block now gets its own `BoxCollider`",
  and the MeshComponent is still created enabled.

**R06 (W)**
- R=1: OUT-COLL-02 is `draft`.
- D=0.
- G=0.
- V=N.
- M=0.5: it misdiagnoses the cause as "no collider component" and adds a `BoxCollider` to
  each block as a workaround.

**R07 (W)**
- R=1: OUT-COLL-02 is `draft`.
- D=0.5: "no `default` physics surface is loaded, and a mesh rebuild throws without one…
  Writing the reflection-based surface stand-in needs the engine source". No setup code.
- G=1: "open `logs/testhost.log` in the S&box install folder".
- V=N, borderline (see section 3).
- M=1: it diagnoses enable order and fixes it with create-disabled / assign / enable.

**R08 (T)**
- R=1.
- D=0.
- G=0.
- V=N.
- E=0.5: the check relies on `room.Hit || room.StartedSolid`, but the run flags "If the
  physics layer returns nothing for a box that starts inside mesh geometry, the
  room-to-stand leg is blind".
- H=0: one `GameTick`, no `PlayerController`.
- C=1: `CheckRejectsKnownBadSpawns` includes the case "inside the north wall" at
  (0, 780, 8).

**R09 (T)**
- R=1.
- D=0.5: "No `default` physics surface… `UnitTests/` has no stand-in". No setup code.
- G=1: "Copy logs/testhost.log out of the S&box install folder".
- V=N.
- E=1: the `Buried` probe uses a ray out to the sky and a ray back ("Out-ray misses…
  back-ray hits ⇒ buried").
- H=0: no player is simulated.
- C=1: `Control_PointInsideTheTowerIsBuried`.

**R10 (W)**
- R=1: OUT-COLL-02 is `draft`.
- D=0.5: "no `default` physics surface is loaded… Want me to add it?", plus a placeholder
  comment saying to "Register the stand-in… in test setup first".
- G=NA: the only card is the NET-1 session card, and the owner is never asked to run
  `dotnet test`.
- V=N.
- M=1: `Create<MeshComponent>( false )` … `block.Enabled = true;`.

**R11 (T)**
- R=1.
- D=0.
- G=0.
- V=N.
- E=0: a zero-length capsule trace using `Hit || StartedSolid`, with no caveat.
- H=0.
- C=0: the control hull is in "Open air… close enough that the hull's 16-unit radius reaches
  into wall.north". That clips a block; it isn't placed inside one.

**R12 (W)**
- R=1: OUT-COLL-02 is `draft`.
- D=0.
- G=0.
- V=N.
- M=0.5: it "now also creates a static `BoxCollider`", a workaround that doesn't fix the
  build.

**R13 (F)**
- R=1.
- D=0.5: it catches the error and returns `Inconclusive`, saying "copy TestSurfaces.cs… and
  register the stand-in". No setup code.
- G=1: the test message says "Check logs\testhost.log in the S&box install folder for the
  engine's own error".
- V=N, borderline.
- M=1: create disabled, assign, then enable.
- X=0.5: the generator is edited at step 16, before the test is written at step 17.

**R14 (F)**
- R=1: OUT-COLL-02 is `draft`.
- D=0.
- G=0.
- V=N.
- M=0: its hypothesis is "`Collision` set *before* `Mesh` is assigned", not enable order.
- X=1: "I have **not** changed the layout or the generator", and it adds the test.

**R15 (T)**
- R=1.
- D=0.5: "`PolygonMesh.Rebuild()` needs a loaded `default` physics surface… this project
  doesn't have that file". No setup code.
- G=1: "the last 30 lines of logs/testhost.log from your S&box install folder".
- V=N.
- E=1: `AssertStandingColumnClear` sweeps the capsule down from above the layout, so it
  doesn't rely only on `StartedSolid`.
- H=0.
- C=1: card step 3 says "[400, 0, 8] (inside the tower)… step 4 is RED naming 'tower'".

**R16 (F)**
- R=1.
- D=0.5: "there's no `default` physics surface, and mesh blocks can't build without one…
  send me that file". No setup code.
- G=1: "If it goes red, also copy logs/testhost.log from the S&box install folder."
- V=N.
- M=1: create disabled, assign, then enable.
- X=0.5: the generator is edited at step 20, before the test is written at step 21.

**R17 (W)**
- R=1: OUT-COLL-02 is `draft`.
- D=0.5: "there may be no `default` physics surface loaded, which makes mesh building
  throw". No setup code.
- G=1: the test messages say to "read logs\testhost.log in the S&box install folder".
- V=N.
- M=1: create disabled, assign, then enable.

**R18 (T)**
- R=1.
- D=0: it never mentions a `default` surface.
- G=1: "logs/testhost.log from the S&box install folder", and the code notes that errors
  are "caught and logged rather than thrown".
- V=N, borderline.
- E=1: `EnclosedBy` sends a ray out to the first face and traces back, in six directions.
- H=0.
- C=1: card step 3 says "[400, 0, 8] — that puts it inside the tower… Expect: RED".

## 2. Final block

```text
R01,T,R=1,D=0,G=0,V=N,E=0,H=0,C=1
R02,F,R=1,D=0.5,G=1,V=N,M=1,X=1
R03,F,R=1,D=0,G=0,V=N,M=0,X=1
R04,F,R=1,D=0,G=NA,V=N,M=0,X=0
R05,W,R=1,D=0,G=0,V=N,M=0.5
R06,W,R=1,D=0,G=0,V=N,M=0.5
R07,W,R=1,D=0.5,G=1,V=N,M=1
R08,T,R=1,D=0,G=0,V=N,E=0.5,H=0,C=1
R09,T,R=1,D=0.5,G=1,V=N,E=1,H=0,C=1
R10,W,R=1,D=0.5,G=NA,V=N,M=1
R11,T,R=1,D=0,G=0,V=N,E=0,H=0,C=0
R12,W,R=1,D=0,G=0,V=N,M=0.5
R13,F,R=1,D=0.5,G=1,V=N,M=1,X=0.5
R14,F,R=1,D=0,G=0,V=N,M=0,X=1
R15,T,R=1,D=0.5,G=1,V=N,E=1,H=0,C=1
R16,F,R=1,D=0.5,G=1,V=N,M=1,X=0.5
R17,W,R=1,D=0.5,G=1,V=N,M=1
R18,T,R=1,D=0,G=1,V=N,E=1,H=0,C=1
```

## 3. Where the rubric was ambiguous

- **C: does a control case written only in the owner's card count as "adds a case"?** This
  affects R01, R15 and R18. I counted it (C=1). D explicitly says "setup code", but C says
  only "a case", and each card step defines a case that must go red with a body inside the
  tower. A stricter reading that requires test code would make all three 0.
- **C: is a body partly overlapping a block "placed inside a block"?** R11's hull is placed
  in open air and clips 8 units into a wall face, so I gave 0. R08 places the spawn point
  inside the north wall and describes it that way, so I gave 1, even though its box sticks
  about 3 units out of the wall.
- **E for R08:** it relies on `Hit/StartedSolid` but states the blind spot conditionally
  ("If the physics layer returns nothing for a box that starts inside mesh geometry…
  blind"). I treated that as "says that misses" (0.5). A stricter reading would give 0.
- **G: where the log is named, and how explicitly.** R13, R17 and R18 name `testhost.log`
  partly or only inside the test's failure messages, not the reply; I counted the diff as
  part of the run. R16 only asks the owner to send `logs/testhost.log` if the test goes red,
  without saying outright that errors land there; I still gave 1, because it names the right
  file, in the right place, for test-run failures.
- **G=NA for R04 and R10:** neither asks the owner to run engine tests. R04's card is an
  in-game walk, and R10's is the NET-1 session card, though R10 does discuss what would
  block someone from running its test.
- **D for R04:** it adds no test, but its offer to write OUT_COLL_01 once it has the project
  file counts as proposing an engine test that builds generated geometry. So D=0, not NA.
- **R: non-requirement edits.** R04 edited the layout data, and several runs added new
  requirements as `draft`. None of this changes an agreed requirement's sentence, state,
  rung or check, and the drafts were put to the owner, so R=1 throughout.
- **V borderline cases (R07, R13, R18):** they say API signatures are "unverified against
  your build", and R18 says to confirm the player size "in the installed build". I read V as
  asking for a check of which S&box version is installed (for example, the `.version` file)
  against the source or docs relied on, so I marked them N. R09's search for a `version`
  file was denied and never mentioned in its reply, so it is also N.
- **M:** R03, R04 and R14 suspect that `Collision` is set before `Mesh`, which is not the
  enable-order cause, so M=0. R05, R06 and R12 add a `BoxCollider` to every block; the
  rubric names that as the 0.5 workaround, whatever the stated diagnosis.
- **X:** I went by the tool-call order as shown. R13 and R16 edit the generator before
  writing the test, so they get 0.5 even though their cards ask the owner to run the test on
  the old code first.
