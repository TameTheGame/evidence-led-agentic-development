# Changelog

## Unreleased

No pending changes.

## 1.03 — 2026-10-21

A rule for breaking changes after `1.0`. No skill changed, and nothing in the core breaks.

- **Breaking changes take a new major number.** `docs/RELEASING.md` now says a release that
  breaks existing projects goes to the next major number, so the first after `1.xx` is
  `2.0`, followed by `2.01`, `2.02`, and so on. Every other release takes the next
  two-digit minor number, as before. A change breaks existing projects when a project
  that moves to it has to change its own files, beyond its pin and the copies it takes,
  for its specs and checks to keep working. ADR-0021 records the owner's decision. Until
  now the policy said what a breaking change does only in `0.x`.

## 1.02 — 2026-10-21

An import reference for S&box. No skill changed, and nothing in the core breaks.

- **An S&box import reference.** `examples/sbox/IMPORTING.md` collects what works and what
  doesn't when bringing old content into S&box, sorted by topic: models, collision,
  physics and breakables, materials and decals, lighting, sound and water, map logic and
  entities, player movement, tools and scripting, and faster ways of working. Each entry
  says what to do, what fails and why, and ends with its evidence (source, seen, or
  inferred), the S&box version it was checked on, and its proof. The file opens with a
  note that S&box is still in development, so entries may go stale, and ends with a
  format for adding entries and steps for rechecking them after an S&box update.
  - The four lessons in the guide's "Lessons from importing old content" move there, and
    that section now points to it.
  - Eighteen entries are new, from a first real project's import of an old Source 1 map
    on S&box `26.10.13a`. Among them: pose a Source prop as Source draws it, at frame 0 of
    its current sequence; use a `Multiply` decal for Source's modulate decals; start
    lights as their "start off" flag says; place track trains on their first path node;
    read Source's door flags and swing rule; let the player use things inside other
    solids; write full type names in `run_csharp` scripts; and ask the original game what
    it does.
  - Entries about Source cite Valve's Source SDK 2013 at commit `be57e3d`. Garry's Mod
    runs its own fork, which isn't public, so its match is inferred.
  - Some entries rest on observation alone, such as OBJ axes in ModelDoc and
    alpha-tested thin wire, and say so. They had waited in a private candidates list
    because the guide's lessons each cite source.

## 1.01 — 2026-10-21

The first release after `1.0`. It adds steps for moving a project to a new release and nine
S&box lessons from a first real project, and it brings back a release for each update, now
with two-digit minor numbers. No skill changed, and nothing in the core breaks.

- **Version numbers after 1.0.** Releases from `1.0` on have a two-digit minor number:
  `1.01`, `1.02`, and so on. Each coherent update that lands on `main` ships as the next
  release, with its changelog section, notes, and tag, and each waits for the owner's typed
  GREEN. `docs/RELEASING.md` and the README say so, and ADR-0021 records the decision.
  `SECURITY.md` names the current release again; it had said `0.6` since that release. The
  README's moving steps say to search for the old version as a whole word, since `1.0` is
  also the start of `1.01`.
- **Three more S&box lessons from a world build.** `examples/sbox/README.md` adds them to
  "Lessons from a world build". In a SceneLoaded hook, `Time.Now` is the caller's clock,
  not play time. Edits made through `run_csharp` don't mark the scene unsaved, so
  `save_scene` writes nothing until the script sets `HasUnsavedChanges` or uses an undo
  scope. `Editor.FileSystem.Content` is read-only. Each cites the `26.10.13` source. A
  first real project found them on S&box `26.10.13a`. "The editor check" no longer calls
  the `HasUnsavedChanges` setter untested: that project used it on `26.10.13a`, and the
  scene saved.
- **Two more S&box lessons from a world build.** `examples/sbox/README.md` adds them to
  "Lessons from a world build". A `GameObjectSystem` runs in every scene, so a player
  spawner written as one also runs in scenes that spawn players through a `NetworkHelper`,
  and should skip them. A test can walk a `PlayerController` without a keyboard by turning
  `UseInputControls` off and setting `WishVelocity`. Each cites the `26.10.13` source. A
  first real project found them on S&box `26.10.13a`.
- **Four S&box lessons from importing old content.** `examples/sbox/README.md` gains
  "Lessons from importing old content". Convert SMD models to FBX, OBJ, or DMX first. Set
  simple properties, such as an enum, `int`, `bool`, or `float`, in a constructor when their
  value isn't a constant, because the code generator copies initializers into
  `[DefaultValue]`. A mesh marked HideInGame still renders in the editor scene and its
  screenshots. `Material.Load` returns an error material, not null, for a missing file, so
  editor code checks `AssetSystem.FindByPath`. Each cites the `26.10.13` source. A first
  real project found them on S&box `26.10.13a`.
