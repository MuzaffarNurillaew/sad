---
name: analytical-writing
description: Use whenever drafting or revising prose in any of the 8 SAD coursework report sections (0-business-case.md through 7-requirements-catalogue.md), or when asked to make a passage "more analytical", "less descriptive", or "tighter". The brief explicitly requires analytical writing and penalizes descriptive filler and concept explanations — this skill enforces that register.
---

# Analytical writing for this coursework report

The brief (`resources/md/Coursework-01-group-v2.md`) states this directly: **"Your report should be analytical. Please do not explain any of the concepts. Descriptive content could be used in the Business case section."** The Business Case rubric row also has an explicit penalty: **"The text is not concise, and it carries no information: -5 points."** Treat both as hard constraints, not style preferences.

## The one test for every sentence

Could this sentence be copy-pasted, unchanged, into any other group's report about a completely different business? If yes, cut it or rewrite it with a fact specific to *this* broiler farm. Generic, textbook-sounding sentences are exactly what gets penalized.

## Register by section

- **`0-business-case.md`** — the one place description is allowed, but it still must be information-dense. Every sentence must convey a fact about this farm (its scale, its products, its actual processes). No filler sentences, no throat-clearing.
- **`1-requirements-gathering-process.md` through `7-requirements-catalogue.md`** — analytical, full stop. This means: interpret, justify, and connect evidence to a conclusion. Do not narrate what you did without saying why, and do not explain what a concept is.

## Never explain taught concepts

The marker wrote the module — they know what a Data Flow Diagram or a Use Case is. Writing a definition of one wastes words and reads as padding.

- ❌ "A Data Flow Diagram shows how data moves through a system between processes, data stores, and external entities."
- ✅ "The feed-ordering process has three external entities (the supplier, the farm manager, and the accounts office) because ordering, approval, and payment are handled by different people with no shared system."

## Justify, don't narrate

Especially in the Requirements Gathering section: don't just state what method you used — state why that method, for this business, beating the alternatives.

- ❌ "We used interviews because they are a common and effective method for requirements elicitation."
- ✅ "We used semi-structured interviews with the farm manager and two workers rather than a questionnaire, because the farm's processes (feed scheduling, batch tracking) are informal and undocumented — a fixed-question survey would have missed the conditional logic (e.g. feed mix depends on bird age) that only surfaced through follow-up questions."

## Self-review checklist before calling the `rigorous-assessor` subagent

- [ ] No sentence defines or explains a standard SAD concept/notation.
- [ ] No sentence is generic enough to drop into another group's report unchanged.
- [ ] Every claim about the farm is either evidenced (interview note, observation, figure) or explicitly flagged as "to confirm with Muzaffar" — not quietly invented.
- [ ] Every methodology/design choice is justified against at least one alternative, not just stated.
- [ ] Word/length limits from the brief are respected (e.g. Business Case ≤ 500 words).
- [ ] Any external claim has a Westminster-Harvard citation.

## How to apply this skill to a passage

When asked to tighten or analyze a piece of text:
1. Identify and remove any sentence that explains a taught concept.
2. Identify any sentence that's generic/interchangeable and either delete it or anchor it to a specific fact about the farm.
3. For every stated choice or finding, add (or demand) the "why", not just the "what".
4. Re-check the word count against that section's limit, if one applies.

This skill only enforces register and information density. It does not check rubric coverage or cross-section consistency — use the `rigorous-assessor` and `consistency-checker` subagents for that, after a pass through this one.
