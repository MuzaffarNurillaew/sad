---
name: requirements-gathering-writeup
description: Use whenever drafting or revising `1-requirements-gathering-process.md` specifically (not the other 7 sections), or when asked to "write up the interview", "justify the requirements gathering methods", or turn interview/observation evidence into the section text. Composes with analytical-writing (this section is NOT the business-case exception - no descriptive padding) and hands off rubric scoring to the `requirements-gathering-assessor` subagent.
---

# Writing `1-requirements-gathering-process.md`

This section is graded on process and evidence, not on findings. The rubric row (Requirements item 2, 15 points, verbatim from `resources/md/Coursework-01-group-v2.md`):

> 2 requirements gathering methods are clearly stated: 3 points. The chosen methods are well justified: 5 points. The carried-out requirements gathering is done effectively: 5 points. Considerable effort was put into the process: 2 points. No evidence of conducting requirements gathering: -10 points.

Plus the brief's own text: "You must collect at least some of your data from prospective users... make sure you can provide evidence of carrying out data gathering processes in your report (e.g. audio recording or transcript of your interview, filled out surveys, etc.)."

Section 7 (Requirements Catalogue) is where functional/non-functional requirements get listed. This section's job stops at *how the data was gathered and what it surfaced* - do not draft requirement statements here.

## State methods, don't just name them

Naming "interview" and "observation" satisfies 3 of the 15 points. The other 12 are earned by justifying each method *for this business specifically* and by citing checkable evidence that it actually happened.

- ❌ "We used interviews because they allow follow-up questions and are a flexible way to gather information."
- ✅ "A small broiler farm with no written SOPs exists only in the director's working knowledge, so a semi-structured interview - which allows follow-up questions when an answer surfaces an undocumented rule - fits better than a fixed questionnaire that would miss conditional logic uncovered only by probing."

This module's own vocabulary (`resources/md/SAD-Tutorial-05.md`) gives the exact terms to justify against, not generic textbook SAD:
- **Interview**: "when detailed, qualitative insights are needed... builds relationships, allows follow-up questions" vs. "time-consuming, may be biased or incomplete."
- **Observation**: "when actual work practices differ from documented ones... reveals real processes, uncovers hidden needs" vs. "can be intrusive, users may change behavior when observed."
- **Survey/Questionnaire**: "when there are many stakeholders or large user groups... quick data collection" vs. "limited depth."
- The quality bar for any method's output: **Complete, Accurate, Unambiguous** - use these words when judging whether a method actually delivered.

## Cite evidence, don't assert it

"Data was gathered through an interview" is an unverifiable claim. The brief explicitly wants evidence *in the report* - a reader (the module leader) must be able to check the claim without taking your word for it.

- ❌ "An interview was conducted with the director and the data was recorded."
- ✅ "A 51-minute interview with the director was conducted on 2026-10-26 (verbal consent obtained and timestamped at the start of the recording; audio and transcript retained as `evidences/Interview_Director_2026-10-26.m4a`/`.txt`). For example, on procurement: director, translated from Uzbek: 'chicks come from Tashkent or Samarkand, and the better the factory you buy from, the higher the meat quality ends up' (Uzbek: 'qanchalik sifatli zavoddan birinchi olib kelsang uni goʻshtni sifat dalasa shunchalik oshadi')." - see the extraction/translation method below for how to get from the raw transcript to this.

A quoted excerpt does two jobs at once: it is the evidence, and it is the "effectively done" sub-criterion's proof, since a vague or evasive quote would itself show the method didn't work well.

**A file path is not evidence to the marker - it's only your own audit trail.** `evidences/` is gitignored and the compile pipeline never pulls anything from it into the submitted `.docx` - the module leader marking `SAD_CW1_STUDENTID.docx` will never open `evidences/Interview_Director_2026-10-26.m4a`, no matter how precisely you cite it. Citing the path proves to your own teammates that the file exists; it proves nothing to the person assigning the 15 points. The only thing that counts as evidence in the actual submission is what appears on the page itself: a quoted excerpt, a reproduced date/duration/timestamp, or a photographed artifact embedded as an image. Cite the file path too (it's good practice and costs nothing), but never treat the path as a substitute for reproducing the actual content.

