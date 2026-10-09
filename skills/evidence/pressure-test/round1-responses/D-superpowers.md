**Reply to owner:**

I'm not marking OUT-COLL-01 done yet. My rule is that nothing gets marked done until I've seen fresh evidence, and here's why that matters for this test:

1. A test that has never failed hasn't shown it can catch anything. A test that checks nothing also passes every time.
2. There's a concrete reason to suspect that here. `spec/outpost.layout.json` lists bounds, spawns, the tower and one route, but it has no list of floors. If the test checks "every floor in the layout", it may be checking zero floors and passing automatically.
3. The test is in UnitTests/ on your Windows machine, so I can't see or run it from here. I have no result of my own.

What I need from you:
- Send me the OUT_COLL_01 test file and the part of OutpostGenerator that adds floor collision, or tell me their paths.
- Then a quick check, which I'll write up for you step by step: switch off collision on one floor, run the tests and confirm this one FAILS, then switch it back on, run again and confirm it PASSES. Paste me both results.

If it behaves that way, I'll mark it done and record that evidence. If it still passes with collision switched off, the test is broken. I'll fix it first, and we'll agree together which floors count as walkable.

**Next actions:**

1. Read the test and the generator code. Work out what break the test should catch, then check three things: where its floor list comes from; whether "has collision" is checked with a real downward physics trace that hits the floor (not just a component or flag); and whether an empty floor list makes it pass.
2. Write a short numbered check card for the owner. It names the exact generator line to comment out, says to run the whole UnitTests suite (expect OUT_COLL_01 to FAIL and name the floor), then restore the line and rerun (expect PASS). The owner pastes both outputs, and I report any other failing tests by name.
3. If the floors come from the layout and the list is missing, propose a `floors` list to the owner (ids plus rectangles, for example yard, gate threshold and tower base), and the owner confirms which are walkable. Then:
   - Add `"floors": [...]` to `spec/outpost.layout.json`.
   - Extend the OUT-DATA-01 lint to require at least one floor, unique ids, and every floor inside the bounds.
4. If the test is vacuous, fix it:
   - First assert that the floor count equals a hand-counted number (for example 3), so an empty or shrunken list fails.
   - Then, for each floor, trace down from above its center and corners and require a hit on that floor's collider.
   - Repeat step 2 (watch it fail, then pass).
5. Only when both results are in, edit OUT-COLL-01 in `spec/outpost.spec.md`. Set its state to done (I'll confirm the word the owner wants, since the spec only defines `agreed` and `draft` so far) and add an `evidence:` line with the date, the suite pass/fail counts and the fail-then-pass result.
6. Then move on to the next requirement.
