# Data Flow Diagram

The diagrams below illustrate how data flows across the farm as it operates today. The farm serves as the system boundary. The processes are carried out by the director, permanent personnel, and a worker who registers weights at the bazaar. The chick provider, the feed supplier, the hired slaughter crew and driver, and the sales agent are all outside the farm and appear as separate organisations.

The farm keeps its records in five places: the director's paper notebook, camera footage, the pDaftar app on his phone, weight images received over Telegram, and the farm's own weight tally.

## Level 0

![DFD Level 0 of the broiler farm](diagrams/dfd-level0.png)

*Figure 5.1. DFD Level 0 of the broiler farm (current system)*

All financial information ends up in pDaftar (D3). Processes 1, 2, and 4 write costs, process 5 writes revenue, and process 6 reads both to calculate a batch's profit. Mortality and feed usage are only recorded in the paper notebook (D1) and never factored into the profit calculation; thus, the farm cannot determine the cost per bird or how efficiently feed is used. The head count from the slaughter team determines how much the crew is paid, although it is not recorded elsewhere.

Process 6 has no Level 1 diagram because it is a single calculation: it reads costs and revenue from pDaftar and writes the batch profit back.

## Level 1: Process 3 Raise & Monitor Batch

![DFD Level 1 for process 3](diagrams/dfd-level1-process3.png)

*Figure 5.2. DFD Level 1, Process 3 Raise & Monitor Batch*

Workers inspect the residences in person, while the director examines them via cameras (3.2). Workers inform the director how many chicks died, and he records the information in his notebook (3.3). He records feed usage in the same notebook (3.4). The mortality record so relies on one person writing down what he was informed.

## Level 1: Process 4 Slaughter Batch

![DFD Level 1 for process 4](diagrams/dfd-level1-process4.png)

*Figure 5.3. DFD Level 1, Process 4 Slaughter Batch*

The director determines the slaughter date (4.1). The hired staff slaughters the birds and records how many are processed (4.2). They are paid per head (4.3), and a driver hired for the nite transports the meat to the bazaar for a one-time price (4.4). Crew wages and transportation costs are entered into pDaftar separately, however the head count for the wages is only agreed upon verbally.

## Level 1: Process 5 Sell Meat to Sales Agent

![DFD Level 1 for process 5](diagrams/dfd-level1-process5.png)

*Figure 5.4. DFD Level 1, Process 5 Sell Meat to Sales Agent*

The sales representative is a self-employed merchant. The farm only has one buyer instead of seven or nine since he purchases the meat for slightly less than the bazaar price and resells it to his own vendors. A farm worker records each scale reading as he weighs the meat (5.3, D5). On Telegram, the agent posts a picture of his own totals (5.4, D4). To determine the revenue, he reports in pDaftar (5.6), the director multiplies the confirmed kilos by the agreed price after comparing the two totals (5.5). This comparison is the only check the farm has on the agent's figures.