## Extracting and translating a quote from a raw transcript

The real transcript this section draws on (`evidences/Interview_Director_2026-10-26.txt`) is raw Uzbek speech-to-text output: no punctuation, no sentence boundaries, filler words, numbers embedded mid-clause, code-switched terms (e.g. "pedaftar" for the bookkeeping app). You cannot quote it directly into an English-language report, and the obvious shortcut - paraphrasing it smoothly into English with no trace of the original - throws away the one thing that makes a quote evidence rather than assertion: falsifiability.

1. **Isolate one self-contained clause** from the run-on text without inventing a sentence break that changes its meaning. Read enough surrounding context to be sure the clause isn't a sentence fragment that depends on something before or after it.
2. **Translate it into English**, keeping names, numbers, and prices exact - never round or smooth a figure while translating.
3. **Quote both**, labelled explicitly as a translation: the original-language fragment, then the English translation. For example: *director, translated from Uzbek: "the agent sends his kilogram totals as a photo, and I check it before working out what he owes" (Uzbek: "ovozni xabardan analiz qilib... raqamlarni va qachon qaysi sanada va sababi nima o'shalarini kerakli joyga kiritadi")*. The pairing itself is the falsifiability check - a bilingual reviewer (a teammate, or a future audit) can verify the translation without needing to trust it blindly; an English-only gloss cannot be checked by anyone who doesn't already know what was said.
4. **Flag ambiguity rather than smoothing it over.** If a number, price, or technical term in the raw transcript is unclear or could be parsed two ways, say so in the write-up instead of silently picking one reading.

## Say plainly which rubric sub-criteria are and aren't covered yet

Do not round up. If only one method has real evidence behind it so far, the write-up itself should state that plainly rather than implying more was done than was:

- "Only the director interview has been carried out with recorded evidence to date; the planned worker observation and artifact review (see `resources/research/1-requirements-gathering-process-research.md`) have not yet been conducted." This single sentence is worth more than silence, because the -10 "no evidence" penalty is about *unverifiable* claims, not about admitting a method is still pending - an honest gap costs less than an inflated one that the assessor or marker catches.

The rubric's "2 methods clearly stated" minimum is satisfied by naming and justifying 2+ methods even if only one currently has carried-out evidence - but "effectively done" and "considerable effort" sub-criteria should only be claimed for methods that actually happened.

## Tie findings forward without doing section 7's job

End with what the gathered data *surfaced*, stated as findings, not requirements:

- ❌ "Therefore the system should have a functional requirement to track mortality automatically." (this is section 7's job)
- ✅ "The interview surfaced that mortality counts pass through two people and a spoken report before being written down, and that no price history is kept anywhere - both gaps section 7's requirements trace back to." (states the finding, defers the requirement statement)

## Self-review checklist

- [ ] At least 2 methods are named, each justified against this business's specific undocumented/informal nature, not generically.
- [ ] Every method claimed as "carried out" cites ALL of: a specific date/duration, a consent timestamp, a named file reference, AND at least one short exact quote reproduced on the page - these are independent checks the assessor scores separately, not substitutes for each other. Satisfying only one or two is a partial pass, not a full one.
- [ ] Any method that is planned but not yet carried out is stated as such, not implied as done.
- [ ] At least one piece of data comes from a "prospective user" who is not the owner/director (currently a gap - see Axis 2 of the assessor).
- [ ] Any quote translated from a non-English source (e.g. the Uzbek transcript) is paired with the original-language fragment, not given as an English-only gloss.
- [ ] No sentence explains what an interview/observation *is* as a concept (analytical-writing's rule - this section gets no descriptive-writing exception, unlike the business case).
- [ ] Findings are stated as evidence/gaps, not drafted as functional/non-functional requirement statements (that's section 7).
- [ ] No word-count concern (the brief has no limit here), but no padding either - every sentence should be a fact, a justification, or a piece of evidence.

For rubric compliance and evidence-integrity scoring, use the `requirements-gathering-assessor` subagent (scoped to this section) rather than the generic `rigorous-assessor`. For register/density, re-run `analytical-writing`'s checklist after any rewrite.
