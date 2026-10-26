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
        "Application": "Nurota Halol Parranda: current operations, procurement and accounts (Figure 2.2)",
        "Use Case Name": "Order Day-Old Chicks",
        "Use Case Description": (
            "The Director orders a new batch of chicks for an empty house from the contracted supplier in Tashkent. Because the contract has the chicks paid for only when the batch ends, the farm is already selling a batch's meat before it has paid for the birds."
        ),
        "Primary Actor": "Director",
        "Secondary Actor(s)": "Chick Supplier",
        "Precondition": "A supply contract is in place with the chick supplier in Tashkent, with payment due when the batch ends.",
        "Postconditions": (
            "Day-old chicks matching the house's capacity have been delivered by the supplier, and their cost "
            "is owed to the supplier until the batch ends."
        ),
        "Trigger": "A house has been emptied at the end of its previous batch.",
        "Basic Flow": [
            "The Director confirms that the house has been cleaned and prepared.",
            "The Director sets the order size from the house's 5,000–10,000-bird capacity.",
            "The Director places the order with the contracted supplier in Tashkent.",
            "The Chick Supplier delivers the chicks to the farm by Damas van (includes Deliver Day-Old Chicks).",
        ],
        "Extensions": [
            "1a. The house is not yet cleaned: the order waits until the Cleaning Crew has finished, then the flow resumes at step 1.",
            "4a. Some chicks arrive dead, or fewer arrive than ordered: under the contract the Chick Supplier bears the loss, so the Director raises it with the supplier rather than absorbing it. The use case then ends as normal.",
        ],
    },
    {
        "Use Case Number": "UC-02",
        "Application": "Nurota Halol Parranda: current operations, slaughter and sales (Figure 2.3)",
        "Use Case Name": "Decide Main Slaughter Date",
        "Use Case Description": (
            "The Director decides when to call in the slaughter crew. He weighs up the birds' age, the average weight of about ten birds and his own experience. We found no written target weight or age, and the call depends on him alone: nobody else could make it or check it."
        ),
        "Primary Actor": "Director",
        "Secondary Actor(s)": "Slaughter Crew",
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
            "The Director weighs a sample of about ten birds and takes their average (includes Weigh Sample Birds).",
            "The Director judges from the age, the sample average and his experience that the batch is ready.",
            "The Director calls in the hired crew, starting UC-03 Run Main Slaughter.",
        ],
        "Extensions": [
            "3a. The Director judges the batch not yet ready: he waits three to five more days, which adds days of feed to the batch, and the flow resumes at step 1 with a new sample.",
        ],
    },
    {
        "Use Case Number": "UC-03",
        "Application": "Nurota Halol Parranda: current operations, slaughter and sales (Figure 2.3)",
        "Use Case Name": "Run Main Slaughter",
        "Use Case Description": (
            "A hired crew of about six slaughters and cleans 1,000–1,200 birds in one overnight session, and the Director calls them back as many times as it takes to empty the house. The butcher is paid per head. The count behind that pay is agreed out loud at the end of each session and is not recorded."
        ),
        "Primary Actor": "Director",
        "Secondary Actor(s)": "Slaughter Crew",
        "Precondition": "The Director has judged the batch ready for slaughter (UC-02 Decide Main Slaughter Date).",
        "Postconditions": (
            "One session's birds are processed and ready for UC-04, the head count that sets the butcher's "
            "pay has been agreed verbally, and the crew has been called back for the next session."
        ),
        "Trigger": "The Director calls in the hired crew, first at the end of UC-02 and then once for each further session.",
        "Basic Flow": [
            "The crew arrives for an overnight session.",
            "The butcher kills each bird.",
            "The scalder loosens the feathers in hot water.",
            "The plucker removes the feathers.",
            "Two to three crew workers clean the internal organs.",
            "The Director and the butcher agree the session's head count verbally.",
            "The Director calls the crew back for the next session.",
        ],
        "Extensions": [
            "7a. No birds remain in the house after the session: the Director does not call the crew back, the batch's slaughter is finished, and the house goes to cleaning before the next order (UC-01). The use case ends.",
        ],
    },
    {
        "Use Case Number": "UC-04",
        "Application": "Nurota Halol Parranda: current operations, slaughter and sales (Figure 2.3)",
        "Use Case Name": "Sell Meat to Bazaar Agent",
        "Use Case Description": (
            "The Bazaar Agent is the farm's largest buyer. As a middleman reselling to seven to nine other sellers, the agent pays only about 26,000 UZS/kg, a little below the bazaar rate. Whoever the Director trusts that day goes to the bazaar, writes down the same weighings as the agent and collects the cash. The farm says the two weight records never disagree, yet only the payment reaches pDaftar; both weight records stay outside it."
        ),
        "Primary Actor": "Director",
        "Secondary Actor(s)": "Bazaar Agent",
        "Precondition": "Meat from a slaughter session (UC-03) is ready for sale.",
        "Postconditions": (
            "The agent has paid total kg × the agreed price per kg, and the revenue is recorded in pDaftar."
        ),
        "Trigger": "A slaughter session finishes and its meat is ready.",
        "Basic Flow": [
            "The Director and the agent agree that day's price per kg between them, a little below the bazaar rate (includes Agree Price per kg).",
            "The Director sends the meat to Navoi bazaar with a temporarily hired driver.",
            "The agent weighs the meat, while a person the Director trusts records the same weighings.",
            "The agent photographs his kg totals and sends them to the Director on Telegram (includes Send Weight Photo by Telegram).",
            "The Director checks the photographed totals against the farm's own record.",
            "The agent pays the total kg × the agreed price per kg in cash to the trusted person at the end of the day.",
            "The Director records the revenue in pDaftar (Record in pDaftar, which Sell Meat includes).",
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
Confirmed 2026-10-26 and used here: chicks only from Tashkent; chicks and feed bought under contract and paid when each batch ends (user confirmed again 2026-10-26: 'paid by contract', at batch end);
suppliers deliver; readiness judged on age + random-sample average weight + experience; number of slaughter sessions per batch not fixed;
Bazaar Agent is an independent middleman paying a little below the bazaar rate; amount owed = kg x price; a second person from the farm
also records the bazaar weighings; agent pays cash or transfer at the end of the day.
To confirm with Muzaffar (question -> table -> marks at stake):
Answered 2026-10-26: weight mismatch 'no chance' (none added); short/dead chicks are the supplier's responsibility (UC-01 4a);
bazaar person = anyone the Director trusts, who also takes the cash (UC-04 steps 3, 6); price agreed before dispatch (UC-04 order kept).
- Has the crew ever disputed the head count, or not turned up? -> UC-03 exception (its only extension, 7a, is an alternate ending) -> +0.5.
- Who weighs the sample birds? (sections 4-5 say the Director) -> UC-02 step 2.
Flag for section 1 (Muzaffar): every 2026-10-24/26 answer used here needs to be recorded there as evidence.
Flag for Nodir: sections 4-5 say the agent pays "at" the day's bazaar rate; confirmed answer is "a little below".
-->

The four use cases follow one batch from buying the chicks to selling the meat. We chose them because each turns on a decision that moves money: what the batch costs (UC-01), when it is slaughtered (UC-02), what slaughtering costs (UC-03) and what the meat earns (UC-04). Feed is ordered on the same contract terms as chicks, so a feed table would repeat UC-01. Selling is shown through the Bazaar Agent, the largest channel and the only sale with steps of its own (Figure 2.3). Two of the four decisions rest on nothing more than a spoken agreement: the butcher's head count (UC-03) and the agent's price per kg (UC-04).
"""

TAIL = ""

body = [HEAD]
for uc in UCS:
    body.append(f"\n**{uc['Use Case Number']}: {uc['Use Case Name']}**\n")
    body.append(table(uc) + "\n")
body.append(TAIL)
open(sys.argv[1], "w").write("\n".join(body))
print("wrote", sys.argv[1])
