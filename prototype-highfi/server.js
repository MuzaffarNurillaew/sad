'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const store = require('./store');
const { MortalityRecord, FeedDelivery, SlaughterSession, SaleRecord } = require('./models');

const PORT = process.env.PORT || 4100;
const PUBLIC_DIR = path.join(__dirname, 'public');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
};

function sendJson(res, status, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (chunk) => (data += chunk));
    req.on('end', () => {
      if (!data) return resolve({});
      try {
        resolve(JSON.parse(data));
      } catch (e) {
        reject(e);
      }
    });
    req.on('error', reject);
  });
}

function authenticate(req) {
  const token = req.headers['x-session-token'];
  if (!token) return null;
  return store.getSession(token);
}

// Shapes a batch for API output. Financial fields (feed cost, sale
// revenue/price, crew payment, profit) are only included for a director -
// enforced here, server-side, not just hidden in the UI (NFR-03). A
// worker still sees quantities/counts they themselves may have entered,
// just never the money attached to them.
function serializeBatch(batch, house, session) {
  const isDirector = session && session.role === 'director';

  const base = {
    id: batch.id,
    houseId: batch.houseId,
    houseName: house ? house.name : null,
    startDate: batch.startDate,
    status: batch.status,
    mortalityCount: batch.mortalityCount(),
    mortalityRecords: batch.mortalityRecords.map((r) => ({
      id: r.id,
      workerName: r.workerName,
      note: r.note,
      timestamp: r.timestamp,
      flaggedDuplicateOfId: r.flaggedDuplicateOfId,
    })),
    totalFeedKg: batch.totalFeedKg(),
    feedDeliveries: batch.feedDeliveries.map((f) => ({
      id: f.id,
      supplier: f.supplier,
      quantityKg: f.quantityKg,
      date: f.date,
      costUzs: isDirector ? f.costUzs : undefined,
    })),
    slaughterSessions: batch.slaughterSessions.map((s) => ({
      id: s.id,
      crewReportedHeadcount: s.crewReportedHeadcount,
      confirmedHeadcount: s.confirmedHeadcount,
      correctionNote: s.correctionNote,
      effectiveHeadcount: s.effectiveHeadcount(),
      date: s.date,
      paymentPerHeadUzs: isDirector ? s.paymentPerHeadUzs : undefined,
      totalPaymentUzs: isDirector ? s.totalPaymentUzs() : undefined,
    })),
    saleRecords: batch.saleRecords.map((s) => ({
      id: s.id,
      buyerName: s.buyer.name,
      kg: s.kg,
      trustedRepKg: s.trustedRepKg,
      crossCheckStatus: s.crossCheckStatus(),
      date: s.date,
      pricePerKg: isDirector ? s.buyer.effectivePricePerKg() : undefined,
      revenueUzs: isDirector ? s.revenueUzs() : undefined,
    })),
  };

  if (isDirector) {
    base.totalFeedCostUzs = batch.totalFeedCostUzs();
    base.totalCrewPaymentUzs = batch.totalCrewPaymentUzs();
    base.totalRevenueUzs = batch.totalRevenueUzs();
    base.profitUzs = batch.profitUzs();
  }

  return base;
}