- **Steps for moving to a new release.** The README gains "Moving to a new release". The
  owner asks for the move in one line. The agent finds the release the project pins, reads
  the notes for every release since then, takes the changed files, updates every place the
  project names its pin, runs the project's checks, and records the move.
  `docs/RELEASING.md` now says a release's compatibility notes always tell projects that
  name their pinned version to update it, even when nothing else needs to change. Setup
  step 3 now has the agent name the ELAD release in `AGENTS.md`, by version and commit, so
  a later move knows where it starts. A first real project's move to v1.0 showed the gap:
  the README covered first setup only, setup recorded no pin, and the release notes didn't
  say to update one.

## 1.0 — 2026-10-18

ELAD's two conditions for `1.0` are met: the skills load on their own in real installs
(v0.7), and a first real project, a private S&box project, has used the method from a pilot
to a first world slice its owner approved. This release records that use and adds three
S&box lessons from it, plus an AI-attribution check. No skill changed, and nothing in the
core breaks.

- **A write-up of the first real project.** `docs/EMPIRICAL_STATUS.md` gains "A first real
  project": what helped, what was ignored, and what got in the way, in synthetic terms, with
  its limits. The project's records show no use of the skills, and its owner also maintains
  ELAD. The roadmap marks the item done, and the status pages say the bar for `1.0` is met.
- **A rewritten README.** It now says who ELAD is for, where it has been used, and how
  to adapt it to another kind of project; what goes wrong without it; how a task runs;
  what ELAD is not; and where things are in the repository. The evidence section is a
  summary with links. The quick start now says the agent does the setup: the owner asks
  for it in one line, and the agent installs the skills, drafts the first spec, and asks
  the owner to approve it and the `AGENTS.md` change. Parts written for agents are set
  apart in quoted blocks marked "For agents". The spec format, the ladder, the skills
  table, and the 1.0 facts are unchanged.
