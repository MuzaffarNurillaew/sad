'use strict';

const crypto = require('crypto');
const {
  Director,
  Worker,
  House,
  Batch,
  MortalityRecord,
  FeedDelivery,
  SlaughterSession,
  SaleRecord,
  BazaarAgent,
  IndividualSeller,
  ShopCustomer,
} = require('./models');

let nextId = 1;
function id() {
  return String(nextId++);
}

const houses = [];
const batches = [];
const sessions = new Map(); // token -> User instance

function findHouse(houseId) {
  return houses.find((h) => h.id === houseId);
}

function findBatch(batchId) {
  return batches.find((b) => b.id === batchId);
}

function findSlaughterSession(sessionId) {
  for (const batch of batches) {
    const session = batch.slaughterSessions.find((s) => s.id === sessionId);
    if (session) return { batch, session };
  }
  return null;
}

function login(role, name) {
  const user = role === 'director' ? new Director(name) : new Worker(name);
  const token = crypto.randomBytes(16).toString('hex');
  sessions.set(token, { user, role });
  return token;
}

function getSession(token) {
  return sessions.get(token) || null;
}

function seed() {
  const houseA = new House(id(), 'House 1', 5000, 10000);
  const houseB = new House(id(), 'House 2', 5000, 10000);
  houses.push(houseA, houseB);

  const daysAgo = (n) => new Date(Date.now() - n * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);

  const batchA = new Batch(id(), houseA.id, daysAgo(38));
  const batchB = new Batch(id(), houseB.id, daysAgo(12));
  batches.push(batchA, batchB);

  batchA.addMortality(new MortalityRecord(id(), batchA.id, houseA.id, 'Aziz', 'found near feeder', Date.now() - 1000 * 60 * 60 * 20));
  batchA.addMortality(new MortalityRecord(id(), batchA.id, houseA.id, 'Bekzod', null, Date.now() - 1000 * 60 * 60 * 5));

  batchA.addFeedDelivery(new FeedDelivery(id(), batchA.id, houseA.id, 'Tashkent Feed Co', 1200, 9_600_000, daysAgo(10)));
  batchA.addFeedDelivery(new FeedDelivery(id(), batchA.id, houseA.id, 'Tashkent Feed Co', 1100, 9_020_000, daysAgo(3)));

  batchB.addFeedDelivery(new FeedDelivery(id(), batchB.id, houseB.id, 'Tashkent Feed Co', 900, 7_380_000, daysAgo(2)));

  const session1 = new SlaughterSession(id(), batchA.id, 1050, 7000, daysAgo(2));
  batchA.addSlaughterSession(session1);

  const agent = new BazaarAgent('Navoi Bazaar Agent', 26000);
  const individual = new IndividualSeller('Nurata Direct Buyer');
  const shop = new ShopCustomer('Farm-gate Shop');

  batchA.addSaleRecord(new SaleRecord(id(), batchA.id, agent, 1180, 1150, daysAgo(2)));
  batchA.addSaleRecord(new SaleRecord(id(), batchA.id, individual, 300, null, daysAgo(2)));
  batchA.addSaleRecord(new SaleRecord(id(), batchA.id, shop, 90, null, daysAgo(1)));
}

seed();

module.exports = {
  houses,
  batches,
  id,
  findHouse,
  findBatch,
  findSlaughterSession,
  login,
  getSession,
  Buyers: { BazaarAgent, IndividualSeller, ShopCustomer },
  Models: { House, Batch, MortalityRecord, FeedDelivery, SlaughterSession, SaleRecord },
};
