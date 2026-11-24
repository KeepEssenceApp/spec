// Pan / zoom for the mock canvas. No dependencies.
(function () {
  const vp = document.getElementById('vp'), world = document.getElementById('world'), zl = document.getElementById('zl');
  let s = 1, x = 0, y = 0;
  const MIN = 0.02, MAX = 3;
  function apply() {
    world.style.transform = 'translate(' + x + 'px,' + y + 'px) scale(' + s + ')';
    zl.textContent = Math.round(s * 100) + '%';
  }
  function zoomAt(cx, cy, f) {
    const ns = Math.min(MAX, Math.max(MIN, s * f));
    x = cx - (cx - x) * (ns / s); y = cy - (cy - y) * (ns / s); s = ns; apply();
  }
  function rectOf(el) {
    let l = 0, t = 0, e = el;
    while (e && e !== world) { l += e.offsetLeft; t += e.offsetTop; e = e.offsetParent; }
    return { x: l, y: t, w: el.offsetWidth, h: el.offsetHeight };
  }
  function fit(r, pad, cap) {
    const W = vp.clientWidth, H = vp.clientHeight, top = 64;
    s = Math.min((W - pad * 2) / r.w, (H - top - pad) / r.h, cap || 1);
    x = (W - r.w * s) / 2 - r.x * s;
    y = top + Math.max(0, (H - top - pad - r.h * s) / 2) - r.y * s;
    apply();
  }
  function fitAll() { fit({ x: 0, y: 0, w: world.offsetWidth, h: world.offsetHeight }, 16, 1); mark(null); }
  function fitWidth(el) {            // show a section from its top-left, as wide as the window allows
    const r = rectOf(el), W = vp.clientWidth, pad = 20;
    s = Math.min((W - pad * 2) / r.w, 1); if (W < 720) s = Math.max(s, 0.42);
    x = pad - r.x * s; y = 76 - r.y * s; apply();
  }
  function mark(id) { document.querySelectorAll('#toc button').forEach(b => b.classList.toggle('on', b.dataset.go === id)); }
  function go(id) { const el = document.getElementById('sec-' + id); if (el) { fitWidth(el); mark(id); } }

  // pointers: one finger / mouse drags, two fingers pinch
  const pts = new Map(); let last = null;
  vp.addEventListener('pointerdown', e => { vp.setPointerCapture(e.pointerId); pts.set(e.pointerId, { x: e.clientX, y: e.clientY }); vp.classList.add('drag'); last = null; });
  vp.addEventListener('pointermove', e => {
    if (!pts.has(e.pointerId)) return;
    const p = pts.get(e.pointerId), dx = e.clientX - p.x, dy = e.clientY - p.y;
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pts.size === 1) { x += dx; y += dy; apply(); }
    else if (pts.size === 2) {
      const [a, b] = [...pts.values()], d = Math.hypot(a.x - b.x, a.y - b.y), cx = (a.x + b.x) / 2, cy = (a.y + b.y) / 2;
      if (last) { x += cx - last.cx; y += cy - last.cy; zoomAt(cx, cy, d / last.d); }
      last = { d, cx, cy };
    }
  });
  const up = e => { pts.delete(e.pointerId); last = null; if (!pts.size) vp.classList.remove('drag'); };
  vp.addEventListener('pointerup', up); vp.addEventListener('pointercancel', up);
  // wheel zooms at the cursor; shift + wheel pans; a trackpad pinch arrives as ctrl + wheel
  vp.addEventListener('wheel', e => {
    e.preventDefault();
    if (e.shiftKey) { x -= e.deltaX || e.deltaY; y -= e.deltaX ? e.deltaY : 0; apply(); return; }
    zoomAt(e.clientX, e.clientY, Math.exp(-e.deltaY * (e.ctrlKey ? 0.012 : 0.0022)));
  }, { passive: false });
  vp.addEventListener('dblclick', e => { const f = e.target.closest('.frame'); if (f) fit(rectOf(f.querySelector('.dev')), 24, 1.4); });

  document.getElementById('toc').addEventListener('click', e => { const b = e.target.closest('button'); if (b) go(b.dataset.go); });
  document.getElementById('z-fit').onclick = fitAll;
  document.getElementById('z-100').onclick = () => zoomAt(vp.clientWidth / 2, vp.clientHeight / 2, 1 / s);
  document.getElementById('z-in').onclick = () => zoomAt(vp.clientWidth / 2, vp.clientHeight / 2, 1.25);
  document.getElementById('z-out').onclick = () => zoomAt(vp.clientWidth / 2, vp.clientHeight / 2, 0.8);
  addEventListener('keydown', e => { if (e.key === '0') fitAll(); if (e.key === '1') document.getElementById('z-100').click(); });
  addEventListener('resize', () => apply());
  // start: the section named in the address (#iphone), or everything
  const h = location.hash.slice(1);
  if (h && document.getElementById('sec-' + h)) go(h); else fitAll();
})();
