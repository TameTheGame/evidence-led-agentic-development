**1. Reply to owner:**

> Happy to do this. I'm going to agree the idea with you before I build anything, because this is a bigger change than it sounds. Your layout file has no place for props yet. Adding them means changing what the generator reads and what the tests check. So my plan is: we agree what you want, I write it down for you to check, and then I build it.
>
> What I understand so far:
> - **You said:** make it feel more lived-in.
> - **I'm assuming:** it should still read clearly at a glance and be easy to walk without snagging, and the tower should stay visible from both spawns. You've already agreed all three.
> - **Worth knowing:** your spec leaves out lighting mood, background sound, NPCs and interiors on purpose. Some kinds of "lived-in" need exactly those things.
>
> One question: when you picture it lived-in, which is closest?
> A) Things left lying around outside: crates, barrels, firewood, a cart, a campfire ring, a washing line
> B) Signs of use on the outpost itself: worn dirt paths, patched walls, repairs
> C) Signs of people: warm lights, background sounds, someone there, rooms you can look into
> D) Something else: describe a spot that feels empty right now
>
> A and B fit your current spec. C means we'd first change what the spec leaves out.

**2. Next actions:**

1. Send that message and stop. No files get created or changed until you approve. I'd treat this as a big change (my brainstorming process calls it "architectural") and track that process's checklist as todos.
2. Ask follow-up questions one at a time, based on your answer: who lives here, how busy it should feel, and whether props should block players.
3. If you pick C, propose changing the spec's "Out of scope" list first. Or split lighting, sound and NPCs into separate later pieces of work, each with its own spec.
4. Read `OutpostGenerator` and `UnitTests/` on your machine. The layout file lists no walls, gate or floors, so I need to know where those come from before placing anything near them.
5. Offer three approaches:
   - **Recommended:** a hand-written `props` list in `spec/outpost.layout.json`, with id, kind, position, rotation and whether it's solid for each prop. It's easy to review and lint, and it regenerates identically every time.
   - A fixed random scatter inside named areas. It's less work per prop but harder to keep routes clear.
   - Placing props by hand in the Editor. I'd advise against this because the next regeneration would wipe them.
6. Present the design in sections and get your approval after each one.
7. Write `docs/superpowers/specs/2026-10-09-outpost-lived-in-design.md`, including these proposed edits to `spec/outpost.spec.md`:
   - Extend the OUT-DATA-01 lint so prop IDs must be unique and inside the bounds.
   - Add a new engine check, OUT-PROP-01: solid props keep standing room clear of every route and spawn.
   - Add a route `north-spawn-to-center` `[[0,600,0],[0,0,0]]`. Today no listed route covers the FEEL-1 walk from the north spawn, so clutter there would go unchecked.
   - Re-run OUT-SIGHT-01 with props in place, since clutter could hide the tower. Add "walk into one solid prop" to card NET-1.
   - Reword OUT-FEEL-01 to include "lived-in". It stays draft until you reply GREEN on FEEL-1.
8. Check the spec for gaps and contradictions, then ask you to review it. Only after that, write the implementation plan. When building, write the tests before the code. The engine tests run on your Windows machine, and you give the final GREEN on card FEEL-1.
