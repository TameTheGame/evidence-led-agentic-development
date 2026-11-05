# Changelog

## Unreleased

- **A tools entry on a PATH that went stale mid-run.** A `winget upgrade` of FFmpeg's
  portable package, partway through a check suite, removed the folder the suite's session
  had on its PATH, so its next FFmpeg check failed as if FFmpeg weren't installed. The
  import reference's [tools section](examples/sbox/IMPORTING.md#tools-and-scripting) now
  says to read PATH again from the registry before calling a tool missing.
- **A tools entry on Git's letter case.** On Windows, Git filed a new file under the letter
  case it already held for the file's folder, so a self-test that expected the spelling it
  planted passed on Linux and failed on Windows. The import reference's
  [tools section](examples/sbox/IMPORTING.md#tools-and-scripting) now says to expect the
  path as the commit filed it.
- **The engine test runner catches an S&box update mid-run, and both checks read Steam's
  build ID.** Steam installs a waiting update once its download has finished and no S&box
  process is running. The editor check read the build again after its last session, but
  `run_engine_tests.ps1` read it only before the run, and its help said it saved the
  engine version, which it didn't. It now reads the build before its source check and after
  the run, saves both in `build.txt`, and reports `NOT RUN` when they differ. Both scripts
  now read the build as the first line of `.version` with the `buildid` in Steam's
  `appmanifest_590830.acf`, so a new Steam build under the same `.version` counts too,
  which hasn't been seen. `-SelfTest` checks the reads on a planted install, including a
  planted fault: a new Steam build under the same `.version`.
- **The re-save lesson adds `26.11.03a`.** That build wrote five new fog fields at their
  defaults on a scene's first save, as `26.10.27` did with a light's. The lesson now says
  that the editor check fails its first save on such a scene until that save is committed,
  and to commit it when only the new fields differ.
- **The editor check starts one more editor after a stalled start.** On `26.11.03a` two
  editors in one project's run stopped logging at `Compiling Tools` and never became ready,
  with no error box, and `sbox-cli` gave up on each. `editor_check.ps1` counted such a
  start as a `FAIL`. It now closes an editor that isn't ready when `sbox-cli` stops or its
  time runs out, notes why with the last line its log reached, and starts one more; when
  that one isn't ready either, it stops with `NOT RUN`. The guide's
  [start-up section](examples/sbox/README.md#when-sbox-cant-start-a-project) adds the rule
  as its fourth step. `-SelfTest` checks it on planted starts.
- **Read a saved scene's references by path and its numbers as float32.** A new lesson in
  the S&box guide says why a check must not compare a saved scene's text. A reference saves
  as a path alone or as an `{"Id", "Path"}` object, depending on whether S&box knows the
  file's GUID, and on `26.11.03a` a project's own model saved as an object. A number's text
  can change while its value doesn't: `26.11.03a` wrote `22.0855522` where `26.10.27c`
  wrote `22.085552`, the same float32. Each broke a real check once. Read from the source
  at `26.10.27`.
- **S&box starts wait while another program uses the GPU.** A new
  `examples/sbox/tools/wait_for_gpu.ps1` reads `nvidia-smi` and holds a start while any
  GPU's use is above 30% or a process that isn't S&box holds 1 GB of video memory or more.
  It checks again every 5 minutes and ends with `NOT RUN` after an hour; each threshold and
  time is a parameter. Where Windows' driver model leaves a process's memory out of
  `nvidia-smi`, it reads Windows' GPU counters, and it warns and goes ahead when there is
  no `nvidia-smi`. It never touches another process. The engine test runner and the editor
  check call it before each S&box start and stop with `NOT RUN` without it, and the guide's
  new [Waiting for a free GPU](examples/sbox/README.md#waiting-for-a-free-gpu) section says
  to run it before any other start. A process's figure larger than the GPU's memory in use,
  or than the GPU, is reported and left out, since one NVIDIA overlay read as more than its
  card. `-SelfTest` checks it on faked `nvidia-smi` output.
- **The editor check puts back the scene's `_d`, fails a scene S&box rewrites, and catches
  an update mid-run.** A save writes a scene's binary data, such as its clutter, to
  `<scene>_d` beside it, and on `26.10.27c` a resave changed it. `editor_check.ps1` put
  back only the scene file and the `.sbproj`, so it could leave the scene and its `_d` out
  of step while it said it left the tree unchanged. It now puts back the scene's `_c`, `_d`
  and `.meta` too, keeping the editor's copy in the results, and asks Git which files the
  run left changed and names them. A first save that rewrites the scene file, in any byte
  but a store package's ID, is now a failed `First save` check, where it was a note, so the
  check can't pass on a committed scene that S&box doesn't write as it is. It also reads
  S&box's build again after its last session and reports `NOT RUN` when the build changed,
  since Steam can install a waiting update between its two sessions; it read the build only
  before the first. `-SelfTest` checks each on planted faults. Read from the source at
  `26.10.27`.
- **Start-up facts: the test folder, Steam's update and `.json` files.** S&box makes no
  `UnitTests` folder: it generates the test project only when the folder is already there.
  The guide's spike notes and the rung-1 starter now say so, and `run_engine_tests.ps1` now
  stops on a missing folder with `NOT RUN` and says to copy the starter's `UnitTests`
  folder in before opening the project, where it said only to open the project. Steam
  installs a waiting update once its download has finished and no S&box process is running,
  with no launch through Steam, and a start through `sbox-cli`, which runs `sbox-dev.exe`
  or `sbox.exe` directly, doesn't install it. So the starter's note on running the source
  check on a schedule says an update can land between any two runs and to read `.version`
  before each, and the editor check's Steam notes say one can land between its two
  sessions. The `.meta` lesson adds that S&box wrote no `.meta` for any `.json` file,
  though a project's own resource type can claim that extension. Seen on `26.10.27c` and
  read from the source at `26.10.27`.
- **Every eye means every height the eye can take.** The S&box guide's lesson on pressing
  through a wall now says which eyes to keep a usable thing out of reach of: at the
  defaults, from 28 in up when crouched to 64 standing, above the ground under each place
  the player can stand, and up to about 53 in more at the top of a jump. A duck in the air
  keeps the eye where it was. It adds that a static check that samples eye positions a step
  apart must fail a thing within `ReachLength` plus that step. Read from the source at
  `26.10.13` and `26.10.27`.
- **The S&box example's commands work in Git Bash.** The guide, the rung-1 starter and the
  scripts' own help wrote `powershell -File tools\<script>.ps1`, and in Git Bash a
  backslash in an unquoted path is an escape, so PowerShell got `tools<script>.ps1`. They
  now use forward slashes, which PowerShell reads the same, quote the `tools/*.cs` pattern
  so Git Bash doesn't expand it, and the starter says why.
- **The S&box example says what a project copies.** A new [Using this example in a
  project](examples/sbox/README.md#using-this-example-in-a-project) section lists each file
  a project copies and where it goes: the domain skill, the starter's `UnitTests/` and
  scripts, the compile check, the editor check with `package_ids.cs` beside it, and the
  Python tools. Setup step 1 links to it, and names the three skill folders to copy, since
  `skills/` also holds `evidence/`. The README and the guide drop lesson counts that had
  gone stale, and the guide and the roadmap no longer list a generated mesh saved into a
  scene as open, since the starter's saved mesh data run loaded one with its collision.
- **The worked spec points at the starter, and its cards are whole.** `outpost.spec.md`'s
  rung-1 sketch names the rung-1 starter for `TestSurfaces`, the stuck check and
  `ProjectRoot`, loads its layout from the project root, and uses
  `BodyStartsInsideGeometry`, since the spike's kit is a record, not code to copy. Its NET-1
  and FEEL-1 cards gain the pass, fail and stop lines the asking-the-owner skill's card
  has. `docs/SPEC_FORMAT.md` and `spec_lint.py`'s notes say to run the owner gate before
  each commit, or against the commit the task started from, since after a commit it
  compares with `HEAD` and reports nothing.
- **Five import reference entries agree with the guide.** The addon entries say that on
  `26.10.13b` no addon of Sandbox could open, link the guide's section on S&box failing to
  start a project, and give a bare addon its `Type` as well as its `ParentPackage`. The
  `GameTask.Yield` entry takes its delays in short steps inside a loop with a limit, as the
  camera lesson does. The water entry says to add a trigger `BoxCollider` before the
  `WaterVolume`, since the installed one requires a `BoxCollider` and brought a solid one.
  Two citations given by file name only now carry the full tagged path, so the recheck's
  search finds them, and the Garry's Mod steps check for a file of the same name before
  writing one, and delete only the files they added.
- **The spec lint fails a requirement heading it can't read.** A `###` heading under
  `## Requirements` without the ` — ` between its ID and sentence was skipped, so that
  requirement dropped out of the format checks, the check lookup and the owner gate with no
  word. `spec_lint.py` now fails each such heading by its line. `test_spec_lint.py`'s
  bad-format case gains one, which the old lint passes over.
- **`scene_refs.py` works through linked folders.** It worked out each file's path by
  resolving it, so a folder linked in from outside the assets root, such as a junction,
  stopped it with a traceback. It now names each file by the path a scene would use, and
  walks every folder through junctions and symbolic links, since `Path.rglob` stops
  following symbolic links from Python 3.13. `test_scene_refs.py` gains a linked bake
  folder, which the old tool fails, and a scene in a linked folder.
- **The hosted checks run the example tools' tests.** The workflow ran only `check.py` and
  its test, so a change that broke `spec_lint.py`, `scene_refs.py`, `check_metas.py` or
  the transcript analyzer still passed. It now runs each of their tests on Ubuntu and
  Windows, one per step, since on Windows a step's shell judges only its last command.
- **Two engine test runs never share a results folder.** `run_engine_tests.ps1` named its
  `test-results` folder to the second before it waited for the lock, so two runs started in
  the same second used one folder, and the second overwrote the first's results, TRX file
  and engine log. It now names the folder once it holds the lock, to the millisecond.
- **The compile check stops on any script path that matches nothing.** `compile_check.ps1`
  stopped only when no `-Scripts` entry matched, so a mistyped second path still gave
  `PASS` for the first script alone. It now stops with `NOT RUN` naming each entry that
  matches no file. Seen on `26.10.27c` with the old check passing such a run.
- **The editor check keeps its quotes in every PowerShell, and says what it left
  unrestored.** `editor_check.ps1` escaped the quotes in its `sbox-cli` arguments only on
  Windows PowerShell, but PowerShell 7.0-7.2, and later ones with
  `$PSNativeCommandArgumentPassing` set to `Legacy`, strip them too, so a call sent
  `{path:...}`. It now escapes them whenever native arguments pass the legacy way. When an
  editor is still listed after the run, the check leaves the scene and `.sbproj` as they
  are, and now says in a `Note:` which of them the run changed, where before it said
  nothing.
- **Blind extracts no longer give the condition away.** With `-HideSkills`,
  `blind_extracts.ps1` dropped the skill calls but kept the step numbers, so the gaps showed
  which runs had the skills: in the S&box skill test's published responses, 8 of the 9
  domain-skill runs show four gaps, and no run without it shows more than three. It now numbers the calls left 1, 2, 3 and points each step
  reference at its new number, and replaces only the extract's own `# Run` line.
  `analyze_transcripts.py` now cleans the final reply with the run's folder, which a quoted
  path could name. No published extract was affected.
- **The transcript analyzer counts only real runs, and says when it can't read.** A step
  that named `spec_lint` or `run_engine_tests`, such as `cat tools/run_engine_tests.ps1`,
  counted as a run, as in three live-test runs; now only a command that starts the script
  does, and every other run in the published extracts still counts. A diff git can't give
  reads `(diff unavailable: <why>)`, not `None.`; a transcript line that isn't JSON is
  skipped and listed, not a traceback; untracked names with spaces or non-ASCII letters
  come through whole; and a `--transcripts` folder with no transcripts is an error.
  `test_analyze_transcripts.py` gains five cases, each of which the old tool fails.
- **The skill-test runners stop on a setup they can't trust.** All three now need
  PowerShell 7, which they use, resolve their path arguments before any session changes
  folder, and stop when git fails while making a run's starting commit.
  `run_skills_test.ps1` stops on a scenario with no prompt. `run_live_test.ps1` stops when
  `SBOX_PUBLIC` is set for the user, since the engine test runner falls back to it, and
  checks the engine paths each project file names after its rewrite, instead of the path it
  meant to write.
- **The S&box skill points at the starter, and keeps lessons where the project says.**
  `sbox-engine-reference` now loads a saved scene with the starter's
  `EngineTestHelpers.LoadSavedScene`, since `SceneFile.LoadFromJson` drops a scene's `_d`
  mesh data; finds the default surface in the starter's `TestSurfaces.cs`, not the spike
  kit; and looks to `SBOX_PUBLIC` or `AGENTS.md` for the engine source clone. It records a
  lesson only in the lessons file `AGENTS.md` names, or, with none named, gives it in the
  report and asks the owner where lessons live, as rule, what happened, why and proof. The
  starter's suggested `AGENTS.md` lines name the clone and `docs/LESSONS.md`, and the import
  reference's entry shape builds on the skill's.
- **New evidence: `skills/evidence/SKILL_UPDATE_TEST.md`.** The change passed its
  pre-registered, blind-scored rule against the v1.07 text in 12 acting sessions. With it,
  3 of 3 runs asked the owner where a lesson should live, where 2 of 3 with the old text
  wrote a lessons file unasked. Saved-scene loading showed no difference, since every run
  used the starter's helper, and no run in either condition fixed a decal's random roll.
  `run_sbox_skill_test.ps1` now takes a plan's own fixture, prompts, starter files and skill
  version, a model, and `-BuildOnly`.
- **The owner gate can't go quiet.** A project that ran the spec lint from its suite showed
  the lint's output only on failure, and `NEEDS OWNER` never fails it, so every finding was
  lost, and after a commit the gate compared `HEAD` with itself. `docs/SPEC_FORMAT.md` and
  `spec_lint.py` now say to compare with the last commit the owner has seen, such as the
  point the branch left the main branch, and to show the output either way, and
  `--owner-exit N` gives a run that needs the owner, or skipped the gate, its own exit code.
  The gate also reports a requirement newly retired, and a retired one removed, since only
  the owner retires one. A spec the base lacks is compared as empty, and when the gate has no
  base, the summary says it was skipped instead of "no agreed requirement changed". The lint
  reports a machine check that doesn't name its ID, as the spec format asks, and the guide
  says the lint looks check names up only for agreed requirements, which rungs are machine
  and human, and that engine and editor checks go to their own rung's runner, not the
  per-change suite. `test_spec_lint.py` gains seven cases, each of which the old lint fails.
- **What closes a requirement, said plainly.** A requirement without `touches` now depends
  on everything, so any change reopens it, and `touches` are paths or data keys, not prose,
  as the samples now write them. A card defines its own replies, such as `GO`, `REVISE` and
  `NO-GO` for a decision, only its passing reply meets the requirement, and an unanswered
  card leaves it unmet. Result and `ACCEPTANCE.md` lines may carry the build they ran on.
  The worked spec's cards gain the build line and FEEL-1's limit.
- **An owner may hand off agreeing requirements, in writing.** The owner chose this in
  [ADR-0022](docs/DECISIONS.md#adr-0022--an-owner-may-hand-off-agreeing-requirements-in-writing)
  after an outside review found an agent agreeing requirements on an owner's written "decide
  on my behalf", which ELAD's rules didn't cover. A hand-off names the requirements or area
  it covers and when it ends, and keeps the owner's words. Each requirement agreed under it
  carries a new `agreed-by` field, and the owner gate still reports it. Changing or retiring
  a requirement stays the owner's. The spec format, the evidence ladder, the authority page
  and the README say so.
- **The skills teach the written hand-off.** `asking-the-owner` gains a section on it and a
  red flag: under a hand-off, agree only what it covers before it ends, give each requirement
  an `agreed-by` line quoting the owner, and list them in the report; consent with no scope
  or end, such as "decide on my behalf", isn't one. `matching-evidence-to-claims` points to
  it. **New evidence: `skills/evidence/HANDOFF_TEST.md`.** The change passed its
  pre-registered, blind-scored rule against the v1.07 text in 18 acting sessions. Both
  versions agreed under a scoped written hand-off and refused vague consent, but only the
  update recorded the hand-off in each requirement, in 3 of 3 runs against 0 of 3.
- **The engine test runner stops on a moved project.** S&box writes a project's `.csproj`
  files with engine paths relative to the project, so a checkout moved one folder deeper
  failed its rung-1 build with `CS0006` until the Editor reopened it. `run_engine_tests.ps1`
  now checks those paths first and stops with `NOT RUN`, naming each one that isn't there.
  `-SelfTest` gains two cases, and the guide gains the lesson, read from the solution
  generator's source.
- **Five more S&box and Windows lessons.** The guide says to space a sealing check's rays
  no wider than the player, 32 in, and cast them up to about 107 in above each floor, from
  the jump, the duck in the air and the step-up, and that the missing-file line can come
  with or without its ` - from <path>` ending on one build, so an excuse accepts both. The
  import reference's Git Bash entry adds that `cmd /c` loses its `/c`, so `cmd` runs nothing
  and exits 0, and a new entry says to search binary files' printable strings, not their raw
  bytes. The spec format says a wrapper should stop on a skipped owner gate, which
  `--owner-exit` now covers, and on an older lint's skip note.

## 1.07 — 2026-11-03

A batch of S&box example and spec format updates: an editor check that stops before it
starts an editor that can't work and checks its captures' size, four spec format rules on
checks and owner input, a spec lint fix for non-ASCII folders on Windows, and new and
extended lessons in the S&box guide and import reference. `tools/check.py` holds release
notes to the form GitHub shows. No skill changed, and nothing in the core breaks.

- **Release notes keep each paragraph on one line.** GitHub keeps every line break in a
  release's notes, so the hard-wrapped v1.06 notes showed a break in mid-sentence on the
  release page and in its email. `releases/v1.06.md` now has one line per paragraph and
  list item, and `docs/RELEASING.md` says to write them that way. `tools/check.py` fails
  when the notes for the version in `VERSION` are missing or have a line that carries on
  the one above it, leaving code blocks, tables, headings and list items alone.
  `test_check.py` gains three cases, and each of five planted faults in the check fails
  one.
- **Release notes link by full URLs pinned to the release's tag.** The release job
  publishes the notes as they are, and on the release page a relative link leads to a
  missing page, as each of the seven in the v1.06 notes did. `releases/v1.06.md` now links
  by full URLs pinned to `v1.06`, and `docs/RELEASING.md` says to link that way.
  `tools/check.py` fails a relative link in the current version's notes, and a link into
  this repository that names another tag, names a file or heading the repository doesn't
  have, or leaves the repository. `test_check.py` gains a case, and each of eight planted
  faults in the check fails one.
- **Two more world-build lessons.** The S&box guide's [More world-build
  lessons](examples/sbox/README.md#more-world-build-lessons) now says to bake envmap probes
  in the editor, keep the compiled bake in Git since it has no source, read a scene's
  `bake_<Id>.vtex` as its `.vtex_c`, and check that each probe holds a bake before a
  capture, since one with no bake reads black. It also says to check from the layout that a
  picture check's camera sees each thing it reads, since one hidden behind another changes
  almost no pixels when it's hidden. The `.meta` lesson and `check_metas.py`'s notes add
  that a file a project's own script writes under the assets folder, such as a bake's
  record, gets no `.meta`, and to leave it out by its folder and name.
- **More on cameras, fog and the clock.** The guide's `Fog` lesson adds that a camera with
  a `PostProcessAnchor` picks its volumes from that object's position, that a camera a
  scene already saved keeps its post-processing settings, so a build sets them on each
  camera it makes, and that the fog's height layer fogs a room below its height however
  near the camera stands. The SceneLoaded lesson adds that `TimeSince` and `TimeUntil` read
  the same clock, and a note after the first lessons list says a static check over the
  project's C# can hold four of them before any S&box run.
- **A check's result line stays on one line.** `docs/SPEC_FORMAT.md` now says a script's
  result line that quotes text another program wrote, such as an engine test's assertion
  message, turns that text's line breaks into spaces, since a runner that judges a result
  by its own line otherwise misses it. A first real project's suite runner failed a passing
  check this way.
- **The starter says to keep the AI block in the `.sbproj`.** An S&box editor opens the
  pipe that `sbox-cli` drives only when the project's `AI.EnableMcpCommunication` isn't
  `false`, even when started with `-mcp`. The rung-1 starter's set-up now has a step that
  says so, shows the block and where S&box writes it, and says the Editor adds it the first
  time it opens a project without one, which leaves the `.sbproj` changed until it is
  committed. The editor check's notes point to it.
- **The editor check stops at once when the AI setting is off.** When the project's
  `.sbproj` sets `AI.EnableMcpCommunication` to `false`, `editor_check.ps1` now stops with
  `NOT RUN` and says so before it starts an editor, where before `sbox-cli` waited out its
  start-up timeout. It reads the setting as S&box does, by its exact name, and leaves a
  `.sbproj` that isn't JSON to S&box's own error box. `-SelfTest` gains six cases, one of
  them a planted `.sbproj` with the setting off.
- **A camera lesson and a planted-refusal lesson.** The S&box guide's [More world-build
  lessons](examples/sbox/README.md#more-world-build-lessons) now says to read a player's
  camera once it has stopped turning, with a real-time limit, and fail one still moving,
  since in 2 of 45 runs a fixed wait after a turn read it part of the way round, though the
  source shows no smoothing of the turn. The starter's [Writing a requirement's
  test](examples/sbox/rung1-starter/README.md#writing-a-requirements-test) says that a
  planted case a step must refuse gets its own entry, which expects the refusal by its
  words, and that later steps don't read output a refused run never makes.
- **A missing-file excuse allows S&box's new line ending.** The guide's lesson on clients
  that log a small resource as missing now says that on `26.10.27c` a client logs the line
  as a warning that can end in ` - from <path>`, such as the run's own scene, and that an
  excuse should allow that ending only with the path it expects, while still matching the
  whole line.
- **The editor check checks its captures' size.** `editor_check.ps1` now refuses a `-Width`
  or `-Height` outside 16-4096 px before it starts, since the screenshot tool clamps them
  without saying so, and fails a capture whose own PNG header gives another size than the
  one asked for. `-SelfTest` gains five cases, one a planted capture at the tool's 1280 by
  720 default. A new world-build lesson says a capture's size comes from the picture, not
  the monitor or the Editor's game view, and that a GPU frame time read in the Editor is
  the Editor's, never the map's frame rate.
- **Two more `Fog` facts.** The guide's `Fog` lesson adds that a `GradientFog` a scene
  already saved still turns the world's own gradient fog on, apart from any `Fog`, so a
  scene that moves to `Fog` drops it and its scene check fails one, and that `Fog`'s sun
  glow is on by default.
- **A rebuild from a new owner input is compared with a fresh build.**
  `docs/SPEC_FORMAT.md` now says that after a project rebuilds the parts named in an
  owner's answer from a new input, it builds that input afresh into a scratch copy and
  compares, since a hand-made list of changed parts can miss one, and the hold compares
  with the last pinned copy, so it never sees the miss.
- **A small owner answer can amend the built parts.** `docs/SPEC_FORMAT.md` now says an
  answer that changes only a few parts built from an owner's input can land as an amendment
  file, pinned by its SHA-256, that names each part. A later new input must carry each
  amended value or say it supersedes it, since a rebuild from it would otherwise undo the
  answer while every check passes.
- **A wall doesn't stop a player's use.** A new world-build lesson in the S&box guide says
  a `PlayerController`'s use trace runs a ray and then two sphere passes, that each pass
  stops at a solid only for itself, and that on `26.10.27c` a player hovered a button
  behind a thin wall within reach. It says to keep a usable thing out of reach of every eye
  behind a wall, and to press in an engine test what the player hovers. The import
  reference's entry on usable things inside other solids now says the trace ends each pass,
  not the whole search, at a solid.
- **A settle wait counts the game's frames.** The camera lesson adds that a wait that saw
  too few frames means the game stalled, which a check fails as a stall, not as a camera
  still turning, and that a static check can fail a fixed wait before a reading in a
  `run_csharp` script. It also says to take the turn and its reading several times in one
  launch, since a part-way read seen in 2 of 45 runs passes most single runs.
- **Scripted input reaches a fixed update only from a fixed-step hook.** The import
  reference's `Input.SetAction` entry now says that a press set at `Stage.StartUpdate`
  reaches only code that runs in the update. The stock player reads move, run, duck and
  jump in its fixed update, which runs before `StartUpdate` with its own input context, so
  the entry says to set `Input.AnalogMove` on every fixed step from a
  `Stage.StartFixedUpdate` hook, and a jump on one step only. Read from the source at
  `26.10.13` and `26.10.27`; not yet seen in a run.
- **A check a spec cites must run in the suite.** `docs/SPEC_FORMAT.md` now says that
  finding a check's name in the test sources doesn't show anything runs it. A check the
  suite and CI leave out holds nothing, so the commit that brings a citation or its check
  adds the check to the suite, with a planted fault it fails. A first real project found a
  generator's check that two records cited and nothing ran.
- **A `-joinlocal` client and `sbox-cli`.** A new session lesson in the S&box guide says a
  game started with `-joinlocal` waits for sign-in and then joins the local host on its own
  as start-up ends, that `sbox-cli` can reach a game only if it was started with `-mcp`,
  which `sbox-cli --game` adds but a script's own start must, and that each such client
  takes a made-up Steam ID from its `+instanceid`. Read from the source at `26.10.13` and
  `26.10.27`.
- **A repeat loop lets a test that didn't run end inconclusive.** The camera lesson adds
  that a loop that catches each failed repeat so the next one still runs must let
  `Assert.Inconclusive` through while no repeat has failed. Otherwise the engine test
  runner reads a test that couldn't run, such as one with no saved scene, as ten failures,
  not `INCONCLUSIVE`.
- **The spec lint finds its repository under a non-ASCII folder on Windows.**
  `spec_lint.py` read Git's path for the repository as text, which Python decodes in the
  ANSI code page on Windows, such as cp1252. Under a folder whose name is outside ASCII,
  the path didn't match the spec's, so the lint skipped the owner gate and the retired-ID
  check with only a note and passed a changed agreed sentence. It now decodes the path as
  Python decodes file names. `test_spec_lint.py` gains a case under such a folder, which
  fails with the old lint when its text runs decode in cp1252, and runs the lint with UTF-8
  mode off, since a PC that sets `PYTHONUTF8=1` decodes text runs as UTF-8 and hid the bug.
- **Git Bash rewrites arguments that start with a slash.** The import reference's Tools and
  scripting section gains an entry: Git Bash, often an agent's Bash tool on Windows, turns
  an argument such as `/old/path` or `^/old/` into a path under Git's install folder before
  a Windows program sees it, so a search for it finds nothing and exits as if there were no
  hits. Put `MSYS_NO_PATHCONV=1` before such a command, with its real paths in Windows
  form, or run it from PowerShell. Seen with Git for Windows 2.56.0, where searches for a
  moved folder's old path missed real hits.
- **Test a Python tool with UTF-8 mode off.** The import reference's Tools and scripting
  section gains an entry: a machine that sets `PYTHONUTF8=1`, or runs Python 3.15, where
  that is the default, decodes text runs and pipes as UTF-8, so a code-page bug that Python
  3.14 and earlier hit on Windows doesn't show there. A tool's tests run it with
  `PYTHONIOENCODING=cp1252` and `PYTHONUTF8=0`, as `test_spec_lint.py` now does.

## 1.06 — 2026-11-02

A batch of S&box example updates: an engine test runner that no longer reads a run that
proved nothing as a pass, an editor check that sets store package IDs aside, a static check
for `.meta` files, and twenty world-build lessons. ELAD's Python tools write UTF-8 on any
pipe, and the spec format guide suggests a hold on files built from an input the owner
adopted. No skill changed, and nothing in the core breaks.

- **The S&box engine test runner no longer reads a run that proved nothing as a pass.**
  `dotnet test` exits 0 when tests stop with `Assert.Inconclusive`, because MSTest records
  them as not executed, so a run whose tests all stopped inconclusive read as a pass.
  `examples/sbox/rung1-starter/tools/run_engine_tests.ps1` now reads each test's outcome
  from the run's TRX file and ends with a `Result:` line: `PASS` (exit 0) only when at
  least one test ran and every test passed, `FAIL` (exit 1) on a failure, and
  `INCONCLUSIVE` (exit 2) when a test didn't run or none ran. It also stops a run at
  `-TimeoutSeconds`, 30 minutes by default, by killing `dotnet test` and every process
  under it, and keeps the output and the engine log. `-SelfTest` checks both without S&box.
  Run on S&box `26.10.27c`: seven passing tests gave `PASS`, a missing scene and a filter
  that matched nothing gave `INCONCLUSIVE`, and a 5-second limit killed the run's whole
  tree.
- **The S&box editor check sets store package IDs aside.** S&box can give a store
  package's files new IDs in each editor session, as it did on `26.10.13a`, and then the
  resave check would fail a scene that used one. `examples/sbox/tools/editor_check.ps1`
  now runs the new `examples/sbox/tools/package_ids.cs` through `run_csharp` after each
  save, and sets a reference's ID aside only when it is exactly the ID its own session gave
  the path; every other byte still has to match. `-SelfTest` checks the comparison on
  planted saves, including a planted break. Run on S&box `26.10.27c`: a scene with a store
  package's model re-saved byte for byte, since the model kept its ID in every session, so
  only the planted saves exercise the ID compare. In another project on the same build, a
  store package's material did get a new ID between sessions. A component that changes its
  own saved value still failed it.
- **One more S&box lesson: compare read-back rotations with atan2.** The S&box guide's
  "More world-build lessons" adds that S&box's float32 quaternions are only nearly unit, so
  `2 acos(|a · b|)` reads two identical rotations as 0.03 degrees apart, and that
  `Rotation.Distance` can't see turns under about 0.03 degrees. Scale to unit length and
  take `4 atan2(|a - b|, |a + b|)`. Read from the source at `26.10.13` and `26.10.27`, and
  seen on `26.10.27c`; the `Rotation.Distance` part is worked from the source, not run.
- **One more S&box lesson: load a sound with `LoadAsync` before reading its length.** The
  S&box guide's "More world-build lessons" adds that `SoundFile.Load` returns a handle and
  loads nothing, so a script that reads `Duration` straight after it fails, and that a
  script should call `LoadAsync` again until `IsLoaded`, with a limit. Read from the source
  at `26.10.13` and `26.10.27`, and seen on `26.10.27c`.
- **One more S&box lesson: a sound component's `Force2d` works with Sound Override off.**
  The S&box guide's "More world-build lessons" adds that `BaseSoundComponent` applies
  `Force2d` whether Sound Override is on or not, and that it turns distance attenuation
  off, so a script that builds sound emitters sets it to false and reads it back. Read from
  the source at `26.10.13` and `26.10.27`, not run. The store package ID lesson adds that a
  store material's ID did change between sessions on `26.10.27c`.
- **Two more S&box lessons: set a picture compare's threshold from runs, and put back a
  failed build's writes.** The S&box guide's "More world-build lessons" adds a way to set
  the share of changed pixels a screenshot compare allows: half the share a planted change
  moves, set only when two captures of one build stay under it, recorded with its runs and
  held to them by the self-test. Two play-mode captures of one build came out byte for byte
  the same on `26.10.27c`. It also adds that `Asset.MetaData.Set` writes the `.meta` file
  on every call, so a build that fails part way can leave some `.meta` files set, and that
  the run that counts starts from Git's copies. Read from the source at `26.10.13` and
  `26.10.27`, and seen on `26.10.27c`.
- **One more S&box lesson: ask for a compile with `Compile`, but don't take its result as
  the verdict.** The S&box guide's "More world-build lessons" adds that
  `NativeAsset.Compile` can return false for a compile that works, and that a compiled file
  an earlier build left counts for nothing, so a script waits with a limit for a compiled
  file written at or after the source, judged by other file times and never by the clock.
  Read from the source at `26.10.13` and `26.10.27`, and seen on `26.10.27c` and in a test
  on Windows.
- **One more S&box lesson: set a decal's `Rotation` to a constant.** The S&box guide's
  "More world-build lessons" adds that a `Decal`'s `Rotation` defaults to a range from 0 to
  360, from which the component takes a new random roll each time it is enabled, so a decal
  left at it turns between loads, and that a scene check can tell a constant from a range
  in the saved scene. Read from the source at `26.10.13` and `26.10.27`, not run.
- **One more S&box lesson: put a map's `Fog` where no camera or post-process volume owns
  it.** The S&box guide's "More world-build lessons" gains it. On `26.10.27`, `Fog`
  replaces the obsolete `GradientFog`, and it is the one post-process effect that is a
  camera effect: it belongs to the nearest camera or volume on its object or above it, and
  with none it fogs every camera. Set its mode, colour and `SkyAffect`, since by default it
  takes its colour from the sky and covers the sky too. Read from the source at `26.10.27`.
- **The spec format guide suggests a hold on files built from an input the owner adopted.**
  `docs/SPEC_FORMAT.md` now says a project's lint can hold the parts it builds from such an
  input, such as a plan, to their copy at the commit that last pinned the input's SHA-256,
  and let them change only in a commit that pins the new input and records the owner's
  answer. Without that route, the owner's first answer can only land by loosening the
  check.
- **The S&box lesson on `.meta` files adds when to commit them.** The Editor writes a
  `.meta` for every new source it mounts, in every folder at once, so a build of one scene
  fails its clean-tree check on another change's sources. Commit new sources with their
  `.meta` files before the build, and a static check that every tracked asset has its
  `.meta` catches a missing one without S&box. Read from the source at `26.10.13` and
  `26.10.27`, and seen on `26.10.27c`.
- **A static check for the `.meta` files S&box writes.**
  `examples/sbox/tools/check_metas.py` fails each file Git tracks under a project's assets
  folder with no tracked `.meta` beside it, comparing names in any letter case and leaving
  out the files S&box writes none for. It ends `NOT RUN` when Git tracks no file there, so
  a run from the wrong folder can't pass. `test_check_metas.py` checks it on throwaway Git
  repositories, with four controls, and each of eight planted faults in the check fails it.
  On a real project's tracked assets it agreed with that project's own check.
- **The S&box example's Python tools write UTF-8 on any pipe.** On Windows, Python gives a
  pipe the ANSI code page, such as cp1252. So `spec_lint.py`'s owner gate showed a changed
  sentence's "·" as a byte a UTF-8 reader can't read and its "≥" or "→" as "?", and
  `scene_refs.py` stopped on a file name outside that code page. `spec_lint.py`,
  `scene_refs.py` and `check_metas.py` now set their output to UTF-8. Each test runs its
  tool with a cp1252 stdout, as Windows pipes it, reads the output as UTF-8, and has a case
  with characters outside cp1252, which fails with the old tool.
- **ELAD's other Python tools and the tests write UTF-8 on any pipe too.** Each prints text
  it didn't write: `tools/check.py` a file name, a link target or a commit's author,
  `analyze_transcripts.py` a lint's last line and its own "exit≠0" mark, and each test a
  failing case's output. On a Windows pipe in the ANSI code page, the first character
  outside it stopped the script with a traceback in place of its report, as on CI's Windows
  leg or in an agent's shell. `check.py`, `analyze_transcripts.py` and the five tests now
  set their output to UTF-8. `test_check.py` gains two cases that run the check with a
  cp1252 stdout, and the new `skills/evidence/tools/test_analyze_transcripts.py` runs the
  tool the same way; each case with characters outside cp1252 fails with the old tool.
- **ELAD releases no longer wait for a GREEN each.** On 2026-11-01 the owner gave standing
  approval for releases. The delivery agent releases a batch on its own when it has
  something a user would notice, in the evening and not every day, always with release
  notes in plain words. The owner can withdraw the approval, and then each release waits
  for a typed GREEN again. `docs/RELEASING.md` says so, and ADR-0021 records it.
- **Twelve more S&box lessons, from world building.** The S&box guide gains a section,
  "More world-build lessons": commit the `.meta` files S&box writes; allow for a store
  package's asset ID changing between sessions, and install a new package in a session
  of its own; change the resource S&box holds for a file rather than a new one; wait with a
  limit for a resource's compiled file; reload a resource yourself behind a junction, which
  the Editor's file watch can't see through; give a generated material its world mapping;
  keep the tags an object's components add; add a code library's assembly to the type
  library in engine tests; read a store package's licence from `AssetLicense`; commit what
  the Editor re-saves after an update adds fields; and tell a waiting S&box update by
  Steam's target build ID. The start-up error section adds that a library's `.sbproj` that
  isn't valid JSON stops the Editor too. Read from the source at `26.10.13` and `26.10.27`,
  and seen on `26.10.13a` to `26.10.27c` except where an entry says otherwise.

## 1.05 — 2026-11-01

A batch of S&box example updates: 27 more import lessons, a guard that stops the editor
check hanging on S&box's start-up error box, a check for clearing out generated files, and
three new sections in the S&box guide. No skill changed, and nothing in the core breaks.

- **Reading the screen's real size on Windows.** The S&box guide's note on checking motion
  on the screen adds that a process that isn't DPI aware is told a scaled screen size, so a
  4K monitor at 150% reads as 2560 x 1440. A check on a recording's size reads the screens
  per-monitor DPI aware and checks them against the video card's real resolution. Seen on
  Windows.
- **A build outside S&box can't catch one Editor compile error.** The import reference's
  entry on setting properties in a constructor adds that only the Editor's compile copies
  property initializers into `[DefaultValue]`, so `dotnet build` and the compile check pass
  code the Editor rejects, and a rule in the source is the guard. The S&box guide's compile
  check section says it doesn't run S&box's code generator. Read from the source at
  `26.10.13` and `26.10.27`.
- **Two more S&box facts, and a fix to the exposure entry.** The S&box guide's world-build
  lessons gain one on a joining client logging small resources as missing even when they
  load, since files under 64 KB reach it only in memory. The import reference's exposure
  entry adds that a probe bake doesn't go through the camera's exposure, and now says that
  turning auto exposure off drops `ExposureCompensation` too, where it said only the
  adaptation stopped.
- **Four more S&box import lessons, on lighting.** `examples/sbox/IMPORTING.md` gains
  entries on bringing Source's glowing textures over as lights and on matching an imported
  map's brightness with auto exposure off. The entry on starting lights as their flag says
  adds that a Source light with no name is lit all game, and the live-screen entry adds
  keeping lights out of the screen's camera, so their shadow maps aren't made again every
  frame. Each was checked on S&box `26.10.13b`.
- **Two more S&box import lessons, and more on timeouts and converters.**
  `examples/sbox/IMPORTING.md` gains entries on turning a Source normal map's green channel
  over and on drawing a live in-world screen from a camera. The `sbox-cli` timeout entry
  now gives the default timeout, says that a timeout cancels a script only if the script
  checks for it, and says to stop rather than resend a call that timed out. The entry on
  files written while the Editor is open adds that a converter should leave a file alone
  when its bytes haven't changed. Each was checked on S&box `26.10.13b`.
- **Throwaway S&box projects come off S&box's project list.** The S&box guide's new section,
  Throwaway projects, says that opening a project in the Editor lists it in
  `<engine>\config\addons.json`, that it stays there until its folder is deleted, and how to
  clear a throwaway project away. The engine-rung spike's clean-up step and the import
  reference's bare-addon entry now point to it. Seen on S&box `26.10.13b`.
- **The S&box editor check no longer waits on S&box's start-up error box.** When the
  Editor can't start a project, it shows an error box and waits for someone to click OK,
  so an agent waiting for the editor waited too. `examples/sbox/tools/editor_check.ps1` now
  watches for that box and for the failure in the editor log while the editor starts. On
  either, it saves the box's text, closes the editor and the box, and stops with `NOT RUN`
  and the error's own words, in seconds rather than after its timeout. The S&box guide's new
  section, When S&box can't start a project, says what sets the box off and how any script
  that starts S&box should guard against it. Checked on S&box `26.10.13b`.
- **One more import lesson, and a sharper fix for players on lifts.**
  `examples/sbox/IMPORTING.md` gains an entry on Python writing `\r\n` line endings on
  Windows that bash's `read` keeps. The entry on waking the player on a moving floor now
  keeps the body awake for as long as it stands on anything that moves, since waking it
  after the floor moves is too late. Each was checked on S&box `26.10.13a` or on Windows.
- **One more S&box import lesson.** `examples/sbox/IMPORTING.md` gains an entry on reading
  a power system's state only from the lamps that start dark. It was checked on S&box
  `26.10.13a`.
- **Two more S&box import lessons, and more on lighting.** `examples/sbox/IMPORTING.md`
  gains entries on Source's `$selfillum` and on traces that pass through one-sided world
  collision. The lamp entry adds soft fill light, the indoor-light entry adds daylight in a
  probe bake and probe spacing for passages, and the entry on files written while the
  Editor is open adds compiling the ones you rewrite. Each was checked on S&box
  `26.10.13a`.
- **A check for clearing out generated files, and four more S&box import lessons.**
  `examples/sbox/tools/scene_refs.py` lists each file in a folder as in use or unused by a
  project's scenes and prefabs, comparing paths the way S&box does, and fails when a scene
  references a file that isn't there. The S&box guide's new section, Clearing out generated
  files, uses it to move old bakes aside safely. `examples/sbox/IMPORTING.md` gains entries
  on Source lamp falloff, a light volume for each lamp state, `sbox-cli` calls that time
  out, and matching a scene's references without regard to case. The live-lighting entry
  now says how to light rooms with baked `IndirectLightVolume`s, which it had only guessed
  at. Each was checked on S&box `26.10.13a`.
- **Seven more S&box import lessons, and Sandbox play in one project.**
  `examples/sbox/IMPORTING.md` gains entries on colliders that carry things, Source's sound
  fade and sound levels, cameras in play, rope width, faces S&box can't triangulate, and
  checking an engine type's members in the running editor before coding from the engine
  source. Playing a map inside Facepunch's Sandbox now takes one addon project, not two,
  and the entry covers the game's project settings and its player's input. The water entry
  covers Sandbox's water, and "Ask the original game what it does" adds checking a
  remembered server rule against the map itself. Each was checked on S&box `26.10.13a`.
- **Two more S&box import lessons, and Source's sound cut-off.**
  `examples/sbox/IMPORTING.md` gains entries on triggering a game's input action from code
  and on trying a bare addon project first when the parent game misbehaves. The sound-fade
  entry adds the distance past which Source never sends a sound, and the sound-level entry
  covers `func_rotating`. Each was checked on S&box `26.10.13a`.
- **Six more S&box import lessons, and checking motion on screen.**
  `examples/sbox/IMPORTING.md` gains entries on making a mesh not solid, Sandbox's physics
  gun events, break pieces' outward burst, melee push, waiting a frame in `run_csharp`, and
  drawing moving brushes without judder. The ragdoll entry now builds knees and elbows as
  hinges, the soundscape entry makes Source's choice, the camera entry keeps the game's own
  camera, the input entry adds hiding an action, and the translucency entry names its cost.
  The S&box guide's ladder section adds recording the game window to check motion a player
  sees. Each was checked on S&box `26.10.13a`.

## 1.04 — 2026-10-21

The first batched release. It brings a release cadence and 32 more S&box import lessons. No
skill changed, and nothing in the core breaks.

- **Releases come in batches.** `docs/RELEASING.md` gains "Release cadence", and ADR-0021
  records it. Finished changes collect on `tamethegame/next-release`, each with a
  changelog line under `Unreleased` and no version bump, and `main` moves only at release
  time. A release is due when the batch has something a user would notice: a new or
  changed skill, a new guide or example, a fix a project needs, or a breaking change.
  Typos and small tidies wait. It goes out on one GREEN from the owner, in the evening and
  not every day. An urgent fix lands on the branch too and ships the batch early.
  `AGENTS.md`, `CONTRIBUTING.md`, and the README now say the same. From `v1.01` to
  `v1.03`, each update was its own release.
- **Twenty more S&box import lessons.** `examples/sbox/IMPORTING.md` gains entries on
  building ragdolls at run time, keeping a Source collision model's convex pieces, taking
  brush entities' collision and mass from the BSP, displacement ground, mass, impact
  breaking, hinge friction, air drag, surfaces with sounds, water, ladders, lifts, and
  registering files the Editor didn't make. "Ask the original game what it does" now says
  how to measure physics and record ragdoll poses, and a new entry says to run a case
  with the fix off before writing a fix. Each was checked on S&box `26.10.13a`.
- **Twelve more S&box import lessons, and a clearer impact-damage entry.**
  `examples/sbox/IMPORTING.md` gains entries on props the player carries, breakable
  brushes, radius damage, traces that start inside a collider, soundscapes, sound loops,
  underwater sound, `func_breakable` sounds, `trigger_hurt`, what a breaking entity takes
  with it, playing a map inside Facepunch's Sandbox, and 3D skyboxes, under a new "World
  geometry" section. The impact-damage entry now says that a prop's mass cancels when it
  hits the world, and that props hit about 1.4 times faster than the speed they lose. Each
  was checked on S&box `26.10.13a`.
- **Two import entries corrected.** The radius-damage entry now gives the 1.25 explosion
  scale to `func_physbox` as well as `func_breakable`. The entry on traces that start
  inside a collider no longer says how Source's trace treats one, since that is engine
  code outside the SDK.

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
