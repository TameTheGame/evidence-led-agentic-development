**1. Reply to owner:**

> I'm not going to mark OUT-COLL-01 done yet. A test that has never failed even once may not be checking anything, and in this case there's a specific reason to think it isn't.
>
> The test is supposed to check "every walkable floor in the layout." But the layout file (`spec/outpost.layout.json`) doesn't list any floors. It only has the outer bounds, two spawns, the tower and one route. If the test goes through the floors one by one and there are zero of them, it passes every time. It would still pass if the outpost had no floor collision at all.
>
> Here's my plan. I'll make the test fail when it finds no floors. I'll also give it a deliberately broken example, a floor with no collision, that it has to catch. If it catches the broken one and the real outpost still passes, I'll mark it done and note the exact version it was checked on. This is all technical work, so you don't need to judge anything.
>
> I do need one thing from you. The test code and the OutpostGenerator code aren't in the folder I can see. Could you give me access to them? Copying the `UnitTests` folder and the generator code into the project folder works.

**2. Next actions:**

1. Rigor: bounded. The check itself is suspect, which is a reason to escalate, and OUT-SPAWN-01 and OUT-ROUTE-01 also depend on floors. The work stays local and an ordinary revert undoes it.
2. Read `OUT_COLL_01_EveryFloorHasCollision` and `OutpostGenerator`. Find out where floors come from (the layout has no `floors` key) and what the test actually asserts: real trace hits, or only that a collider component exists.
3. Write the failing checks before changing anything else:
   - Assert that the number of floors equals the count declared in the layout, so the generator's output doesn't decide the answer. Zero floors means FAIL.
   - Add control fixtures that must FAIL: a floor generated without collision, and a layout with no floors.
   - For each floor, trace downward from above at its centre and corners, and require a hit on that floor's collider. Traces miss mesh faces from behind, and component presence or `HasCollision` proves nothing.
   - Build each mesh disabled, then assign it, then enable it. Register the stand-in `default` surface in test setup.
4. Data: add a `floors` array to `spec/outpost.layout.json` that matches what the generator already builds, so nothing changes visually, and have the generator read it. Extend the OUT-DATA-01 lint to require at least one floor and to check that every spawn and route point sits over a floor. If the code shows a floor layout the spec never intended, give the owner options with a recommendation instead of choosing.
5. Run the tests on the Windows machine. The control fixtures must fail for the right reason and the real outpost must pass. Copy `logs\testhost.log` after every run and check it for engine errors the test output doesn't show. If I can't reach that machine, give the owner one command to paste and ask them to send back the output and the log.
6. Only then report `OUT-COLL-01 engine pass <commit>`. The folder isn't a git repo, so I need to pin a commit or build identity first. This doesn't get an `ACCEPTANCE.md` line because no owner check was involved, and the result reopens if the layout or generator changes.
7. Check whether the OUT-SPAWN-01 and OUT-ROUTE-01 tests have control cases, since they rely on the same missing floors. Report what I find, and don't widen the scope without asking.
