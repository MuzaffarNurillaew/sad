'use strict';

/**
 * Domain model for FarmTrack, the proposed information system for
 * Nurota Halol Parranda MCHJ (the broiler farm analysed in CW1).
 * Every class here traces to a specific requirement in
 * 7-requirements-catalogue.md (see README.md for the full mapping).
 */

class User {
  constructor(name) {
    this.name = name;
  }
  canViewFinancials() {
    return false;
  }
}

class Director extends User {
  canViewFinancials() {
    return true;
  }
}

class Worker extends User {}

// Buyer hierarchy: the three channels named in the business case, each
// with its own, farm-set-nothing pricing rule (NFR traces: none directly,
// but FR-05/FR-03 depend on buyer.effectivePricePerKg()).
class Buyer {
  constructor(name) {
    this.name = name;
  }
  effectivePricePerKg() {
    throw new Error('effectivePricePerKg must be implemented by a subclass');
  }
}

class BazaarAgent extends Buyer {
  constructor(name, dailyRateUzs) {
    super(name);
    this.dailyRateUzs = dailyRateUzs;
  }
  effectivePricePerKg() {
    return this.dailyRateUzs;
  }
}

class IndividualSeller extends Buyer {
  constructor(name, rateUzs = 27000) {
    super(name);
    this.rateUzs = rateUzs;
  }
  effectivePricePerKg() {
    return this.rateUzs;
  }
}

class ShopCustomer extends Buyer {
  constructor(name, rateUzs = 28000) {
    super(name);
    this.rateUzs = rateUzs;
  }
  effectivePricePerKg() {
    return this.rateUzs;
  }
}

class House {
  constructor(id, name, capacityMin, capacityMax) {
    this.id = id;
    this.name = name;
    this.capacityMin = capacityMin;
    this.capacityMax = capacityMax;
  }
}

const DUPLICATE_WINDOW_MS = 2 * 60 * 1000;

class MortalityRecord {
  constructor(id, batchId, houseId, workerName, note, timestamp = Date.now()) {
    this.id = id;
    this.batchId = batchId;
    this.houseId = houseId;
    this.workerName = workerName;
    this.note = note || null;
    this.timestamp = timestamp;
    this.flaggedDuplicateOfId = null;
  }
}

class FeedDelivery {
  constructor(id, batchId, houseId, supplier, quantityKg, costUzs, date) {
    this.id = id;
    this.batchId = batchId;
    this.houseId = houseId;
    this.supplier = supplier;
    this.quantityKg = quantityKg;
    this.costUzs = costUzs;
    this.date = date;
  }
}

class SlaughterSession {
  constructor(id, batchId, crewReportedHeadcount, paymentPerHeadUzs, date) {
    this.id = id;
    this.batchId = batchId;
    this.crewReportedHeadcount = crewReportedHeadcount;
    this.paymentPerHeadUzs = paymentPerHeadUzs;
    this.date = date;
    this.confirmedHeadcount = null;
    this.correctionNote = null;
  }
  confirm(count, note) {
    this.confirmedHeadcount = count;
    this.correctionNote = note || null;
  }
  effectiveHeadcount() {
    return this.confirmedHeadcount != null ? this.confirmedHeadcount : this.crewReportedHeadcount;
  }
  totalPaymentUzs() {
    return this.effectiveHeadcount() * this.paymentPerHeadUzs;
  }
}

class SaleRecord {
  constructor(id, batchId, buyer, kg, trustedRepKg, date) {
    this.id = id;
    this.batchId = batchId;
    this.buyer = buyer;
    this.kg = kg;
    this.trustedRepKg = trustedRepKg != null ? trustedRepKg : null;
    this.date = date;
  }
  // FR-05: cross-check the bazaar agent's reported total against the
  // Trusted Representative's own weighing for the same session.
  crossCheckStatus() {
    if (this.trustedRepKg == null) return 'not_applicable';
    if (this.kg === this.trustedRepKg) return 'match';
    const diff = Math.abs(this.kg - this.trustedRepKg);
    return diff / this.trustedRepKg > 0.03 ? 'mismatch_flagged' : 'minor_variance';
  }
  revenueUzs() {
    return this.kg * this.buyer.effectivePricePerKg();
  }
}

class Batch {
  constructor(id, houseId, startDate) {
    this.id = id;
    this.houseId = houseId;
    this.startDate = startDate;
    this.status = 'active';
    this.mortalityRecords = [];
    this.feedDeliveries = [];
    this.slaughterSessions = [];
    this.saleRecords = [];
  }

  // FR-01: flag a death as a possible duplicate if another death was
  // logged for the same batch within the same couple of minutes by a
  // different worker, rather than silently double-counting it.
  addMortality(record) {
    const possibleDuplicate = this.mortalityRecords.find(
      (r) => Math.abs(r.timestamp - record.timestamp) < DUPLICATE_WINDOW_MS && r.workerName !== record.workerName
    );
    if (possibleDuplicate) {
      record.flaggedDuplicateOfId = possibleDuplicate.id;
    }
    this.mortalityRecords.push(record);
    return record;
  }

  addFeedDelivery(delivery) {
    this.feedDeliveries.push(delivery);
    return delivery;
  }

  addSlaughterSession(session) {
    this.slaughterSessions.push(session);
    return session;
  }

  addSaleRecord(sale) {
    this.saleRecords.push(sale);
    return sale;
  }

  mortalityCount() {
    return this.mortalityRecords.filter((r) => !r.flaggedDuplicateOfId).length;
  }

  totalFeedKg() {
    return this.feedDeliveries.reduce((sum, f) => sum + f.quantityKg, 0);
  }

  totalFeedCostUzs() {
    return this.feedDeliveries.reduce((sum, f) => sum + f.costUzs, 0);
  }

  totalCrewPaymentUzs() {
    return this.slaughterSessions.reduce((sum, s) => sum + s.totalPaymentUzs(), 0);
  }

  totalRevenueUzs() {
    return this.saleRecords.reduce((sum, s) => sum + s.revenueUzs(), 0);
  }

  // FR-03: profit per batch, not pooled across houses.
  profitUzs() {
    return this.totalRevenueUzs() - this.totalFeedCostUzs() - this.totalCrewPaymentUzs();
  }

  totalBirdsSlaughtered() {
    return this.slaughterSessions.reduce((sum, s) => sum + s.effectiveHeadcount(), 0);
  }

  // FR-02: feed used per bird still alive and fed in this batch.
  feedPerBirdKg(initialBirdCount) {
    const birdsRemaining = initialBirdCount - this.mortalityCount();
    if (birdsRemaining <= 0) return null;
    return this.totalFeedKg() / birdsRemaining;
  }
}

module.exports = {
  User,
  Director,
  Worker,
  Buyer,
  BazaarAgent,
  IndividualSeller,
  ShopCustomer,
  House,
  Batch,
  MortalityRecord,
  FeedDelivery,
  SlaughterSession,
  SaleRecord,
};
