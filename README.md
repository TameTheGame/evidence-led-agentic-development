# Evidence-Led Agentic Development

**Use the cheapest reliable evidence that can justify the next action.**

Evidence-Led Agentic Development (ELAD) is a method for building software with coding
agents. It doesn't tie you to any AI vendor, tool, or engine. It is for projects where "it
works" is really several claims. Some can be settled just by reading the code or data.
Others need the real thing: a test inside a game engine, saving and reopening a file in an
editor, a second computer joining, or a person looking at the result. ELAD gives the agent
a way to tell those claims apart, prove each one as cheaply as it can, and leave you only
the decisions that are yours.

It has three parts:

- **A spec format.** Each requirement is one testable sentence. It also names the kind of
  evidence that settles it and the check that proves it. A task then becomes "make these
  requirements pass".
- **An evidence ladder.** Five levels of checking, called rungs, ordered from cheapest to
  most expensive: from a quick look at the files up to the owner trying it in person. The
  ladder says what each rung can and can't prove.
- **Three agent skills.** Short instructions in the [Agent Skills](https://agentskills.io/)
  format. They teach an agent to judge how careful to be on a task, to pick the right check
  for each claim, and to ask the owner only at the end.

ELAD is a method, not a program. It runs nothing on its own and never gives an agent
permission to do anything. Permission comes from you and from your project's own
`AGENTS.md`, the file that says what your agents may do. See
[Authority and Safety](docs/AUTHORITY_AND_SAFETY.md).

**Current version: 1.02.** See the [release notes](releases/v1.02.md) and
[Versions](#versions).

## Who it is for

ELAD is for anyone who builds software with coding agents and wants "done" to mean proven,
not just claimed. It grew out of one kind of work: coding agents building game maps in
S&box, a game platform from Facepunch, with the agent running the checks and the owner
judging the result. Its examples and its evidence come from that work, which is why some
rungs have names like engine and editor. Those game details are an example, not a limit.

Nothing in the method is tied to games. The spec format, the ladder, and the skills are
meant for any kind of software, such as a web app, a command-line tool, or a data
pipeline. What changes from project to project is the ladder. Each project keeps the rungs
that fit it and skips the rest. In a web app, for example, the engine rung becomes the
app's own automated tests, and there is usually no editor rung. Quirks of a platform that
agents should know about go in a short skill of their own, as the
[S&box example](examples/sbox/README.md) does.

ELAD's current examples and tests are all game maps. An example from outside games is
[on the roadmap](ROADMAP.md#examples).

## What it fixes

Coding agents left to themselves fail in a few familiar ways. Each rule in ELAD answers one
of them.

| Without a method | With ELAD |
|---|---|
| "It compiles, so it works." "The screenshot looks right, so collision is fine." | Each claim is checked on the rung that can actually prove it. A cheap check never stands in for one that needs more. |
| "The test passes." It has never failed, so no one knows whether it can. | Every new check is broken once on purpose, to show it can catch a real problem. |
| The owner is asked to run checks, find file paths, or judge things an automatic check could settle. | Everything objective is the agent's job. The owner gets one short request at the end, called a card, for what only a person can judge, such as feel, fit, and risk. |
| An agreed requirement is quietly reworded to match what the code does. | Only the owner approves or changes a requirement. The agent proposes new wording and waits. |
| A rule such as "try once, and if it fails, stop the project" gets applied to a local test too, so one small bug halts all the work. | One-try limits are kept for actions that are hard to undo. A local, reversible step gets two attempts per root cause, then a diagnosis and a report. |
| Every task, however small, gets a plan, a review, and a design document. | Small tasks stay light. The agent adds process only for a reason it can name. |

## Quick start

You don't set ELAD up by hand. In your project, tell your coding agent:

```text
Set up ELAD from https://github.com/TameTheGame/evidence-led-agentic-development
```

The agent reads this page and does the setup. Your part is to say what the project is for,
approve the first requirements, and approve what agents may do without asking.

After that, ask for what you want in ordinary words. The agent works out which requirements
are affected, checks them on the cheapest rung that can settle them, and asks you only for
the decisions that are yours.

> **For agents: setup steps**
>
> 1. **Install the skills.** From the latest release, copy the three folders in
>    [`skills/`](skills/README.md) into the project's skills folder: `.claude/skills/`
>    for Claude Code, or `.agents/skills/` for Codex. Any tool that supports the Agent
>    Skills format loads a skill when its description matches the work.
> 2. **Draft a first spec.** Ask the owner what the project is for. Then write a spec for
>    one small area at `spec/<area>.spec.md`, in the [spec format](docs/SPEC_FORMAT.md),
>    with every requirement as `draft`. If the project already has gates or sign-off
>    steps, map them first, as [Projects That Already Have Gates](docs/EXISTING_GATES.md)
>    shows.
> 3. **Propose a change to `AGENTS.md`.** Point it to the spec, and name the ELAD release
>    the skills came from, by version and commit, so a later move knows where it starts.
>    Suggest that agents run the project's checks without asking, including starting the
>    engine or editor for a test, and ask the owner first only for actions that are hard
>    to undo. `AGENTS.md` decides what agents may do, and the skills never override it, so
>    the owner approves this change.
> 4. **Ask the owner to agree the requirements.** Show the draft and ask which to make
>    `agreed`. Only the owner can.
>
> If the skills don't load on their own, add the [skills snippet](skills/AGENTS_SNIPPET.md)
> to `AGENTS.md`. It is a few lines saying which skill fits which moment.

## Moving to a new release

A project stays on the ELAD release it pinned until you decide to move. To move, tell your
agent:

```text
Move this project to the latest ELAD release
```

> **For agents: moving to a new release**
>
> 1. **Find the release the project pins.** Its `AGENTS.md` or decision log usually names
>    it. If nothing does, compare the project's copied skills with
>    [`skills/`](skills/README.md) at each release tag.
> 2. **Read the notes for every release since then,** in [`releases/`](releases/). Each
>    one's "Compatibility and migration" section says what changed and what a project must
>    do.
> 3. **Take the changed files.** Replace each copied file that changed, such as a skill or
>    an example script. Where the project adapted a copy, carry the change into its version
>    by hand, and say which copies you changed that way.
> 4. **Update every place the project names its pin,** even when nothing else changed,
>    such as the version line in `AGENTS.md`, source lines on copied files, and any check
>    that compares the copies with a release. Search the project for the old version, as a
>    whole word, and its commit to find them all; `1.0` is also the start of `1.01`.
> 5. **Run the project's checks,** and fix what the move broke.
> 6. **Record the move** where the project records decisions: the old and new versions and
>    the new release's commit. If a release suggests a change to what agents may do,
>    propose it in `AGENTS.md` for the owner to approve, as at setup.
>
> To go back to an earlier release, follow the same steps toward it.

## How a task runs

1. **Intent.** You say what you want. If no `agreed` requirement covers it, the agent
   drafts one and asks you to approve it.
2. **Checks first.** For claims a quick automated test can settle, the agent writes the
   test first, watches it fail for the right reason, and only then changes the content or
   code.
3. **Climb.** The agent runs the checks from cheapest to most expensive, as far as it can
   without help. At the first failure, it stops and finds the cause before changing
   anything else.
4. **Report.** One line per requirement: the ID, the rung reached, the result, and the
   commit. After that come the cards. A card is a short, numbered set of steps for
   something only you can judge. It says what pass and fail look like and how to reply.
5. **Owner.** You reply `GREEN` or `RED`, and the agent records your answer in
   `spec/ACCEPTANCE.md`.

```text
OUT-SPAWN-01  engine   pass   a1b2c3d
OUT-ROUTE-01  engine   FAIL   a1b2c3d  blocked at segment 2; cause: <first failure>
OUT-NET-01    session  card NET-1 ready for the owner
```

The full loop, and the rules behind each step, are in
[Evidence Ladder](docs/EVIDENCE_LADDER.md#how-a-task-runs).

## The spec format

Each requirement is one testable sentence, with its rung and its check:

```markdown
### OUT-SPAWN-01 — Every spawn lands on solid ground with room to stand
- state: agreed
- rung: engine
- check: OUT_SPAWN_01_EverySpawnLandsOnSolidGround
- touches: spec/outpost.layout.json, generator code
```

Only the owner moves a requirement from `draft` to `agreed`. Results stay out of the spec.
Machine checks report through test output, and owner checks add one line to
`spec/ACCEPTANCE.md`. A requirement counts as met when its check last passed at a known
commit and nothing it depends on has changed since. The full format is in
[Spec Format](docs/SPEC_FORMAT.md).

## The evidence ladder

| Rung | Runs where | Can prove |
|---|---|---|
| **0 · static** | anywhere | file structure, data validity, saved-file contents, compiling |
| **1 · engine** | the dev machine, headless | collision, physics, traces, exact program behavior |
| **2 · editor** | the real authoring tool | save and reopen, serialization, a rendered capture |
| **3 · session** | the product as users run it | host and remote behavior, clean installs |
| **4 · owner** | the owner, in person | feel, look, fitness for purpose |

Projects without an editor or a networked session skip those rungs.

> **For agents: the rules that matter most**
>
> - Settle each requirement at the cheapest rung that can prove it.
> - A cheaper rung never settles a claim that needs a higher one.
> - A check you have never seen fail may not be testing anything.
> - Ask the owner last, with a short card.

The full rules are in [Evidence Ladder](docs/EVIDENCE_LADDER.md).

## The skills

| Skill | Use when |
|---|---|
| [`choosing-rigor`](skills/choosing-rigor/SKILL.md) | Starting a task, when a request sets an attempt limit or a stop rule, or when something unexpected happens mid-task |
| [`matching-evidence-to-claims`](skills/matching-evidence-to-claims/SKILL.md) | Deciding how to prove a change works, and before reporting done |
| [`asking-the-owner`](skills/asking-the-owner/SKILL.md) | A decision or check needs the project owner |

Each skill is one `SKILL.md` file. Each ends with a table of red flags, which pairs a
tempting thought with why it is wrong. A project can add its own skills about its platform
beside them, as the S&box example does.

**A skill changes only when a pressure test shows the change makes agents behave
differently.** The test compares fresh agents with and without the change. Their answers
are scored against a rubric written in advance, by a scorer who doesn't know which is
which. Small fixes, such as broken links and typos, need only the repository check. See
[Skills](skills/README.md).

## What the evidence says

Every claim here rests on a recorded test, and each test is written up with its limits.

- **A first real project.** A private S&box project used the spec format and the ladder
  through a pilot and a first world slice, which passed all 18 machine checks and its
  owner's review. Its records show no use of the skills. See
  [Empirical Status](docs/EMPIRICAL_STATUS.md#a-first-real-project-v10).
- **Pressure tests.** Agents with the skills were compared with agents without them. The
  agents wrote plans rather than doing the work, and a scorer who didn't know which was
  which graded the plans against a rubric written in advance. With the skills, agents
  recommended a better rule than a risky "one try, then stop forever" instruction in 2 of
  3 runs, against 0 of 3 without them, and ran cheaper checks first. See
  [Pressure tests](skills/evidence/PRESSURE_TEST_RESULTS.md).
- **Real installs.** In Claude Code sessions that could edit files and were told nothing
  about the skills, the skills loaded on their own. Agents left agreed requirements to the
  owner, and a simple typo fix didn't pick up extra process. See the
  [triggering](skills/evidence/TRIGGERING_TEST.md) and
  [engagement](skills/evidence/ENGAGE_TEST.md) tests.
- **A real engine.** Starter tests ran collision, spawn, and saved-scene checks inside
  S&box without opening the editor, from a project's own test code. See the
  [S&box example](examples/sbox/README.md).
- **The S&box skill in use.** On made-up S&box test projects, the example's S&box skill
  loaded on its own and helped agents fix a bug planted for the test. With the starter
  tests, agents ran the engine tests and saw them fail before fixing anything. See the
  [domain-skill](skills/evidence/SBOX_SKILL_TEST.md), [live](skills/evidence/LIVE_TEST.md),
  and [refactor](skills/evidence/REFACTOR_TEST.md) tests.
- **Limits.**
  - The samples are small: three runs per setup, with one model and one agent tool, on
    Windows.
  - One real project used it, and its owner also maintains ELAD.
  - Every test of the method in its current form, made-up or real, was on a game map in
    S&box.

[Empirical Status](docs/EMPIRICAL_STATUS.md) separates what the evidence supports from what
it doesn't, and lists the
[claims ELAD doesn't make](docs/EMPIRICAL_STATUS.md#claims-elad-does-not-currently-make).

## What ELAD is not

- **Not software you run.** There is no server or service, and nothing to install beyond
  the three skills. Having ELAD's files in a project doesn't let an agent do anything new.
- **Not a permission system.** Nothing in ELAD lets an agent do more than your `AGENTS.md`
  allows. A skill or a passing check can make an agent more careful, never give it more
  permission. Merging, releasing, and publishing stay separate decisions, and each one is
  the owner's.
- **Not a guarantee.** ELAD doesn't promise that coding agents are safe, and it hasn't been
  tested across many AI providers, models, agent tools, or platforms.

## With Superpowers

[Superpowers](https://github.com/obra/superpowers) is a skill library for coding agents,
and a project can use it alongside ELAD. The table and the reasons, from the pressure
tests, are in [Evidence Ladder](docs/EVIDENCE_LADDER.md#with-superpowers).

> **For agents: using ELAD with Superpowers**
>
> Keep its verification skill, add requirement IDs to its plans, use its test-first skill
> only for the static and engine rungs, and skip its brainstorming when the spec already
> covers the change.

## Example

[`examples/sbox/`](examples/sbox/README.md) applies the method to a made-up game map in
S&box. It includes a sample spec, the ladder for S&box, starter engine tests, a compile
check, an editor check that runs on its own, a spec checker, an S&box skill, thirteen
[lessons from a world build](examples/sbox/README.md#lessons-from-a-world-build), and an
[import reference](examples/sbox/IMPORTING.md) for bringing old content into S&box.
It is an example, not part of the method's rules.

## Repository map

| Path | What it holds |
|---|---|
| [`docs/`](docs/) | The method: the spec format, the evidence ladder, authority and safety, and the guide for existing gates. Background: principles, decisions, research basis, licensing, releasing, and empirical status |
| [`skills/`](skills/README.md) | The three skills, the optional snippet, and the record of every pressure test |
| [`examples/`](examples/README.md) | Examples, not rules; today, one for S&box |
| [`tools/`](tools/) | `check.py` and its tests |
| [`releases/`](releases/) | The notes for each release |
| [`STATUS.md`](STATUS.md), [`ROADMAP.md`](ROADMAP.md), [`CHANGELOG.md`](CHANGELOG.md) | Where ELAD stands, what would change it, and what changed |
| [`AGENTS.md`](AGENTS.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`GOVERNANCE.md`](GOVERNANCE.md) | How this repository is worked on |

## Checks and contributing

ELAD has one check script, `tools/check.py`. It checks four things: that the skill files
are well formed, that every relative link and anchor resolves, that no private word
appears in the repository, and that no commit credits an AI tool. Passing proves the
repository is well formed, nothing more. See [Contributing](CONTRIBUTING.md#checks).

> **For agents: checking a change to this repository**
>
> Run `python tools/check.py`. It needs only Python 3.10 or newer and git. Then run
> `git diff --check` and read the exact diff.

## Versions

- Versions are `MAJOR.MINOR`, tags are `vMAJOR.MINOR`, and a released tag never moves. See
  [Releasing](docs/RELEASING.md). Each release has notes in [`releases/`](releases/) and a
  dated section in the [changelog](CHANGELOG.md).
- From `1.0` on, the minor number has two digits: `1.01`, `1.02`, and so on. Each update
  that lands on `main` is released with the next number.
- `1.0` marks the first time coding agents built something real under the method. On a
  private S&box project, they built the first slice of a game world, checked it at every
  rung, and its owner approved it. The two formal conditions for `1.0`, skills that trigger
  on their own in a real install and use on one real project, are met within the limits
  above. The number grants no maturity or authority.
- Version 0.6 replaced the older protocol with the spec format, the ladder, and the skills.
  That protocol (schemas, templates, and validators) is archived at the `v0.5` tag. See
  [Archive](ARCHIVE.md).

## License

ELAD is licensed under [Apache-2.0](LICENSE). Provenance and credits are in
[Licensing and Provenance](docs/LICENSING_AND_PROVENANCE.md),
[Research Basis](docs/RESEARCH_BASIS.md), and [Principles](docs/PRINCIPLES.md).
