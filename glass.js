/* glass.js - tiny behaviour layer for glass.css (MIT, The Mishakin Group). No dependencies.
   Include with <script src="glass.js" defer></script>. Everything is opt-in through data attributes:
     data-g-theme              button toggles light/dark (stored in localStorage, wrapped in try/catch)
     data-g-accent="teal"      button sets <html data-accent>
     .g-seg / .g-tabs buttons  click sets aria-selected on the clicked one, fires "g:select" on the group
     data-g-open="#dialogId"   opens a <dialog class="g-sheet">; data-g-close closes it; backdrop click closes
     .g-refract                Chromium only: adds an SVG lens (edge refraction) behind that glass element
   API: GlassKit.toast(text, {icon, ms}), GlassKit.chartDefaults(Chart) -> palette, GlassKit.setPilotLevel(0..1),
        GlassKit.demoPilot(orbButton, panel) (fake states for galleries; the real voice kit drives data-state) */
(function () {
  "use strict";
  var root = document.documentElement;
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  };

  /* theme: explicit attribute always set, so accent presets resolve the same in OS-dark mode */
  var params = new URLSearchParams(location.search);
  var theme = params.get("theme") || store.get("g-theme") ||
    (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  root.classList.add("g-no-transition");            /* no colour animation on first paint */
  root.setAttribute("data-theme", theme);
  requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.remove("g-no-transition"); }); });
  var accent = params.get("accent") || store.get("g-accent");
  if (accent) root.setAttribute("data-accent", accent);
  if (params.get("rt") === "1") root.classList.add("g-reduce-transparency");

  function setTheme(t) { root.setAttribute("data-theme", t); store.set("g-theme", t); document.dispatchEvent(new CustomEvent("g:theme", { detail: t })); }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-g-theme]");
    if (t) { setTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark"); return; }
    var a = e.target.closest("[data-g-accent]");
    if (a) { root.setAttribute("data-accent", a.getAttribute("data-g-accent")); store.set("g-accent", a.getAttribute("data-g-accent")); }
    var s = e.target.closest(".g-seg > button, .g-tabs > button");
    if (s) {
      Array.prototype.forEach.call(s.parentElement.children, function (b) { if (b.tagName === "BUTTON") b.setAttribute("aria-selected", b === s ? "true" : "false"); });
      s.parentElement.dispatchEvent(new CustomEvent("g:select", { detail: s.value || s.textContent.trim(), bubbles: true }));
      return;
    }
    var o = e.target.closest("[data-g-open]");
    if (o) { var d = document.querySelector(o.getAttribute("data-g-open")); if (d && d.showModal) { e.preventDefault(); d.showModal(); } return; }
    var c = e.target.closest("[data-g-close]");
    if (c) { var dl = c.closest("dialog"); if (dl) dl.close(); return; }
    if (e.target.tagName === "DIALOG" && e.target.classList.contains("g-sheet")) e.target.close(); /* backdrop click */
  });

  /* toast */
  function toast(text, opts) {
    opts = opts || {};
    var host = document.querySelector(".g-toast-host");
    if (!host) { host = document.createElement("div"); host.className = "g-toast-host"; host.setAttribute("role", "status"); host.setAttribute("aria-live", "polite"); document.body.appendChild(host); }
    var el = document.createElement("div");
    el.className = "g-toast";
    el.innerHTML = (opts.icon ? '<span class="g-tile g-tile--sm ' + (opts.tone ? "g-tile--" + opts.tone : "") + '"><svg class="g-i"><use href="' + (opts.sprite || "icons.svg") + "#" + opts.icon + '"/></svg></span>' : "") + "<span></span>";
    el.lastChild.textContent = text;
    host.appendChild(el);
    setTimeout(function () { el.classList.add("is-leaving"); setTimeout(function () { el.remove(); }, 260); }, opts.ms || 3200);
    return el;
  }

  /* Chart.js defaults from the tokens. Call after Chart loads; call again on "g:theme". Returns the palette. */
  function chartDefaults(Chart) {
    var cs = getComputedStyle(root);
    var v = function (n) { return cs.getPropertyValue(n).trim(); };
    var d = Chart.defaults;
    d.font.family = v("--g-font"); d.font.size = 12; d.color = v("--g-text-3");
    d.borderColor = v("--g-chart-grid");
    d.elements.line.tension = 0.35; d.elements.line.borderWidth = 2.25;
    d.elements.point.radius = 0; d.elements.point.hoverRadius = 4;
    d.elements.bar.borderRadius = 6; d.elements.bar.borderSkipped = false;
    d.plugins.legend.labels.usePointStyle = true; d.plugins.legend.labels.boxWidth = 8; d.plugins.legend.labels.boxHeight = 8;
    var tt = d.plugins.tooltip;
    tt.backgroundColor = v("--g-surface"); tt.titleColor = v("--g-text"); tt.bodyColor = v("--g-text-2");
    tt.borderColor = v("--g-line-2"); tt.borderWidth = 1; tt.padding = 10; tt.cornerRadius = 12; tt.boxPadding = 4;
    d.scale.grid.color = v("--g-chart-grid"); d.scale.border.display = false; d.scale.ticks.color = v("--g-chart-axis");
    return [1, 2, 3, 4, 5, 6].map(function (i) { return v("--g-chart-" + i); });
  }

  /* voice level for the orb + wave (0..1). The voice-pilot kit can call this or set --pilot-level itself. */
  function setPilotLevel(x) { root.style.setProperty("--pilot-level", Math.max(0, Math.min(1, x)).toFixed(3)); }

  /* demo-only state machine so galleries show every orb state without a microphone */
  function demoPilot(orb, panel) {
    if (!orb) return;
    var raf = 0, t0 = 0, timers = [];
    var status = panel && panel.querySelector("[data-pilot-status]");
    function clearTimers() { timers.forEach(clearTimeout); timers = []; }   /* a closed panel must not keep advancing the orb */
    function state(s) {
      orb.setAttribute("data-state", s);
      if (panel) panel.setAttribute("data-state", s);
      if (status) status.textContent = { idle: "Tap to ask", listening: "Listening", thinking: "Thinking", speaking: "Answering" }[s] || s;
    }
    function wobble(ts) { if (!t0) t0 = ts; var k = (ts - t0) / 1000; setPilotLevel(0.35 + 0.3 * Math.sin(k * 7) * Math.sin(k * 2.3) + 0.2 * Math.random()); raf = requestAnimationFrame(wobble); }
    orb.addEventListener("click", function () {
      var open = panel && !panel.hidden;
      clearTimers(); cancelAnimationFrame(raf);
      if (open) { panel.hidden = true; setPilotLevel(0); state("idle"); return; }
      if (panel) panel.hidden = false;
      state("listening"); t0 = 0; raf = requestAnimationFrame(wobble);
      timers.push(setTimeout(function () { state("thinking"); }, 2400));
      timers.push(setTimeout(function () { state("speaking"); }, 3600));
      timers.push(setTimeout(function () { cancelAnimationFrame(raf); setPilotLevel(0); state("idle"); }, 7600));
    });
  }

  /* refraction: an SVG displacement map per element, bending the backdrop near the rounded edges.
     Chromium only (backdrop-filter: url() is ignored elsewhere, so we do not set it there at all). */
  var isChromium = !!(navigator.userAgentData && navigator.userAgentData.brands &&
    navigator.userAgentData.brands.some(function (b) { return /Chromium|Google Chrome|Microsoft Edge/.test(b.brand); }));
  var reduceT = window.matchMedia && matchMedia("(prefers-reduced-transparency: reduce)").matches;
  var lensId = 0, svgHost = null;

  function lensMap(w, h, r, bezel) {
    var c = document.createElement("canvas"); c.width = w; c.height = h;
    var ctx = c.getContext("2d"), img = ctx.createImageData(w, h), px = img.data;
    var cx = w / 2, cy = h / 2, hx = cx - r, hy = cy - r;
    for (var y = 0; y < h; y++) for (var x = 0; x < w; x++) {
      var dx = Math.abs(x + 0.5 - cx) - hx, dy = Math.abs(y + 0.5 - cy) - hy;
      var ox = Math.max(dx, 0), oy = Math.max(dy, 0);
      var dist = Math.sqrt(ox * ox + oy * oy) + Math.min(Math.max(dx, dy), 0) - r; /* signed distance, <0 inside */
      var t = -dist, nx = 0, ny = 0, m = 0;
      if (t >= 0 && t < bezel) {
        if (dx > 0 && dy > 0) { var l = Math.sqrt(ox * ox + oy * oy) || 1; nx = ox / l; ny = oy / l; }
        else if (dx > dy) { nx = 1; } else { ny = 1; }
        nx *= Math.sign(x + 0.5 - cx); ny *= Math.sign(y + 0.5 - cy);
        var s = 1 - t / bezel; m = s * s;                        /* convex profile: strongest at the rim */
      }
      var i = (y * w + x) * 4;
      px[i] = 128 + Math.round(-nx * m * 127); px[i + 1] = 128 + Math.round(-ny * m * 127); px[i + 2] = 128; px[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    return c.toDataURL();
  }

  function refract(el) {
    if (!isChromium || reduceT) return;
    var rect = el.getBoundingClientRect(), w = Math.round(rect.width), h = Math.round(rect.height);
    if (w < 8 || h < 8 || w * h > 1600000) return;
    var cs = getComputedStyle(el);
    var r = Math.min(parseFloat(cs.borderTopLeftRadius) || 0, h / 2, w / 2);
    var bezel = Math.min(parseFloat(el.getAttribute("data-g-bezel")) || Math.max(10, Math.min(28, h * 0.32)), h / 2);
    var scale = parseFloat(el.getAttribute("data-g-strength")) || 34;
    if (!svgHost) {
      svgHost = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svgHost.setAttribute("aria-hidden", "true"); svgHost.style.cssText = "position:absolute;width:0;height:0;overflow:hidden";
      document.body.appendChild(svgHost);
    }
    var id = el.getAttribute("data-g-lens") || ("g-lens-" + (++lensId));
    el.setAttribute("data-g-lens", id);
    var old = document.getElementById(id); if (old) old.remove();
    var f = document.createElementNS("http://www.w3.org/2000/svg", "filter");
    f.setAttribute("id", id); f.setAttribute("x", "0"); f.setAttribute("y", "0"); f.setAttribute("width", w); f.setAttribute("height", h);
    f.setAttribute("filterUnits", "userSpaceOnUse"); f.setAttribute("color-interpolation-filters", "sRGB");
    var blur = parseFloat(cs.getPropertyValue("--_blur")) || 22;
    /* blur, then bend, then saturate, all inside one SVG filter (CSS blur() after url() is unreliable) */
    f.innerHTML = '<feGaussianBlur in="SourceGraphic" stdDeviation="' + blur + '" edgeMode="duplicate" result="blur"/>' +
      '<feImage href="' + lensMap(w, h, r, bezel) + '" x="0" y="0" width="' + w + '" height="' + h + '" result="map" preserveAspectRatio="none"/>' +
      '<feDisplacementMap in="blur" in2="map" scale="' + scale + '" xChannelSelector="R" yChannelSelector="G" result="bent"/>' +
      '<feColorMatrix in="bent" type="saturate" values="1.8"/>';
    svgHost.appendChild(f);
    el.style.backdropFilter = "url(#" + id + ")";
  }

  function refractAll() { document.querySelectorAll(".g-refract").forEach(refract); }
  if (isChromium && !reduceT) {
    root.classList.add("g-refract-on");
    var rt = 0;
    window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(refractAll, 200); });
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", refractAll); else refractAll();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(refractAll);
  }

  window.GlassKit = { toast: toast, chartDefaults: chartDefaults, setPilotLevel: setPilotLevel, demoPilot: demoPilot, refract: refract, setTheme: setTheme, isChromium: isChromium };
})();
