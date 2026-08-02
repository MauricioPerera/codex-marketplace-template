const $ = (selector) => document.querySelector(selector);
let catalog = { marketplace: {}, plugins: [] };
let category = 'all';

function render() {
  const query = $('#search').value.trim().toLowerCase();
  const visible = catalog.plugins.filter((plugin) => (category === 'all' || plugin.category === category) && `${plugin.name} ${plugin.displayName} ${plugin.description} ${plugin.capabilities.join(' ')}`.toLowerCase().includes(query));
  $('#result-count').textContent = visible.length;
  $('#empty-state').hidden = visible.length > 0;
  $('#plugin-grid').innerHTML = visible.map((plugin) => `<article class="plugin-card"><div class="card-top"><div class="plugin-icon">${plugin.icon || '✦'}</div><span class="badge">${plugin.category}</span></div><h3>${plugin.displayName || plugin.name}</h3><p>${plugin.description}</p><div class="card-footer"><span class="version">v${plugin.version} · ${plugin.capabilities.join(' · ')}</span><a class="card-link" href="${plugin.source}" target="_blank" rel="noreferrer">Ver plugin ↗</a></div></article>`).join('');
}

function setup() {
  const { marketplace } = catalog;
  document.title = `${marketplace.displayName || marketplace.name} | Codex`;
  $('#hero-description').textContent = marketplace.description;
  $('#github-link').href = marketplace.github;
  $('#footer-github').href = marketplace.github;
  $('#footer-author').textContent = marketplace.author;
  $('#footer-name').textContent = marketplace.displayName;
  const categories = [...new Set(catalog.plugins.map((plugin) => plugin.category))];
  $('.filters').innerHTML = ['all', ...categories].map((value) => `<button class="filter ${value === 'all' ? 'active' : ''}" data-category="${value}">${value === 'all' ? 'Todos' : value}</button>`).join('');
  document.querySelectorAll('.filter').forEach((button) => button.addEventListener('click', () => { $('.filter.active').classList.remove('active'); button.classList.add('active'); category = button.dataset.category; render(); }));
  $('#search').addEventListener('input', render);
  $('#copy-command').addEventListener('click', async () => { try { await navigator.clipboard.writeText($('#install-command').textContent); $('#copy-status').textContent = 'Copiado'; } catch { $('#copy-status').textContent = 'Selecciona y copia'; } });
  render();
}

fetch('catalog.json').then((response) => response.json()).then((data) => { catalog = data; setup(); }).catch(() => { $('#empty-state').hidden = false; $('#empty-state').textContent = 'No se pudo cargar el catálogo.'; });
