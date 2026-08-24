# Light Task — <observable outcome>

Use this only when the work is confined, deterministic, easy to reverse, low
consequence, and covered by an exact trustworthy evaluator. The evaluator may be an
existing check or a new regression with independently grounded expected behavior; its
newness alone does not require fallible-evaluator calibration. This file is optional: an
existing issue or accepted prompt containing the same facts is enough.

## Contract

- Outcome: <one observable result>
- Allowed scope: <exact files or bounded component>
- Non-goals: <what must remain unchanged>
- Reversibility: <ordinary revert or other cheap recovery>

## Cheapest reliable check

- Check: <existing deterministic test, compiler, linter, calculation, or exact comparison>
- Expected result: <predeclared outcome independent of the implementation>
- Realistic failure detected: <what this check would catch>

## Stop or escalate if

<Unexpected nondeterminism, scope expansion, evaluator weakness, external effect,
greater consequence, or another fact makes `light` rigor insufficient. Escalation
requires a fresh decision and never widens authority by itself.>

## Completion

- Result: <pass/fail and smallest useful observation>
- Changed paths: <paths>
- Remaining uncertainty: <none or exact open issue>

No JSON packet, manifest, capability certificate, independent model review, or human
receipt is required merely because the blueprint contains those optional mechanisms.
