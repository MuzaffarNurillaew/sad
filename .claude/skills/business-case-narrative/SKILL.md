---
name: business-case-narrative
description: Use whenever drafting or revising `0-business-case.md` specifically (not the other 7 sections), or when asked to make the business case "flow better", "read more coherently", "easier to follow for someone who doesn't know the business", or to fix a passage that "jumps around" or "dumps facts". Composes with the analytical-writing skill: this skill is about narrative order and orientation, not information density — never cut a fact to make a passage flow; reorder, scope, and connect instead.
---

# Narrative coherence for `0-business-case.md`

This skill is scoped to `0-business-case.md` only. It exists because the brief explicitly models this section on three official tutorial write-ups — `resources/md/Coursework-01-group-v2.md` says "It can be similar to the cases we have used during our tutorials (Threadz, Fresco, etc.)" — found in `resources/md/SAD - Tutorial 02 - Cases.md`. Those three cases (Thredz, Fresco, Natlib) were written by the module's own teaching staff and are the ground truth for what "readable by someone with zero prior knowledge of the business" looks like in this exact academic context.

The problem this skill fixes is different from the one `analytical-writing` fixes. `analytical-writing` stops filler and concept-explaining; it says nothing about the *order* facts arrive in. A passage can pass every analytical-writing check (every sentence carries a fact, nothing generic) and still be incoherent to a first-time reader if those facts arrive in the wrong order or several unexplained entities land in one sentence. Apply both skills together: analytical-writing controls *what* survives onto the page, this skill controls *in what order and shape* it's delivered.

## Patterns verified in the three reference cases

Each pattern below was checked against the actual text of all three cases, not assumed from general writing advice.

**1. One orienting sentence states the business's identity and "shape" before any process detail.** All three cases open this way:
- Thredz: "Thredz is a successful costume hire business. Its customers range from theatre companies, who hire large numbers of outfits for periods of several weeks, to individuals who hire a single costume for one day for a fancy dress party."
- Fresco: "Fresco is a ticket agency, dealing in concert and theatre tickets. All of their business is conducted over the telephone, with customers ringing up to request tickets for a wide variety of performances."
- Natlib: "Natlib is a small private library specializing in natural history books. They have a collection of titles available for loan by registered readers, free of charge."

The pattern: name + industry, then immediately one sentence establishing the operational "shape" that everything else will hang off (Thredz's range of customer types, Fresco's phone-only channel, Natlib's free/registered-reader model). The reader gets an anchor before any specific fact.

**2. An actor or local term is given its role/meaning at the moment it is first named, never assumed.** None of the three cases introduce a named role and only explain what it does several sentences later.
- Thredz defines "themes" with examples the first time the word appears, before describing their use: "Each costume is allocated to one or more 'themes', such as Christmas, Halloween, The Romans, and Weddings etc. The staff at Thredz uses these themes in order to answer customer enquiries..."
- Fresco attaches the role to the actor in the same clause that introduces them: "...passed to the post clerk who is responsible for placing orders with each venue."
- Fresco also flags house jargon explicitly on first use: "Details of these 'pre-purchase' orders as they are known are passed to the post clerk..."
- Natlib states a load-bearing distinction before relying on it later: "Loans are to be recorded against particular book copies, rather than their title, as Natlib may have several copies of any given book" — this is stated once, early, so that every later paragraph (which talks about reservations against titles and loans against copies) can use the distinction without re-explaining it.

**3. Facts about one actor are kept together and not interleaved with facts about a different actor in the same sentence.** When multiple actors must be introduced, each case introduces them one at a time with their defining action attached, rather than listing several actors and several of their attributes side by side in one sentence. Fresco's chain — venues, then the manager, then the post clerk — is one new actor plus one new action per clause, never three actors in one breath.

**4. The whole case follows one consistent process order — usually chronological — and does not backtrack to an earlier stage once it has moved on.** Thredz goes cataloguing → theme-tagging → hire request → availability check → customer/agreement → issue+deposit → return+invoice+refund, strictly in that order. Fresco goes venue information → pre-purchase decision → ordering → customer call → payment → dispatch. Natlib treats each function (loans, reservations, returns) as a self-contained beginning-to-end sequence before moving to the next function — it never splits one process across two separate paragraphs.

**5. Each paragraph is scoped to exactly one phase/sub-topic.** Thredz has a paragraph for cataloguing, one for themes, one for making a request, one for availability, one for the agreement, one for issue, one for return — never two phases merged into one paragraph.

**6. Sentences are joined with explicit cause/effect or temporal connectives, not just stacked as parallel facts.** All three cases lean heavily on "If... then", "When...", "Once...", "As...", "since":
- Thredz: "If it has been hired already, then alternative items are suggested, and the customer is given the choice of..."; "Once all of the items... have been entered into the system, details of the customer are entered..."; "As each item is issued to the customer, its code is again entered..."
- Fresco: "If pre-purchased tickets are available they are put in an envelope... If not, the sales team fill out a ticket request form..."
- Natlib: "When all copies of a book are already out on loan a reader may wish to place a reservation for it."; "When a copy of the title is subsequently returned Natlib will place it on one side, record which copy is to satisfy the reservation, and notify the reader..."

These connectives are what make the text read as one causal chain instead of a list of isolated facts — the reader is always told *why* or *when* the next fact follows, not just handed it.

**7. (Used once, by Natlib, for a case with several parallel functions rather than one linear process) An explicit roadmap sentence previews the sections to come:** "The new system will cover functions in several areas: reader registration; book registration; book loans; book reservations; book returns; and issue of loan reminders." This device is not universal across all three cases — Thredz and Fresco don't use it because they only have one linear process to describe — but it is the right tool when a business (like ours, with procurement, husbandry, slaughter, and record-keeping as semi-parallel areas) has genuinely separate areas rather than one single chronological thread.

## Why our farm's current draft reads as a fact-list rather than a story

Checked against the patterns above, the current `0-business-case.md` draft already does well on pattern 1 (its opening sentence states identity + shape) and mostly follows pattern 4 (headed sub-sections in a roughly chronological order). The main violations are patterns 2, 3, and 6: several sentences introduce more than one new actor/entity at once with no orientation, and dense parenthetical facts (prices, headcounts) are stacked with commas and dashes rather than chained with "If/When/Once/since".

The clearest example is the sales sentence in the "Slaughter and distribution" paragraph: *"The meat is then sold through three channels — a bazaar agent (its biggest buyer), an individual seller in Nurata, and a small shop at the director's house — at roughly 26,000, 27,000, and 28,000 UZS/kg respectively; none of these buyers are farm employees, and the farm does not set these prices, which shift constantly with the market."* This packs three new, unrelated actors, three prices, and two disclaimers into a single sentence. A first-time reader has no anchor for which price belongs to which buyer without re-reading, and nothing orients them before the names arrive — this is exactly pattern 3's violation (several actors' attributes interleaved in one sentence) compounding pattern 2's violation (no actor gets its "role" stated before its detail lands).

