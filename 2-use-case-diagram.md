# Use Case Diagram

<!-- Rubric: resources/md/Coursework-01-group-v2.md, Requirements item 3 (10 points). -->

<!--
Scope: AS-IS (the farm's current manual process), per CLAUDE.md. The proposed system belongs in section 7 only.
One diagram, embedded as diagrams/use-case-diagram.png. Its source is diagrams/use-case-diagram.puml, rendered with Graphviz dot
(the pipeline's smetana engine cannot lay out 22 use cases legibly). Re-render: java -jar tools/plantuml.jar -tpng diagrams/use-case-diagram.puml

Now stated in 0-business-case.md (updated 2026-10-25): suppliers on contract paid by bank transfer; verbal death reports logged in the
notebook with feed use; butcher paid per head on a verbally agreed count; Bazaar Agent is a middleman who sends daily kg photos on
Telegram and settles by cash or transfer; pDaftar holds costs, revenue and profit.

Confirmed by Muzaffar (2026-10-24) but not in 0-business-case.md:
- Per-kg price with the Bazaar Agent is agreed verbally each time, following that day's bazaar rate.
- Delivery driver for the meat run: a temporary hire arranged by the Director; not an actor.
- Cameras: the earlier business-case draft said the Director checks the camera app remotely (Monitor Houses by Camera).

In sections 4-5 (Nodir) but NOT in 0-business-case.md or Muzaffar's answers - not used here until confirmed:
- a Worker writing down every weight reading at the bazaar, and the Director comparing it with the agent's photo;
- the Director weighing the sample birds himself;
- main slaughter repeating session by session until the houses are empty (assumed in UC-03 extension 8a and in section 5 - needs Muzaffar's confirmation).

Still open:
- Who slaughters the ~4,000 birds at day 35-40, and who buys that meat?
- Who places the 50-100-bird client orders (one of the three buyers, or a fourth channel)?
- How do the Nurata seller and the shop customers receive the meat and pay?
- Who cleans and prepares a house between batches, and who receives the chick delivery? (no use case yet)
- Do workers record anything when they check a house?
Reference names for sections 3-7: Director, Worker, Slaughter Crew, Chick Supplier, Feed Supplier, Buyer / Bazaar Agent / Nurata Seller / Shop Customer, and the use case names below.
-->

![Use case diagram of the farm's current operations](diagrams/use-case-diagram.png)

*Figure 2.1: Use case diagram of the farm's current (as-is) operations*

The boundary is the farm's current way of working, from procurement and daily production through the slaughter stages to sale. The farm has no computer system, so each use case is a manual task; some leave a record on paper, in pDaftar or on Telegram, and the diagram's value is in showing which ones do and which do not.

Two includes expose the farm's central record-keeping problem. Report Dead Chicks and Log Feed Use both include Write in Notebook, because the Worker reports deaths verbally and the Director copies the figure into the same paper notebook as feed use. Paying suppliers, paying the crew, arranging delivery, selling meat and calculating batch profit all include Record in pDaftar instead, so that use case collects every money step in the cycle. Production data and money therefore sit in two stores that never meet: Calculate Batch Profit can draw only on pDaftar, so a batch's profit is never set against the deaths and feed use that explain it. Two steps that decide money leave no record at all: the head count on which the butcher is paid, and the per-kg price agreed verbally with the Bazaar Agent at that day's bazaar rate.

The Director is linked to more use cases than any other actor because every decision passes through him: ordering, culling, deciding when to thin the flock, timing the slaughter, paying and selling. Both suppliers work under contract, so each order includes Pay Supplier by Bank Transfer, and the payment, not the order, is what reaches pDaftar. Decide Main Slaughter Date includes Weigh Sample Birds, because the timing rests on the average weight of about ten birds, and Postpone Slaughter extends it only when that average is too low, matching the three-to-five-day wait the farm uses. Buyer is generalised into the Bazaar Agent, the Nurata Seller and the Shop Customer: all three buy meat at a market-following price, but only a sale to the Bazaar Agent, a middleman reselling to seven to nine other sellers, triggers the two extensions: Agree Price per kg, settled verbally at that day's bazaar rate, and Send Weight Photo by Telegram, whose daily kg totals are the only weight record the farm receives for its largest sales channel. The Slaughter Crew takes part in Run Main Slaughter and in Pay Slaughter Crew per Head; within the crew, the butcher is paid per head on a count agreed verbally with the Director. The delivery driver is not an actor, because he is a temporary hire who appears only as a cost in Arrange Delivery. Slaughter Client Order is shared by the Director and the Worker because these 50–100-bird orders are slaughtered in-house, without the hired crew.