- **A sixth S&box lesson: a dedicated server doesn't mount a library's assets.**
  `examples/sbox/README.md` adds it to "Lessons from a world build": content that lives only
  in a `Libraries\` project loads in the Editor but is not found on a dedicated server, so
  keep it in the game's own `Assets` or link it there. It cites the `26.10.13` source. A
  first real project found it, and a link fixed it on S&box `26.10.13a`.
- **A seventh S&box lesson: wait for an active scene.** `examples/sbox/README.md` adds it to
  "Lessons from a world build": while a game loads, `instance_status` can report the game
  set and `IsLoading` false before a scene opens, so a check also waits for `ActiveScene`.
  It cites the `26.10.13` source. A first real project found it on S&box `26.10.13a`, where
  a server check that didn't wait started a second early and failed.
- **An AI-attribution check.** `tools/check.py` now fails when a commit reachable from
  `HEAD` credits an AI coding tool, such as Claude, Cursor, or Copilot: an author or
  committer naming one, a trailer such as `Co-authored-by:` naming one, a trailer such as
  `Claude-Session:`, or a "Generated with" line naming one. Ordinary mentions in a message
  pass. Both push hooks run it with the rest of the check. CI now checks out the full
  history, because its shallow checkout let the commit checks read only the newest commit.
  `tools/test_check.py` adds ten cases. Every commit on `main` passes.
- **An eighth S&box lesson: a hidden dedicated server doesn't listen on its game port.**
  `examples/sbox/README.md` adds it to "Lessons from a world build": with
  `net_hide_address` on, which is the default, the game socket goes through a Steam FakeIP
  and only the query port is bound. So a port check asks the server for its settings and
  checks the query port and the server's `status` instead. It cites the `26.10.13` source.
  A first real project found it on S&box `26.10.13a`.
- **The checks print plain hyphens.** `tools/check.py` and `tools/test_check.py` put an em
  dash in their result lines, which the Windows CI log showed as a replacement character.
  They now print a plain hyphen, as the example spec lint does.

## 0.10 — 2026-10-18

A first real project found gaps, and this release fills them: a guide for projects that
already have gates, clearer spec-format and ladder rules, a stricter example spec lint,
and S&box tools and lessons that hold up on a real map. No skill changed, and nothing in
the core breaks.

- **Five S&box lessons from a world build.** `examples/sbox/README.md` gains "Lessons from a
  world build": read scene-load errors from editor start; don't end a scene string in a
  file extension, which S&box takes as a file reference; check the `.sbproj` out the way
  S&box writes it, or the Editor rewrites it on every start; a dedicated server is listed
  on Steam, so checking with one needs the owner's yes; and an unpublished game can't run
  on a dedicated server, so its session rung uses an Editor host. Each cites the
  `26.10.13` source. A first real project found them. The editor check already read errors
  from editor start.
- **The editor check puts the `.sbproj` back.** The Editor writes a project's `.sbproj`
  again on each start when its text differs from what S&box writes, such as LF line endings
  on Windows, so the check could leave a modified file behind. `editor_check.ps1` now
  restores the `.sbproj` along with the scene, and adds a note when the Editor rewrote it.
  A first real project found it. Checked on S&box `26.10.13a`, in both shells: with the
  `.sbproj` checked out with LF endings, the previous script passed but left it modified
  with CRLF endings, and the new one passed, restored it, and said so. Checked out with
  CRLF endings, it wasn't rewritten.
- **The example spec lint checks everything the spec format lists.**
  `examples/sbox/tools/spec_lint.py` now also fails on an ID not shaped `AREA-TOPIC-NN`, a
  retired ID used again, an owner-rung check that isn't a card, and a card the spec doesn't
  define. With `--sources` it looks up each agreed requirement's check in the test and
  script folders, and reports any it can't find without failing, because checks are
  written after the owner agrees. `docs/SPEC_FORMAT.md` says which items fail and which are
  reported. Its output now uses plain hyphens, because a Windows console showed its dashes
  as a replacement character. A first real project found the lint did less than the format
  described.
- **A spec can name a data file before it exists.** `docs/SPEC_FORMAT.md` says to mark it
  `(not written yet)` on the `data:` line. A first real project had no wording for it.
- **Compiling is a static check.** `docs/EVIDENCE_LADDER.md` and the README list it on
  rung 0. A compile against an installed engine's libraries runs only on the dev machine,
  but it starts nothing, so it runs before rung 1. The `matching-evidence-to-claims` skill
  already said this; a first real project found the ladder didn't.
- **Routine checks stay off the ask-first list.** The quick start and
  `docs/EXISTING_GATES.md` say to let agents run the project's checks, including starting
  the engine or editor for a test, and to keep the owner's ask-first list for actions that
  are hard to undo. A first real project put engine runs on that list, and its agent
  stopped before each one.
- **Old gate records are pinned by Git identity.** `docs/EXISTING_GATES.md` says to compare
  blob IDs, not hashes of checked-out files, which break when a checkout's line endings
  differ. A first real project's old evidence broke that way.
- **Why the editor check forces saves with a marker.** The S&box example notes that the
  session's public `HasUnsavedChanges` setter would also force a save, but only through
  `run_csharp`, which the check doesn't use.
- **A private-word check.** `tools/check.py` now fails when a tracked file, a file name, or
  a commit message contains a listed private word, such as a private project's name. The
  repository holds only SHA-256 fingerprints, in `tools/private-words.sha256`; the readable
  list stays with the owner. A Claude Code hook runs the check before every `git push` from
  a session started in this repository and blocks the push if it fails. A git hook in
  `.githooks/` does the same for any push once a clone turns it on, which covers cloud
  sessions with several repositories, since those don't load a repository's hooks.
  `tools/test_check.py` tests the check and both hooks with made-up words, and CI runs it
  on Linux and Windows. Checked with Claude Code `2.1.237` on Windows and `2.1.302` on
  Linux: the Claude Code hook blocked a planted push and let a clean one through.
- **A guide for projects that already have gates.** `docs/EXISTING_GATES.md` says how to
  move a project's own gates, sign-offs, and permission files onto specs: map each gate to
  a requirement, retire it with a reason, or postpone it to a named spec. A first real
  project found ELAD said nothing about this. The S&box example also gains "A map with no
  code", on testing and playing a content project, from the same project on S&box
  `26.10.13a`.
- **Script checks report one line per requirement.** `docs/SPEC_FORMAT.md` now says where a
  script check's requirement ID goes, and that a script run settling several
  requirements prints one PASS or FAIL line per ID and fails if any line fails. A first
  real project found the format named script checks only by example.
- **The editor check runs on projects without code.** `examples/sbox/tools/editor_check.ps1`
  read a missing compile result as a failed compile, so it stopped on a content project,
  such as a map, which has nothing to compile. It now waits for a compile only when the
  project or one of its libraries has a `Code` or `Editor` folder. A first real project
  found it. Checked on S&box `26.10.13a`: a content project passed, where the previous
  script stopped, and a game project still passed.
- **Saved scenes simulate in the rung-1 starter.** Its `LoadSavedScene` now loads without a
  loading screen, as S&box's own scene tests do. Before, a saved scene stayed in its loading
  phase in headless tests and `GameTick` skipped it, so a player in it never moved. The new
  `Setup_SavedSceneSimulates` lands a player on the saved scene's floor. A first real project
  found it. Checked on S&box `26.10.13a`: all 6 starter tests passed, and with the old
  loader only the new test failed.
- **Engine source follows a hotfix before it is tagged.** The rung-1 starter's
  `sync_engine_source.ps1` checks out the nearest tagged release before an untagged hotfix,
  such as `26.10.13` for `26.10.13a`, and prints `NEAREST`; a later run picks up the tag.
  Before, it printed `NOT SYNCED` and left the clone wherever it was. The starter README
  says how to cite engine facts while the line says `NEAREST`, what to rerun after
  `SYNCED`, and how to run the script at the start of each agent session. A first real
  project found it. Checked on S&box `26.10.13a`, in both shells: the real clone printed
  `NEAREST` at `26.10.13` and was left clean with `master` in place. A throwaway repository
  gave `NEAREST`, then `SYNCED` once the hotfix was tagged, `NEAREST` at an earlier hotfix,
  and `NOT SYNCED` for a missing release tag and for local changes. The `SessionStart` hook
  put the line in a new session's context.
- **Saved scenes keep their mesh data in the rung-1 starter.** S&box saves editable mesh
  and terrain data in a `<scene>_d` file beside the scene, and `LoadSavedScene` dropped it,
  so saved meshes loaded empty and traces passed through them. It now reads the `_d` file
  the way the editor does, and the new `Setup_SavedSceneKeepsMeshData` checks that a saved
  block stops a trace. A first real project found it. Checked on S&box `26.10.13a`: all 7
  starter tests passed, and with the loader ignoring the `_d` file only the new test failed.
  A scene the Editor saved with a mesh block got a `_d` file, and a test that loaded it hit
  the block.
- **A compile check for `run_csharp` scripts.** `examples/sbox/tools/compile_check.ps1`
  builds them against the installed engine's assemblies without starting S&box, so a wrong
  name fails in seconds instead of in the Editor. A first real project had no check on
  these scripts before they ran. Checked on S&box `26.10.13a`, in both shells: a script using
  real APIs passed, and the same script with one misspelled member failed at its own file
  and line. A script using a helper passed with `-Include` and failed without it, and a
  wrong `-Engine` stopped with `NOT RUN`. No S&box process started. The first run found that
  scripts using `Log` failed, because `run_csharp` also brings in the game's global names.
  The check now does too, for scripts and included code, with `run_csharp`'s compiler
  settings.
- **The editor check says why an editor didn't start.** `editor_check.ps1` saves each
  editor's `sbox-cli` output and editor log with its results, and prints their last lines
  on a failure. It stops with `NOT RUN` when Steam isn't running. Before, a failed start
  said only that `sbox-cli` stopped. A first real project found it. Checked on S&box
  `26.10.13a`, in both shells: a scratch scene passed with both editors' `sbox-cli` output
  and logs saved. With a 5-second limit the check failed with `wasn't ready`, printed the
  last lines of both files, and left no S&box process. Windows PowerShell garbled the log's
  non-ASCII text until the script read it as UTF-8. Steam stayed open, so the `NOT RUN`
  branch was read, not run.
