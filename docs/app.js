const $ = (selector) => document.querySelector(selector);
let catalog = { marketplace: {}, plugins: [] };
let category = 'all';

function render() {
  const query = $('#search').value.trim().toLowerCase();
  const visible = catalog.plugins.filter((plugin) => (category === 'all' || plugin.category === category) && `${plugin.name} ${plugin.displayName} ${plugin.description} ${plugin.capabilities.join(' ')}`.toLowerCase().includes(query));
  $('#result-count').textContent = visible.length;
  $('#empty-state').hidden = visible.length > 0;
  $('#plugin-grid').innerHTML = visible.map((plugin) => `<article class="plugin-card"><div class="card-top"><div class="plugin-icon">${plugin.icon || '✦'}</div><span class="badge">${plugin.category}</span></div><h3>${plugin.displayName || plugin.name}</h3><p>${plugin.description}</p><div class="platform-install-links"><button class="install-link claude-link" type="button" data-install-claude="${plugin.name}">Copiar para Claude Code</button><button class="install-link codex-link" type="button" data-install-codex="${plugin.name}">Copiar para Codex</button><span class="install-status" role="status" aria-live="polite"></span></div><div class="card-footer"><span class="version">v${plugin.version} · ${plugin.capabilities.join(' · ')}</span><a class="card-link" href="${plugin.source}" target="_blank" rel="noreferrer">GitHub ↗</a></div></article>`).join('');
  document.querySelectorAll('[data-install-claude]').forEach((button) => button.addEventListener('click', () => copyInstallCommand(button, 'claude')));
  document.querySelectorAll('[data-install-codex]').forEach((button) => button.addEventListener('click', () => copyInstallCommand(button, 'codex')));
}

function installCommand(pluginName, platform) {
  return platform === 'claude'
    ? `claude plugin marketplace add YOUR_GITHUB_USER/YOUR_REPOSITORY\nclaude plugin install ${pluginName}@YOUR_MARKETPLACE_NAME-claude`
    : `codex plugin marketplace add YOUR_GITHUB_USER/YOUR_REPOSITORY\ncodex plugin install ${pluginName}`;
}

async function copyInstallCommand(button, platform) {
  const command = installCommand(button.dataset[platform === 'claude' ? 'installClaude' : 'installCodex'], platform);
  const status = button.parentElement.querySelector('.install-status');
  try { await navigator.clipboard.writeText(command); status.textContent = 'Comandos copiados'; } catch { status.textContent = command; }
}

function setup() {
  const { marketplace } = catalog;
  document.title = `${marketplace.displayName || marketplace.name} | Claude Code + Codex`;
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
