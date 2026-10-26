# Use Case Diagram

<!-- Rubric: resources/md/Coursework-01-group-v2.md, Requirements item 3 (10 points). -->

<!--
Scope: AS-IS (the farm's current manual process), per CLAUDE.md. The proposed system belongs in section 7 only.
One diagram, embedded as diagrams/use-case-diagram.png. Its source is diagrams/use-case-diagram.puml, rendered with Graphviz dot
(the pipeline's smetana engine cannot lay out 24 use cases legibly). Re-render: java -jar tools/plantuml.jar -tpng diagrams/use-case-diagram.puml

Stated in 0-business-case.md: suppliers on contract; verbal death reports logged in the notebook with feed use; butcher paid per
head on a verbally agreed count; Bazaar Agent is a middleman who sends daily kg photos on Telegram and settles by cash or transfer;
pDaftar holds costs, revenue and profit.

Confirmed by Muzaffar but not (yet) in 0-business-case.md:
- 2026-10-24: per-kg price with the Bazaar Agent is agreed verbally each time; delivery driver for the meat run is a temporary hire
  arranged by the Director (not an actor); the Director checks the camera app (Monitor Houses by Camera).
- 2026-10-26 (interview): chicks come only from Tashkent; chicks and feed are bought under contract and paid when
  each batch ends; the suppliers deliver both; the agent is an independent middleman who pays a little below the bazaar rate;
  readiness is judged on age + random-sample average weight + experience; the number of slaughter sessions per batch is not fixed;
  birds are sold only as meat; amount owed = kg x price, and a second person from the farm also records the bazaar weighings.
  NOTE for Muzaffar: 0-business-case.md still says "Samarkand or Tashkent" and "standing contract paid by bank transfer" - update it.

Still open (no use case or actor added until confirmed):
- Who slaughters the ~4,000 birds at day 35-40, and who buys that meat?
- Who places the 50-100-bird client orders (one of the three buyers, or a fourth channel)?
- How do the Nurata seller and the shop customers receive the meat and pay?
- Who cleans and prepares a house between batches, who receives the chick delivery, and who feeds the birds?
- Who is the "second person from our side" at the bazaar? Is the batch-end supplier payment still by bank transfer?
Step 0 decisions (2026-10-26): boundary = the farm's manual procedures and records, so Director and Workers are actors
(section 4 draws the boundary around the farm itself, hence they are inside there; reconciled in the visible text).
The Director is kept as one actor; his three roles (owner, production decider, record keeper) are stated as a finding.
Postpone Slaughter removed from the diagram: it restarts the decision rather than adding to it, so it is UC-02 extension 3a.
Calculate Batch Profit no longer includes Record in pDaftar: it only reads it.
2026-10-26 rename: "Pay Slaughter Crew per Head" -> "Pay Slaughter Crew" (section 0 says only the butcher is paid per head).
FLAG for Nodir: 4-data-flow-diagram.md line 33 still uses the old name.
UC-02 now lists the Slaughter Crew as secondary actor, so the diagram links Slaughter Crew to Decide Main Slaughter Date.
Reference names for sections 3-7: Director, Worker, Slaughter Crew, Chick Supplier, Feed Supplier, Buyer / Bazaar Agent / Nurata Seller / Shop Customer, and the use case names below.
-->

The diagram shows how Nurota Halol Parranda runs today, from ordering chicks to selling the meat, with no computer system involved. We drew the boundary around the farm's manual procedures and records rather than around the farm itself. That is why the Director and the Workers are actors here but sit inside the boundary in the section 4 DFD. The two suppliers, the hired Slaughter Crew and the buyers are outside. The Bazaar Agent, the Nurata Seller and the Shop Customer are kinds of Buyer. Small client orders are linked to Buyer in general, since we do not yet know which buyers place them. House cleaning between batches is left off until we know who does it. The delivery driver is a temporary hire who shows up only as a cost in Arrange Delivery, so the driver is not an actor.

![Use case diagram of the farm's current operations](diagrams/use-case-diagram.png)

*Figure 2.1: Use case diagram of the farm's current (as-is) operations*

The farm keeps two kinds of record and never joins them. Report Dead Chicks and Log Feed Use both include Write in Notebook. Paying the suppliers, paying the crew, arranging delivery and selling meat all include Record in pDaftar. Calculate Batch Profit reads only pDaftar, so a batch's profit is never set against the deaths and feed use behind it. A house check leaves a record only when a dead chick is found, and that is the one point where Report Dead Chicks extends Check Houses.

The Director is linked to 15 of the 24 use cases. In practice the farm's owner, production manager and bookkeeper are the same person. Three of his money decisions rest on judgement or a spoken agreement: the butcher's head count, the agent's price per kg, and the slaughter date, which he sets from a sample of about ten birds and his own experience. The butcher is paid per head, but every buyer pays per kilogram, and no record links the two. As a result, the farm cannot tell what slaughtering costs per kilogram sold. Under the supply contract, chicks and feed are paid for when the batch ends, and Pay Supplier at Batch End is drawn apart from ordering for that reason: a batch's chick and feed bills are settled only after its meat has been sold.

Sell Meat to Bazaar Agent is a special case of Sell Meat because only this sale has steps of its own: a price agreed each time in conversation, and a Telegram photo of the weights. It is also the one place where the farm checks a figure from an outsider. Someone from the farm writes down the same weighings as the agent.
