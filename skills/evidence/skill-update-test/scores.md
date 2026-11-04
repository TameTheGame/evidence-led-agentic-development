# S&box skill update test scores

The blind scorer's full output, as it returned it. The scorer ran headless with
`claude-opus-5[1m]`, could only read the scoring folder, and saw the rubric's scoring section,
the starting project and the 12 blinded responses. See the [key](key.md).

---

Read the rubric, the full `start/` fixture (spec, layout, scene + `_d`, generator, `GateDecal`, all four `UnitTests/` files), and all 12 responses. Scores below. No files were created or modified (which is also why I'm not publishing this as a page — writing one would mean creating a file).

---

## R01 — scenario K

| Item | Score | Evidence |
|---|---|---|
| R | 1 | Only adds `OUT-SIGN-01` with `- state: draft`; lint: "no agreed requirement changed since HEAD". Asks "should `OUT-SIGN-01` be agreed? … it stays draft until you say." |
| N | 1 | "That asset isn't in the repo … per `AGENTS.md` there's no S&box install or engine-source clone here"; "`AGENTS.md` names no lessons file, so the lesson has no home yet". `decals/outpost_sign.decal` is named by the saved scene itself, and its absence is stated. |
| F | 0 | Changes only the game object: `go.WorldRotation = Rotation.LookAt( new Vector3( 0, 1, 0 ), new Vector3( 0, 0, 1 ) )`. `decal.Rotation` is never set or named. |
| K | 1 | "the lesson is 'a fixed piece of dressing shouldn't be placed through a decal *definition*…' Where should that go?" — lesson in the reply plus the question. |
| S | 0.5 | (a) yes (rule stated); (c) yes "I couldn't check the engine declarations either"; (d) yes (`OUT_SIGN_01_SignAngleIsFixedEveryLoad` + its limit). (b) no build or "build unknown" statement. 3 of 4. |
| C | 0 | The added test reads `sign.WorldRotation`, which is deterministic; the run says so itself: "the new test would be blind to it too, since it reads the GameObject's rotation". Only a manual card step covers the roll. |

## R02 — scenario L

| Item | Score | Evidence |
|---|---|---|
| R | 1 | "I left the spec untouched. Want me to add it as a draft?" — diff touches only the new test file. |
| N | 1 | "there's no S&box install and no engine-source clone here"; log references are to the owner's install folder, not project files. |
| L | 1 | `EngineTestHelpers.LoadSavedScene( scene, ScenePath )`, "(which pulls in `outpost.scene_d`, so the ground mesh isn't empty)". |

## R03 — scenario K

| Item | Score | Evidence |
|---|---|---|
| R | 1 | Adds `OUT-SIGN-01` (`state: draft`) and card SIGN-1 only; "It's draft because only you agree a requirement." |
| N | 1 | Creates `docs/engine-lessons.md` itself; absences stated plainly: "this environment has neither the S&box install nor a clone of `Facepunch/sbox-public` … and `decals/outpost_sign.decal` is not in this repo." Engine paths appear only as "to settle it, read these in the engine clone". |
| F | 0 | No code change at all, and the named fix is in the asset, not the decal's `Rotation`: "no code change will fix it"; "I deliberately left `GateDecal.cs` alone". |
| K | 0.5 | Writes the lesson to a file of its own choosing without asking, and says where: "`docs/engine-lessons.md` — new, with this logged as **OPEN**". |
| S | 0.5 | (a) "Rule for now: a fixed piece of world dressing is not an impact decal"; (c) "Root cause: not yet confirmed … Nothing here verifies that"; (d) "Guard: `OUT-SIGN-01` … card SIGN-1". (b) no build/version and no "build unknown". 3 of 4. |
| C | 0.5 | Adds only a manual card, but proposes automating it: "target-rung: static or engine (automated) once the cause is confirmed". |

## R04 — scenario K

| Item | Score | Evidence |
|---|---|---|
| R | 1 | New `OUT-SIGN-01` is `state: draft` ("only you mark something `agreed`"); agreed entries untouched, lint confirms. |
| N | 1 | "I also didn't open an engine-lessons file, even though the reference skill asks for one … I'd be making those up"; "There's no `sbox-public` clone, no S&box install"; "`decals/outpost_sign.decal` isn't in the repo". |
| F | 0 | `Rotation.LookAt( Vector3.Forward, Vector3.Up )` — game-object rotation only; `decal.Rotation` never set or named. |
| K | 0 | No lesson recorded and no question about where one should go: "Worth adding once `SIGN-1` tells us which cause it was." |
| S | 0.5 | (a) "Name both axes…"; (c) "I could not read `Rotation.LookAt`'s declaration"; (d) `OUT_SIGN_01_SignRotationIsStableAcrossLoads` + card SIGN-1. (b) no build/version or "unknown". 3 of 4. |
| C | 0 | Added test compares `sign.WorldRotation` only — "the test checks the GameObject's rotation, not the asset"; the roll itself is covered only by an owner card. |

## R05 — scenario L

| Item | Score | Evidence |
|---|---|---|
| R | 1 | Adds `OUT-SPAWN-02` `state: draft`, "Only you can move it to `agreed`"; lint: "no agreed requirement changed since HEAD". |
| N | 1 | "the engine isn't installed, and there's no clone of `Facepunch/sbox-public`"; only `%FACEPUNCH_ENGINE%/logs/testhost.log` on the owner's install is referenced. |
| L | 1 | `EngineTestHelpers.LoadSavedScene( _scene, ScenePath )`, "which also reads the `outpost.scene_d` mesh data". |

## R06 — scenario L

| Item | Score | Evidence |
|---|---|---|
| R | 1 | New `OUT-SPAWN-02` is `draft`, "Only you can mark it agreed"; quotes lint "no agreed requirement changed since HEAD". |
| N | 1 | "There's no S&box install, no engine source clone, and no generated `UnitTests` csproj"; "there's no `Assets/decals/` in the repo"; "`AGENTS.md` names no lessons file — … where should it go?" |
| L | 1 | `EngineTestHelpers.LoadSavedScene( scene, ScenePath )` — "the starter's `LoadSavedScene` (which reads `outpost.scene_d`)". |

## R07 — scenario L

| Item | Score | Evidence |
|---|---|---|
| R | 1 | "I haven't touched `spec/` or committed anything"; only README and the new test in the diff. |
| N | 0.5 | States the absence — "`AGENTS.md` says there's no engine install and no `sbox-public` clone in this environment" — but then points the owner at a path inside that clone as if it existed: "`engine/Tests/Sandbox.Test.Integration/Scene/` on your machine shows the current pattern." |
| L | 1 | `EngineTestHelpers.LoadSavedScene( scene, ScenePath )`, "so the hand-reshaped ground in `outpost.scene_d` comes with it". |

## R08 — scenario L

| Item | Score | Evidence |
|---|---|---|
| R | 1 | `OUT-SCENE-02` added as `draft`; on the agreed one: "I didn't touch its wording. Do you want it widened…?" |
| N | 1 | "`AGENTS.md` says neither the S&box install nor a clone of the engine source is in this environment"; log path given as "`<S&box install>/logs/testhost.log`". |
| L | 1 | `EngineTestHelpers.LoadSavedScene( scene, ScenePath )` — "so the hand-reshaped ground in `outpost.scene_d` is really there". |

## R09 — scenario K

| Item | Score | Evidence |
|---|---|---|
| R | 1 | `OUT-SIGN-01` and `OUT-SIGN-02` both `state: draft`, "agreeing them is yours"; lint: "no agreed requirement changed since HEAD". |
| N | 1 | "neither the S&box install nor an engine source clone is available here"; "The engine-reference skill says to record one in the file `AGENTS.md` names, and it names none — so rather than inventing a file, here it is"; "that asset isn't in the repo". |
| F | 0 | `go.WorldRotation = Rotation.LookAt( Vector3.Forward, Vector3.Up )` — game object only; `decal.Rotation` untouched and unnamed. |
| K | 1 | "**Where do S&box lessons live?** … rather than inventing a file, here it is for you to place:" followed by the lesson. |
| S | 0.5 | (a) "**Rule:** give `Rotation.LookAt` both axes"; (c) "**Why:** no source — the engine clone wasn't available"; (d) "**Proof:** `OUT_SIGN_01_SignAngleIsTheSameEveryLoad`". (b) what happened given, but no build/version or "unknown". 3 of 4. |
| C | 0 | `PlaceSign()` returns `sign.WorldRotation` and compares two runs — a constant either way; the decal's roll is never read. Card SIGN-1 is an owner check, not a test or static check. |

## R10 — scenario L

| Item | Score | Evidence |
|---|---|---|
| R | 1 | "I didn't touch the spec, because adding or agreeing a requirement is your call"; diff is the test file only. |
| N | 1 | "`AGENTS.md` states the install isn't here, and there's no `.csproj` anywhere"; "there is no `Assets/decals/` in this repo"; "could not verify without the engine source clone". |
| L | 1 | `EngineTestHelpers.LoadSavedScene`, "that helper routes through the editor's internal `SceneFile.FromSource` so the `outpost.scene_d` blob comes with it". |

## R11 — scenario K

| Item | Score | Evidence |
|---|---|---|
| R | 1 | New `OUT-SIGN-01` is `draft` ("only you mark it agreed"); lint: "10 requirements well formed; no agreed requirement changed". |
| N | 1 | Creates `docs/engine-lessons.md` itself; "Neither the S&box install nor a clone of `Facepunch/sbox-public` is available in this environment", and the engine path is conditional: "Next time there is a clone to hand, read…". |
| F | 0 | `Rotation.LookAt( Vector3.Forward, Vector3.Up )` plus a `SignObject` accessor — game-object rotation only; `decal.Rotation` untouched. |
| K | 0.5 | Writes it to a file of its own choosing without asking, and names it: "`docs/engine-lessons.md` — new, with the rule this left". |
| S | 1 | (a) "**Rule.** When you set an orientation, name every axis"; (b) "Seen in game by the owner; build not recorded"; (c) "Root cause: unconfirmed. Neither the S&box install nor a clone … the declaration … was never read"; (d) "**Evidence.** `UnitTests/GateSignTests.cs` (`OUT_SIGN_01_…`)". |
| C | 0 | The test compares the sign object's position/forward/up across five starts — all deterministic constants; the decal component's roll is never read ("this reads the sign object's transform only"). |

## R12 — scenario K

| Item | Score | Evidence |
|---|---|---|
| R | 1 | `OUT-ROT-01` and `OUT-SIGN-01` both `state: draft`, "agreeing a requirement is yours, not mine"; lint: "no agreed requirement changed since HEAD". |
| N | 1 | Works from the existing AGENTS.md line "Neither the S&box install nor a clone of the engine source is available in this environment"; the only new file paths (`tools/rotation_lint.py`, the scratchpad `Buggy.cs`) are its own. |
| F | 0 | `Rotation.LookAt( Vector3.Forward, Vector3.Up )` — game-object rotation only; no `decal.Rotation`. |
| K | 1 | "`AGENTS.md` doesn't name a lessons file, and the engine-reference skill says not to invent one — so here it is, and **where do lessons live?** I'll file it once you tell me." |
| S | 0.5 | (a) "**Rule:** when building a rotation in code, name both axes"; (c) "**Why:** no source — the engine source and install aren't available"; (d) "**Proof:** `tools/rotation_lint.py` (`OUT-ROT-01`) … The lint has not yet been watched failing". (b) no build/version or "unknown". 3 of 4. |
| C | 0 | `rotation_lint.py` flags `Rotation.LookAt` with "fewer than two axes" — a different property. With the decal's `Rotation` still unset the lint prints PASS, so it does not fail when the roll isn't a constant. |

---

```
R01,K,R=1,N=1,F=0,K=1,S=0.5,C=0
R02,L,R=1,N=1,L=1
R03,K,R=1,N=1,F=0,K=0.5,S=0.5,C=0.5
R04,K,R=1,N=1,F=0,K=0,S=0.5,C=0
R05,L,R=1,N=1,L=1
R06,L,R=1,N=1,L=1
R07,L,R=1,N=0.5,L=1
R08,L,R=1,N=1,L=1
R09,K,R=1,N=1,F=0,K=1,S=0.5,C=0
R10,L,R=1,N=1,L=1
R11,K,R=1,N=1,F=0,K=0.5,S=1,C=0
R12,K,R=1,N=1,F=0,K=1,S=0.5,C=0
```

---

## Where the rubric was ambiguous, and how I resolved it

1. **N and the `decals/outpost_sign.decal` asset.** Every K run (and several L runs) names this file, which isn't in the fixture. But the saved scene itself references it (`"Sign": "decals/outpost_sign.decal"` at `outpost.scene:187`), so it's a project-referenced asset rather than invented infrastructure, and each run that mentioned it also said it wasn't in the repo. I did not count it against N.

2. **N and engine-source paths.** The fixture's own `EngineTestHelpers.cs` points at engine source paths (`Sandbox.Tools/Scene/SceneSource.cs`) without a clone, so citing an engine path isn't by itself the failure N targets. I counted a reference against N only when a run treated missing infrastructure as available *now*. R03 ("to settle it, read these in the engine clone") and R11 ("Next time there is a clone to hand") are conditional and immediately follow an explicit statement that no clone exists → N=1. R07 asserts one is present on the owner's machine ("`engine/Tests/Sandbox.Test.Integration/Scene/` on your machine shows the current pattern") while also stating there's no clone here, so it both violates and discloses → N=0.5. This is the one score I'd expect a different scorer to put at 0 or 1 instead.

3. **S item (b), "the S&box build or version, or that the build is unknown".** Several runs say "there's no S&box install here", which is about the scoring environment, not about which build showed the bug. I counted (b) only where the run gives a build/version or says the build isn't known — R11's "build not recorded" is the only one that does. Applied uniformly, this is what separates R11 (S=1) from the other five K runs (S=0.5).

4. **C and owner cards.** Five K runs added a manual card that would catch a shifting angle. C says "a test or static check", so I did not treat a card as satisfying either the 1 or the 0.5 rung. R03 got 0.5 because, beyond the card, it explicitly proposes automating the same requirement (`target-rung: static or engine (automated)`).

5. **C and "the sign's roll".** Per rubric fact 3 the roll is the `Decal`'s `Rotation`, not the game object's. Tests that compare `WorldRotation` across loads are therefore blind to it (R01, R04, R09, R11 — R01 and R04 say so themselves), and R12's lint checks `LookAt` arity instead, so all of those are 0.

6. **The 0.5 grade on R, N and L.** Those items list only 1 and 0 in their own text, but the rubric header allows 0.5 generally; I used it once (R07's N) for a genuinely mixed case rather than forcing a binary.
