"""Generates 3-use-cases.md: the four use case tables, as pandoc grid tables
so numbered steps survive into the docx. Edit the UCS data below, not the
generated file.

Usage: python3 scripts/generate_use_cases.py 3-use-cases.md
"""
import re
import sys
import textwrap

L, R = 24, 66  # column content widths

UCS = [
    {
        "Use Case Number": "UC-01",
        "Application": "Nurota Halol Parranda current operations: procurement (Figure 2.1)",
        "Use Case Name": "Order Day-Old Chicks",
        "Use Case Description": (
            "The Director orders a new batch of chicks for an empty house from the contracted supplier in Tashkent. The chicks are bought on credit and paid for only when the batch ends, so the batch's chick cost stays unpaid while its meat is already being sold."
        ),
        "Primary Actor": "Director",
        "Secondary Actor(s)": "Chick Supplier",
        "Precondition": "A supply contract with credit terms is in place with the chick supplier in Tashkent.",
        "Postconditions": (
            "Day-old chicks matching the house's capacity have been delivered by the supplier, and their cost "
            "is owed to the supplier until the batch ends."
        ),
        "Trigger": "A house has been emptied at the end of its previous batch.",
        "Basic Flow": [
            "The Director confirms that the house has been cleaned and prepared.",
            "The Director sets the order size from the house's 5,000–10,000-bird capacity.",
            "The Director places the order on credit with the contracted supplier in Tashkent.",
            "The supplier delivers the chicks to the farm by Damas van.",
        ],
        "Extensions": [
            "1a. The house is not yet cleaned: the order waits until cleaning is finished, then the flow resumes at step 1.",
        ],
    },
    {
        "Use Case Number": "UC-02",
        "Application": "Nurota Halol Parranda current operations: slaughter and sales (Figure 2.1)",
        "Use Case Name": "Decide Main Slaughter Date",
        "Use Case Description": (
            "The Director decides when to call in the slaughter crew, judging the birds' age, the average weight of about ten birds and his own experience together. No record of a target weight or age is named, so the decision cannot be checked or made by anyone else."
        ),
        "Primary Actor": "Director",
        "Secondary Actor(s)": "None",
        "Precondition": (
            "The batch is near the end of its growth period, and the early thinning of roughly 4,000 birds "
            "around day 35–40 has taken place."
        ),
        "Postconditions": (
            "The slaughter crew has been called in for the first session."
        ),
        "Trigger": "The batch approaches the end of its 40–50-day growth period.",
        "Basic Flow": [
            "The Director checks the batch's age against its 40–50-day growth period.",
            "The Director obtains the average weight of a random sample of about ten birds (includes Weigh Sample Birds).",
            "The Director judges from the age, the sample average and his experience that the batch is ready.",
            "The Director calls in the hired crew, starting UC-03 Run Main Slaughter.",
        ],
        "Extensions": [
            "3a. The Director judges the batch not yet ready: he waits three to five more days, which adds days of feed to the batch, and the flow resumes at step 1 with a new sample.",
        ],
    },
    {
        "Use Case Number": "UC-03",
        "Application": "Nurota Halol Parranda current operations: slaughter and sales (Figure 2.1)",
        "Use Case Name": "Run Main Slaughter",
        "Use Case Description": (
            "The Director has a hired crew of about six slaughter and clean 1,000–1,200 birds in one overnight session, and a batch needs as many sessions as it takes to empty the house. The butcher is paid per head on a count agreed by word of mouth, so the figure that sets his pay is not recorded anywhere."
        ),
        "Primary Actor": "Director",
        "Secondary Actor(s)": "Slaughter Crew",
        "Precondition": "UC-02 Decide Main Slaughter Date has concluded that the batch is ready for slaughter.",
        "Postconditions": (
            "One session's birds are processed and ready for UC-04, and the head count that sets the butcher's "
            "pay has been agreed verbally."
        ),
        "Trigger": "The Director calls in the hired crew.",
        "Basic Flow": [
            "The crew arrives for an overnight session.",
            "The butcher kills each bird.",
            "The scalder loosens the feathers in hot water.",
            "The plucker removes the feathers.",
            "Two to three crew workers clean the internal organs.",
            "The Director and the butcher agree the session's head count verbally.",
        ],
        "Extensions": [
            "6a. Birds remain in the house after the session: the use case ends with the batch only partly slaughtered, and the Director calls the crew back for a further session, which starts this use case again.",
        ],
    },
    {
        "Use Case Number": "UC-04",
        "Application": "Nurota Halol Parranda current operations: slaughter and sales (Figure 2.1)",
        "Use Case Name": "Sell Meat to Bazaar Agent",
        "Use Case Description": (
            "The Director sells each session's meat to the Bazaar Agent, the farm's largest buyer, who resells it to seven to nine other sellers and so pays around 26,000 UZS/kg, a little below the bazaar rate. The agent's Telegram photo of the kilograms is checked against a second record kept by someone from the farm, but neither weight record reaches pDaftar, only the payment."
        ),
        "Primary Actor": "Director",
        "Secondary Actor(s)": "Bazaar Agent",
        "Precondition": "Meat from a slaughter session (UC-03) is ready for sale.",
        "Postconditions": (
            "The agent has paid total kg × the agreed price per kg, and the revenue is recorded in pDaftar."
        ),
        "Trigger": "A slaughter session finishes and its meat is ready.",
        "Basic Flow": [
            "The Director and the agent agree the price per kg verbally, a little below that day's bazaar rate (includes Agree Price per kg).",
            "The Director sends the meat to Navoi bazaar with a temporarily hired driver.",
            "The agent weighs the meat, while a second person from the farm records the same weighings.",
            "The agent photographs his kg totals and sends them to the Director on Telegram (includes Send Weight Photo by Telegram).",
            "The Director checks the photographed totals against the farm's own record.",
            "The agent pays the Director the total kg × the agreed price per kg in cash at the end of the day.",
            "The Director records the revenue in pDaftar (includes Record in pDaftar, via Sell Meat).",
        ],
        "Extensions": [
            "6a. The agent pays by bank transfer instead of cash: the flow resumes at step 7.",
        ],
    },
]

