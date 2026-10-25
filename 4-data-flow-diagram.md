# Data Flow Diagram

The diagrams show how Nurota Halol Parranda handles its data today, without any computer system. The boundary is the farm itself. The Director and the Workers carry out every process inside it, so neither appears as an external entity. Outside are the two suppliers, the Slaughter Crew and the Delivery Driver who are hired for each slaughter, and the three buyers: the Bazaar Agent, the Nurata Seller and the Shop Customer. The Delivery Driver is not an actor in the use case diagram, but he is drawn here because the farm sends him a call-in date and a fee.

The farm's records end up in five places: the Director's paper notebook, the camera footage, the pDaftar app on his phone, the weight photos the Bazaar Agent sends on Telegram, and the tally a Worker keeps while the meat is weighed at the bazaar. None of them is linked to another.

## Level 0

![DFD Level 0 of the farm's current system](diagrams/dfd-level0.png)

*Figure 4.1: DFD Level 0, the farm's current system*

Every money figure goes into pDaftar (D3). Processes 1, 2 and 4 add costs, process 5 adds sales income, and process 6 reads both back to get the profit of a batch. Chick deaths and feed use go only into the notebook (D1), and no process reads them back, so they never reach the profit figure and the farm cannot see the cost per bird or how much feed a batch really used. This matches the business case, where decisions rest on the Director's experience rather than on these records. The head count that sets the crew's pay comes in from the crew and is turned straight into a payment without being written down.

Processes 1, 2 and 6 are not broken down further. Each order is a single exchange with one supplier, paid by bank transfer under the standing contract, and process 6 is one calculation made from figures already in pDaftar.

The early cull of sick chicks around day 25, the slaughter of about 4,000 birds around day 35–40 and the small client orders of 50–100 birds are not drawn. The farm has not yet confirmed what each of these records or who buys those birds, so only the main slaughter is modelled.

## Level 1: Process 3 Monitor Flock

![DFD Level 1 for process 3](diagrams/dfd-level1-process3.png)

*Figure 4.2: DFD Level 1, Process 3 Monitor Flock*

Workers check each house every 15–30 minutes (3.1). When one of them finds a dead chick he tells the Director, who writes it in the notebook (3.3), and feed use goes into the same notebook (3.4). The death count passes through two people and a spoken message before it is written down, which is why the business case calls it approximate. The cameras record the houses (3.2), but the footage stays in the monitoring app and feeds nothing else, so it adds no record the farm can use later.

## Level 1: Process 4 Run Main Slaughter

![DFD Level 1 for process 4](diagrams/dfd-level1-process4.png)

*Figure 4.3: DFD Level 1, Process 4 Run Main Slaughter*

Process 4 brings together four use cases from section 2: Decide Main Slaughter Date, Run Main Slaughter, Pay Slaughter Crew per Head and Arrange Delivery. The Director weighs about ten birds (4.1) and uses their average to decide whether to call in the crew and the driver now or wait three to five more days (4.2). After the session the crew reports how many birds it slaughtered, the Director accepts that count verbally (4.3) and pays the crew from it, with the butcher paid per head (4.4). Only the payment reaches pDaftar. The count behind it is never recorded, so a wrong count cannot be checked later. The driver's fee for taking the meat to the bazaar (4.5) goes into pDaftar as well.

## Level 1: Process 5 Sell Meat

![DFD Level 1 for process 5](diagrams/dfd-level1-process5.png)

*Figure 4.4: DFD Level 1, Process 5 Sell Meat*

The meat goes to three buyers (5.2), and the farm treats them very differently. The Bazaar Agent, an independent middleman who resells to seven to nine other sellers, takes the largest share. His price per kg is agreed verbally at that day's bazaar rate (5.1). While he weighs the meat, a Worker writes down every reading (5.3), and the agent later sends his own totals as a photo on Telegram (5.4). The Director compares the two totals (5.5) and only then works out what the agent owes, the confirmed kilograms times the agreed price (5.6). The Nurata Seller and the Shop Customer pay the farm directly, and that income goes into pDaftar with the rest (5.7). The farm has not yet confirmed how it measures the meat these two take.
