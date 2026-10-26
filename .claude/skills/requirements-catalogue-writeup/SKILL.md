---
name: requirements-catalogue-writeup
description: Use whenever drafting or revising `7-requirements-catalogue.md` specifically (not the other 7 sections), or when asked to "write the requirements catalogue", "turn these gaps into requirements", or "classify this as functional or non-functional". Composes with analytical-writing (every requirement row must be a specific, testable statement, not a generic category label) and hands off rubric/traceability scoring to the `requirements-catalogue-assessor` subagent.
---

# Writing `7-requirements-catalogue.md`

This is the highest-value section in the report (20 of 100 points) and the one place the report pivots from documenting what exists to proposing what should be built — see `CLAUDE.md`'s "As-is now, to-be only at the end" section. Everything here is for **the proposed information system**, not a restatement of the manual process.

The rubric row (Requirements item 8, 20 points total, verbatim from `resources/md/Coursework-01-group-v2.md`):

> There are 5 functional and 5 non-functional requirements: 8 points. All requirements are detailed and cover all edge cases: 12 points. Requirements are short and don't cover all the details: -2 points/req.

Plus the brief's own text: "Based on the gathered data and your subsequent interpretation and analysis of the data, draw requirements catalogue summaries and identify five functional and five non-functional requirements for the information system," using the table format `Requirements ID | Requirements name | Requirement Description`.

Read that last clause carefully: **"based on the gathered data and your subsequent interpretation."** This section is graded on whether each requirement actually comes from somewhere — a real gap documented in sections 0, 1, or 4 — not on whether it sounds like a plausible requirement for a generic farm app.

## Functional vs. non-functional, in this module's own terms

From the module's own lecture material, not generic textbook SAD:

- **Functional requirement**: "an action the product must take — check, calculate, record, retrieve... derived from the fundamental purpose of the product... not a quality." If a requirement describes a *quality* the system has rather than an *action* it performs, it's not functional.
- **Non-functional requirement**: "a quality the product must have," falling into one of eight named categories — **Look and Feel, Usability, Performance, Operational, Maintainability and Portability, Security, Cultural and Political, Legal**. Name the category for every NFR; "the system should be good" is not gradable, "Usability: the system must be usable one-handed from a phone in the field" is.
- **Constraints are a subtype of non-functional**, not a third category. Don't invent a separate "constraints" bucket.
- **Quality bar**: every requirement must be unambiguous and non-vague, to the standard of "could a developer build this just from reading the requirement, without having to contact anyone else?" If a requirement needs a follow-up question to implement, it's not done yet.

## Every requirement must trace to a real, already-documented gap

This is the section's real failure mode — not missing the FR/NFR split (that's a mechanical count), but writing requirements that could apply to literally any small business, with no link back to anything actually found. The group already has real, specific gaps on record:

- Mortality counts pass through a worker's verbal report to the director before being written down by hand, making the resulting count only an approximation.
- No price history is kept anywhere, so buying/selling decisions rely entirely on intuition.
- pDaftar pools costs/revenue/profit in one running total; the director explicitly wants it separated by batch.
- Camera footage, the paper notebook, and pDaftar are three disconnected records that are never linked.
- The hired crew's pay is settled against a head count agreed verbally after the session — the count itself is never recorded, so it can't be checked later.
- The director stated a future tool should be phone-based, not desktop-based, since he's rarely at one fixed location.
- Feed-quality timing (which factory's feed arrives first in a batch) measurably affects outcome but isn't tracked anywhere.

(These are illustrative, pulled from what's already on record — don't treat this list as exhaustive or copy it verbatim; trace each requirement to the specific finding it actually addresses, including any the group documents later.)

- ❌ "FR: The system shall allow users to record chick mortality." — could be written for any poultry app on earth; doesn't reference what's actually broken about mortality recording today.
- ✅ "FR: The system shall let a worker log a chick death directly, at the point it's found, without routing through the director first — closing the two-person, verbal-then-handwritten path that currently makes the count only an approximation."
- ❌ "NFR: The system should be user-friendly." — no category, not testable, not traced to anything.
- ✅ "NFR (Usability): The system must be fully usable from a phone with no fixed desk, matching the director's own statement that a future tool should be phone-based since he spends most of his time away from any one location."

Citing another section of the same report (e.g. "per the business case...") is a normal, expected cross-reference here — it's not the same as citing an external evidence file, and it's exactly what makes a requirement traceable rather than invented.

## Detail and edge cases (the 12-point sub-criterion)

A requirement earns the "detailed, covers edge cases" credit when it states what happens in the non-default case, not just the happy path:

- ❌ "FR: The system shall record the agent's payment."
- ✅ "FR: The system shall record the agent's payment and flag any case where the agent's reported kg total doesn't match the farm's own weighing record, rather than accepting the agent's figure automatically."

The rubric's own penalty clause is explicit and mechanical: **-2 points per requirement that is short and doesn't cover the details** — so a one-line, un-elaborated requirement is a direct, countable point loss, not a style nitpick.

## Self-review checklist

- [ ] Exactly 5 functional and 5 non-functional requirements, each in the `ID | Name | Description` table format.
- [ ] Every functional requirement describes an action (check/calculate/record/retrieve), not a quality.
- [ ] Every non-functional requirement names one of the eight categories (Look and Feel, Usability, Performance, Operational, Maintainability and Portability, Security, Cultural and Political, Legal) and states a testable threshold, not a vague aspiration.
- [ ] No separate "constraints" category — any constraint is filed under non-functional.
- [ ] Every requirement traces to a specific, real gap already documented elsewhere in the report (or a new one the group has since confirmed) — not a generic requirement that could belong to any business.
- [ ] Every requirement covers at least one edge case / non-default scenario, not just the happy path.
- [ ] No requirement needs a follow-up question to be buildable as written.
- [ ] No sentence explains what a functional/non-functional requirement *is* as a concept — analytical-writing's rule applies here in full, no exception.

For rubric and traceability scoring, use the `requirements-catalogue-assessor` subagent (scoped to this section) rather than the generic `rigorous-assessor`. For register/density, re-run `analytical-writing`'s checklist after any rewrite.
