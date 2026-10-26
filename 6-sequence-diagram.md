# Sequence Diagram

Each diagram traces to one of the four use cases in `3-use-cases.md`, reusing its actors and basic-flow order.

```plantuml
@startuml
actor Director
participant "Chick Supplier" as Supplier

Director -> Director : confirm house cleaned and prepared
Director -> Director : set order size from house capacity
Director -> Supplier : place order for day-old chicks
activate Supplier
Supplier -->> Director : deliver chicks by Damas van
deactivate Supplier
alt some chicks dead or short on arrival
  Supplier -->> Director : loss stays the supplier's responsibility
else chicks delivered as ordered
end
@enduml
```

*Figure 6.1: UC-01 Order Day-Old Chicks*

```plantuml
@startuml
actor Director
participant "Slaughter Crew" as Crew

Director -> Director : check batch age against growth period
Director -> Director : weigh sample of about ten birds
alt batch judged ready
  Director -> Director : judge ready from age, sample weight, experience
else batch not yet ready
  Director -> Director : wait three to five more days, then recheck
end
Director -> Crew : call in hired crew (starts UC-03 Run Main Slaughter)
@enduml
```

*Figure 6.2: UC-02 Decide Main Slaughter Date*

```plantuml
@startuml
actor Director
participant "Slaughter Crew" as Crew

Director -> Crew : call in crew for an overnight session
activate Crew
Crew -> Crew : butcher kills each bird
Crew -> Crew : scalder loosens feathers in hot water
Crew -> Crew : plucker removes feathers
Crew -> Crew : two to three workers clean internal organs
Crew -->> Director : butcher reports head count (sets his pay)
deactivate Crew
Director -> Director : accept count verbally, not written down
alt birds remain in the house
  Director -> Crew : call crew back for another session
else no birds remain
  Director -> Director : slaughter finished; house goes to Cleaning Crew
end
@enduml
```

*Figure 6.3: UC-03 Run Main Slaughter*

```plantuml
@startuml
actor Director
participant "Bazaar Agent" as Agent
participant "Trusted Representative" as Rep

Director -> Agent : agree price per kg before meat leaves
activate Agent
Agent -->> Director : confirm price, a little below bazaar rate
deactivate Agent
Director -> Rep : send meat to Navoi bazaar with hired driver
activate Rep
Agent -> Agent : write down each weighing
Rep -> Rep : record the same weighings
Agent -->> Director : send photo of weight page via Telegram
alt agent pays cash
  Agent -->> Rep : pay total kg x price in cash
else agent pays by bank transfer
  Agent -->> Director : pay total kg x price by bank transfer
end
deactivate Rep
Director -> Director : record revenue in pDaftar
@enduml
```

*Figure 6.4: UC-04 Sell Meat to Bazaar Agent*
