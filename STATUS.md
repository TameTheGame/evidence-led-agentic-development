# Status

**Current version:** `1.02`

**What ELAD is:**

- the spec format, in [docs/SPEC_FORMAT.md](docs/SPEC_FORMAT.md);
- the evidence ladder, in [docs/EVIDENCE_LADDER.md](docs/EVIDENCE_LADDER.md);
- three skills, in [skills/](skills/README.md); and
- one page of authority and safety rules, in
  [docs/AUTHORITY_AND_SAFETY.md](docs/AUTHORITY_AND_SAFETY.md).

The S&box example in [examples/sbox/](examples/sbox/README.md) is target-specific and
non-normative.

**Authority:** none. ELAD runs nothing and grants nothing. Each project's owner and
`AGENTS.md` decide what agents may do.

## Evidence

- **A first real project** (v1.0). A private S&box project used the spec format and the
  ladder through a pilot and a first world slice, which passed all 18 machine checks and
  its owner's review. Its records show no use of the skills. See
  [Empirical Status](docs/EMPIRICAL_STATUS.md#a-first-real-project-v10).
- **Two pressure-test rounds.** The clearest effect appeared in both: with the skills,
  agents recommended a better rule than "one try, then stop forever". Round 2 confirmed it
  with three samples per cell. Round 1 was mixed elsewhere: on one scenario the skills
  scored lowest. The tests were dry runs with small samples, scored blind by a model. See
  [skills/evidence/](skills/evidence/PRESSURE_TEST_RESULTS.md).
- **Real headless installs.** These were acting Claude Code sessions, told nothing about
  the skills.
  - **The [triggering test](skills/evidence/TRIGGERING_TEST.md)** found gaps in the v0.6
    skills.
  - **The [engagement test](skills/evidence/ENGAGE_TEST.md)** confirmed the v0.7
    configuration in a pre-registered, blind-scored check. The skills loaded on their own,
    agreed requirements were left to the owner in 3 of 3 east-spawn runs, the probe pushed
    back in 2 of 3, and a typo fix stayed light in 3 of 3.
- **One engine-rung spike.** It proved headless rung-1 checks on S&box `26.10.02`, on
  Windows.
- **The S&box domain-skill test** (v0.8). The example `sbox-engine-reference` skill
  loaded on its own in 9 of 9 runs and passed its pre-registered, blind-scored rule. With
  it, agents fixed a planted engine bug in 6 of 6 runs, against 0 of 6 without it. See
  [the test](skills/evidence/SBOX_SKILL_TEST.md).
- **The S&box live retest** (v0.8). The same scenarios ran in compiled projects with
  the [rung-1 starter](examples/sbox/rung1-starter/README.md), and agents could run the
  engine tests. Every geometry test had a default surface, tests failed before fixes in 11
  of 12 runs, and reference probes confirmed the fix in 12 of 12, with or without the
  domain skill. The rule failed only on a refactor scenario that didn't fit its project.
  See [the retest](skills/evidence/LIVE_TEST.md).
- **The S&box refactor rerun** (v0.8). With two areas sharing the generator and a
  named change, all 6 runs refactored and reran every shared check afterwards, and
  reference probes confirmed the build in 6 of 6. The rule failed because no run ran those
  checks before the change. See [the rerun](skills/evidence/REFACTOR_TEST.md).
- **Four reference-project experiments** against v0.3.0. They are historical; see
  [Empirical Status](docs/EMPIRICAL_STATUS.md).

## Gaps

- **Tested, within limits:** automatic skill triggering. It was tested in real headless
  installs with three runs per cell, one model, one harness, and Windows only.
- **Met for `1.0`:** use on one real project. It's one project, owned by ELAD's
  maintainer, so it isn't independent adoption, and its records show no use of the skills.
  See [Releasing](docs/RELEASING.md).
- **S&box next steps:** all four on the [roadmap](ROADMAP.md#sbox-next-steps) are done.
  The refactor rerun proposed two "baseline first" rules for shared checks. Each needs its
  own pressure test before any skill changes.
- **Still open in the S&box example:** saved scenes that reference prefabs or collision
  models.

## History

Through v0.5, ELAD was a protocol blueprint, with schemas, templates, validators, and an
authenticated bundle. Those are archived at the `v0.5` tag; see [Archive](ARCHIVE.md).
