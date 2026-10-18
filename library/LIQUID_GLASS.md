# Liquid Glass on the web: reference for the glass kit

Researched 2026-10-18 for 48-hour hackathon builds (floating nav bar, bottom tab bar, voice orb, sheets). Source tags look like [S8] and map to the list at the end. "My rule" or "my computation" means it is not from a source. Anything I could not verify says "unverified".

## Summary: rules to follow without reading further

1. Glass is only for the floating navigation and control layer: bars, orb, sheets, popovers. Never for cards, lists, tables or page backgrounds. [S4][S8]
2. One layer only. No glass inside glass. On the web a nested backdrop-filter only sees its parent, not the page, so it also fails technically. [S8][S15]
3. Default to the "regular" look. Use "clear" only over photo or video, for icon-sized controls, with a dark dimming layer (Apple suggests 35 percent when the media is bright). [S4]
4. Legibility beats look. Fill alpha floors: light 0.62 and dark 0.66 for anything carrying text, 0.78 for sheets. One text colour on glass, no greys. Text-shadow is not a fix (section 3).
5. Tint only the primary action, colour the background and not the label, at most one tinted control per view. [S5][S8][S10]
6. Recipe: blur + saturate + translucent fill + 1px lit top edge + soft shadow. Bars are capsules. Nested radii are concentric (inner radius = outer radius minus the gap). [S9]
7. SVG refraction is optional, Chromium only, 1 to 3 small elements, switched on by JavaScript. Never put `url()` in the shared declaration: Safari ignores it and Firefox may drop the whole backdrop-filter. [S14][S22][S23]
8. Keep `-webkit-backdrop-filter` (Safari before 18). Write literal values inside backdrop-filter, no `var()`. [S17][S24]
9. Honour settings: `prefers-reduced-transparency`, `prefers-contrast: more`, `prefers-reduced-motion`, `forced-colors`, and `@supports not` all fall back to a near-opaque surface. Safari and Firefox do not expose reduced-transparency, so the default must already be legible.
10. Budget: at most 3 glass layers in view, small areas, blur at most 20px, never animate blur radius. Test the fixed bars on a real iPhone. [S34]

## 1. Apple's rules

