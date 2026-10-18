/* Tailwind preset carrying the glass.css tokens (MIT, The Mishakin Group).
 *
 * Tailwind v3:  tailwind.config.js -> module.exports = { presets: [require("./glass/tailwind/preset.js")], content: [...] }
 * Tailwind v4:  prefer tailwind/theme.css (CSS-first). This file also works via `@config "./glass/tailwind/preset.js";`
 *
 * The values are CSS variables, so glass.css must be loaded too (it defines them and flips them for dark mode).
 * Dark mode follows <html data-theme="dark">, same switch as glass.js.
 * Limitation (v3 only): opacity modifiers such as bg-accent/40 do not work on var() colours; use the -soft tokens.
 */
const plugin = (() => { try { return require("tailwindcss/plugin"); } catch (e) { return (fn) => ({ handler: fn }); } })();

const v = (name) => `var(--g-${name})`;

const glass = (fill, blur) => ({
  backgroundColor: v(fill),
  backgroundImage: v("glass-sheen"),
  WebkitBackdropFilter: `blur(${blur}) saturate(180%)`,   /* literal: Safari 18 drops var() in backdrop-filter */
  backdropFilter: `blur(${blur}) saturate(180%)`,
  border: `1px solid ${v("glass-border")}`,
  boxShadow: v("glass-shadow"),
  "--g-text-2": v("glass-text-2"),
  "--g-text-3": v("glass-text-2"),
  "--g-accent-text": v("glass-accent-text"),
});

module.exports = {
  darkMode: ["selector", '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        bg: v("bg"),
        surface: { DEFAULT: v("surface"), 2: v("surface-2") },
        sunken: v("sunken"),
        line: { DEFAULT: v("line"), 2: v("line-2") },
        ink: { DEFAULT: v("text"), 2: v("text-2"), 3: v("text-3") },
        accent: { DEFAULT: v("accent"), ink: v("accent-ink"), text: v("accent-text"), soft: v("accent-soft"), hover: v("accent-hover") },
        good: { DEFAULT: v("good"), text: v("good-text"), soft: v("good-soft") },
        warn: { DEFAULT: v("warn"), text: v("warn-text"), soft: v("warn-soft") },
        bad: { DEFAULT: v("bad"), text: v("bad-text"), soft: v("bad-soft") },
        chart: { 1: v("chart-1"), 2: v("chart-2"), 3: v("chart-3"), 4: v("chart-4"), 5: v("chart-5"), 6: v("chart-6"), grid: v("chart-grid") },
      },
      fontFamily: {
        sans: ["Geist", "Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "system-ui", "sans-serif"],
        mono: ["Geist Mono", "ui-monospace", "SF Mono", "Menlo", "monospace"],
      },
      fontSize: {
        hero: [v("t-hero"), { lineHeight: "0.98", letterSpacing: "-0.045em", fontWeight: "600" }],
        display: [v("t-display"), { lineHeight: "1.04", letterSpacing: "-0.04em", fontWeight: "600" }],
        h1: [v("t-h1"), { lineHeight: "1.1", letterSpacing: "-0.03em", fontWeight: "600" }],
        h2: ["22px", { lineHeight: "1.25", letterSpacing: "-0.02em", fontWeight: "600" }],
        h3: ["17px", { lineHeight: "1.35", letterSpacing: "-0.012em", fontWeight: "600" }],
        lede: [v("t-lede"), { lineHeight: "1.5" }],
        body: ["15px", { lineHeight: "1.55" }],
        small: ["13px", { lineHeight: "1.45" }],
        micro: ["11.5px", { lineHeight: "1.3", letterSpacing: "0.06em" }],
        "num-hero": [v("t-num-hero"), { lineHeight: "0.9", letterSpacing: "-0.055em", fontWeight: "600" }],
        num: [v("t-num"), { lineHeight: "1", letterSpacing: "-0.04em", fontWeight: "600" }],
      },
      borderRadius: { xs: "8px", sm: "12px", md: "16px", lg: "22px", xl: "28px", "2xl": "36px", pill: "999px" },
      boxShadow: { 1: v("shadow-1"), 2: v("shadow-2"), 3: v("shadow-3"), glass: v("glass-shadow") },
      backdropBlur: { thin: "12px", regular: "20px", thick: "24px" },
      transitionTimingFunction: { spring: v("ease-spring"), out: v("ease") },
      transitionDuration: { 1: "120ms", 2: "200ms", 3: "320ms", 4: "520ms" },
      maxWidth: { page: "1240px" },
    },
  },
  plugins: [
    plugin(function ({ addComponents }) {
      addComponents({
        ".glass": glass("glass-regular", "20px"),
        ".glass-thin": { ...glass("glass-thin", "12px"), "--g-text-2": v("text"), "--g-text-3": v("text"), "--g-accent-text": v("text") },
        ".glass-thick": glass("glass-thick", "24px"),
        "@media (prefers-reduced-transparency: reduce)": {
          ".glass, .glass-thin, .glass-thick": { backgroundColor: v("surface"), backgroundImage: "none", backdropFilter: "none", WebkitBackdropFilter: "none" },
        },
      });
    }),
  ],
};