FIELDS = ["Use Case Number", "Application", "Use Case Name", "Use Case Description", "Primary Actor",
          "Secondary Actor(s)", "Precondition", "Postconditions", "Trigger", "Basic Flow", "Extensions"]
LABEL = {"Extensions": "Extensions (Alternate Flows)"}
EXT_RE = re.compile(r"^\d+[a-z]\.")  # extension labels like "3a." carry their own numbering


def wrap_left(text):
    return textwrap.wrap(text, L, break_on_hyphens=False) or [""]


def wrap_right(value):
    if isinstance(value, str):
        return textwrap.wrap(value, R, break_on_hyphens=False)
    lines = []
    for i, item in enumerate(value, 1):
        if EXT_RE.match(item):
            if lines:
                lines.append("")
            lines += textwrap.wrap(item, R, break_on_hyphens=False)
        else:
            lines += textwrap.wrap(f"{i}. {item}", R, subsequent_indent="   ", break_on_hyphens=False)
    return lines


def table(uc):
    sep = "+" + "-" * (L + 2) + "+" + "-" * (R + 2) + "+"
    out = [sep]
    for f in FIELDS:
        left = wrap_left(f"**{LABEL.get(f, f)}**")
        right = wrap_right(uc[f])
        n = max(len(left), len(right))
        left += [""] * (n - len(left))
        right += [""] * (n - len(right))
        for a, b in zip(left, right):
            assert len(a) <= L and len(b) <= R, (a, b)
            out.append(f"| {a.ljust(L)} | {b.ljust(R)} |")
        out.append(sep)
    return "\n".join(out)