**Layering.** Liquid Glass "defines a new functional layer in the UI, floating above your content" [[WWDC25 356]](https://developer.apple.com/videos/play/wwdc2025/356/). HIG: "Don't use Liquid Glass in the content layer"; use standard materials for app backgrounds; exception is transient controls such as sliders and toggles, which take on glass while pressed [[HIG Materials]](https://developer.apple.com/design/human-interface-guidelines/materials). "Use Liquid Glass effects sparingly" (same page), and [[Adopting Liquid Glass]](https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass) says to limit them to "the most important functional elements in your app" and to separate content from navigation clearly. WWDC 219: glass is "best reserved for the navigation layer that floats above the content" [S8].

**Glass on glass.** "Avoid overcrowding or layering Liquid Glass elements on top of each other" [S3]. WWDC 219: stacking "can quickly make the interface feel cluttered and confusing"; put fills, transparency and vibrancy on top of glass instead [S8]. WWDC 323: glass samples a region larger than itself and "glass can not sample other glass", so neighbouring glass elements belong in one `GlassEffectContainer` [S10]. Web translation: group tab items inside one glass surface, do not give each its own.

**Regular vs clear.** Regular "blurs and adjusts the luminosity of background content to maintain legibility" and suits anything with a lot of text (alerts, sidebars, popovers). Clear is "highly translucent", only for components over visually rich media. If the media is bright, "consider adding a dark dimming layer of 35% opacity" [S4]. WWDC 219 adds: use clear only when the element is over media, a dimming layer will not hurt the content, and the content on top is bold and bright; never mix the two variants [S8].

**Tint and colour.** Glass has no colour of its own; it takes colour from what is behind it. Apply colour sparingly, to the background of primary actions rather than symbols or text, and not to multiple controls. With colourful backgrounds prefer monochrome bars [S5]. Tint "to convey meaning and not just for visual effect" [S10].

**Optics.** Apple's launch text: the material "reflects and refracts its surroundings" and its colour "adapts between light and dark environments" [S1]; the technology overview [S2] mostly links onward to the sessions. Lensing: the material "bends, shapes, and concentrates light in real time"; objects "materialize" in and out by modulating that bending instead of fading. Small glass (nav bars, tab bars) can flip light/dark with the content behind; large glass (menus, sidebars) adapts but does not flip and looks more opaque. Larger elements get deeper shadows, stronger lensing and softer scattering. Shadow opacity rises over text and falls over a plain light background [S8]. The web cannot sample the backdrop luminance, so the kit picks light or dark by `prefers-color-scheme`, not per pixel.

**Shape.** Three kinds: fixed radius, capsule (radius = half the height) and concentric (inner radius = parent radius minus padding). On phones use a capsule with extra margin from the screen edge [S9]. Apple does not publish device corner radii in the pages I read, so pick one and nest from it.

**Scroll edge effect.** A subtle blur and fade under bars that replaces hard dividers; it "obscur[es] content that scrolls beneath" controls; one per view; only where floating UI exists; "not decorative", it does not block or darken like an overlay [S3][S9]. Web analogue: a gradient scrim under the bar (section 2).

**Bars and sheets.** Tab bar floats above content on a glass background, labels with icons, few tabs, navigation only, not actions [S7]. Modal sheets: "pair Liquid Glass with a dimming layer"; a sheet dragged upward recedes, "becoming more opaque" [S9]. Resizable sheets get a grabber [S7].

**Motion and accessibility.** Reduce Transparency makes glass "frostier" and hides more of the background; Increase Contrast makes elements mostly black or white with a contrasting border; Reduce Motion lowers effect intensity and removes elastic behaviour [S8]. HIG Accessibility: meet WCAG AA (4.5:1 up to 17pt, 3:1 for bold or large), and under Reduce Motion replace transitions with fades and avoid "animating into and out of blurs" [S6]. Label every icon [S3]. The user-facing iOS 26.1 setting is Settings > Display & Brightness > Liquid Glass with two options, Clear (default look) and Tinted (more frosted, closer to iOS 18) [S11]; the Macworld page describes it in beta 4. I did not open a source confirming the final release, though search snippets said it shipped in 26.1. I found nothing saying web content can read it: unverified. Do not confuse these two options with the developer variants regular and clear.

**Criticism, and where sources differ.** Apple says regular glass maintains legibility [S4]; it publishes no contrast numbers for glass in the pages read. NN/g (Raluca Budiu, 2025-10-10) found "the contrast between the text and the background is often too low", floating translucent controls that compete with content, and "motion for motion's sake" [S12]. Pixel Envy makes the structural point: "when something in a user interface is not entirely opaque, it is not possible to predict what will be behind it", and contrast falls as opacity falls [S13]. That is the case for the alpha floors below.

## 2. Web recipe

Layer order inside one element: backdrop-filter processes what is behind it, then the fill (`background`), the border and inset shadows (specular rim), then content. Outer `box-shadow` is not drawn under the element, so it does not fight the blur.

```css
/* glass.css core. Alpha floors come from the worst-case contrast computation in section 3. */
:root {
  --glass-fill: 255 255 255;            /* rgb triplet so alpha can vary */
  --a-thin: .45; --a-regular: .62; --a-thick: .78;
  --glass-ink: #111114;                 /* the only text colour used on glass */
  --glass-rim: rgb(255 255 255 / .60);  /* specular: lit top edge */
  --glass-hair: rgb(255 255 255 / .18);
  --glass-shadow: 0 8px 32px rgb(0 0 0 / .16);
  --page-bg: 245 245 247;               /* rgb triplet of the page background, used by .scroll-edge */
}
@media (prefers-color-scheme: dark) {
  :root { --glass-fill: 28 28 32; --a-thin: .50; --a-regular: .66; --a-thick: .78;
    --glass-ink: #fff; --glass-rim: rgb(255 255 255 / .30); --glass-hair: rgb(255 255 255 / .10);
    --glass-shadow: 0 8px 32px rgb(0 0 0 / .45); --page-bg: 12 12 14; }
}
.glass {
  --a: var(--a-regular);
  position: relative; isolation: isolate;
  border-radius: var(--r, 28px);        /* capsule: --r:999px. nested: --r:calc(outer - gap) */
  color: var(--glass-ink);
  background: rgb(var(--glass-fill) / var(--a));
  -webkit-backdrop-filter: blur(16px) saturate(160%);  /* literals on purpose, no var() */
  backdrop-filter: blur(16px) saturate(160%);
  border: 1px solid var(--glass-hair);
  box-shadow: inset 0 1px 0 var(--glass-rim), inset 0 -1px 0 rgb(0 0 0 / .06), var(--glass-shadow);
}
.glass--thin  { --a: var(--a-thin);  -webkit-backdrop-filter: blur(8px) saturate(140%);  backdrop-filter: blur(8px) saturate(140%); }
.glass--thick { --a: var(--a-thick); -webkit-backdrop-filter: blur(20px) saturate(180%); backdrop-filter: blur(20px) saturate(180%); }
.glass--tint  { background: rgb(var(--tint, 0 90 220) / .90); color: #fff; }  /* primary action only; 4.8:1 worst case */
.glass--clear { --a: .10; }            /* media only, icon-sized, needs a .dim element behind it */
.dim          { background: rgb(0 0 0 / .35); }                 /* Apple's number for bright media [S4] */
.scroll-edge  { position: fixed; inset: 0 0 auto; height: calc(var(--bar-h, 64px) + 24px); z-index: 9; pointer-events: none;
  background: linear-gradient(rgb(var(--page-bg) / .92), rgb(var(--page-bg) / 0)); }   /* sits under the bar (z-index 10) */
```

Optional gradient rim (instead of only the inset shadow): a `::before` with `inset:0; padding:1px; border-radius:inherit; background:linear-gradient(...)` and `-webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude;`. Standard `mask-composite` is Chrome 120, Firefox 53, Safari 15.4, with a note that Safari's older prefixed form uses different keywords [S17]. I did not test it; the inset shadow above is the safe default.

Component map (my rule, derived from the Apple rules above):
- Nav bar: `.glass` capsule or 22px radius, floating with 8 to 12px margin, safe-area insets, over a `.scroll-edge` scrim.
- Tab bar: one `.glass` capsule holding at most 5 items, icon plus single-word label, selected item marked by a plain translucent fill (no nested glass), padded `env(safe-area-inset-bottom)`. iOS Safari 26 draws its own floating toolbar, so check overlap on a device (unverified; seen only in a PR note [S34]).
- Voice orb: circular `.glass--thin`, 56px or more, `aria-label`, `.glass--tint` only in the active listening state. Apple has no orb-specific guidance in the pages read.
- Sheet: `.glass--thick` plus a plain `rgb(0 0 0 / .35)` scrim (no backdrop-filter on the scrim), grabber, large top radius.
- Motion: enter with transform and opacity on the glass element itself (about 200ms). Opacity on an ancestor makes that ancestor a backdrop root, so the glass no longer sees the page behind it [S15].

### SVG displacement refraction (Chromium only)

CSS filters cannot move pixels, so real refraction needs an SVG `feDisplacementMap` fed with a map image; kube.io derives the map from Snell's law, uses `feImage` plus `feDisplacementMap`, a second `feImage` for the specular rim, `color-interpolation-filters="sRGB"`, and warns that the map must match the element size and is costly to rebuild [S14]. The code below follows that pattern but is my own and was not rendered in a browser during this research. If edges look smeared outward instead of bent inward, flip the sign of `scale`. `shift_px = scale * (channel/255 - 0.5)`, so the maximum shift is `scale / 2`.

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs id="glass-defs"></defs></svg>
```
```js
// glass-refract.js (ES module). Progressive enhancement: do nothing unless this is desktop-class Chromium.
// My assumption, not verified here: navigator.userAgentData is absent in Safari and Firefox (and iOS browsers use WebKit).
const chromium = !!navigator.userAgentData?.brands?.some(b => b.brand === 'Chromium');
const ok = chromium && matchMedia('(hover:hover) and (pointer:fine)').matches &&
  !matchMedia('(prefers-reduced-transparency: reduce), (prefers-contrast: more), (forced-colors: active)').matches;
const NS = 'http://www.w3.org/2000/svg';
const set = (e, o) => (Object.entries(o).forEach(([k, v]) => e.setAttribute(k, v)), e);
let n = 0;
function mapURL(w, h, radius, bezel) {                      // red = x shift, green = y shift, 128 = neutral
  const c = Object.assign(document.createElement('canvas'), { width: w, height: h }), x = c.getContext('2d');
  const img = x.createImageData(w, h), hw = w / 2, hh = h / 2, r = Math.min(radius, hw, hh);
  for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
    const px = i + .5 - hw, py = j + .5 - hh, qx = Math.abs(px) - (hw - r), qy = Math.abs(py) - (hh - r);
    const ox = Math.max(qx, 0), oy = Math.max(qy, 0), out = Math.hypot(ox, oy);
    const depth = -(out + Math.min(Math.max(qx, qy), 0) - r);            // px inward from the rounded-rect edge
    let nx = 0, ny = 0;                                                  // outward unit normal
    if (out > 0) { nx = Math.sign(px) * ox / out; ny = Math.sign(py) * oy / out; }
    else if (qx > qy) nx = Math.sign(px); else ny = Math.sign(py);
    const m = (1 - Math.min(Math.max(depth / bezel, 0), 1)) ** 2;       // 1 at the rim, 0 once past the bezel
    const k = (j * w + i) * 4;
    img.data.set([128 - nx * m * 127, 128 - ny * m * 127, 128, 255], k); // sample from inside the element
  }
  x.putImageData(img, 0, 0); return c.toDataURL();
}
export function refract(el, { bezel = 18, scale = 36 } = {}) {
  if (!ok) return;
  const id = 'glass-refract-' + ++n;
  const f = set(document.createElementNS(NS, 'filter'), { id, x: 0, y: 0, width: '100%', height: '100%', 'color-interpolation-filters': 'sRGB' });
  const im = set(document.createElementNS(NS, 'feImage'), { x: 0, y: 0, result: 'map', preserveAspectRatio: 'none' });
  const dp = set(document.createElementNS(NS, 'feDisplacementMap'), { in: 'SourceGraphic', in2: 'map', scale, xChannelSelector: 'R', yChannelSelector: 'G' });
  f.append(im, dp); document.getElementById('glass-defs').append(f);
  new ResizeObserver(() => {                                             // the map must match the element size
    const w = el.offsetWidth, h = el.offsetHeight; if (!w || !h) return;
    const r = parseFloat(getComputedStyle(el).borderTopLeftRadius) || 0;   // px radii only (999px for a capsule is fine, % is not)
    set(im, { width: w, height: h, href: mapURL(w, h, r, bezel) });
  }).observe(el);
  el.style.setProperty('--glass-refract', `url(#${id})`); el.dataset.refract = '';
}
```
```css
/* Only Chromium ever gets data-refract, so var() inside backdrop-filter is safe here. Keep the fill alpha floors. */
.glass[data-refract] { backdrop-filter: var(--glass-refract) blur(2px) saturate(160%); }
```
Scope: use it on the orb, icon buttons or one small bar, never on sheets or text-heavy surfaces (a map rebuild per resize, and strong displacement under text hurts reading).

**Which browsers.** MDN lists `url()` as valid backdrop-filter syntax [S15], but in practice: Chromium renders it (kube.io: "only Chromium"; the WebKit and Mozilla bug threads both note that Chrome renders it; a Chrome Canary 108 repro from 2022 is the oldest version I saw, no minimum version verified) [S14][S22][S23]. Safari: no effect; WebKit bug 245510 is still NEW, with fix PRs posted 2026-07 and a trunk GPU-process crash noted 2026-09-05, nothing landed [S22]. Firefox: bug 1961378 "backdrop-filter gets ignored if it would fall back to a blob image (such like with some SVG url filters)"; Mozilla says `feDisplacementMap` and `feImage` are not GPU-accelerated in WebRender, so the effect silently fails; `feColorMatrix` does work in Firefox per the WebKit thread [S22][S23]. I did not verify whether `blur()` in the same declaration still applies in Firefox, so assume it does not. buildmvpfast reports that Firefox parses `url()` as valid, so `@supports` passes while nothing renders [S27]; I did not test Safari, but the bug shows no effect there, so assume the same. Hence the JavaScript gate. Chrome Android, WebView and Samsung Internet: unverified. A second pattern exists (DEV article, liquid-glass-react): `backdrop-filter: blur(...)` plus the SVG filter in the plain `filter` property on the same element; liquid-glass-react skips it only in Firefox by a UA check, and its README says Safari and Firefox "only partially support the effect (displacement will not be visible)" [S25][S28]. I did not render either pattern. liquid-glass-js uses WebGL 2 plus html2canvas instead, which is heavier [S26].

### Fallbacks block (put last in glass.css so it wins on equal specificity; the `@supports` pattern follows web.dev [S30])

```css
/* Variants are always combined with the base: class="glass glass--thin". :not(.glass--tint) keeps tinted buttons from turning white-on-white. */
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass:not(.glass--tint) { background: rgb(var(--glass-fill) / .94); }
}
@media (prefers-reduced-transparency: reduce) {
  .glass { -webkit-backdrop-filter: none; backdrop-filter: none; }
  .glass:not(.glass--tint) { background: rgb(var(--glass-fill) / .94); }
  .glass[data-refract] { backdrop-filter: none; }
}
@media (prefers-contrast: more) {   /* the only Apple-device signal CSS can read for Increase Contrast */
  .glass { -webkit-backdrop-filter: none; backdrop-filter: none; border: 2px solid currentColor; box-shadow: none; }
  .glass:not(.glass--tint) { background: rgb(var(--glass-fill) / .97); }
  .glass[data-refract] { backdrop-filter: none; }
}
@media (prefers-reduced-motion: reduce) {
  .glass, .glass * { transition-property: opacity; animation: none; }   /* fades only, no blur or scale motion [S6] */
}
@media (forced-colors: active) {   /* MDN: box-shadow is forced to none; backdrop-filter is not mentioned [S21] */
  .glass { -webkit-backdrop-filter: none; backdrop-filter: none; background: Canvas; color: CanvasText; border: 1px solid CanvasText; }
  .glass[data-refract] { backdrop-filter: none; }
}
```

## 3. Legibility and contrast rules

- WCAG 1.4.3 requires 4.5:1 for text and 3:1 for large text (18pt, or 14pt bold), measured against "the specified background over which the text is rendered in normal usage" [S32]. On glass that background is whatever is scrolling behind it, so there is no single ratio to test. WCAG 1.4.11 (3:1 for icons and control states) says for gradients to test the least contrasting area [S33]; applying that to glass is my reading, WCAG does not mention translucency.
- Rule: choose the fill alpha for the worst backdrop, not the typical one. Light glass (white fill, dark text) fails first over black; dark glass (near-black fill, white text) fails first over white. My computation (WCAG relative luminance, plain sRGB alpha compositing, blur and saturate ignored because the worst case is already pure black or pure white): `#111` on white fill needs alpha 0.49 for 4.5:1 and 0.38 for 3:1 over pure black; `#3c3c43` grey needs 0.66; white text on `rgb(28 28 32)` fill needs 0.61 over pure white and 0.47 for 3:1. The tiers add headroom: regular 0.62 gives 7.1:1 (light) and 0.66 gives 5.5:1 (dark). Thin (0.45 and 0.50) is for icon-only controls (3:1) and must not carry text. Thick 0.78 gives 11.2:1 and 8.3:1.
- Use one text colour. Secondary or grey text on thin or regular glass fails the worst case (`#3c3c43` at 0.62 is 4.1:1).
- Tinted controls: check the label against the tint blended with a white backdrop; the default tint `0 90 220` at 0.90 is 4.8:1 or better.
- Text-shadow is not a fix. WCAG 1.4.3 treats a wide halo as "background" [S32], so a shadow counts only if it is solid enough to be the measured background; a soft blurred shadow gives no reliable ratio (my reading). Raising blur radius does not fix it either; Josh Comeau's own fixes are a bigger blur or a semi-opaque background [S29], and only the second is reliable.
- Under bars, fade the scrolled content with the `.scroll-edge` scrim, which is Apple's own answer [S3].
- Focus rings and non-text edges (my rule): 2px solid ring, 3:1 against both the glass and the page. The glass edge itself need not meet 3:1 if the control is identifiable by its icon or label (1.4.11 does not require a visible hit-area boundary) [S33].
- Test by placing every glass element over pure black, pure white, saturated red, blue and yellow, and one busy photo, with the lowest ratio deciding. Known fixed backgrounds may justify lower alpha if you measure the real pixels.

