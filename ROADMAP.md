# Roadmap

ELAD grows only when evidence shows a change helps. Each item says what would show it.

## Toward 1.0

1. **Test automatic triggering in a real install.** *Done in v0.7, in real headless
   installs.* See the [triggering](skills/evidence/TRIGGERING_TEST.md) and
   [engagement](skills/evidence/ENGAGE_TEST.md) tests.
   - **Repeat it** on another model or harness, or on a non-Windows machine, before
     claiming the result more widely.
2. **Use ELAD on one real project.**
   - Adopt the spec format, the ladder, and the skills on a real project, through that
     project's own decision.
   - Record what helped, what was ignored, and what got in the way.
   - Bring back synthetic lessons only.

Item 2 is the remaining condition for `1.0`; see [Releasing](docs/RELEASING.md).

## Skills

- **Scenarios not yet tested:** 3 (fall-through report), 5 (shared generator refactor),
  and 6 (publishing).

## S&box next steps

These are the next steps for improving ELAD on S&box projects. Each one gets a rubric and
decision rule committed before any run, and blind scoring.

1. **Pressure-test the S&box domain skill.** `examples/sbox/skills/sbox-engine-reference`
   has never been tested.
   - **Scenarios.** Build synthetic S&box coding scenarios from the engine-rung spike kit:
     "players fall through the floor near the gate", "write the engine test for
     OUT-SPAWN-01", and "the generated wall has no collision in game".
   - **Triggering.** Check whether the skill loads on its own.
   - **Behavior.** Check whether agents follow what it teaches:
     - read `logs\testhost.log` when a component silently fails;
     - create a `MeshComponent` disabled, assign it, then enable it;
     - register the stand-in default surface in test setup;
     - use the enclosure probe, not `StartedSolid` alone; and
     - compare the installed `.version` with the engine source.
2. **Package a rung-1 starter.** Turn the
   [engine-rung spike](examples/sbox/engine-rung-spike/README.md) into a copyable
   `examples/sbox/rung1-starter/`, containing:
   - test setup with the labelled default-surface scaffolding;
   - player helpers;
   - the enclosure-probe stuck check;
   - the saved-scene JSON loader; and
   - one test named after a requirement.

   It stays unbuilt until the owner compiles it once with a short card. Then test it
   with step 1's scenarios.

## Examples

- **A second, non-game target example,** to check that the rung names and the skills
  carry over.
- **S&box:** saved scenes that reference prefabs or collision models, and generated
  geometry saved into a scene. These are still open after the
  [spike](examples/sbox/README.md#what-the-spike-settled).

## Not planned

These stay archived at the `v0.5` tag unless a real need appears:

- schemas;
- packets and receipts;
- the lifecycle oracle; and
- the maturity levels.

A need would be repeated cross-context handoffs that plain specs and test output can't
support.
