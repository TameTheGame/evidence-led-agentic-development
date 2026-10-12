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

- **Scenarios not yet tested:** 5 (shared generator refactor) and 6 (publishing). Scenario 3
  (fall-through report) has only been run inside the
  [S&box domain-skill test](skills/evidence/SBOX_SKILL_TEST.md), with a planted engine bug.

## S&box next steps

These are the next steps for improving ELAD on S&box projects. Each one gets a rubric and
decision rule committed before any run, and blind scoring.

1. **Pressure-test the S&box domain skill.** *Done; see the
   [domain-skill test](skills/evidence/SBOX_SKILL_TEST.md).* The skill loaded on its own and
   passed its rule. Agents knew a default physics surface was needed, but none could write
   the scaffolding without the spike kit's code.
2. **Package a rung-1 starter.** *Done; see the
   [rung-1 starter](examples/sbox/rung1-starter/README.md).* It passed 5 of 5 on S&box
   `26.10.02`. Its runner surfaced the engine's hidden component error in a control run.
3. **Retest live with the starter.** Rerun step 1's scenarios in a real compiled project
   that has the starter, with agents allowed to run its runner.
   - Use step 1's results as the baseline.
   - Add scenario 5 (shared generator refactor).
   - Runs go one at a time, because the engine log is shared.
   - Success means agents wire up the default surface instead of only naming it, and get
     a test to fail before they fix.

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