- **The engine-test runner flags source it didn't match.** `run_engine_tests.ps1` and
  `sync_engine_source.ps1` read `FACEPUNCH_ENGINE` and `SBOX_PUBLIC` from the user's settings
  when the shell started without them, and the runner ends with a warning unless the source
  line says `MATCH` or `SYNCED`. A first real project's run said `NOT CHECKED` on a line
  that was easy to miss. Checked on S&box `26.10.13a`, in both shells: with both variables
  cleared in the shell, the runner found the install through the user's `FACEPUNCH_ENGINE`.
  `NOT CHECKED` and `NEAREST` ended with the warning, and `MATCH` and `SYNCED` didn't. The
  user-level `SBOX_PUBLIC` wasn't tested, because the test machine doesn't set it.
- **The status docs say ELAD is in use.** `README.md`, `STATUS.md`, and
  `docs/EMPIRICAL_STATUS.md` said ELAD hadn't been used on a real project. They now say it is
  in use on its first real project, that the use isn't yet written up as evidence, and that
  the owner decides when it meets the bar for `1.0`.

## 0.9 — 2026-10-14

The S&box example's editor rung runs unattended, and the older skill-test runners keep the
test machine's own settings out of test sessions. No skill changed, and nothing breaks.

- **The two older skill-test runners load project settings only.** `run_skills_test.ps1` and
  `run_sbox_skill_test.ps1` now pass `--setting-sources project,local`, as `run_live_test.ps1`
  already did, so skills and instructions installed for the test machine's user stay out of
  test sessions. Checked on Claude Code `2.1.237`: with the setting, a session saw the
  project's skill but none of the user's. Earlier results are unchanged.
