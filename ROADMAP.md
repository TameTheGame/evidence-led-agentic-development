# Roadmap

ELAD grows only when evidence shows a change helps. Each item says what would show it.

## Toward 1.0

1. **Test automatic triggering in a real install.** *Done in v0.7, in real headless
   installs.* See the [triggering](skills/evidence/TRIGGERING_TEST.md) and
   [engagement](skills/evidence/ENGAGE_TEST.md) tests.
   - **Repeat it** on another model or harness, or on a non-Windows machine, before
     claiming the result more widely.
2. **Use ELAD on one real project.** *Done in v1.0, on a private S&box project.* See
   [A first real project](docs/EMPIRICAL_STATUS.md#a-first-real-project-v10).
   - **Repeat it** on a project whose owner doesn't maintain ELAD, and record whether the
     skills are used, before claiming more.

Both conditions for `1.0` in [Releasing](docs/RELEASING.md) are met.

## Skills

- **Scenario not yet tested:** 6 (publishing). Scenario 3 (fall-through report) has only
  been run inside the S&box [domain-skill test](skills/evidence/SBOX_SKILL_TEST.md) and
  [live retest](skills/evidence/LIVE_TEST.md), with a planted engine bug. Scenario 5 (shared
  generator refactor) was tested in the [refactor rerun](skills/evidence/REFACTOR_TEST.md):
  agents reran every shared check after the change but none before, and rated it light
  rather than raising rigor.

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
3. **Retest live with the starter.** *Done; see the
   [live retest](skills/evidence/LIVE_TEST.md).* It failed its rule on the refactor
   scenario alone, which didn't test refactoring. Every geometry test had a default
   surface (18 of 18), and tests failed before fixes in 11 of 12 runs, so the "watch it
   fail first" fallback isn't needed. Without the domain skill, agents fixed the planted
   bug too, guided by the starter's own code.
4. **Retest scenario 5 on its own.** *Done; see the
   [refactor rerun](skills/evidence/REFACTOR_TEST.md).* In a project whose two areas share
   the generator, with a request that names the change, all 6 runs refactored and reran
   every shared check afterwards. None ran them before, so it failed its rule. A
   "baseline first" rule for shared surfaces is proposed, but untested.

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
