# Projects That Already Have Gates

Some projects come to ELAD with a process of their own: numbered gates, sign-off cards,
permission files, and receipts that record each pass. This page says how to move such a
project onto specs without quietly losing what its gates protected.

It comes from one move on one project, so it is a starting point, not a tested rule. The
examples are synthetic.

## Map every old gate

Put an **Old gates** table at the end of the first spec, with one row per gate. Each row
ends in exactly one of three outcomes:

| Outcome | When | The row says |
|---|---|---|
| **Requirement** | The gate proved something observable about the product, such as collision or a clean save. | The new requirement IDs. |
| **Retired** | The gate checked the old process itself, depended on a tool that no longer exists, or applied only if another gate failed. | `Retired:`, the reason, and what takes its place, if anything. |
| **Postponed** | The claim still matters, but not to this spec. | `Postponed to` the spec that will carry it, and why it waits. |

A gate that mixes these gets one row that names the requirement for the part that maps and
says why the rest is retired. A gate with no row has been dropped without a decision.

A synthetic outpost map moving seven gates into `spec/outpost.spec.md`:

| Old gate | Now |
|---|---|
| G-00 gate-tool conformance | Retired: it checked the gate tooling this move replaces. The spec lint takes its place. |
| G-01 editor command allowlist | Retired: `AGENTS.md` now lists what needs the owner first. |
| G-02 collision fixture | OUT-COLL-01 |
| G-03 save and reopen | OUT-SAVE-01 |
| G-04 safe rebuild | OUT-REBUILD-01 covers rerunning a build that stopped halfway. The rest is retired: it checked the old job queue, which nothing uses now. |
| G-05 remote client | Postponed to `spec/network.spec.md`, not yet written: the outpost has no networking yet. |
| G-06 fallback if G-05 fails | Retired: it applied only if G-05 failed. If the network spec's client check fails, the fix becomes a new requirement there. |

## Rewrite gates as requirements

- **Write one observable sentence** in the [spec format](SPEC_FORMAT.md). Give it a new
  `AREA-TOPIC-NN` ID, and put the gate's old ID in its `why:` line, such as `why: old G-02`,
  so the history stays easy to find.
- **Choose the rung again.** A gate often ran on an expensive rung because its tooling lived
  there. A collision check that traced inside the editor can move to a headless engine
  test once the project has one. Use the cheapest rung that can settle the claim today.
- **Split mixed gates.** A gate that checked both a clean save and how a screenshot looks
  becomes a machine requirement and an owner card.
- **Watch each new check fail once.** Break it on purpose before trusting it. A gate that
  passed under the old tooling says nothing about the new check.

## Give postponed gates a home

- **Name the spec that will carry each one,** even before that spec is written, and say why
  it waits.
- **That spec gets its own Old gates table** when it's written, with one row for each gate
  postponed to it:

  | Old gate | Now |
  |---|---|
  | G-05 remote client | NET-CLIENT-01 |

- **Until then, postponed rows are open work.** A report on the project's state lists them,
  rather than counting them as settled.

## Old results stay as history

- **Keep the old records unchanged,** and stop running them. Don't delete them, and don't
  edit them to fit the new format. A small rung-0 check that they never change is cheap.
- **They don't count as results for new requirements.** A requirement is met only when its
  own check passes at a commit. Rerun the machine checks, and ask the owner again only for
  what is theirs.

## Keep one source of permission

Old processes often carry their own permission system, such as grants, leases, approval
lists, or qualification certificates. After the move, the project's `AGENTS.md` alone says
what agents may do; see [Authority and Safety](AUTHORITY_AND_SAFETY.md).

- **Move each permission rule or retire it.** A rule that still matters becomes a plain line
  in `AGENTS.md`, such as a list of actions that need the owner first. The rest is retired
  in the table.
- **Mark the old permission files as history.** Two sources of permission disagree sooner
  or later.

## The owner decides the move

- **Agents draft; the owner agrees.** Retiring a gate is like retiring a requirement, so
  only the owner agrees it, along with the spec.
- **Ask the hard rows on their own.** When retiring a gate could drop a protection the owner
  cares about, ask that one as a short question with a recommendation, rather than leaving
  it in the table.
- **Record the move once** in the project's own decision log: the ELAD version and commit
  it pins, what it supersedes, why, and what stays as history.

## Start with a small spec

Map the gates onto a small first spec, such as a pilot, not the whole roadmap. Gates the
pilot doesn't need are postponed to the specs that will. In the one move so far, the
pilot's spec fit on one page, and the next spec's draft built its checks on the pilot's.
