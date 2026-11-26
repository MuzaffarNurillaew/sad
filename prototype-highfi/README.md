# FarmTrack — high-fidelity prototype

Executable prototype of the proposed information system for Nurota Halol
Parranda MCHJ, the broiler farm analysed in CW1. Built for CW2's Solution
Prototypes deliverable with AI assistance (Claude), as permitted by the brief.

## Scope

Implements the full procurement-to-sale record-keeping spine that CW1's
requirements catalogue (`../7-requirements-catalogue.md`) already specifies
as fully elicited and stable:

| Requirement | Where in this prototype |
|---|---|
| FR-01 Direct worker mortality logging, duplicate flag | `Batch.addMortality()` in `models.js`; Mortality panel in UI |
| FR-02 Batch-tagged feed delivery recording, feed/bird | `Batch.addFeedDelivery()`, `Batch.feedPerBirdKg()` |
| FR-03 Per-batch profit calculation | `Batch.profitUzs()`; profit panel |
| FR-04 Recorded slaughter crew head count, correction | `SlaughterSession.confirm()`; slaughter panel |
| FR-05 Bazaar agent total cross-check | `SaleRecord.crossCheckStatus()`; sales panel |
| NFR-01 Phone-first field use | mobile-first single-column CSS, no desktop-only control |
| NFR-02 Multi-worker field entry | any worker can post a record for any house without going through the director |
| NFR-03 Director-only financial visibility | enforced server-side in `server.js` (fields stripped per role, `/api/batches/:id/profit` returns 403 for workers) — not just hidden in the UI |
| NFR-05 Arbitrary house/batch count | `House`/`Batch` are plain configuration objects; director can add a house at runtime via "Add a house" |

FR-06 (voice entry), FR-07 (environment monitoring), FR-08 (remote
lighting), FR-09 (flock density analysis) are **not** in this prototype —
they depend on hardware/AI validation not yet proven, and are shown only as
planned packages in the architecture diagram (`2-uml-class-diagram.md`).

## Run it

No external dependencies — pure Node.js core modules only.

```sh
cd prototype-highfi
node server.js
# open http://localhost:4100
```

Log in as **worker** to see field-entry-only access (no financial figures,
`/api/batches/:id/profit` returns 403). Log in as **director** to see the
full picture, confirm a slaughter headcount, and record a sale.

## Code structure

- `models.js` — domain classes (`User`/`Director`/`Worker`, `Buyer` hierarchy,
  `House`, `Batch`, `MortalityRecord`, `FeedDelivery`, `SlaughterSession`,
  `SaleRecord`). Mirrors the detailed class diagram directly.
- `store.js` — in-memory data store, seeded with two houses and realistic
  batch data drawn from the business case (`../0-business-case.md`).
- `server.js` — plain `http` server: a small JSON API plus static file
  serving for `public/`.
- `public/` — vanilla HTML/CSS/JS front end (no framework, no build step).
