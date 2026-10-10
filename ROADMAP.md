# Roadmap

ELAD grows only when evidence shows a change helps. Each item says what would show it.

## Toward 1.0

1. **Test automatic triggering in a real install.**
   - Install the three skills in a real agent tool without telling the agent to read them.
   - Check that each skill loads when its description matches the work, and stays out of
     the way when it doesn't.
   - Record the result under `skills/evidence/`.
   - **First run done** ([results](skills/evidence/TRIGGERING_TEST.md)). It found partial
     triggering.
   - **Next:** pressure-test the proposed `choosing-rigor` description, then rerun the
     probe and control scenarios. Success means it triggers on the probe in at least 2 of
     3 runs, with no added process on the control.
2. **Use ELAD on one real project.**
   - Adopt the spec format, the ladder, and the skills on a real project, through that
     project's own decision.
   - Record what helped, what was ignored, and what got in the way.
   - Bring back synthetic lessons only.

Both are needed for `1.0`; see [Releasing](docs/RELEASING.md).

## Skills

- **A round-3 pressure test,** if a skill changes. Add a rubric item for leaving agreed
  requirements unchanged until the owner agrees; round 2 showed the gap.
- **Scenarios not yet tested:** 1 (typo), 3 (fall-through report), 5 (shared generator
  refactor), and 6 (publishing).

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
