# UML Class Diagram

FarmTrack's class model implements the core record-keeping requirements
already fixed by CW1's catalogue (FR-01–05, NFR-01/02/03/05); the
IoT/voice/vision requirements (FR-06–09) are shown only as planned,
unimplemented packages, since they depend on hardware and AI validation not
yet carried out. Both diagrams reflect the prototype's actual code
(`prototype-highfi/models.js`, `server.js`), not an idealised design drawn
separately from it.

## Architecture Diagram (packages and sub-systems)

```plantuml
@startuml
!pragma layout smetana
skinparam packageStyle rectangle

package "Presentation\n(public/*.html, app.js)" as Presentation {
  class WebClient {
    +renderDashboard()
    +renderBatch(batchId)
    +submitForm(form)
  }
}

package "Application Services\n(server.js)" as Services {
  class AuthService {
    +login(role, name) : token
    +authenticate(token) : Session
  }
  class BatchService {
    +recordMortality(batchId, workerName, note)
    +recordFeedDelivery(batchId, delivery)
    +recordSlaughterSession(batchId, session)
    +recordSale(batchId, sale)
  }
  class FinancialGuard {
    +canSee(session, field) : boolean
  }
}

package "Domain Model\n(models.js)" as Domain {
  class House
  class Batch
  class "User hierarchy" as UserH
  class "Buyer hierarchy" as BuyerH
  class MortalityRecord
  class FeedDelivery
  class SlaughterSession
  class SaleRecord
}

package "Data Store\n(store.js)" as Store {
  class InMemoryStore {
    +houses : House[]
    +batches : Batch[]
    +sessions : Map
  }
}

package "Planned Extensions\n(not yet implemented)" as Planned {
  class VoiceEntryService <<planned>> {
    +parseSpokenRecord(audio) : Record
  }
  class EnvironmentMonitorService <<planned>> {
    +readSensors(houseId) : Reading
  }
  class LightingControlService <<planned>> {
    +setLighting(houseId, on)
  }
  class FlockDensityAnalyzer <<planned>> {
    +estimateDensity(houseId) : Estimate
  }
}

Presentation --> Services : HTTP/JSON (fetch)
Services --> Domain : operates on
Services --> Store : reads/writes
AuthService --> FinancialGuard : role check (NFR-03)
Planned ..> Domain : would extend House/Batch
note right of Planned
  FR-06 (voice entry), FR-07 (environment
  monitoring), FR-08 (remote lighting),
  FR-09 (density analysis) - deferred,
  not in the executable prototype.
end note
@enduml
```

## Detailed Class Diagram (core record-keeping module)

```plantuml
@startuml
!pragma layout smetana

abstract class User {
  +name : String
  +canViewFinancials() : boolean
}
class Director extends User {
  +canViewFinancials() : boolean
}
class Worker extends User
User <|-- Director
User <|-- Worker

abstract class Buyer {
  +name : String
  +effectivePricePerKg() : Number
}
class BazaarAgent extends Buyer {
  +dailyRateUzs : Number
  +effectivePricePerKg() : Number
}
class IndividualSeller extends Buyer {
  -rateUzs : Number
  +effectivePricePerKg() : Number
}
class ShopCustomer extends Buyer {
  -rateUzs : Number
  +effectivePricePerKg() : Number
}
Buyer <|-- BazaarAgent
Buyer <|-- IndividualSeller
Buyer <|-- ShopCustomer

class House {
  +id : String
  +name : String
  +capacityMin : Number
  +capacityMax : Number
}

class Batch {
  +id : String
  +houseId : String
  +startDate : String
  +status : String
  -mortalityRecords : MortalityRecord[]
  -feedDeliveries : FeedDelivery[]
  -slaughterSessions : SlaughterSession[]
  -saleRecords : SaleRecord[]
  +addMortality(record) : MortalityRecord
  +addFeedDelivery(delivery) : FeedDelivery
  +mortalityCount() : Number
  +totalFeedKg() : Number
  +totalFeedCostUzs() : Number
  +totalRevenueUzs() : Number
  +totalCrewPaymentUzs() : Number
  +profitUzs() : Number
  +feedPerBirdKg(initialBirdCount) : Number
}

class MortalityRecord {
  +id : String
  +workerName : String
  +note : String
  +timestamp : Number
  +flaggedDuplicateOfId : String
}

class FeedDelivery {
  +id : String
  +supplier : String
  +quantityKg : Number
  -costUzs : Number
  +date : String
}

class SlaughterSession {
  +id : String
  +crewReportedHeadcount : Number
  +confirmedHeadcount : Number
  -paymentPerHeadUzs : Number
  +correctionNote : String
  +confirm(count, note)
  +effectiveHeadcount() : Number
  +totalPaymentUzs() : Number
}

class SaleRecord {
  +id : String
  +kg : Number
  +trustedRepKg : Number
  +date : String
  +crossCheckStatus() : String
  +revenueUzs() : Number
}

House "1" o-- "*" Batch : runs over time
Batch "1" *-- "*" MortalityRecord : logs
Batch "1" *-- "*" FeedDelivery : logs
Batch "1" *-- "*" SlaughterSession : logs
Batch "1" *-- "*" SaleRecord : logs
SaleRecord "1" --> "1" Buyer : sold to
Worker ..> MortalityRecord : creates
Worker ..> FeedDelivery : creates
Director ..> SlaughterSession : creates/confirms
Director ..> SaleRecord : creates
@enduml
```

Relationship types used: **generalization** (`User`→`Director`/`Worker`,
`Buyer`→its three subtypes), **composition** (`Batch` owns its mortality,
feed, slaughter and sale records — none of these exist independently of
the batch they belong to), **aggregation** (`House` has `Batch`es across
successive production cycles, but a `Batch` is meaningful on its own record
once closed), **association** (`SaleRecord`→`Buyer`, since a buyer exists
independently of any one sale), and **dependency** (`Worker`/`Director`
creating specific record types, reflecting the role split in NFR-02/NFR-03).