- **The S&box example's editor rung runs unattended.** S&box `26.10.13` added `sbox-cli`,
  which drives the Editor over a local named pipe. The new `examples/sbox/tools/editor_check.ps1`
  uses it to save a scene, close the Editor, reopen it, and check that nothing changed, with a
  screenshot from a fixed camera. The outpost spec's OUT-SAVE-01 now names that check, and its
  owner card SAVE-1 is gone. Verified on `26.10.13`: a scratch scene passed, and a control
  scene that changes itself on load failed.
- **The rung-1 starter suggests running the engine-source sync on a schedule.** Steam
  updates S&box only when S&box starts, so an open session misses an update from a launch
  made by hand. An hourly Windows scheduled task covers it; one was checked on 2026-10-14.
- **Removed the Harness Readiness Suite section** from `docs/EMPIRICAL_STATUS.md`. The
  owner retired that companion repository. Nothing in ELAD used it, and it was not part of
  the evidence this document lists. Older tags still mention it.

## 0.8 — 2026-10-13

The S&box example gains a rung-1 starter and an engine-source sync, and three tests in
acting sessions checked them and the example's domain skill. No skill changed, and nothing
breaks.

- **New evidence: `skills/evidence/SBOX_SKILL_TEST.md`.** It is the first test of the
  example `sbox-engine-reference` skill: 18 acting sessions on a synthetic S&box game
  project, with and without it, scored blind against a frozen rubric. The skill passed. It
  loaded in 9 of 9 runs, and with it agents fixed the planted enable-order bug in 6 of 6
  runs, against 0 of 6 without it. No run could write the default-surface scaffolding. No
  skill changed.
- **New evidence: `skills/evidence/LIVE_TEST.md`.** It reran those scenarios in 24 acting
  sessions in compiled S&box projects with the rung-1 starter, where agents could run the
  engine tests, and added the shared-generator refactor. It failed its frozen rule on the
  refactor scenario alone: the project had one area, so agents asked which refactor was
  meant. Every geometry test had a default surface, tests failed before fixes in 11 of 12
  runs, and reference probes confirmed the fix in 12 of 12, with or without the domain
  skill. No skill changed.
- **New evidence: `skills/evidence/REFACTOR_TEST.md`.** It reran the shared-generator
  refactor alone, in 6 acting sessions in a compiled project whose two areas share the
  generator, with a request that names the change. Every run refactored and reran every
  shared check afterwards, and reference probes confirmed the build in 6 of 6. It failed its
  frozen rule because no run ran those checks before the change. No skill changed.
- **Test tools.**
  - Added `run_sbox_skill_test.ps1` and `run_live_test.ps1`. The live runner also builds
    the two-area refactor project (scenario `G2`) and has a build-only phase.
  - `analyze_transcripts.py` gains `--context` and `--new-files`, and scrubs local paths
    from diffs. It also captures engine-runner output, including runs started in the
    background, and marks a non-zero exit apart from a permission refusal.
  - `blind_extracts.ps1` gains `-Messages`, `-Fixture`, and `-HideSkills`.
- **Added `examples/sbox/rung1-starter/`.** It is a copyable starting point for a project's
  engine tests, packaged from the engine-rung spike:
  - the default-surface scaffolding;
  - player and stuck-check helpers;
  - the saved-scene loader;
  - one requirement test with its control case; and
  - `tools/run_engine_tests.ps1`. It saves the engine log with each run, lists the
    component errors the engine caught, and makes concurrent runs wait.

  Verified on S&box `26.10.02`: 5 of 5 passed. In a control run with the default surface
  disabled, the runner reported the hidden `MeshComponent` error at `ModelBuilder.AddSurface`.
- **Added `sync_engine_source.ps1` to the rung-1 starter.** It reads the installed S&box
  release from `.version` and checks the matching tag out in a local clone of
  `Facepunch/sbox-public`, so agents read the source of the engine they run. It refuses a
  clone with local changes and changes no branch. The runner calls it before each run when
  `SBOX_PUBLIC` names the clone. Verified on a real clone, 74 commits past `26.10.02`.
