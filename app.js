(function () {
  const grid = document.getElementById('wf-grid');
  const countEl = document.getElementById('wf-count');
  const searchEl = document.getElementById('wf-search');
  const modal = document.getElementById('wf-modal');
  const modalBody = document.getElementById('wf-modal-body');
  const modalClose = document.getElementById('wf-modal-close');
  const toolsEl = document.getElementById('wf-tools');
  const featuredEl = document.getElementById('featured-tools');

  if (!grid) return;

  let catalog = null;
  let activeCategory = 'all';
  let activeType = 'all';
  let activeSource = 'all';
  let activeTool = 'all';
  let searchQuery = '';

  const CATEGORY_CLASS = {
    Outbound: 'cat-outbound',
    Content: 'cat-content',
    ABM: 'cat-abm',
    RevOps: 'cat-revops',
  };

  const GRADIENT = {
    Outbound: 'linear-gradient(135deg, #000000 0%, #1a1a1a 100%)',
    Content:  'linear-gradient(135deg, #FF3000 0%, #cc2000 100%)',
    ABM:      'linear-gradient(135deg, #1a1a1a 0%, #444444 100%)',
    RevOps:   'linear-gradient(135deg, #e0e0e0 0%, #c0c0c0 100%)',
  };

  function favicon(domain) {
    return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;
  }

  function toolDomain(name) {
    const map = {
      Clay: 'clay.com', Smartlead: 'smartlead.ai', HeyReach: 'heyreach.io',
      n8n: 'n8n.io', Apollo: 'apollo.io', HubSpot: 'hubspot.com',
      Instantly: 'instantly.ai', Findymail: 'findymail.com', Claude: 'anthropic.com',
      Prospeo: 'prospeo.io', Python: 'python.org', Slack: 'slack.com',
      MiniMax: 'minimax.io', Playwright: 'playwright.dev', JavaScript: 'javascript.info',
      LinkedIn: 'linkedin.com', OpenAI: 'openai.com', YAML: 'yaml.org',
      G2: 'g2.com', Apify: 'apify.com', RB2B: 'rb2b.com', Warmly: 'warmly.ai',
      BuiltWith: 'builtwith.com', Crunchbase: 'crunchbase.com', Trigify: 'trigify.io',
      PhantomBuster: 'phantombuster.com', Salesforce: 'salesforce.com', Outreach: 'outreach.io',
      Amplitude: 'amplitude.com', Beehiiv: 'beehiiv.com', Notion: 'notion.so',
      Webflow: 'webflow.com', Jungler: 'jungler.ai', Freckle: 'freckle.io',
      ChatGPT: 'openai.com', Chilipiper: 'chilipiper.com', LeadMagic: 'leadmagic.io',
      Deepline: 'deepline.io', CSV: 'python.org', 'Sales Navigator': 'linkedin.com',
      OutboundSync: 'outboundsync.com',
    };
    return map[name] || `${name.toLowerCase().replace(/\s+/g, '')}.com`;
  }

  function sourceLabel(id) {
    if (id === 'rasul') return 'Production';
    if (id === 'coldiq') return 'ColdIQ';
    if (id === 'workflows-io') return 'workflows.io';
    return id;
  }

  function primaryCategory(wf) {
    return wf.categories[0] || 'RevOps';
  }

  function matches(wf) {
    if (activeCategory !== 'all' && !wf.categories.includes(activeCategory)) return false;
    if (activeType !== 'all' && wf.type !== activeType) return false;
    if (activeSource !== 'all' && wf.source !== activeSource) return false;
    if (activeTool !== 'all' && !wf.tools.includes(activeTool)) return false;
    if (searchQuery) {
      const hay = `${wf.title} ${wf.description} ${wf.tools.join(' ')} ${wf.categories.join(' ')}`.toLowerCase();
      if (!hay.includes(searchQuery)) return false;
    }
    return true;
  }

  function cardHtml(wf) {
    const cat = primaryCategory(wf);
    const grad = GRADIENT[cat] || GRADIENT.RevOps;
    const tools = wf.tools.slice(0, 4);
    const extra = wf.tools.length - tools.length;
    const cats = wf.categories.map(c => `<span class="wf-cat ${CATEGORY_CLASS[c] || ''}">${c}</span>`).join('');
    const toolIcons = tools.map(t =>
      `<img src="${favicon(toolDomain(t))}" alt="" width="20" height="20" loading="lazy" title="${t}" />`
    ).join('');
    const extraTools = extra > 0 ? `<span class="wf-tool-more">+${extra}</span>` : '';

    return `
      <article class="wf-card" data-id="${wf.id}" tabindex="0" role="button" aria-label="Open ${wf.title}">
        <div class="wf-cover" style="background:${grad}"></div>
        <div class="wf-card-body">
          <div class="wf-tools-row">${toolIcons}${extraTools}</div>
          <h3 class="wf-title">${wf.title}</h3>
          <p class="wf-desc">${wf.description}</p>
          <div class="wf-meta">
            <div class="wf-cats">${cats}</div>
            <span class="wf-source wf-source-${wf.source}">${sourceLabel(wf.source)}</span>
          </div>
          <div class="wf-author">${wf.author}</div>
        </div>
      </article>`;
  }

  function render() {
    const filtered = catalog.workflows.filter(matches);
    countEl.textContent = `${filtered.length} workflow${filtered.length === 1 ? '' : 's'}`;
    grid.innerHTML = filtered.map(cardHtml).join('');
    grid.querySelectorAll('.wf-card').forEach(el => {
      el.addEventListener('click', () => openModal(el.dataset.id));
      el.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openModal(el.dataset.id); }
      });
    });
  }

  function openModal(id) {
    const wf = catalog.workflows.find(w => w.id === id);
    if (!wf) return;
    const cat = primaryCategory(wf);
    const steps = (wf.steps || []).map((s, i) => `<li><span>${i + 1}</span>${s}</li>`).join('');
    const metrics = wf.metrics ? Object.entries(wf.metrics).map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('') : '';
    const links = [];
    if (wf.repo) links.push(`<a href="${wf.repo}" class="btn-primary" target="_blank" rel="noopener">View repo</a>`);
    if (wf.schema) links.push(`<a href="${wf.schema}" class="btn-primary">Framework schema (JSON)</a>`);
    if (wf.engine_path) links.push(`<a href="${wf.engine_path}" class="btn-primary">Context Engine motion</a>`);
    if (wf.engine_id) links.push(`<a href="#engine" class="btn-secondary" onclick="document.getElementById('engine-motion').value='${wf.engine_id}';document.getElementById('engine-route-btn')?.click();">Route in engine</a>`);
    if (wf.n8n) links.push(`<a href="${wf.n8n}" class="btn-secondary" target="_blank" rel="noopener">Import n8n</a>`);
    if (wf.external) links.push(`<a href="${wf.external}" class="btn-secondary" target="_blank" rel="noopener">Original on workflows.io</a>`);
    if (wf.source_url) links.push(`<a href="${wf.source_url}" class="btn-secondary" target="_blank" rel="noopener">ColdIQ skill</a>`);
    if (wf.pdf) links.push(`<a href="${wf.pdf}" class="btn-secondary" target="_blank" rel="noopener">Case study PDF</a>`);

    modalBody.innerHTML = `
      <div class="wf-modal-cover" style="background:${GRADIENT[cat] || GRADIENT.RevOps}"></div>
      <div class="wf-modal-content">
        <div class="wf-modal-tags">
          ${wf.categories.map(c => `<span class="wf-cat ${CATEGORY_CLASS[c] || ''}">${c}</span>`).join('')}
          <span class="wf-type">${wf.type}</span>
          <span class="wf-source wf-source-${wf.source}">${sourceLabel(wf.source)}</span>
        </div>
        <h2 id="wf-modal-title">${wf.title}</h2>
        <p class="wf-modal-desc">${wf.description}</p>
        ${metrics ? `<dl class="wf-modal-metrics">${metrics}</dl>` : ''}
        ${steps ? `<h3>Steps</h3><ol class="wf-steps">${steps}</ol>` : ''}
        <h3>Tools</h3>
        <div class="wf-modal-tools">${wf.tools.map(t => `<span><img src="${favicon(toolDomain(t))}" alt="" width="16" height="16" />${t}</span>`).join('')}</div>
        <div class="wf-modal-actions">${links.join('')}</div>
        <p class="wf-modal-credit">By ${wf.author}${wf.inspired_by ? ` · Inspired by <a href="${wf.inspired_by}" target="_blank" rel="noopener">workflows.io</a>` : ''}${wf.source === 'coldiq' ? ' · <a href="https://github.com/sachacoldiq/ColdIQ-s-GTM-Skills" target="_blank" rel="noopener">ColdIQ GTM Skills</a>' : ''}${wf.source === 'workflows-io' ? ' · <a href="https://www.workflows.io/workflows" target="_blank" rel="noopener">workflows.io</a>' : ''}${wf.source === 'rasul' && wf.type === 'engine' ? ' · Rasul-owned implementation' : ''}</p>
      </div>`;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    modalClose.focus();
  }

  function closeModal() {
    modal.hidden = true;
    document.body.style.overflow = '';
  }

  function bindFilters() {
    document.querySelectorAll('[data-filter-cat]').forEach(btn => {
      btn.addEventListener('click', () => {
        activeCategory = btn.dataset.filterCat;
        document.querySelectorAll('[data-filter-cat]').forEach(b => b.classList.toggle('active', b === btn));
        render();
      });
    });
    document.querySelectorAll('[data-filter-type]').forEach(btn => {
      btn.addEventListener('click', () => {
        activeType = btn.dataset.filterType;
        document.querySelectorAll('[data-filter-type]').forEach(b => b.classList.toggle('active', b === btn));
        render();
      });
    });
    document.querySelectorAll('[data-filter-source]').forEach(btn => {
      btn.addEventListener('click', () => {
        activeSource = btn.dataset.filterSource;
        document.querySelectorAll('[data-filter-source]').forEach(b => b.classList.toggle('active', b === btn));
        render();
      });
    });
    if (searchEl) {
      searchEl.addEventListener('input', () => {
        searchQuery = searchEl.value.trim().toLowerCase();
        render();
      });
    }
  }

  function renderFeatured() {
    if (!featuredEl || !catalog) return;
    featuredEl.innerHTML = catalog.featured_tools.map(t => `
      <button type="button" class="featured-tool" data-tool="${t.name}" title="Filter by ${t.name}">
        <img src="${favicon(t.domain)}" alt="" width="24" height="24" loading="lazy" />
        <span>${t.name}</span>
      </button>`).join('');
    featuredEl.querySelectorAll('.featured-tool').forEach(btn => {
      btn.addEventListener('click', () => {
        const name = btn.dataset.tool;
        activeTool = activeTool === name ? 'all' : name;
        featuredEl.querySelectorAll('.featured-tool').forEach(b =>
          b.classList.toggle('active', b.dataset.tool === activeTool)
        );
        render();
      });
    });
  }

  function renderToolFilter() {
    if (!toolsEl || !catalog) return;
    const tools = [...new Set(catalog.workflows.flatMap(w => w.tools))].sort();
    toolsEl.innerHTML = tools.map(t =>
      `<button type="button" class="tool-chip" data-tool-filter="${t}">${t}</button>`
    ).join('');
    toolsEl.querySelectorAll('.tool-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        activeTool = activeTool === btn.dataset.toolFilter ? 'all' : btn.dataset.toolFilter;
        toolsEl.querySelectorAll('.tool-chip').forEach(b =>
          b.classList.toggle('active', b.dataset.toolFilter === activeTool)
        );
        featuredEl?.querySelectorAll('.featured-tool').forEach(b =>
          b.classList.toggle('active', b.dataset.tool === activeTool)
        );
        render();
      });
    });
  }

  modalClose?.addEventListener('click', closeModal);
  modal?.addEventListener('click', e => { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !modal.hidden) closeModal(); });

  fetch('data/workflows.json')
    .then(r => r.json())
    .then(data => {
      catalog = data;
      bindFilters();
      renderFeatured();
      renderToolFilter();
      render();
    })
    .catch(() => {
      grid.innerHTML = '<p class="wf-error">Could not load workflows catalog.</p>';
    });
})();