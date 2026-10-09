# Evidence-Led Agentic Development

**Use the cheapest reliable evidence that can justify the next action.**

Evidence-Led Agentic Development (ELAD) is a provider-neutral method for building software
with coding agents. It is three things:

- **a spec format**, so each requirement names the check that proves it;
- **an evidence ladder**, which orders checks by cost; and
- **three agent skills**, which teach an agent to use them.

ELAD runs nothing and grants no authority. Permission always comes from you and your
project; see [Authority and Safety](docs/AUTHORITY_AND_SAFETY.md).

**Current version: 0.6**, a breaking reshape of v0.5. The v0.5 protocol (schemas,
templates, and validators) is archived at the `v0.5` tag; see [Archive](ARCHIVE.md).

## Quick start

1. **Install the skills.** Copy the three folders in [`skills/`](skills/README.md) into
   your agent's skill folder, for example `.claude/skills/` for Claude Code. Tools that
   support the Agent Skills format load them when their descriptions match the work.
2. **Write a spec** for the area you're working on, at `spec/<area>.spec.md`. The format
   is in [Spec Format](docs/SPEC_FORMAT.md).
3. **Point your project's `AGENTS.md` at the spec.** Your `AGENTS.md` still decides what
   agents may do; the skills never override it.

Then ask for what you want in ordinary words. The agent works out which requirements are
affected, checks them on the cheapest rung that can settle them, and asks you only for
decisions that are yours.

## The spec format

Each requirement is one observable sentence with its rung and its check:

```markdown
### OUT-SPAWN-01 — Every spawn lands on solid ground with room to stand
- state: agreed
- rung: engine
- check: OUT_SPAWN_01_EverySpawnLandsOnSolidGround
- touches: spec/outpost.layout.json, generator code
```

Only the owner moves a requirement from `draft` to `agreed`. Results stay out of the spec:
machine checks report through test output, and owner checks add one line to
`spec/ACCEPTANCE.md`.

## The evidence ladder

| Rung | Runs where | Can prove |
|---|---|---|
| **0 · static** | anywhere | file structure, data validity, saved-file contents |
| **1 · engine** | the dev machine, headless | collision, physics, traces, exact program behavior |
| **2 · editor** | the real authoring tool | save and reopen, serialization, a rendered capture |
| **3 · session** | the product as users run it | host and remote behavior, clean installs |
| **4 · owner** | the owner, in person | feel, look, fitness for purpose |

**The rules that matter most:**

- Settle each requirement at the cheapest rung that can prove it.
- A lower rung never closes a higher claim.
- A check that has never failed may be blind.
- Ask the owner last, with a short card.

The full rules are in [Evidence Ladder](docs/EVIDENCE_LADDER.md).

## The skills

| Skill | Use when |
|---|---|
| [`choosing-rigor`](skills/choosing-rigor/SKILL.md) | Starting a task, or when something unexpected happens mid-task |
| [`matching-evidence-to-claims`](skills/matching-evidence-to-claims/SKILL.md) | Deciding how to prove a change works, and before reporting done |
| [`asking-the-owner`](skills/asking-the-owner/SKILL.md) | A decision or check needs the project owner |

**A skill change has to show it changes agent behavior** in a pressure test before it
merges; see [Skills](skills/README.md).

## Evidence and limits

- **Pressure tests.** The skills were tested against agents without them, and in round 1
  also against an unmodified Superpowers library. The tests were dry runs, scored blind
  against a rubric frozen beforehand.
  - **Round 2:** with the skills, agents pushed back on a risky "one try, then stop forever"
    rule in 2 of 3 runs, against 0 of 3 without them.
  - **The east-spawn task:** they ran cheaper checks first and reported by requirement and
    rung.
  - Results are in [`skills/evidence/`](skills/evidence/PRESSURE_TEST_RESULTS.md).
- **Engine-rung spike.** A real game engine (S&box) ran rung-1 checks from a project's own
  tests: collision, traces, spawn landing, stuck detection, and a saved scene. See the
  [S&box example](examples/sbox/README.md).
- **Limits.** The samples are small. Automatic skill triggering hasn't been tested in a
  real install, and ELAD hasn't yet been used on a real project at this version. See
  [Empirical Status](docs/EMPIRICAL_STATUS.md).

## Example

[`examples/sbox/`](examples/sbox/README.md) applies the method to a synthetic game map. It
includes a spec, the ladder for that target, a working rung-1 test kit, and a
target-specific skill.

## Checks and license

```text
python tools/check.py
```

The script is dependency-free and needs Python 3.10 or newer. It lints the skills and
checks that every relative link resolves. Passing proves the repository is well formed,
nothing more.

ELAD is licensed under [Apache-2.0](LICENSE). Provenance and credits are in
[Licensing and Provenance](docs/LICENSING_AND_PROVENANCE.md),
[Research Basis](docs/RESEARCH_BASIS.md), and [Principles](docs/PRINCIPLES.md).
