(function () {
  const motionSelect = document.getElementById('engine-motion');
  const signalSelect = document.getElementById('engine-signal');
  const signal2Select = document.getElementById('engine-signal-2');
  const routeBtn = document.getElementById('engine-route-btn');
  const outputEl = document.getElementById('engine-output');
  const stepsEl = document.getElementById('engine-steps');
  const diagramEl = document.getElementById('engine-diagram');

  if (!motionSelect) return;

  let engine = null;
  let skillRouter = null;
  let activeBundle = null;

  const HEAT_COLORS = {
    'red-hot': '#dc2626',
    hot: '#ea580c',
    warm: '#2563eb',
    cool: '#64748b',
    cold: '#94a3b8',
  };

  function heatLabel(tier) {
    if (!tier) return 'No signal';
    return `${tier.id.replace('-', ' ')} (${tier.min_score}+ pts)`;
  }

  function renderMotionCards() {
    const cards = document.getElementById('engine-motion-cards');
    if (!cards || !engine) return;
    cards.innerHTML = engine.motions.map(m => {
      const n = (m.layers || m.steps || []).length;
      const unit = m.layers ? 'layers' : 'steps';
      return `
      <button type="button" class="engine-motion-card" data-motion="${m.id}">
        <span class="engine-motion-num">${n} ${unit}</span>
        <h3>${m.title}</h3>
        <p>${m.description.slice(0, 120)}...</p>
        <span class="engine-motion-repo">${m.primary_repo}</span>
      </button>`;
    }).join('');
    cards.querySelectorAll('.engine-motion-card').forEach(btn => {
      btn.addEventListener('click', () => {
        motionSelect.value = btn.dataset.motion;
        routeBundle();
        cards.querySelectorAll('.engine-motion-card').forEach(b =>
          b.classList.toggle('active', b.dataset.motion === btn.dataset.motion)
        );
      });
    });
  }

  function populateSignals() {
    if (!skillRouter) return;
    const opts = Object.keys(skillRouter.signals).sort();
    [signalSelect, signal2Select].forEach(sel => {
      if (!sel) return;
      const current = sel.value;
      sel.innerHTML = '<option value="">None</option>' +
        opts.map(s => `<option value="${s}">${s.replace(/-/g, ' ')}</option>`).join('');
      if (current) sel.value = current;
    });
  }

  function scoreSignals(sigs) {
    const points = skillRouter?.signals || {};
    let score = 0;
    const contexts = [];
    sigs.forEach(sig => {
      const ctx = points[sig];
      if (ctx) {
        score += ctx.points || 0;
        contexts.push({ signal: sig, ...ctx });
      }
    });
    if (sigs.length >= 2) score += skillRouter?.compound_rules?.stack_bonus_points || 15;
    return { score, contexts };
  }

  function resolveTier(score) {
    if (!engine) return null;
    const tiers = [...engine.heat_tiers].sort((a, b) => b.min_score - a.min_score);
    return tiers.find(t => score >= t.min_score) || tiers[tiers.length - 1];
  }

  function routeBundle() {
    const motionId = motionSelect.value;
    const motion = engine.motions.find(m => m.id === motionId);
    if (!motion) return;

    const sigs = [signalSelect?.value, signal2Select?.value].filter(Boolean);
    const { score, contexts } = scoreSignals(sigs);
    const tier = sigs.length ? resolveTier(score) : null;
    const copyHook = contexts[0]?.copy_hook || 'billboard';
    const stepsKey = motion.layers ? 'layers' : 'steps';
    const steps = motion[stepsKey] || [];

    activeBundle = { motion, sigs, score, contexts, tier, copyHook, steps };

    if (outputEl) {
      outputEl.innerHTML = `
        <div class="engine-result-grid">
          <div class="engine-result-item">
            <dt>Motion</dt>
            <dd>${motion.title}</dd>
          </div>
          <div class="engine-result-item">
            <dt>Primary repo</dt>
            <dd><a href="https://github.com/rasulshaikh/${motion.primary_repo}" target="_blank" rel="noopener">${motion.primary_repo}</a></dd>
          </div>
          <div class="engine-result-item">
            <dt>Score</dt>
            <dd>${sigs.length ? score : '-'}</dd>
          </div>
          <div class="engine-result-item">
            <dt>Heat tier</dt>
            <dd class="engine-heat" style="color:${tier ? HEAT_COLORS[tier.id] || 'inherit' : 'inherit'}">${heatLabel(tier)}</dd>
          </div>
          <div class="engine-result-item">
            <dt>Copy hook</dt>
            <dd>${copyHook}</dd>
          </div>
          <div class="engine-result-item">
            <dt>Signal skill</dt>
            <dd>${contexts[0]?.skill || 'multi-signal'}</dd>
          </div>
        </div>
        <div class="engine-gates">
          <span class="engine-gates-label">Gates:</span>
          ${engine.gates.map(g => `<span class="engine-gate">${g.id} (${g.threshold})</span>`).join('')}
        </div>`;
    }

    if (stepsEl) {
      stepsEl.innerHTML = steps.map(s => `
        <li>
          <span>${s.order}</span>
          <div>
            <strong>${s.name}</strong>
            <span class="engine-step-impl">${s.implementation || ''}</span>
            ${s.ref ? `<span class="engine-step-ref">${s.ref}</span>` : ''}
          </div>
        </li>`).join('');
    }

    if (diagramEl) {
      const nodes = steps.map((s, i) => {
        const isGate = s.name.toLowerCase().includes('gate') || s.implementation?.includes('scorecard');
        return `${i > 0 ? ' --> ' : ''}${s.order}["${s.name}${isGate ? ' (gate)' : ''}"]`;
      }).join('');
      diagramEl.innerHTML = `<pre class="engine-mermaid">flowchart LR\n  ${nodes}\n  ${tier ? `--> T["${tier.id} tier"]` : ''}</pre>`;
    }
  }

  routeBtn?.addEventListener('click', routeBundle);
  motionSelect?.addEventListener('change', routeBundle);
  signalSelect?.addEventListener('change', routeBundle);
  signal2Select?.addEventListener('change', routeBundle);

  Promise.all([
    fetch('context-engine/data/gtm-context-engine.json').then(r => r.json()),
    fetch('context-engine/signals/skill-router.json').then(r => r.json()),
  ])
    .then(([eng, router]) => {
      engine = eng;
      skillRouter = router;
      populateSignals();
      renderMotionCards();
      routeBundle();
    })
    .catch(() => {
      if (outputEl) outputEl.innerHTML = '<p class="wf-error">Could not load context engine.</p>';
    });
})();