## 4. Performance budget

- I found no controlled benchmarks; web.dev's whole advice is "may harm performance. Test it" [S30]. Caps in the guides are estimates: 3 to 5 simultaneous blurred elements on mobile [S31], 3 to 4 glass layers per viewport [S27]. My rule: at most 3 glass layers in view on phones (nav + tab bar + one orb or sheet), 2 on low-end Android.
- The pattern we want, fixed or sticky bars with blur, is the one two PRs blame for iOS Safari scroll jank ("WebKit can't cache the blurred backdrop behind a sticky/fixed layer", no numbers; the other PR measured median frame 50ms to 16.7ms under 6x CPU throttle after dropping backdrop-filter on touch plus other changes) [S34]. Mitigation: keep bars short, blur 16px or less, fill alpha already high so removing blur on `(hover:none)` still looks right, and test on a real iPhone before the demo.
- Never animate blur radius or any filter value; no permanent `will-change: backdrop-filter` (my rule; OpenReplay's sample uses it, buildmvpfast says sparingly). Animate transform and opacity of the glass element itself. [S27][S31]
- Blur 20px or less on large surfaces [S27]. Modal scrims use a plain rgba fill, not backdrop-filter. Do not blur the full viewport.
- Backdrop root: an ancestor with `opacity` below 1, `filter`, `mask`, `clip-path`, `mix-blend-mode` or `will-change` of those makes a boundary, and the child blurs only what is between them [S15]. Keep glass elements near the root, with no such ancestors.
- Safari quirks: `var()` inside backdrop-filter was reported broken. WebKit 297620 (still NEW) says it fails on macOS Sonoma with Safari 18.x and works on macOS 26 with Safari 26.1; 289149 was closed INVALID after a different cause was found [S24]. A blog claims `-webkit-backdrop-filter` never resolves `var()` [S27]; the bugs show it is narrower than that. Literal values avoid the question.
- Firefox: `backdrop-filter` on a `position: sticky` element with an ancestor having `overflow` and `border-radius` broke; Josh Comeau says a fix landed 2026-09, initially Nightly only [S29].
- Edge bleed: blur only samples pixels behind the element's box; the fix is a child twice the height masked to the visible half (overflow:hidden works in Chrome 142 and later) [S29]. Optional polish, not needed for a hackathon.

## 5. Browser support

| Feature | Chrome / Edge | Safari macOS | Safari iOS | Firefox |
|---|---|---|---|---|
| `backdrop-filter` unprefixed | 76 / 79 | 18 | 18 (BCD mirrors macOS) | 103 |
| `-webkit-` prefix needed | no | yes, 9 to 17.x | yes, 9 to 17.x | no |
| `backdrop-filter: url()` SVG filter | works (no version floor verified) | no effect, bug open | same as macOS | displacement and feImage ignored; feColorMatrix works |
| `prefers-reduced-transparency` | 118 (MDN, Chrome blog) or 119 (caniuse) | no | no | behind a pref only (113) |
| `prefers-contrast` | 96 | 14.1 | mirrors macOS (version unverified) | 101 |
| `prefers-reduced-motion` | 74 | 10.1 | mirrors | 63 |
| `forced-colors` | 89 / 79 | 16 | mirrors | 89 |

Notes. Overall `backdrop-filter` is Baseline 2024 "newly available" on MDN [S15] and 97.08 percent global usage on caniuse [S16]; the version numbers come from the MDN compat data [S17] (the caniuse text I got did not show the Safari prefix note). Disagreement: OpenReplay says Safari 17+ needs no prefix [S31], MDN data says 18; trust the data and keep both declarations. The DEV article says backdrop-filter works in "Safari (all versions)", true only with the prefix [S28]. That Chrome and other browsers on iOS follow iOS Safari's version (WebKit) is an inference, unverified. Reduced transparency exists as an OS setting on Apple, Windows and others, but Safari and Firefox do not expose it to CSS [S18][S19][S20]; Chrome's own blog dated 2023-10 may be stale for Firefox [S19]. The Tinted setting from iOS 26.1 is not readable by CSS as far as I could find: unverified.

## Sources

Apple's documentation pages are rendered by JavaScript and returned only a title, so I read the same documents from Apple's JSON mirror at the path `developer.apple.com/tutorials/data/...json`. S2 to S7 are those documents.

- S1 https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/ : Apple Newsroom, June 2025. Glass "reflects and refracts", adapts light/dark, controls float above apps.
- S2 https://developer.apple.com/tutorials/data/documentation/technologyoverviews/liquid-glass.json : Liquid Glass technology overview; points to WWDC25 sessions; little rule text.
- S3 https://developer.apple.com/tutorials/data/documentation/technologyoverviews/adopting-liquid-glass.json : Adopting Liquid Glass (first 100k of 152k characters read). Backgrounds, glass on glass, sparing use, scroll edge, concentricity, accessibility testing.
- S4 https://developer.apple.com/tutorials/data/design/human-interface-guidelines/materials.json : HIG Materials. Regular vs clear, 35 percent dimming layer, no glass in the content layer.
- S5 https://developer.apple.com/tutorials/data/design/human-interface-guidelines/color.json : HIG Color (first 100k of 182k read). Liquid Glass colour guidance; no contrast ratios.
- S6 https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json : HIG Accessibility. WCAG AA table, Increase Contrast, Reduce Motion practices; no Liquid Glass text.
- S7 https://developer.apple.com/tutorials/data/design/human-interface-guidelines/tab-bars.json and https://developer.apple.com/tutorials/data/design/human-interface-guidelines/sheets.json : HIG Tab bars (floating, labels, navigation not actions) and Sheets (detents, grabber; no Liquid Glass guidance).
- S8 https://developer.apple.com/videos/play/wwdc2025/219/ : WWDC25 Meet Liquid Glass, transcript. Lensing, materialize, adaptivity, shadows, tint, clear vs regular, accessibility behaviours.
- S9 https://developer.apple.com/videos/play/wwdc2025/356/ : WWDC25 Get to know the new design system, transcript. Layers, concentricity, scroll edge, bars, sheets.
- S10 https://developer.apple.com/videos/play/wwdc2025/323/ : WWDC25 Build a SwiftUI app with the new design, transcript. tint, interactive, GlassEffectContainer, glass cannot sample glass.
- S11 https://www.macworld.com/article/2947565/ios-26-1-beta-4-does-the-unthinkable-you-can-control-how-glassy-liquid-glass-should-be.html : iOS 26.1 beta 4 Clear/Tinted setting and location.
- S12 https://www.nngroup.com/articles/liquid-glass/ : NN/g, "Liquid Glass Is Cracked, and Usability Suffers in iOS 26", 2025-10-10.
- S13 https://pxlnv.com/blog/on-liquid-glass/ : Pixel Envy on opacity versus contrast; opinion, no measurements.
- S14 https://kube.io/blog/liquid-glass-css-svg : refraction with SVG, displacement map, specular layer, Chromium-only note.
- S15 https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter : syntax including `url()`, backdrop root rules, Baseline 2024.
- S16 https://caniuse.com/css-backdrop-filter : 97.08 percent usage; first versions.
- S17 https://raw.githubusercontent.com/mdn/browser-compat-data/main/css/properties/backdrop-filter.json , https://raw.githubusercontent.com/mdn/browser-compat-data/main/css/at-rules/media.json , https://raw.githubusercontent.com/mdn/browser-compat-data/main/css/properties/mask-composite.json : MDN compat data for the versions in the table.
- S18 https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency : definition; "Limited availability", experimental.
- S19 https://developer.chrome.com/blog/css-prefers-reduced-transparency : Chrome and Edge 118, Firefox flag, Safari not supported (page updated 2023-10-25).
- S20 https://caniuse.com/wf-prefers-reduced-transparency : Chrome and Edge 119; Firefox and Safari none.
- S21 https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast and https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors : both Baseline widely available; forced-colors forces box-shadow to none.
- S22 https://bugs.webkit.org/show_bug.cgi?id=245510 : Safari ignores `backdrop-filter: url()`; status NEW; 2026 PRs unmerged.
- S23 https://bugzilla.mozilla.org/show_bug.cgi?id=1961378 and https://bugzilla.mozilla.org/show_bug.cgi?id=1972363 : Firefox ignores non-accelerated SVG backdrop filters; prefs; Safari behaves the same.
- S24 https://bugs.webkit.org/show_bug.cgi?id=297620 and https://bugs.webkit.org/show_bug.cgi?id=289149 : `var()` in backdrop-filter on Safari 18.x / Sonoma; the second closed INVALID.
- S25 https://github.com/rdev/liquid-glass-react and https://raw.githubusercontent.com/rdev/liquid-glass-react/master/src/index.tsx : README browser note; Firefox-only UA skip; blur 6px + saturate 140 percent defaults.
- S26 https://github.com/dashersw/liquid-glass-js : WebGL 2 approach, no documented fallback.
- S27 https://www.buildmvpfast.com/blog/liquid-glass-css-backdrop-filter-recipes-2026 : recipes, Firefox `@supports` caveat, UA-gate advice, performance and accessibility notes; secondary blog, figures unsourced.
- S28 https://dev.to/fabiosleal/how-to-create-the-apple-liquid-glass-effect-with-css-and-svg-2o06 : feTurbulence filter via `filter: url()`, inset-shadow specular layer; browser claims partly wrong.
- S29 https://www.joshwcomeau.com/css/backdrop-filter/ : edge bleed fix, flicker, readability, Firefox sticky bug; no performance section.
- S30 https://web.dev/articles/backdrop-filter : `@supports` fallback pattern, "may harm performance. Test it".
- S31 https://blog.openreplay.com/creating-blurred-backgrounds-css-backdrop-filter/ : mobile blur reduction, 3 to 5 element estimate, reduced-transparency and contrast fallbacks.
- S32 https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html : 1.4.3 text contrast, background definition, halo remark.
- S33 https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html : 1.4.11 3:1, gradients, boundaries.
- S34 https://github.com/mwhobrey/domi-ops/pull/57 and https://github.com/aaronangxz/xuanze.dev/pull/36 : anecdotal iOS Safari scroll jank from fixed or sticky blur; Safari 26 floating toolbar blur.
