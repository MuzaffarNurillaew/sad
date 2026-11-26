(function () {
  'use strict';

  let token = localStorage.getItem('farmtrack_token');
  let role = localStorage.getItem('farmtrack_role');
  let name = localStorage.getItem('farmtrack_name');
  let currentBatchId = null;
  let lastState = null;

  const el = (id) => document.getElementById(id);

  function show(viewId) {
    ['loginView', 'dashboardView', 'batchView'].forEach((v) => el(v).classList.toggle('hidden', v !== viewId));
  }

  async function api(path, opts = {}) {
    const headers = Object.assign({ 'Content-Type': 'application/json' }, opts.headers || {});
    if (token) headers['X-Session-Token'] = token;
    const res = await fetch(path, Object.assign({}, opts, { headers }));
    const body = await res.json().catch(() => ({}));
    return { status: res.status, body };
  }

  function uzs(n) {
    if (n === undefined || n === null) return '—';
    return Number(n).toLocaleString('en-US') + ' UZS';
  }

  function updateWhoAmI() {
    if (role) {
      el('whoami').classList.remove('hidden');
      el('whoamiText').textContent = `${name} (${role})`;
    } else {
      el('whoami').classList.add('hidden');
    }
  }

  async function refreshState() {
    const { status, body } = await api('/api/state');
    if (status !== 200) {
      logout();
      return;
    }
    lastState = body;
    renderDashboard();
    if (currentBatchId) renderBatch(currentBatchId);
  }

  function renderDashboard() {
    const container = el('housesList');
    container.innerHTML = '';
    lastState.houses.forEach((house) => {
      const card = document.createElement('div');
      card.className = 'house-card';
      const batches = lastState.batches.filter((b) => b.houseId === house.id);
      card.innerHTML = `<strong>${house.name}</strong> <span class="hint">(${house.capacityMin}-${house.capacityMax} birds)</span>`;
      batches.forEach((b) => {
        const row = document.createElement('div');
        row.className = 'batch-row';
        row.innerHTML = `<span>Batch #${b.id} — started ${b.startDate} — ${b.mortalityCount} deaths logged</span>`;
        const btn = document.createElement('button');
        btn.textContent = 'Open';
        btn.style.width = 'auto';
        btn.onclick = () => openBatch(b.id);
        row.appendChild(btn);
        card.appendChild(row);
      });
      container.appendChild(card);
    });
    document.querySelectorAll('#addHouseForm').forEach((f) => f.classList.toggle('hidden', role !== 'director'));
  }

  function openBatch(batchId) {
    currentBatchId = batchId;
    show('batchView');
    renderBatch(batchId);
  }

  function renderBatch(batchId) {
    const batch = lastState.batches.find((b) => b.id === batchId);
    if (!batch) return;
    el('batchTitle').textContent = `${batch.houseName} — Batch #${batch.id}`;

    document.querySelectorAll('.director-only').forEach((f) => f.classList.toggle('hidden', role !== 'director'));

    if (role === 'director') {
      el('profitPanel').classList.remove('hidden');
      el('profitDenied').classList.add('hidden');
      el('profitPanel').innerHTML = `
        <h3>Per-batch profit (FR-03, NFR-03)</h3>
        <div>Revenue: ${uzs(batch.totalRevenueUzs)}</div>
        <div>Feed cost: ${uzs(batch.totalFeedCostUzs)}</div>
        <div>Crew payment: ${uzs(batch.totalCrewPaymentUzs)}</div>
        <div><strong>Profit: ${uzs(batch.profitUzs)}</strong></div>`;
    } else {
      el('profitPanel').classList.add('hidden');
      el('profitDenied').classList.remove('hidden');
    }

    el('mortalityList').innerHTML = batch.mortalityRecords
      .map(
        (r) =>
          `<div class="record">${new Date(r.timestamp).toLocaleString()} — ${r.workerName}${r.note ? ' — ' + r.note : ''}
          ${r.flaggedDuplicateOfId ? '<div class="flag">possible duplicate of record #' + r.flaggedDuplicateOfId + '</div>' : ''}</div>`
      )
      .join('') || '<div class="hint">No deaths logged yet.</div>';

    el('feedList').innerHTML = batch.feedDeliveries
      .map(
        (f) =>
          `<div class="record">${f.date} — ${f.supplier} — ${f.quantityKg} kg${f.costUzs !== undefined ? ' — ' + uzs(f.costUzs) : ''}</div>`
      )
      .join('') || '<div class="hint">No feed deliveries yet.</div>';

    el('slaughterList').innerHTML = batch.slaughterSessions
      .map((s) => {
        const confirmBtn =
          role === 'director' && s.confirmedHeadcount == null
            ? `<br><button type="button" data-session="${s.id}" class="confirmBtn" style="width:auto;margin-top:4px;">Confirm/correct count</button>`
            : '';
        return `<div class="record">${s.date} — crew reported ${s.crewReportedHeadcount}${
          s.confirmedHeadcount != null ? `, confirmed ${s.confirmedHeadcount}` : ''
        }${s.totalPaymentUzs !== undefined ? ' — payment ' + uzs(s.totalPaymentUzs) : ''}${confirmBtn}</div>`;
      })
      .join('') || '<div class="hint">No slaughter sessions yet.</div>';

    document.querySelectorAll('.confirmBtn').forEach((btn) => {
      btn.onclick = async () => {
        const count = prompt('Confirmed headcount:');
        if (count === null) return;
        const note = prompt('Correction note (optional):') || undefined;
        await api(`/api/slaughter/${btn.dataset.session}/confirm`, {
          method: 'POST',
          body: JSON.stringify({ confirmedHeadcount: Number(count), note }),
        });
        refreshState();
      };
    });

    el('saleList').innerHTML = batch.saleRecords
      .map((s) => {
        const cls = s.crossCheckStatus === 'mismatch_flagged' ? 'mismatch' : s.crossCheckStatus === 'match' ? 'match' : '';
        return `<div class="record">${s.date} — ${s.buyerName} — ${s.kg} kg${s.revenueUzs !== undefined ? ' — ' + uzs(s.revenueUzs) : ''}
          ${s.trustedRepKg != null ? `<div class="${cls}">cross-check vs trusted rep (${s.trustedRepKg} kg): ${s.crossCheckStatus.replace('_', ' ')}</div>` : ''}</div>`;
      })
      .join('') || '<div class="hint">No sales recorded yet.</div>';
  }

  function logout() {
    token = null;
    role = null;
    name = null;
    currentBatchId = null;
    localStorage.removeItem('farmtrack_token');
    localStorage.removeItem('farmtrack_role');
    localStorage.removeItem('farmtrack_name');
    updateWhoAmI();
    show('loginView');
  }

  el('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const n = el('loginName').value.trim();
    const r = el('loginRole').value;
    const { body } = await api('/api/login', { method: 'POST', body: JSON.stringify({ role: r, name: n }) });
    token = body.token;
    role = body.role;
    name = body.name;
    localStorage.setItem('farmtrack_token', token);
    localStorage.setItem('farmtrack_role', role);
    localStorage.setItem('farmtrack_name', name);
    updateWhoAmI();
    show('dashboardView');
    refreshState();
  });

  el('logoutBtn').addEventListener('click', logout);
  el('backBtn').addEventListener('click', () => {
    currentBatchId = null;
    show('dashboardView');
  });

  el('addHouseForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await api('/api/houses', { method: 'POST', body: JSON.stringify({ name: el('newHouseName').value }) });
    el('newHouseName').value = '';
    refreshState();
  });

  el('mortalityForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await api(`/api/batches/${currentBatchId}/mortality`, { method: 'POST', body: JSON.stringify({ note: el('mortalityNote').value }) });
    el('mortalityNote').value = '';
    refreshState();
  });

  el('feedForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await api(`/api/batches/${currentBatchId}/feed`, {
      method: 'POST',
      body: JSON.stringify({
        supplier: el('feedSupplier').value,
        quantityKg: el('feedQty').value,
        costUzs: el('feedCost').value,
        date: new Date().toISOString().slice(0, 10),
      }),
    });
    e.target.reset();
    refreshState();
  });

  el('slaughterForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await api(`/api/batches/${currentBatchId}/slaughter`, {
      method: 'POST',
      body: JSON.stringify({
        crewReportedHeadcount: el('slaughterHeadcount').value,
        paymentPerHeadUzs: el('slaughterPay').value,
        date: new Date().toISOString().slice(0, 10),
      }),
    });
    e.target.reset();
    refreshState();
  });

  el('saleForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await api(`/api/batches/${currentBatchId}/sale`, {
      method: 'POST',
      body: JSON.stringify({
        buyerType: el('saleBuyerType').value,
        kg: el('saleKg').value,
        trustedRepKg: el('saleTrustedKg').value || null,
        dailyRateUzs: el('saleRate').value || null,
        date: new Date().toISOString().slice(0, 10),
      }),
    });
    e.target.reset();
    refreshState();
  });

  // boot
  updateWhoAmI();
  if (token) {
    show('dashboardView');
    refreshState();
  } else {
    show('loginView');
  }
})();
