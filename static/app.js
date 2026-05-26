let allDestinations = [];

async function fetchDestinations() {
  try {
    const res = await fetch('/destinations');
    allDestinations = await res.json();
    renderCards(allDestinations);
    updateStats(allDestinations);
  } catch {
    showToast('Failed to load', 'error');
  }
}

function renderCards(destinations) {
  const grid = document.getElementById('cards-grid');
  const empty = document.getElementById('empty-state');

  if (destinations.length === 0) {
    grid.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }

  empty.classList.add('hidden');
  grid.innerHTML = destinations.map(d => `
    <div class="card" id="card-${d.id}">
      <div class="card-body">
        <div class="card-destination">${esc(d.destination)}</div>
        <div class="card-country">${esc(d.country)}</div>
      </div>
      <div class="card-rating">
        <span class="stars">${stars(d.rating)}</span>
        <span class="rating-num">${d.rating.toFixed(1)}</span>
      </div>
      <div class="card-actions">
        <button class="btn-edit" onclick="openEditModal(${d.id})">Edit</button>
        <button class="btn-delete" onclick="deleteDestination(${d.id})">Delete</button>
      </div>
    </div>
  `).join('');
}

function updateStats(destinations) {
  document.getElementById('total-count').textContent = destinations.length;

  if (destinations.length === 0) {
    document.getElementById('avg-rating').textContent = '—';
    document.getElementById('top-country').textContent = '—';
    return;
  }

  const avg = destinations.reduce((s, d) => s + d.rating, 0) / destinations.length;
  document.getElementById('avg-rating').textContent = avg.toFixed(1);

  const counts = {};
  destinations.forEach(d => counts[d.country] = (counts[d.country] || 0) + 1);
  const top = Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
  document.getElementById('top-country').textContent = top.length > 10 ? top.slice(0, 9) + '…' : top;
}

function stars(rating) {
  const full = Math.floor(rating);
  const half = rating - full >= 0.5 ? 1 : 0;
  return '★'.repeat(full) + (half ? '½' : '') + '☆'.repeat(5 - full - half);
}

function esc(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function filterCards() {
  const q = document.getElementById('search-input').value.toLowerCase();
  renderCards(allDestinations.filter(d =>
    d.destination.toLowerCase().includes(q) || d.country.toLowerCase().includes(q)
  ));
}

function openModal() {
  document.getElementById('modal-title').textContent = 'Add Destination';
  document.getElementById('submit-btn').textContent = 'Add';
  document.getElementById('edit-id').value = '';
  document.getElementById('destination-form').reset();
  document.getElementById('modal-overlay').classList.remove('hidden');
}

function openEditModal(id) {
  const d = allDestinations.find(x => x.id === id);
  if (!d) return;
  document.getElementById('modal-title').textContent = 'Edit Destination';
  document.getElementById('submit-btn').textContent = 'Save';
  document.getElementById('edit-id').value = id;
  document.getElementById('input-destination').value = d.destination;
  document.getElementById('input-country').value = d.country;
  document.getElementById('input-rating').value = d.rating;
  document.getElementById('modal-overlay').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
}

async function handleSubmit(e) {
  e.preventDefault();
  const id = document.getElementById('edit-id').value;
  const payload = {
    destination: document.getElementById('input-destination').value.trim(),
    country: document.getElementById('input-country').value.trim(),
    rating: parseFloat(document.getElementById('input-rating').value),
  };

  try {
    await fetch(id ? `/destinations/${id}` : '/destinations', {
      method: id ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    closeModal();
    fetchDestinations();
    showToast(id ? 'Updated' : 'Added', 'success');
  } catch {
    showToast('Something went wrong', 'error');
  }
}

async function deleteDestination(id) {
  if (!confirm('Delete this destination?')) return;
  try {
    await fetch(`/destinations/${id}`, { method: 'DELETE' });
    fetchDestinations();
    showToast('Deleted', 'success');
  } catch {
    showToast('Failed to delete', 'error');
  }
}

let toastTimer;
function showToast(msg, type = 'success') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = `toast ${type}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.add('hidden'), 2800);
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

fetchDestinations();
