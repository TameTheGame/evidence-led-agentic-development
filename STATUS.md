# Status

**Current version:** `0.6`

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

- **Two pressure-test rounds.** The clearest effect appeared in both: with the skills,
  agents recommended a better rule than "one try, then stop forever". Round 2 confirmed it
  with three samples per cell. Round 1 was mixed elsewhere: on one scenario the skills
  scored lowest. The tests were dry runs with small samples, scored blind by a model. See
  [skills/evidence/](skills/evidence/PRESSURE_TEST_RESULTS.md).
- **One engine-rung spike.** It proved headless rung-1 checks on S&box `26.10.02`, on
  Windows.
- **Four reference-project experiments** against v0.3.0. They are historical; see
  [Empirical Status](docs/EMPIRICAL_STATUS.md).

## Gaps

- **Partly working:** automatic skill triggering in a real install. The
  [first test](skills/evidence/TRIGGERING_TEST.md) found the skills used in every working
  run, but loaded through the skill mechanism in only 4 of 6. `choosing-rigor` didn't
  trigger on the one-shot probe.
  - **The [engagement test](skills/evidence/ENGAGE_TEST.md)** tried the snippet and the
    skill edits. `choosing-rigor` then loaded in 15 of 15 acting sessions, and no agreed
    requirement was changed without the owner.
  - **Its frozen decision rule failed on the control,** which got wordier in 2 of 3 runs.
  - **The one allowed correction cycle failed too.** It narrowed the snippet, and the
    control with the snippet then stayed light in 2 of 3. Without the snippet it stayed
    light in 3 of 3, so the snippet is now optional.
  - **Pending:** the skill edits and the snippet await the owner's decision. A
    report-format fix is proposed but untested.
- **Not yet done:** using ELAD on one real project at this version.
- **Still open in the S&box example:** saved scenes that reference prefabs or collision
  models.

Closing the first two is the bar for `1.0`; see [Releasing](docs/RELEASING.md).

## History

Through v0.5, ELAD was a protocol blueprint, with schemas, templates, validators, and an
authenticated bundle. Those are archived at the `v0.5` tag; see [Archive](ARCHIVE.md).