- **Docs.** `README.md`, `STATUS.md`, and `docs/EMPIRICAL_STATUS.md` now report the S&box
  tests. `STATUS.md` no longer lists the refactor rerun as the next S&box step.

## 0.7 — 2026-10-10

The skills engage on their own in real installs, and they now leave agreed requirements to
the owner. No breaking changes.

- **Skill edits.** All three were tested in acting headless sessions; see
  `skills/evidence/ENGAGE_TEST.md`.
  - The `choosing-rigor` description now also covers requests to run a check, and
    requests that set an attempt limit or a stop condition.
  - The `matching-evidence-to-claims` description adds "running" tests and checks.
  - `asking-the-owner` gains a red flag: a "wording change" to an agreed requirement is
    still the owner's decision.
- **Added `skills/AGENTS_SNIPPET.md`.** It is an optional block for `AGENTS.md` mapping
  moments to skills, for projects whose agents don't pick up the skills. Testing found the
  skills engaged without it, and a typo fix stayed lighter without it, so it is not a
  quick-start step.
- **Added `examples/sbox/tools/spec_lint.py`.** It is an example rung-0 spec lint, with
  fixtures and `test_spec_lint.py`.
  - Its format checks fail the run.
  - Its owner gate reports any change to an agreed requirement since the last commit as
    `NEEDS OWNER`, without blocking.
  - `docs/SPEC_FORMAT.md` now recommends an owner gate and points to this example.
- **New evidence in `skills/evidence/`.**
  - `TRIGGERING_TEST.md`: 9 sessions with the v0.6 skills. They were used in every working
    run but loaded through the skill mechanism in only 4 of 6, and all three east-spawn
    runs edited an agreed requirement.
  - `ENGAGE_TEST.md`: 33 acting sessions scored blind against frozen rules.
    - The original rule and its one correction cycle failed on a wordier typo control with
      the snippet.
    - The release configuration (edited skills, the lint, no snippet) then passed its own
      check: 3 of 3 east spawn, 2 of 3 probe, and 3 of 3 control.
- **Test tools in `skills/evidence/tools/`.** These are `analyze_transcripts.py`,
  `run_skills_test.ps1`, and `blind_extracts.ps1`, so each skill change can be pressure-
  tested cheaply.
- **Docs.**
  - `README.md` and `docs/EMPIRICAL_STATUS.md` now report the headless-install evidence.
  - `ROADMAP.md` lists the next S&box steps: testing the S&box domain skill, and a rung-1
    starter.
## 0.6 — 2026-10-09

A breaking reshape, approved through the promotion proposal; see ADR-0020 in
`docs/DECISIONS.md`.

- **The core is now three parts.**
  - `docs/SPEC_FORMAT.md`: requirements in the project's spec, each naming its rung and
    check.
  - `docs/EVIDENCE_LADDER.md`: checks ordered by cost, plus the rules for climbing them.
  - Three skills in `skills/`: `choosing-rigor`, `matching-evidence-to-claims`, and
    `asking-the-owner`.
- **Rationale folded in.** `ADAPTIVE_RIGOR.md`, `EVALUATION_AND_EVIDENCE.md`,
  `HUMAN_DECISION_BOUNDARY.md`, and `OPERATIONS_AND_LEARNING.md` were folded into
  `docs/EVIDENCE_LADDER.md`, then archived.
- **New `docs/AUTHORITY_AND_SAFETY.md`.** It carries forward the general rules from
  `ARCHITECTURE.md`, `THREAT_MODEL.md`, `MODEL_QUALIFICATION.md`, and the v0.5
  `SECURITY.md`.
- **The S&box material moved to `examples/sbox/`:** the outpost spec, the engine-rung spike
  kit with results from seven runs, and the `sbox-engine-reference` skill.
- **The pressure-test record moved to `skills/evidence/`.** Rounds 1 and 2, with responses,
  rubrics, keys, and scores.
- **Archived at `v0.5` and removed from `main`; see `ARCHIVE.md`:**
  - all schemas and registries;
  - all templates;
  - the validators, vectors, and fixtures;
  - `protocol-bundle.json` and `blueprint.json`;
  - the episode and promotion drafts;
  - the protocol examples;
  - the adapter and reference placeholders;
  - `START_HERE.md`, `MANIFEST.md`, and `docs/FIRST_RUN.md`; and
  - the protocol documents.
