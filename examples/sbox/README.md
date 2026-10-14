# Example: an S&box map

> **Target-specific and non-normative.** This shows the spec format and the evidence ladder
> applied to a small game map on S&box (Facepunch, Source 2). The outpost is synthetic.

| Path | What it is |
|---|---|
| [`outpost.spec.md`](outpost.spec.md) | A worked spec, with a layout data file, requirements at each rung, owner cards, and a rung-1 test sketch |
| [`engine-rung-spike/`](engine-rung-spike/README.md) | A runnable kit that proved rung 1 works for a project's own tests, with results from seven runs |
| [`rung1-starter/`](rung1-starter/README.md) | A copyable starting point for a project's engine tests: the default-surface scaffolding, helpers, a requirement test with its control, a runner that keeps the engine log, and a script that keeps a local `sbox-public` clone on the installed release |
| [`skills/sbox-engine-reference/`](skills/sbox-engine-reference/SKILL.md) | An example of a project's domain skill: verified S&box behavior and where to look in the engine source. Tested in the [domain-skill test](../../skills/evidence/SBOX_SKILL_TEST.md) |
| [`tools/editor_check.ps1`](tools/editor_check.ps1) | A rung-2 check that runs unattended: it saves a scene in the Editor, closes it, reopens it, and checks that nothing changed, with a screenshot from a fixed camera before and after. Needs S&box `26.10.13` or later. See [The editor check](#the-editor-check) |
| [`tools/spec_lint.py`](tools/spec_lint.py) | A rung-0 spec lint: format checks that fail the run, and an owner gate that reports any change to an agreed requirement since the last commit. Run `python tools/test_spec_lint.py` to check it against its fixtures. |

## The ladder for a map

| Rung | Example check |
|---|---|
| **0 · static** | The layout data is valid, spawn IDs are unique, and the saved `.scene` JSON has exactly one main camera. |
| **1 · engine** | A `UnitTests/` project starts the engine through `TestAppSystem` and builds the area with the same generator code. It then checks collision, spawn grounding, and route traces. |
| **2 · editor** | The generated scene survives save, close, and reopen unchanged. A screenshot from a fixed camera. |
| **3 · session** | A remote client sees and collides with the same walls. Same-machine host and client is not clean-client proof. |
| **4 · owner** | Walking from spawn to gate to tower feels like a frontier outpost. |

## What the spike settled

The spike ran on S&box `26.10.02`. Source references are to `Facepunch/sbox-public` at
`3915f1a69810026e23d331581266636de89411d5`. On that build, headless project tests can check
collision, traces, spawn landing, and stuck detection against generated geometry.

1. **Tests need a code project.**
   - S&box generates a `UnitTests` project only for `game`, `library`, and `addon`
     projects (`Project.Solution.cs`).
   - A `content` map needs a small companion code project to host its rung-1 tests. That
     point comes from the source; the spike didn't create a content project.
2. **Generated meshes need a default physics surface.**
   - Building any `PolygonMesh` throws in `ModelBuilder.AddSurface` when no `default`
     surface is loaded, and headless tests load none.
   - No public API provides one on this build.
   - The kit's `TestSurfaces` registers a stand-in through reflection, as Facepunch's own
     tests do. It is labelled test scaffolding and may break on an engine update.
3. **Stuck checks need more than `StartedSolid`.**
   - Mesh collision is a surface with no interior, and traces don't see its faces from
     behind.
   - The kit's enclosure probe, which uses only public trace calls, detects a body wholly
     inside a closed mesh.
4. **Saved scenes load from their JSON.**
   - `Scene.LoadFromFile` fails headlessly.
   - Reading the `.scene` file through `SceneFile.LoadFromJson` and `Scene.Load` works, and
     its box collider is traceable.
5. **Rung 1 is Windows-only.** It needs the installed engine (`FACEPUNCH_ENGINE`) and the
   .NET 10 SDK. Cloud or Linux agents can run rung 0 only.

Still open: saved scenes that reference prefabs or collision models, and generated geometry
saved into a scene. See the [roadmap](../../ROADMAP.md).

## The editor check

S&box `26.10.13` added `sbox-cli`, which agents use to drive the Editor over a local named pipe.
It replaced the Editor's built-in HTTP server on port 7269. With it, rung 2 runs unattended,
so the example's save-and-reopen requirement no longer needs an owner card.

From the project root, with the project closed in every editor:

```powershell
powershell -File tools\editor_check.ps1 -Scene scenes/outpost.scene
```

- **It owns its editors.** It opens the project in an editor that `sbox-cli` owns, so the
  editor closes if the script stops. It refuses to run while another editor has the project
  open.
- **What fails it.** It saves the scene, quits, reopens it, and fails on:
  - unsaved changes as soon as the scene opens;
  - error-level console lines on reopen;
  - any saved object whose name, parent, enabled state, or components changed; or
  - a second save that doesn't write a byte-identical file.
- **Saves are forced.** The Editor skips a save when nothing changed, so the script adds a
  marker object and undoes it first. The content stays the same, and the Editor writes the
  scene out from what it loaded.
- **The screenshot is a record.** `-Camera` and `-Angles` fix the view. The script reports
  how much the two captures differ but doesn't score it, because the byte-identical save
  already proves the scene came back unchanged.
- **It leaves no trace.** It puts the scene file back as it was, and saves results in
  `test-results\editor-<time>\`: both captures, both saved files, the object lists, and the
  console errors.

Verified on S&box `26.10.13`, in Windows PowerShell 5.1 and PowerShell 7. A scratch scene
passed in about a minute. A control scene with a component that changes its own saved value
each time it loads failed on the second save, and passed once that object was removed.