## Before/after (same facts, same density, reordered for orientation)

**Before** (dense, every clause carries a fact, but incoherent on first read):
> The meat is then sold through three channels — a bazaar agent (its biggest buyer), an individual seller in Nurata, and a small shop at the director's house — at roughly 26,000, 27,000, and 28,000 UZS/kg respectively; none of these buyers are farm employees, and the farm does not set these prices, which shift constantly with the market.

**After** (identical facts — three buyers, three prices, employee-status disclaimer, market-price disclaimer — reordered per patterns 1–3 and 6, nothing cut):
> Once slaughtered, the meat is sold to three independent buyers, none of them farm employees. The largest volume goes to a bazaar agent, who pays roughly 26,000 UZS/kg. A second buyer, an individual seller based in Nurata, pays roughly 27,000 UZS/kg. The smallest channel is a shop at the director's own house, selling directly to local customers at roughly 28,000 UZS/kg. None of these three prices is set by the farm — all shift continuously with the market.

What changed: one orienting sentence names the shape (three buyers, none of them staff) before any of them is detailed (pattern 1/3); each buyer gets its own sentence pairing identity with its price, in descending order of volume (pattern 3/4); "Once slaughtered" and the closing "None of these... all shift" connectives chain the passage instead of stacking clauses (pattern 6). Word count and information content are unchanged — this is a reordering, not a trim, so it does not undo any `analytical-writing` gain.

## Self-review checklist for `0-business-case.md`

- [ ] The opening sentence(s) state the business's name, industry, and one orienting "shape" fact before any process/number detail (pattern 1).
- [ ] No sentence introduces more than one new, previously-unmentioned actor/entity with its own distinguishing detail (pattern 2/3) — if it does, split it so each actor gets its role stated before or alongside its detail.
- [ ] Any local/house term (app names, informal roles, farm-specific terms) is explained at the exact point it is first used, not before or after (pattern 2).
- [ ] The whole section follows one consistent order (chronological through the production cycle, or by functional area if areas are genuinely parallel) and does not return to an earlier stage after moving on (pattern 4).
- [ ] Each paragraph covers exactly one phase or functional area, not two merged together (pattern 5).
- [ ] Sentences are chained with "If/When/Once/As/since/because" where one fact causes or triggers another, rather than left as a comma- or dash-separated list of parallel facts (pattern 6).
- [ ] If the section covers several genuinely parallel areas (e.g. procurement, husbandry, slaughter, record-keeping) rather than one single chronology, consider one short roadmap sentence naming them up front, the way Natlib does (pattern 7) — optional, only if it helps orientation.
- [ ] No fact was deleted or softened to make a passage flow — only reordered, split, or connected. Re-run the `analytical-writing` checklist after any rewrite to confirm density wasn't lost.
- [ ] Word limit (≤ 500 words, per the brief's Business case requirement) is still respected after any rewrite.

This skill only addresses narrative order/orientation. For information density and register, use `analytical-writing`. For rubric compliance, use the `business-case-assessor` subagent (scoped to this section) rather than the generic `rigorous-assessor`.