HEAD = """# Use Cases

<!-- Rubric: resources/md/Coursework-01-group-v2.md, Requirements item 4 (15 points). Four use cases from the diagram in 2-use-case-diagram.md. -->

<!--
Generated by scripts/generate_use_cases.py - edit the data there and re-run it, not the tables here. Names and actors must match 2-use-case-diagram.md.
Facts beyond 0-business-case.md come from Muzaffar's confirmed answers (see the comment in 2-use-case-diagram.md).
Confirmed 2026-10-26 and used here: chicks only from Tashkent; chicks and feed bought on credit under contract and paid when each batch ends;
suppliers deliver; readiness judged on age + random-sample average weight + experience; number of slaughter sessions per batch not fixed;
Bazaar Agent is an independent middleman paying a little below the bazaar rate; amount owed = kg x price; a second person from the farm
also records the bazaar weighings; agent pays cash or transfer at the end of the day.
To confirm with Muzaffar (question -> table -> marks at stake):
- If the agent's photo kg and the farm's record disagree, what happens? -> UC-04 exception 5a -> +1 (quality).
- Has the crew ever disputed the head count, or not turned up? -> UC-03 / UC-02 exception -> +0.5.
- Have chicks ever arrived short or dead? What did the Director do? -> UC-01 exception -> +0.5.
- Who is the "second person from our side" at the bazaar? (sections 4-5 say a Worker) -> UC-04 step 3.
- Who weighs the sample birds? (sections 4-5 say the Director) -> UC-02 step 2.
- Is the batch-end supplier payment still by bank transfer? (section 0 says bank transfer) -> UC-01.
Flag for section 1 (Muzaffar): every 2026-10-24/26 answer used here needs to be recorded there as evidence.
Flag for Nodir: sections 4-5 say the agent pays "at" the day's bazaar rate; confirmed answer is "a little below".
-->

The four use cases follow one batch from buying the chicks to selling the meat, and each turns on a decision that moves money: what the batch costs (UC-01), when it is slaughtered (UC-02), what processing costs (UC-03) and what the meat earns (UC-04). The Feed Supplier is left out because a feed order runs on the same credit terms as UC-01. The Worker, the Nurata Seller and the Shop Customer are left out because the farm has not described the steps of their use cases. Two of the four decisions rest only on word of mouth: the butcher's head count (UC-03) and the agent's price per kg (UC-04).
"""

TAIL = """
Each gap these use cases expose has to be closed by a requirement in section 7.

| Finding | Evidence | Where it shows | Section 7 must cover |
|---|---|---|---|
| Deaths and feed use never reach the profit figure | Section 0: notebook and pDaftar kept separately | Write in Notebook, Record in pDaftar (Figure 2.1) | One batch record linking deaths, feed, costs and sales |
| The slaughter date rests on a sample and judgement, with no recorded target | Section 0; interview 26-10 | UC-02 steps 2-3 | Recording sample weights and age per batch |
| The butcher's pay rests on a spoken head count | Section 0 | UC-03 step 6 | Recording the head count per session |
| The agent's price per kg is agreed by word of mouth | Interview 24-10 | UC-04 step 1 | Recording the agreed price and keeping a price history |
| The agent's kilograms can be checked only against a second record kept by the farm | Interview 26-10 | UC-04 steps 3-5 | Recording both weights and flagging any difference |
| Chick and feed costs are settled only when the batch ends | Interview 26-10 | UC-01; Pay Supplier at Batch End | Running batch cost from the day the chicks arrive |
| The crew is paid per head but every buyer pays per kg | Section 0 | UC-03 step 6, UC-04 step 6 | Recording heads and kilograms per session |
"""

body = [HEAD]
for uc in UCS:
    body.append(f"\n**{uc['Use Case Number']}: {uc['Use Case Name']}**\n")
    body.append(table(uc) + "\n")
body.append(TAIL)
open(sys.argv[1], "w").write("\n".join(body))
print("wrote", sys.argv[1])