- **New checks.** `tools/check.py` replaces the validators: a skill frontmatter lint and a
  relative-link check. CI runs it on Ubuntu and Windows with one Python version. The
  release job checks that the tag matches `VERSION` and that the notes exist.
- **Version policy.** `docs/RELEASING.md` now says 0.x minor releases may include breaking
  changes. `1.0` waits for a real-install triggering test and one real project.
- **Rewritten:** README, AGENTS.md, STATUS, ROADMAP, CONTRIBUTING, and SECURITY. GOVERNANCE
  was trimmed to match.
- **The skill-change rule.** A change to what a skill tells an agent to do (its
  instructions, description, or red flags) needs a blind pressure test. Mechanical fixes
  that don't change meaning (paths, links, typos) need only `tools/check.py` and a
  CHANGELOG line. The rule is stated in AGENTS.md and mirrored in CONTRIBUTING, the skills
  README, the README, GOVERNANCE, and ADR-0020.
- **Mechanical fix:** `sbox-engine-reference` now points to the spike kit at
  `examples/sbox/engine-rung-spike/` instead of its old drafts path.

## 0.5 — 2026-09-05

- Adopted two-component `MAJOR.MINOR` versions and `vMAJOR.MINOR` release tags, beginning
  with `v0.5`. Historical three-component tags remain unchanged.
- Made version bumps, checked-in release notes, and a verified GitHub Release the default
  completion path for authorized user-facing blueprint updates. Valid version tags
  publish only after the full hosted conformance matrix passes.
- Rebound all active protocol, schema, registry, template, example, vector, bundle, and
  validator identities to exact `0.5`; preserved non-normative historical drafts and
  existing adopter pins. Mixed-version chains remain invalid.
- Consolidated blueprint development onto the canonical public repository and its clean
  `main` history. Retired private history and release-preparation copies remain external
  recovery material; the separate Harness Readiness Suite remains an optional companion.
- Added canonical Direct/Conserve operating-mode guidance, independent of rigor:
  capable primary-agent delivery and explicit eligible cheaper/local routing.
  Replaced blanket local-first routing and required document preloads with conditional
  worker controls and task-selected context. Existing qualification, effect boundaries,
  review budgets and runtime evidence remain intact; release identities advance together.
- Added a dated, non-normative Astra instruction-audit note with primary attribution;
  it makes no model-superiority claim and activates no runtime or downstream adoption.

## 0.4.0 — 2026-08-29

- Promoted the complete normative protocol, authenticated bundle, conformance corpus,
  and dependency-free validators to exact `0.4.0` identities. Existing `0.3.0`
  adopters remain valid while pinned; adopting `0.4.0` requires an explicit repin and
  claim-scoped revalidation of affected target-owned review-flow bindings.
- Added lifecycle-cost proportionality, hard non-resetting review budgets, claim-scoped
  revalidation, Git-native tracked-artifact identity, and qualified local-first
  verification without adding a new schema or control platform.
- Documented the separately maintained ELAD Harness Readiness Suite `v0.1.0` as an
  optional model- and harness-agnostic operational companion; retained Level 0,
  default-deny authority, exact-subject qualification, and bounded empirical claims.
- Corrected the onboarding flow so project owners can describe a high-level outcome or
  simply ask what comes next; the agent, not the owner, performs ELAD's task decomposition,
  uncertainty analysis, rigor selection, and evidence planning.
- Visually distinguished agent-only headings from reader-facing steps with a restrained
  blockquote treatment in the onboarding guides.
- Reframed the empirical summary around ELAD's four deliberate reference-project
  experiments and their positive results, while keeping the production-scale and
  generality limits explicit.
- Reworked the reader-facing process guides around progressive disclosure: start with one
  small task, add evaluation for uncertain claims, and introduce qualification or formal
  assurance only when repeated autonomy or consequential effects justify them.
- Added a prominent `Why ELAD` section explaining how right-sized scaffolding and
  evidence-backed stopping rules make autonomous agentic development practical without
  overstating the bounded empirical record.
- Simplified process language, shortened repeated protocol explanations, and routed
  implementation detail to the technical references while preserving authority,
  claim-specific evidence, evaluator calibration, and explicit stopping boundaries.
- Clarified the first-run voice by speaking directly to the project owner while prefixing
  every coding-agent procedure with `Agent instructions:`.
- Replaced the first copyable prompt's protocol vocabulary with a plain-language request
  to state the intended change, boundaries, and verification before seeking approval.

## 0.3.0 — 2026-08-23