async function handleApi(req, res, url) {
  const parts = url.pathname.split('/').filter(Boolean); // ['api', ...]

  if (req.method === 'POST' && url.pathname === '/api/login') {
    const { role, name } = await readBody(req);
    if (role !== 'director' && role !== 'worker') {
      return sendJson(res, 400, { error: 'role must be director or worker' });
    }
    const token = store.login(role, name || (role === 'director' ? 'Director' : 'Worker'));
    return sendJson(res, 200, { token, role, name: name || (role === 'director' ? 'Director' : 'Worker') });
  }

  const session = authenticate(req);
  if (!session) return sendJson(res, 401, { error: 'login required' });

  if (req.method === 'GET' && url.pathname === '/api/state') {
    const payload = {
      role: session.role,
      name: session.user.name,
      houses: store.houses.map((h) => ({ id: h.id, name: h.name, capacityMin: h.capacityMin, capacityMax: h.capacityMax })),
      batches: store.batches.map((b) => serializeBatch(b, store.findHouse(b.houseId), session)),
    };
    return sendJson(res, 200, payload);
  }

  if (req.method === 'POST' && url.pathname === '/api/houses') {
    if (session.role !== 'director') return sendJson(res, 403, { error: 'only the director can configure a new house (NFR-05)' });
    const { name, capacityMin, capacityMax } = await readBody(req);
    const house = new store.Models.House(store.id(), name, Number(capacityMin) || 5000, Number(capacityMax) || 10000);
    store.houses.push(house);
    return sendJson(res, 201, { id: house.id });
  }

  if (req.method === 'POST' && url.pathname === '/api/batches') {
    const { houseId, startDate } = await readBody(req);
    if (!store.findHouse(houseId)) return sendJson(res, 404, { error: 'house not found' });
    const batch = new store.Models.Batch(store.id(), houseId, startDate || new Date().toISOString().slice(0, 10));
    store.batches.push(batch);
    return sendJson(res, 201, { id: batch.id });
  }

  // /api/batches/:id/mortality|feed|slaughter|sale
  if (req.method === 'POST' && parts[0] === 'api' && parts[1] === 'batches' && parts[3]) {
    const batch = store.findBatch(parts[2]);
    if (!batch) return sendJson(res, 404, { error: 'batch not found' });
    const action = parts[3];
    const body = await readBody(req);

    if (action === 'mortality') {
      const record = batch.addMortality(new MortalityRecord(store.id(), batch.id, batch.houseId, session.user.name, body.note));
      return sendJson(res, 201, { id: record.id, flaggedDuplicateOfId: record.flaggedDuplicateOfId });
    }

    if (action === 'feed') {
      const delivery = batch.addFeedDelivery(
        new FeedDelivery(store.id(), batch.id, batch.houseId, body.supplier, Number(body.quantityKg), Number(body.costUzs), body.date)
      );
      return sendJson(res, 201, { id: delivery.id });
    }

    if (action === 'slaughter') {
      if (session.role !== 'director') return sendJson(res, 403, { error: 'director only' });
      const s = batch.addSlaughterSession(
        new SlaughterSession(store.id(), batch.id, Number(body.crewReportedHeadcount), Number(body.paymentPerHeadUzs), body.date)
      );
      return sendJson(res, 201, { id: s.id });
    }

    if (action === 'sale') {
      if (session.role !== 'director') return sendJson(res, 403, { error: 'director only' });
      let buyer;
      if (body.buyerType === 'bazaar') buyer = new store.Buyers.BazaarAgent(body.buyerName || 'Bazaar Agent', Number(body.dailyRateUzs));
      else if (body.buyerType === 'individual') buyer = new store.Buyers.IndividualSeller(body.buyerName || 'Individual Buyer');
      else if (body.buyerType === 'shop') buyer = new store.Buyers.ShopCustomer(body.buyerName || 'Shop');
      else return sendJson(res, 400, { error: 'invalid buyerType' });

      const sale = batch.addSaleRecord(
        new SaleRecord(store.id(), batch.id, buyer, Number(body.kg), body.trustedRepKg != null ? Number(body.trustedRepKg) : null, body.date)
      );
      return sendJson(res, 201, { id: sale.id, crossCheckStatus: sale.crossCheckStatus() });
    }

    return sendJson(res, 404, { error: 'unknown action' });
  }

  if (req.method === 'POST' && parts[0] === 'api' && parts[1] === 'slaughter' && parts[3] === 'confirm') {
    if (session.role !== 'director') return sendJson(res, 403, { error: 'director only' });
    const found = store.findSlaughterSession(parts[2]);
    if (!found) return sendJson(res, 404, { error: 'session not found' });
    const { confirmedHeadcount, note } = await readBody(req);
    found.session.confirm(Number(confirmedHeadcount), note);
    return sendJson(res, 200, { ok: true });
  }

  if (req.method === 'GET' && parts[0] === 'api' && parts[1] === 'batches' && parts[3] === 'profit') {
    if (session.role !== 'director') return sendJson(res, 403, { error: 'director only (NFR-03)' });
    const batch = store.findBatch(parts[2]);
    if (!batch) return sendJson(res, 404, { error: 'batch not found' });
    return sendJson(res, 200, {
      totalRevenueUzs: batch.totalRevenueUzs(),
      totalFeedCostUzs: batch.totalFeedCostUzs(),
      totalCrewPaymentUzs: batch.totalCrewPaymentUzs(),
      profitUzs: batch.profitUzs(),
    });
  }

  return sendJson(res, 404, { error: 'not found' });
}

function serveStatic(req, res, pathname) {
  let filePath = path.join(PUBLIC_DIR, pathname === '/' ? 'index.html' : pathname);
  if (!filePath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403);
    return res.end('forbidden');
  }
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      return res.end('not found');
    }
    const ext = path.extname(filePath);
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  if (url.pathname.startsWith('/api/')) {
    handleApi(req, res, url).catch((err) => {
      sendJson(res, 500, { error: err.message });
    });
  } else {
    serveStatic(req, res, url.pathname);
  }
});

server.listen(PORT, () => {
  console.log(`FarmTrack prototype running at http://localhost:${PORT}`);
});