- Released a clean public source tree under Apache-2.0, with verified primary-source
  research attribution, exact licensed CI dependencies, a clean-history publication
  boundary, public contribution/security guidance, and no product-specific residue.
- Added a cross-platform `python tools/validate_all.py` entrypoint, made hosted CI execute
  all six validation slices, added a short first-run walkthrough, and published a candid empirical
  status that separates internal conformance from bounded portability observations and
  untested operational claims.
- Made evaluation an explicit build/observe/evaluate/error-analysis feedback loop.
- Separated project maturity, per-task rigor, and effect authority.
- Added `light`, `bounded`, `evaluated`, and `assured` profiles plus a genuine
  lightweight path with no mandatory JSON artifacts.
- Classified strict packets, manifests, receipts, qualification, fencing, negative
  suites, and adversarial/human review as conditional assurance modules rather than
  universal per-task ceremony.
- Added an advisory, authority-free task-rigor registry/schema/template, eleven positive
  vectors, 37 malicious/contradictory vectors, and a dependency-free validator. Profile
  bases are claim/effect neutral; closed per-claim evaluator, claim-domain, and task-effect
  modules prevent irrelevant semantic, runtime, or rollback ceremony.
- Applied the four-observation portability correction: evaluator maturity is per claim;
  a new exact regression is not an unproven fallible evaluator; program execution does
  not itself create an operational claim; and AI-assisted development does not itself
  create stochastic product behavior.
- Preserved the integrated agentic-episode schema, template, and unfinished vectors as
  non-normative drafts because no semantic composition validator supports an assured
  claim; the focused component contracts remain normative.
- Retained the 44,100 lifecycle cross-product and added a separately implemented rule
  predicate plus focused claim-aggregate, 15-shape, and single-field-denial vectors.
- Added an explicit authenticated artifact inventory and deterministic inert-artifact
  regeneration tool so filename globs cannot silently make a draft normative.
- Clarified reusable evaluator calibration, heterogeneous cloud/local routing, compact
  orchestrator context, progressive adoption, gate admission, and process simplification.
- Added a compact bounded-worker packet and a mixed deterministic/semantic example;
  distinguished supervised workers from bounded handoffs, coding from product-inference
  harnesses, generator from evaluator sampling, LLM-judge evidence from external-human
  acceptance, and causal closure from perfect-score chasing.
- Retained Level 0/default-deny status; no live model, target, adapter, authority,
  promotion, or publication surface was added.

## 0.2.0 — 2026-08-22

- Replaced the shared two-repository authority/evidence design with separate
  repository-owned authority records and evidence policies; shared risk/data policy is
  explicitly narrowing only.
- Added claim classes, pre-run subject selectors, and exact resolved subjects across
  evidence, receipt, review, and human-decision records.
- Made `evidenceAcceptance` an enforced operational closure condition and bound machine
  delegation to exact claim class, evidence class, evaluator, and eligible writer.
- Added a closed-world 44,100-combination receipt lifecycle oracle with exactly 33
  admitted sealed tuples.
- Added full configured-writer -> measured-certificate -> requested-packet ->
  observed-receipt budget containment, including sequential/total tool-call and resource
  envelope checks.
- Defined canonical structured-JSON hashing separately from raw-byte source/evidence
  hashing.
- Added review-bundle and continuation-anchor contracts and an exact-byte synthetic
  continuation rooted outside the receipt chain; external human receipts now bind the
  exact reviewed bundle and eligible reviewer.
- Expanded the malicious path corpus to cover all reserved `COM2`-`COM8` and
  `LPT2`-`LPT8` bare, case, extension, and intermediate forms.
- Expanded the protocol to 19 schemas and 20 inert JSON templates.
- Retained Level 0/default-deny status: the synthetic continuation is conformance
  evidence only and no live controller, project authority, model, adapter, runtime,
  evidence service, promotion, or publication path exists.

This is a breaking pre-release hardening change. `0.1.0` is retained as the failed
adversarial-review baseline and must not be treated as compatible or adoption-ready.

## 0.1.0 — 2026-08-22

- Established the Level 0, non-operational, default-deny blueprint.
- Added normative guidance, draft contracts, inert templates, synthetic examples, and a
  dependency-free self-validator.
- Reserved live adapters, leases, evidence acceptance, promotion, and publication for
  separately authorized and reviewed maturity transitions.

Historical review subsequently found false-green risks in cross-repository ownership,
evidence delegation, continuation trust, claim subjects, receipt lifecycle, budget
containment, and path-corpus coverage. Those findings are corrected in `0.2.0`.
